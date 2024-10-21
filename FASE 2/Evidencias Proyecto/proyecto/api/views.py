from rest_framework import viewsets
from .serializers import AcreditacionSerializer, AcreditadoSerializer, AcreditadorSerializer, AccesoSerializer, RolSerializer, \
    EventoSerializer, EmpresaSerializer, EncargadoSerializer
from management.models import Acreditacion, Acreditado, Acreditador, Acceso, Rol, \
    Empresa, Encargado, Evento

class AcreditacionViewset(viewsets.ModelViewSet):
    queryset = Acreditacion.objects.all()
    serializer_class = AcreditacionSerializer

class AcreditadoViewset(viewsets.ModelViewSet):
    queryset = Acreditado.objects.all()
    serializer_class = AcreditadoSerializer

class AcreditadorViewset(viewsets.ModelViewSet):
    queryset = Acreditador.objects.all()
    serializer_class = AcreditadorSerializer

class AccesoViewset(viewsets.ModelViewSet):
    queryset = Acceso.objects.all()
    serializer_class = AccesoSerializer

class RolViewset(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class EmpresaViewset(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EncargadoViewset(viewsets.ModelViewSet):
    queryset = Encargado.objects.all()
    serializer_class = EncargadoSerializer

class EventoViewset(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

