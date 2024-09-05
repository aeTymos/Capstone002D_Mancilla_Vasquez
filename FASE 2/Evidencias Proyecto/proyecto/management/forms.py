from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Acreditador
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    
    rut = forms.CharField(max_length=12, required=True)
    nombre = forms.CharField(max_length=30, required=True)
    apellido_paterno = forms.CharField(max_length=30, required=True)
    apellido_materno = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['rut', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'password1', 'password2']

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if Acreditador.objects.filter(rut_acreditador=rut).exists():
            raise ValidationError('El RUT ingresado ya existe.')
        return rut
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.apellido_paterno = self.cleaned_data['apellido_paterno']
        user.apellido_materno = self.cleaned_data['apellido_materno']
        user.email = self.cleaned_data['email']

        usuario_base = f"{user.nombre[:2].lower()}.{user.apellido_paterno.lower()}"
        username = usuario_base
        contador = 1
        while User.objects.filter(username=username).exists():
            username = f"{usuario_base}{contador}"
            contador += 1
        user.username = username

        if commit:
            user.save()

            acreditador, created = Acreditador.objects.get_or_create(user=user)
            acreditador.rut_acreditador = self.cleaned_data['rut']
            acreditador.nombre = user.nombre
            acreditador.app_paterno = user.apellido_paterno
            acreditador.app_materno = user.apellido_materno
            acreditador.correo = user.email
            acreditador.save()

        return user