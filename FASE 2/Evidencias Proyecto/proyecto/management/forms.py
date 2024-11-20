from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from datetime import datetime

from .models import Acreditador, Acreditado, Asistencia
from home.models import Contacto

class CustomUserCreationForm(UserCreationForm):
    
    rut = forms.CharField(max_length=12, required=True)
    nombres = forms.CharField(max_length=40, required=True)
    apellido_paterno = forms.CharField(max_length=30, required=True)
    apellido_materno = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    contacto_manager = forms.BooleanField(
        required=False,
        label='¿Puede gestionar mensajes?',
        initial=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Acreditador
        fields = ['rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'email', 'password1', 'password2']

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if Acreditador.objects.filter(rut=rut).exists():
            raise ValidationError('El RUT ingresado ya existe.')
        return rut

    def clean_email(self):
        email = self.cleaned_data['email']
        if Acreditador.objects.filter(email=email):
            raise ValidationError('El correo ingresado ya existe.')
        return email
            
    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data['nombres'].title()
        apellido_paterno = self.cleaned_data['apellido_paterno'].capitalize()
        apellido_materno = self.cleaned_data.get('apellido_materno', '').capitalize()

        user.last_name = f'{apellido_paterno} {apellido_materno}'.strip()
        user.email = self.cleaned_data['email']

        usuario_base = f"{user.first_name[:2].lower()}.{apellido_paterno.lower()}"
        username = usuario_base
        contador = 1
        while Acreditador.objects.filter(username=username).exists():
            username = f"{usuario_base}{contador}"
            contador += 1
        user.username = username

        if commit:
            user.save()

        if self.cleaned_data['contacto_manager']:

            group_name = 'Contacto manager'
            group, _ = Group.objects.get_or_create(name=group_name)

            permisos = [
                'home.view_contacto',
                'home.add_contacto',
            ]

            contacto_content_type = ContentType.objects.get_for_model(Contacto)

            for perm in permisos:
                permiso, _ = Permission.objects.get_or_create(codename=perm.split('.')[-1], content_type=contacto_content_type)
                group.permissions.add(permiso)
            user.groups.add(group)

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

    dias_de_asistencia = forms.CharField(
        required=True,
        label='Selecciona el o los días que asistirá.',
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        dias_de_asistencia = cleaned_data.get('dias_de_asistencia')

        print(f'dias_de_asistencia value: {dias_de_asistencia}')

        if not dias_de_asistencia:
            raise ValidationError('Debes seleccionar al menos un día de asistencia.')
        
        fechas = dias_de_asistencia.split(',')
        fechas_invalidas = [fecha for fecha in fechas if not self.es_fecha_valida(fecha)]
        
        if fechas_invalidas:
            raise ValidationError(f'Fechas inválidas: {", ".join(fechas_invalidas)}')

        return cleaned_data

    def es_fecha_valida(self, date_str):
        try:
            datetime.strptime(date_str.strip(), '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def save(self, commit=True):

        acreditado = super().save(commit=False)
        acreditado.rut_acreditado = self.cleaned_data['rut']
        acreditado.nombre = self.cleaned_data['nombre']
        acreditado.app_paterno = self.cleaned_data['app_paterno']
        acreditado.app_materno = self.cleaned_data['app_materno']
        acreditado.empresa = self.cleaned_data['empresa']
        acreditado.acceso = self.cleaned_data['acceso']
        acreditado.rol = self.cleaned_data['rol']
        
        
        contador = 1
        pulsera_base = "NO-PULSERA"
        pulsera = None

        while True:
            pulsera = f"{pulsera_base}-{contador}"
            if not Acreditado.objects.filter(id_pulsera=pulsera).exists():
                break
            contador += 1
        
        acreditado.id_pulsera = pulsera
        
        if commit:
            acreditado.save()

        fechas_asistencia = self.cleaned_data['dias_de_asistencia'].split(',')
        for date_str in fechas_asistencia:
            asistencia_date = datetime.strptime(date_str.strip(), '%d-%m-%Y').date()
            Asistencia.objects.create(dia=asistencia_date, acreditado=acreditado)

        return acreditado

    class Meta:
        model = Acreditado
        fields = ['rut', 'nombre', 'app_paterno', 'app_materno', 'dias_de_asistencia', 'empresa', 'acceso', 'rol']