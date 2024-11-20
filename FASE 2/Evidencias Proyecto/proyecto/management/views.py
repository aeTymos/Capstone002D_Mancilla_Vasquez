from django.shortcuts import render, get_object_or_404
from .forms import CustomUserCreationForm, AcreditadoForm
from django.shortcuts import redirect
from .models import Acreditado, Evento, Acreditacion, Acreditador
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'management/dashboard.html')

@csrf_protect
@permission_required('auth.add_user')
def registro(request):

    data = {
        'form': CustomUserCreationForm()    
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            
            user = formulario.save()
            Token.objects.create(user=user)

            nombre_grupo = 'Acreditadores'
            grupo, _ = Group.objects.get_or_create(name=nombre_grupo)
            permisos = [
                'management.view_acreditado',
                'management.add_acreditado',
                'management.modify_acreditado',
                'management.view_evento',
                'management.view_acceso',
                'management.view_rol',
                'management.view_acreditacion',
                'management.add_acreditacion',
            ]

            acreditado_ct = ContentType.objects.get_for_model(Acreditado)

            for perm in permisos:
                permiso, _ = Permission.objects.get_or_create(codename=perm.split('.')[-1], content_type=acreditado_ct)
                grupo.permissions.add(permiso)
            user.groups.add(grupo)

            messages.success(request, f'Usuario para {user.first_name} {user.last_name} creado correctamente')
            return redirect('listado_acreditadores')
        else:
            for error in formulario.errors.values():
                messages.error(request, error)
            data["form"] = formulario
    else:
        CustomUserCreationForm()

    return render(request, 'management/r_acreditadores.html', data)

@permission_required('auth.view_user')
def listado_acreditadores(request):

    acreditadores = Acreditador.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(acreditadores, 10)
        acreditadores = paginator.page(page)
    except Exception:
        raise Http404    

    data = {
        'entity': acreditadores,
        'paginator': paginator,
    }

    return render(request, 'management/l_acreditadores.html', data)

@login_required
def listado_acreditados(request):
    acreditados = Acreditado.objects.all()
    page = request.GET.get('page', 1)
    dias_de_trabajo = {acreditado.id: acreditado.dias_de_trabajo() for acreditado in acreditados}

    try:
        paginator = Paginator(acreditados, 10)
        acreditados = paginator.page(page)
    except Exception:
        raise Http404    

    data = {
        'entity': acreditados,
        'paginator': paginator,
        'dias_de_trabajo': dias_de_trabajo,
    }

    return render(request, 'management/l_acreditados.html', data)


@csrf_protect
@permission_required('management.add_acreditado')
def registro_acreditado(request):

    data = {
        'form': AcreditadoForm()
    }

    if request.method == 'POST':
        formulario = AcreditadoForm(data=request.POST)
        if formulario.is_valid():
            acreditado = formulario.save()
            messages.success(request, f'Acreditación para {acreditado.nombre} {acreditado.app_paterno} realizada correctamente')
            return redirect('listado_acreditados')
        else:
            for error in formulario.errors.values():
                messages.error(request, error)
            data["form"] = formulario
    else:
        AcreditadoForm()

    return render(request, 'management/r_acreditados.html', data)


####### REGISTRO ID & PULSERA ACREDITADO
@csrf_exempt
def registrar_qr(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        acreditado_id = request.POST.get('acreditado_id')

        try:
            acreditado = Acreditado.objects.get(id=acreditado_id)
            
            # Verifica que el acreditado aún no tenga un id_pulsera
            if not acreditado.id_pulsera:
                acreditado.id_pulsera = qr_data
                acreditado.save()
                message = f"Pulsera vinculada exitosamente para {acreditado.nombre} {acreditado.app_paterno}."
            else:
                message = "Este acreditado ya tiene una pulsera asignada."

        except Acreditado.DoesNotExist:
            message = "Acreditado no encontrado."

        return JsonResponse({'success': True, 'message': message})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})



@login_required
@permission_required('management.change_acreditado')
def registrar_qr_evento(request, acreditado_id):
    acreditado = get_object_or_404(Acreditado, id=acreditado_id)
    return render(request, 'management/registro_qr.html', {'acreditado_id': acreditado.id})
