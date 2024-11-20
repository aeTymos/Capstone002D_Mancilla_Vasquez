from django import forms
from django.core.exceptions import ValidationError

from .models import Contacto
from .validators import MaxSizeValidator

import magic

class ContactoForm(forms.ModelForm):

    archivo = forms.FileField(required=False, validators=[MaxSizeValidator(max_file_size=2)])

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')

        if not archivo:
            raise ValidationError('No se subió ningún archivo')

        extensiones_validas = ['.xlsx', '.csv']
        ext = archivo.name.split('.')[-1].lower()
        print(f'Extensión detectada: {ext}')

        if f'.{ext}' not in extensiones_validas:
            raise ValidationError('Tipo de archivo inválido. Solo se aceptan archivos excel (.xslx y .csv).')

        mime = magic.from_buffer(archivo.read(2048), mime=True)
        archivo.seek(0)

        if mime == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' and ext != 'xlsx':
            raise ValidationError('Archivo Excel inválido. Asegúrese de que el archivo tenga una extensión .xlsx.')
        elif mime == 'text/csv' and ext != 'csv':
            raise ValidationError('Archivo CSV inválido. Asegúrese de que el archivo tenga una extensión .csv.')

        return archivo

    class Meta:
        model = Contacto
        fields = ['nombre', 'correo', 'tipo_consulta', 'mensaje', 'archivo']

class UploadFileForm(forms.Form):
    file = forms.FileField()