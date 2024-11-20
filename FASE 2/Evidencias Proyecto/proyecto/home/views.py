from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.db import DatabaseError, IntegrityError

from .forms import UploadFileForm, ContactoForm
from management.models import Acreditado, Empresa, Rol, Acceso
from datetime import datetime

import json
import pandas as pd


ACREDITADO_FIELDS = [
    'rut', 'id_pulsera', 'nombre', 'app_paterno', 'app_materno', 
    'fec_inicio', 'fec_termino', 'empresa', 'acceso', 'rol'
]

def index(request):
    return render(request, 'home/index.html')

def events(request):
    return render(request, 'events/crear_evento.html')

@csrf_exempt
def qr(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        
        if qr_data:
            print(f"QR Code Data: {qr_data}")
            
            # Search for the Acreditado with matching id_pulsera
            try:
                acreditado = Acreditado.objects.get(id_pulsera=qr_data)
                result = f"{acreditado.nombre} {acreditado.app_paterno} {acreditado.app_materno}, Access: {acreditado.acceso.tipo_acceso}"
            except Acreditado.DoesNotExist:
                result = "No Autorizado"

            return JsonResponse({'success': True, 'qr_data': f"Nivel de Acceso: {result}"})

        return JsonResponse({'success': False, 'message': 'Error en el envio.'})

    return render(request, 'home/qr.html')


@csrf_exempt
def import_excel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            df = df.dropna(how='all')


            # Convert the DataFrame to an editable HTML table
            # Detect rows where all values are numeric (or lists of numbers) and drop them
            df = df[df.apply(lambda row: not all(is_numeric_or_list_of_numbers(val) for val in row), axis=1)]
            table_html = df_to_editable_html(df)

            print(df)
            # Return both the dropdown and table in the response
            return JsonResponse({'table': table_html})
    
    form = UploadFileForm()
    return render(request, 'home/import.html', {'form': form})

def is_numeric_or_list_of_numbers(value):
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, list) and all(isinstance(i, (int, float)) for i in value):
        return True
    return False


def df_to_editable_html(df):
    # Create the table headers
    html = '<table class="table table-striped table-bordere" id="editable-table">'
    
    # Add the delete buttons above each dropdown
    html += '<thead><tr>'
    for _ in df.columns:
        html += '<th><button class="delete-col btn btn-danger btn-sm">Delete</button></th>'
    html += '<th></th>'  # Empty cell for alignment with the Action column (no delete button here)
    html += '</tr>'
    
    # Add the column mapping dropdowns in the second header row
    html += '<tr>'
    for col in df.columns:
        html += '<th>'
        html += f'<select name="column_mapping_{col}" class="form-select">'
        for field in ACREDITADO_FIELDS:
            html += f"<option value='{field}'>{field}</option>"
        html += '</select></th>'
    html += '<th>Action</th>'  # Delete button column for rows
    html += '</tr></thead>'
    
    # Create table rows with delete row buttons only in the last column
    html += '<tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for cell in row:
            html += f'<td contenteditable="true">{cell}</td>'
        html += '<td><button class="delete-row btn btn-danger btn-sm">Delete</button></td>'  # Delete button at the end
        html += '</tr>'
    html += '</tbody>'
    
    html += '</table>'
    return html

@csrf_exempt
def save_table(request):
    if request.method == 'POST':
        try:
            
            # Check if data is present in the request
            raw_table_data = request.POST.get('table_data')
            raw_column_mapping = request.POST.get('column_mapping')
            
            if not raw_table_data or not raw_column_mapping:
                return JsonResponse({'status': 'error', 'message': 'Missing table data or column mapping'})


            # Try parsing the JSON
            try:
                table_data = json.loads(raw_table_data)
                column_mapping = json.loads(raw_column_mapping)
            except json.JSONDecodeError as json_error:
                print(f"JSON decode error: {json_error}")
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})
            
            # Continue with the existing code...
            df = pd.DataFrame(table_data)
            df.drop(df.columns[-1], axis=1, inplace=True)  # Drop the last column
            df.columns = column_mapping

            df = df.drop(index=[0, 1])  # Drop header rows or irrelevant rows
            print(df)           # Iterate through each row and create Acreditado instances
            for index, row in df.iterrows():
                print(f"Processing row: {row.to_dict()}")

                try:
                    # Get or create the Empresa object
                    try:
                        empresa, created = Empresa.objects.get_or_create(nombre=row['empresa'])
                        print(f"Empresa: {empresa} {'created' if created else 'retrieved'}")
                    except (DatabaseError, IntegrityError) as empresa_error:
                        raise ValueError(f"Failed to create or retrieve Empresa: {empresa_error}")

                    # Get or create the Acceso object
                    try:
                        acceso, created = Acceso.objects.get_or_create(
                            tipo_acceso=row['acceso'],
                            defaults={'desc_acceso': f'Description for {row["acceso"]}'}
                        )
                        print(f"Acceso: {acceso} {'created' if created else 'retrieved'}")
                    except (DatabaseError, IntegrityError) as acceso_error:
                        raise ValueError(f"Failed to create or retrieve Acceso: {acceso_error}")

                    # Get or create the Rol object
                    try:
                        rol, created = Rol.objects.get_or_create(tipo_rol=row['rol'])
                        print(f"Rol: {rol} {'created' if created else 'retrieved'}")
                    except (DatabaseError, IntegrityError) as rol_error:
                        raise ValueError(f"Failed to create or retrieve Rol: {rol_error}")

                    # Define your default dates
                    default_fec_inicio = datetime.strptime('09/10/2024', '%d/%m/%Y').date()
                    default_fec_termino = datetime.strptime('01/11/2024', '%d/%m/%Y').date()

                    # Generate the next id_pulsera
                    base_id = f"{rol.tipo_rol[:1].upper()}{acceso.tipo_acceso[:3].upper()}"
                    existing_ids = Acreditado.objects.filter(id_pulsera__startswith=base_id).values_list('id_pulsera', flat=True)
                    existing_numbers = [int(id_pulsera.split('-')[-1]) for id_pulsera in existing_ids]

                    # Find the next number for id_pulsera
                    next_number = max(existing_numbers, default=0) + 1
                    id_pulsera = f"{base_id}-{next_number}"

                    # Create and save the Acreditado instance
                    try:
                        acreditado = Acreditado(
                            rut=row['rut'],
                            id_pulsera=id_pulsera,
                            nombre=row['nombre'],
                            app_paterno='apellido',
                            app_materno='apellido',
                            fec_inicio=default_fec_inicio,
                            fec_termino=default_fec_termino,
                            empresa=empresa,
                            acceso=acceso,
                            rol=rol
                        )
                        acreditado.save()
                        print(f"Acreditado saved: {acreditado}")
                    except (DatabaseError, IntegrityError) as acreditado_error:
                        raise ValueError(f"Failed to save Acreditado: {acreditado_error}")

                except ValueError as row_error:
                    # Log or return row-specific error with more context
                    print(f"Error processing row {index}: {row_error}")
                    return JsonResponse({
                        'status': 'error',
                        'message': f"Error processing row {index}: {row_error}"
                    })

            # Success message if everything was processed correctly
            return JsonResponse({'status': 'success', 'message': 'Table saved successfully!'})

        except Exception as e:
            # General error handling for issues outside row processing
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_protect
def contacto(request):
    
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        form = ContactoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': '¡Mensaje enviado!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactoForm()

    return render(request, 'home/contacto.html', data)
