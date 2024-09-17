from django.urls import path, include
from .views import dashboard, registro, listado_acreditadores, listado_acreditados, registro_acreditado

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/acreditadores/', listado_acreditadores, name='listado_acreditadores'),
    path('acreditadores/registro', registro, name='registro_acreditador'),
    path('dashboard/acreditados/', listado_acreditados, name='listado_acreditados'),
    path('acreditados/registro', registro_acreditado, name='registro_acreditado'),
]