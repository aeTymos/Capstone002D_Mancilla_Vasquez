from django.shortcuts import render, redirect
from .forms import EventoForm
from management.models import Evento

#Vista para crear_eventos
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

    return render(request, 'events/crear_evento.html', {'form': form, 'eventos': eventos})

# Crear la vista lista_eventos
def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'events/lista_eventos.html', {'eventos': eventos})