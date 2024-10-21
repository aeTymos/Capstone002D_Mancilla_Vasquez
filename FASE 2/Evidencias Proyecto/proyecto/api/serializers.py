from rest_framework import serializers
from management.models import Acceso, Rol, Acreditacion, Acreditado, Acreditador, \
    Evento, Encargado, Empresa

class AcreditadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acreditado
        fields = '__all__'

class AcreditadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acreditador
        fields = '__all__'

class AcreditacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acreditacion
        fields = '__all__'

class AccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceso
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class EncargadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encargado
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

