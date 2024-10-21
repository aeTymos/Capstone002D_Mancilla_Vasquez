from django.urls import path, include
from .views import index, qr, contacto

urlpatterns = [
    path('', index, name='index'),
    path('contacto/', contacto, name='contacto'),
    path('qr/', qr, name='qr'),
]