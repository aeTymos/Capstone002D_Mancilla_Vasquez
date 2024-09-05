from django.urls import path, include
from .views import index, qr

urlpatterns = [
    path('', index, name='index'),
    path('qr/', qr, name='qr'),
]