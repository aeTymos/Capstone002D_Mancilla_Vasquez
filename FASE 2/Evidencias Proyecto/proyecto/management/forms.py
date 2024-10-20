from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Acreditador, Acreditado
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput

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

    def clean_email(self):
        email = self.cleaned_data['email']
        if Acreditador.objects.filter(correo=email):
            raise ValidationError('El correo ingresado ya existe.')
        return email
            
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
    
class AcreditadoForm(forms.ModelForm):

    app_paterno = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido paterno'
    )
    app_materno = forms.CharField(
        max_length=30, 
        required=False,
        label='Apellido materno'
    )

    fec_inicio = forms.DateField(
        label='Fecha de inicio',
        widget=DatePickerInput()
    )
    fec_termino = forms.DateField(
        label='Fecha de termino',
        widget=DatePickerInput()
    )

    rol = forms.CharField(
        label='Cargo',
    )

    def clean(self):
        cleaned_data = super().clean()
        fec_inicio = cleaned_data.get('fec_inicio')
        fec_termino = cleaned_data.get('fec_termino')
        if fec_inicio and fec_termino and fec_inicio > fec_termino:
            raise ValidationError('La fecha de inicio no puede ser mayor a la fecha de término.')
        return cleaned_data

    def save(self, commit=True):

        acreditado = super().save(commit=False)
        acreditado.rut_acreditado = self.cleaned_data['rut']
        acreditado.nombre = self.cleaned_data['nombre']
        acreditado.app_paterno = self.cleaned_data['app_paterno']
        acreditado.app_materno = self.cleaned_data['app_materno']
        acreditado.fec_inicio = self.cleaned_data['fec_inicio']
        acreditado.fec_termino = self.cleaned_data['fec_termino']
        acreditado.empresa = self.cleaned_data['empresa']
        acreditado.acceso = self.cleaned_data['acceso']
        acreditado.rol = self.cleaned_data['rol']
        
        contador = 10000
        pulsera_base = f"{acreditado.rol.tipo_rol[:1].upper()}{acreditado.acceso.tipo_acceso[:3].upper()}"
        pulsera = None

        while True:
            pulsera = f"{pulsera_base}-{contador}"
            if not Acreditado.objects.filter(id_pulsera=pulsera).exists():
                break
            contador += 1

        if commit:
            acreditado.id_pulsera = pulsera
            acreditado.save()

        return acreditado

    class Meta:
        model = Acreditado
        fields = ['rut', 'nombre', 'app_paterno', 'app_materno', 'fec_inicio', 'fec_termino', 'empresa', 'acceso', 'rol']