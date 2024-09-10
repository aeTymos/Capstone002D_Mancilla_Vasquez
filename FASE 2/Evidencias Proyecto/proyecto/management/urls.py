from django.urls import path, include
from .views import dashboard, registro, listado_acreditadores

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('acreditadores/', listado_acreditadores, name='listado_acreditadores'),
    path('acreditadores/registro', registro, name='registro_acreditador'),
]