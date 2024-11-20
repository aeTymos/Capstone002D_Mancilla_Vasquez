from django.test import TestCase
from home.forms import ContactoForm
from home.models import Contacto
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError



class ContactoFormTest(TestCase):

    ### PRUEBA DE ARCHIVO VÁLIDO (.CSV) ###
    def test_form_valid_file_csv(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertTrue(form.is_valid())

    ### PRUEBA DE ARCHIVO VÁLIDO (.XLSX) ###
    def test_form_valid_file_xlsx(self):
        archivo = SimpleUploadedFile("test.xlsx", b"contenido de prueba", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertTrue(form.is_valid())

    ### PRUEBA DE ARCHIVO CON EXTENSIÓN INVÁLIDA ###
    def test_form_invalid_extension(self):
        archivo = SimpleUploadedFile("test.txt", b"contenido,de,prueba", content_type="text/plain")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('Tipo de archivo inválido. Solo se aceptan archivos excel (.xslx y .csv).', form.errors['archivo'])

    ### PRUEBA SIN ARCHIVO SUBIDO ###
    def test_form_no_file_uploaded(self):
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('No se subió ningún archivo', form.errors['archivo'])

    ### NOMBRE VACÍO ###
    def test_nombre_empty(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form_data = {
            'nombre': '',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### NOMBRE DEMASIADO LARGO ###
    def test_nombre_too_long(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form_data = {
            'nombre': 'Juan' * 41,  # Más de la longitud máxima
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### CORREO FORMATO INCORRECTO ###
    def test_correo_invalid_format(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'correo-invalido',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)

    ### CORREO VACÍO ###
    def test_correo_empty(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': '',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)

    ### TIPO DE CONSULTA VACÍO ###
    def test_tipo_consulta_empty(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': '',  # Campo vacío
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_consulta', form.errors)

    ### MENSAJE VACÍO ###
    def test_mensaje_empty(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': ''  # Campo vacío
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('mensaje', form.errors)

    ### ARCHIVO EXCEDE EL TAMAÑO MÁXIMO ###
    def test_archivo_exceeds_max_size(self):
        # Archivo de tamaño 3 MB (supera el límite de 2 MB)
        archivo = SimpleUploadedFile("test.csv", b"0" * 3 * 1024 * 1024, content_type="text/csv")
        form_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 'Consulta general',
            'mensaje': 'Este es un mensaje de prueba.'
        }
        form = ContactoForm(data=form_data, files={'archivo': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('archivo', form.errors)