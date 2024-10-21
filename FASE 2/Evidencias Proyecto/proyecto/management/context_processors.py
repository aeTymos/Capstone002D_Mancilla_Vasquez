from .models import Evento

def eventos_recientes(request):
    eventos = Evento.objects.all().order_by('-fec_termino')[:5]
    data = {
        'eventos_recientes': eventos   
    }
    return data