from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_evento, name='crear_evento'),
]