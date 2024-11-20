from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from bs4 import BeautifulSoup
from os.path import basename
import os
import re
from datetime import datetime, timedelta, date
from calendar import monthrange
import pandas as pd
from io import BytesIO
import magic
import logging

from home.models import Contacto
from management.models import Acreditado, Asistencia, Rol, Empresa, Acceso, Evento

def parseo_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    records = []

    table = soup.find('table')
    rows = table.find_all('tr')[1:]

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            nombre = cols[0].get_text(strip=True)
            rut = cols[1].get_text(strip=True)
            empresa = cols[2].get_text(strip=True)
            rol = cols[3].get_text(strip=True)
            acceso = cols[4].get_text(strip=True)
            dias = cols[5].get_text(strip=True).split(', ')

        empresa_instance, _ = Empresa.objects.get_or_create(nombre=empresa)
        acceso_instance, _ = Acceso.objects.get_or_create(tipo_acceso=acceso)
        rol_instance, _ = Rol.objects.get_or_create(tipo_rol=rol)

        name_parts = nombre.split()
        primer_nombre = name_parts[0]
        segundo_nombre = ' '.join(name_parts[2:-1]) if len(name_parts) > 3 else ''
        app_paterno = name_parts[1] if len(name_parts) > 1 else ''
        app_materno = name_parts[-1] if len(name_parts) > 2 else ''

        nombres = f'{primer_nombre} {segundo_nombre}'

        acreditado = Acreditado(
            rut=rut,
            id_pulsera='',
            nombre=nombres,
            app_paterno=app_paterno,
            app_materno=app_materno,
            empresa=empresa_instance,
            acceso=acceso_instance,
            rol=rol_instance
        )

        records.append((acreditado, dias))

    return records

def get_acreditado_days(record):
    
    _, dias = record
    dias_asistencia = []

    for dia in dias:
        try:
            day = int(dia)
            dias_asistencia.append(day)
        except ValueError:
            continue

    return dias_asistencia

def extrae_info_encargado(file):
    
    df = pd.read_excel(file, header=None)
    encargado_info = {}

    encargado_info['nombre'] = df.iloc[0, 2]
    encargado_info['telefono'] = df.iloc[1, 2]
    encargado_info['correo'] = df.iloc[2, 2]

    return encargado_info

def crea_asistencia(acreditado_instance, dias_asistencia, fec_inicio, fec_termino, allow_past_dates=False):
    mes_actual = fec_inicio.month
    anno_actual = fec_inicio.year

    for index, dia in enumerate(dias_asistencia):
        try:
            print(f"Processing day {dia} for acreditado {acreditado_instance.rut}")
            
            day = int(dia)
   
            fecha_asistencia = date(anno_actual, mes_actual, day)
            print(f"Creating asistencia for {acreditado_instance.rut} on {fecha_asistencia}")

            # Check if the date is within the event range
            if fec_inicio > fecha_asistencia and not allow_past_dates:
                print(f"Skipped creating asistencia for {acreditado_instance.rut} on {fecha_asistencia} (before event start date)")
                continue  # Skip if the date is before the event start date

            if fec_inicio <= fecha_asistencia <= fec_termino or allow_past_dates:
                # Create the asistencia entry only if it doesn't exist
                if not Asistencia.objects.filter(dia=fecha_asistencia, acreditado=acreditado_instance).exists():
                    print(f"Asistencia creada para {acreditado_instance.rut} en {fecha_asistencia}")
                    Asistencia.objects.create(dia=fecha_asistencia, acreditado=acreditado_instance)
                    if day == 30 or day == 31:
                        if index + 1 < len(dias_asistencia) and int(dias_asistencia[index + 1]) == 1:
                            mes_actual += 1
                            if mes_actual > 12:
                                mes_actual = 1
                                anno_actual += 1
                else:
                    print(f"Asistencia for {acreditado_instance.rut} already exists on {fecha_asistencia}")
            else:
                print(f"Skipped creating asistencia for {acreditado_instance.rut} on {fecha_asistencia} (outside event range)")

        except ValueError as e:
            print(f"Error creating Asistencia for {acreditado_instance.rut} with dia {dia}: {e}")
        
        except Exception as e:
            print(f'General error: {e}')

def process_file(file_content):
    
    try:
        mime = magic.from_buffer(file_content, mime=True)

        if mime == 'text/csv':
            df = pd.read_csv(BytesIO(file_content), skiprows=11)
        elif mime in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
            df = pd.read_excel(BytesIO(file_content), skiprows=11)
        else:
            print("File format no, allow_past_dates=Truet supported")
            return None, JsonResponse({'error': f'Tipo de archivo no soportado: {mime}'})

        print(f"File read successfully, shape: {df.shape}")

        df = df.iloc[:, 1:]
        df.dropna(axis=1, how='all', inplace=True)
        df.columns = df.columns.str.replace('\n', ' ').str.strip()

        df['RUT  (Sin puntos y con guión) XXXXXXXX-X'] = df['RUT  (Sin puntos y con guión) XXXXXXXX-X'].str.replace('.', '').str.replace(',', '')
        df['NOMBRE COMPLETO (Apellidos - Nombres)'] = df['NOMBRE COMPLETO (Apellidos - Nombres)'].str.title()
        df['EMPRESA'] = df['EMPRESA'].str.upper()
        df['CARGO DEL  TRABAJADOR'] = df['CARGO DEL  TRABAJADOR'].str.upper()

        identified_day_columns = [col for col in df.columns if 'DIA' in col.upper()]
        if not identified_day_columns:
            return None, JsonResponse({'error': 'No hay columnas de días disponibles.'})

        # Columnas de la nómina original
        id_vars = [
            'NOMBRE COMPLETO (Apellidos - Nombres)', 
            'RUT  (Sin puntos y con guión) XXXXXXXX-X',
            'EMPRESA', 
            'CARGO DEL  TRABAJADOR',
            'NIVEL ACCESO WP-AA-AAA-S',
        ]

        # Chequea por columnas faltantes
        missing_vars = [var for var in id_vars if var not in df.columns]
        if missing_vars:
            return None, JsonResponse({'error': f'Las siguientes columnas no están presentes en el DataFrame: {", ".join(missing_vars)}'})

        melted_days = pd.melt(df, id_vars=id_vars, 
                               value_vars=identified_day_columns, 
                               var_name='Dia_Type', 
                               value_name='Dia')
        melted_days['Dia'] = pd.to_numeric(melted_days['Dia'], errors='coerce')
        melted_days = melted_days[melted_days['Dia'].notna()]
        if melted_days.empty:
            return None, JsonResponse({'error': 'No hay datos válidos en las columnas de días.'})

        grouped_df = melted_days.groupby(id_vars).agg({
            'Dia': lambda x: ', '.join(sorted(set(map(str, x.astype(int))), key=lambda d: (int(d) < 20, int(d))) or ['-'])
        }).reset_index()
        grouped_df.rename(columns={'Dia': 'Dias'}, inplace=True)

        html_table = grouped_df.to_html(classes='table table-striped', index=False)
        return html_table, None

    except Exception as e:
        logging.error(f'Error processing file: {str(e)}')
        return None, JsonResponse({'error': f'Error al cargar el contenido del archivo: {str(e)}'})

@login_required
def listar_archivos(request):
    
    contactos = Contacto.objects.all()
    page = request.GET.get('page', 1)
    
    try:
        paginator = Paginator(contactos, 10)
        contactos = paginator.page(page)
    except Exception:
        raise Http404  

    for contacto in contactos:
        contacto.filename = basename(contacto.archivo.name)

    data = {
        'entity': contactos,
        'paginator': paginator,
    }

    return render(request, 'files/listado_archivos.html', data)

@csrf_protect
@login_required
def aceptar_archivo(request, id):

    if request.method == 'POST':
        html = request.POST.get('html_data')

        registros = parseo_html(html)

        try:
            evento = Evento.objects.get(activo=True)
            fec_inicio = evento.fec_inicio
            fec_termino = evento.fec_termino
            print(f"Event start: {fec_inicio}, Event end: {fec_termino}")
        except Evento.DoesNotExist:
            return JsonResponse({'error': 'No hay ningún evento activo en este momento.'})

        for acreditado, dias in registros:

            empresa_instance, _ = Empresa.objects.get_or_create(nombre=acreditado.empresa)
            acceso_instance, _ = Acceso.objects.get_or_create(tipo_acceso=acreditado.acceso)
            rol_instance, _ = Rol.objects.get_or_create(tipo_rol=acreditado.rol)

            contador = 1
            pulsera_base = "NO-PULSERA"
            pulsera = None

            while True:
                pulsera = f"{pulsera_base}-{contador}"
                if not Acreditado.objects.filter(id_pulsera=pulsera).exists():
                    break
                contador += 1

            acreditado_instance, _ = Acreditado.objects.get_or_create(
                rut=acreditado.rut,
                defaults={
                    'id_pulsera': pulsera,
                    'nombre': acreditado.nombre,
                    'app_paterno': acreditado.app_paterno,
                    'app_materno': acreditado.app_materno,
                    'empresa': empresa_instance,
                    'acceso': acceso_instance,
                    'rol': rol_instance,
                }
            )

            if _:
                print(f'Creada nueva instancia de Acreditado para: {acreditado.rut}')
            else:
                print(f"Acreditado instance already exists for {acreditado.rut}")
        
            dias_asistencia = get_acreditado_days((acreditado, dias))

            crea_asistencia(acreditado_instance, dias_asistencia, fec_inicio, fec_termino)

        return JsonResponse({'message': 'Archivo aceptado y registros guardados.'})
    
    return JsonResponse({'error': 'Método no permitido.'})

@csrf_protect
@login_required
def rechazar_archivo(request, id):
    
    if request.method == 'POST':
        contacto = get_object_or_404(Contacto, id=id)
        archivo = basename(contacto.archivo.name)
        correo_contacto = contacto.correo

        send_mail(
            'Archivo rechazado',
            f"""El archivo con nombre {archivo} fue rechazado por problemas con el formato.
            Asegurate de que no hayan columnas sin marcar en la nómina.""",
            'postmaster@mg.acreditacionesqr.online',
            [correo_contacto],
            fail_silently=False,
        )

        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Error al rechazar el archivo.'})

@login_required
def preview_file(request, id):
    uploaded_file = get_object_or_404(Contacto, id=id)
    file_path = uploaded_file.archivo.name  # Get the file path from the model
    
    try:
        with default_storage.open(file_path, 'rb') as file:
            file_content = file.read()
        
        html_table, error_response = process_file(file_content)
        if error_response:
            return error_response

        return JsonResponse({'html': html_table})

    except Exception as e:
        return JsonResponse({'error': f'Error al cargar el contenido del archivo: {str(e)}'})