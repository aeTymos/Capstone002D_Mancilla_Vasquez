from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventoForm
from management.models import Evento, Acreditacion
from django.http import Http404
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

#Vista para crear_eventos
@csrf_protect
@permission_required('management.add_evento')
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            accmin = form.cleaned_data['accmin']
            accmax = form.cleaned_data['accmax']

            # Validación del rango de IDs de pulseras
            if accmin > accmax:
                form.add_error('accmax', 'El valor máximo debe ser mayor al mínimo.')
            else:
                form.save()
                return redirect('listar_eventos')  # Redirige a la lista de eventos tras guardar
    else:
        form = EventoForm()

    eventos = Evento.objects.all()
    data = {'form': form, 'eventos': eventos}

    return render(request, 'events/crear_evento.html', data)


# Crear la vista lista_eventos
@login_required
def lista_eventos(request):
    
    eventos = Evento.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(eventos, 10)
        eventos = paginator.page(page)
    except:
        raise Http404    

    data = {
        'entity': eventos,
        'paginator': paginator,
    }

    return render(request, 'events/listar_eventos.html', data)


def detalle_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    acreditaciones = Acreditacion.objects.filter(evento=evento)

    query = request.GET.get('q')
    if query:
        acreditaciones = acreditaciones.filter(
            acreditado__nombre__icontains=query
        ) | acreditaciones.filter(
            acreditado__app_paterno__icontains=query
        ) | acreditaciones.filter(
            acreditado__app_materno__icontains=query
        ) | acreditaciones.filter(
            acreditado__rut__icontains=query
        )

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'events/detalles_evento.html', {'acreditaciones': acreditaciones, 'evento': evento})

    data = {
        'evento': evento,
        'acreditaciones': acreditaciones,
    }

    return render(request, 'events/detalles_evento.html', data)