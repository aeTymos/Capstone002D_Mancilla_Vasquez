from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.conf import settings

from home.models import Contacto
import os

class ContactoModelTest(TestCase):

    def setUp(self):
        
        self.file = SimpleUploadedFile('test_file.csv', b'File content', content_type='text/csv')

        self.contacto_data = {
            'nombre': 'Juan Pérez',
            'correo': 'juan.perez@example.com',
            'tipo_consulta': 0,
            'mensaje': 'Necesito más información sobre sus actividades.',
            'archivo': self.file,
        }

    def tearDown(self):

        try:
            file_path = self.contacto_data['archivo'].name
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
        except Exception as e:
            print(f"Error deleting file during cleanup: {e}")

    def test_create_contacto(self):
        
        contacto = Contacto.objects.create(**self.contacto_data)
        self.assertEqual(contacto.nombre, 'Juan Pérez')
        self.assertEqual(contacto.correo, 'juan.perez@example.com')
        self.assertEqual(contacto.tipo_consulta, 0)
        self.assertEqual(contacto.mensaje, 'Necesito más información sobre sus actividades.')

        file_name = contacto.archivo.name
        self.assertIsNotNone(contacto.archivo)
        self.assertTrue(file_name.startswith('uploads/tmp/test_file'), f"Expected file name to start with 'uploads/tmp/test_file.csv', but got {file_name}")

        self.assertIsInstance(contacto.hora_subido, timezone.datetime)
        self.assertFalse(contacto.aceptado, False)
    
    def test_str_method(self):
        
        contacto = Contacto.objects.create(**self.contacto_data)
        self.assertEqual(str(contacto), 'Juan Pérez')

    def test_tipo_consulta_invalida(self):

        with self.assertRaises(ValidationError):
            
            contacto = Contacto(
                nombre='Contacto inválido',
                correo='invalido@example.com',
                tipo_consulta=999,
                mensaje='Testeo de contacto inválido',
                archivo=self.file
            )
            contacto.full_clean()
            contacto.save()
        
    def test_choices_validos_tipo_consulta(self):

        valores_validos = [0, 1]
        for valor in valores_validos:
            
            contacto = Contacto(
                nombre='Contacto válido',
                correo='valido@example.com',
                tipo_consulta=valor,
                mensaje='Test de tipo de contacto válido.',
                archivo=self.file
            )
            contacto.full_clean()
        
    def test_default_aceptado(self):

        contacto = Contacto.objects.create(**self.contacto_data)
        self.assertFalse(contacto.aceptado)

    def test_autoadd_now(self):

        contacto = Contacto.objects.create(**self.contacto_data)
        self.assertIsInstance(contacto.hora_subido, timezone.datetime)
        self.assertLess(contacto.hora_subido, timezone.now())