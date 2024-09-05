from django.urls import path, include
from .views import dashboard, registro

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('acreditadores/', registro, name='acreditadores'),
]