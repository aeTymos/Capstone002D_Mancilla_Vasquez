from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventoForm
from management.models import Evento
from django.http import Http404
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required

#Vista para crear_eventos
@csrf_protect
@permission_required('management.add_evento')
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            return redirect('crear_evento')
    else:
        form = EventoForm()

    # Fetch all events to display them
    eventos = Evento.objects.all()

    data = {
        'form': form, 
        'eventos': eventos
    }

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

    data = {
        'evento': evento,
    }

    return render(request, 'events/detalles_evento.html', data)