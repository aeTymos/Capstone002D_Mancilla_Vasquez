from django.urls import path, include
from .views import listar_archivos, aceptar_archivo, preview_file, rechazar_archivo

urlpatterns = [
    path('dashboard/listado-archivos/', listar_archivos, name='lista_archivos'),
    path('dashboard/listado-archivos/aceptar/<id>/', aceptar_archivo, name="aceptar_archivo"),
    path('dashboard/listado-archivos/preview/<id>/', preview_file, name='preview_archivo'),
    path('dashboard/listado-archivos/rechazar/<id>/', rechazar_archivo, name='rechazar_archivo'),
]