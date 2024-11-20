from django.urls import path
from .views import lista_eventos, crear_evento, detalle_evento

urlpatterns = [
    path('dashboard/eventos/', lista_eventos, name='listar_eventos'),
    path('dashboard/eventos/crear/', crear_evento, name='crear_evento'),
    path('dashboard/eventos/evento/<id>/', detalle_evento, name='detalle_evento')
]