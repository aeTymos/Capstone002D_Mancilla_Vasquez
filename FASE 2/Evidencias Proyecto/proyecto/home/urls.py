from django.urls import path, include
from .views import index, qr, contacto, import_excel, save_table

urlpatterns = [
    path('', index, name='index'),
    path('contacto/', contacto, name='contacto'),
    path('qr/', qr, name='qr'),
    path('importar/', import_excel, name='importar'),
    path('save_table/', save_table, name='save_table')
]