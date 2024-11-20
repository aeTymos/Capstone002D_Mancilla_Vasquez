from django.urls import path, include
from .views import dashboard, registro, listado_acreditadores, listado_acreditados, registro_acreditado , registrar_qr, registrar_qr_evento

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/acreditadores/', listado_acreditadores, name='listado_acreditadores'),
    path('dashboard/acreditadores/registro/', registro, name='registro_acreditador'),
    path('dashboard/acreditados/', listado_acreditados, name='listado_acreditados'),
    path('dashboard/acreditados/registro/', registro_acreditado, name='registro_acreditado'),
    # Ruta para acceder a la página de escaneo y vinculación de QR, con acreditado_id
    path('dashboard/acreditados/registrar_qr/<int:acreditado_id>/', registrar_qr_evento, name='registrar_qr_evento'),
    # Ruta para el procesamiento AJAX del código QR y acreditado
    path('registrar_qr/', registrar_qr, name='registrar_qr'),
]