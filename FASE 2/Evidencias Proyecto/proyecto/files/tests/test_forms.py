from django.test import TestCase
from home.forms import UploadFileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

class UploadFileFormTest(TestCase):

    ### FORMULARIO VÁLIDO CON ARCHIVO CSV ###
    def test_upload_file_form_valid_csv(self):
        archivo = SimpleUploadedFile("test.csv", b"contenido,de,prueba", content_type="text/csv")
        form = UploadFileForm(files={'file': archivo})
        self.assertTrue(form.is_valid())

    ### FORMULARIO VÁLIDO CON ARCHIVO XLSX ###
    def test_upload_file_form_valid_xlsx(self):
        archivo = SimpleUploadedFile("test.xlsx", b"contenido de prueba", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        form = UploadFileForm(files={'file': archivo})
        self.assertTrue(form.is_valid())

    ### ARCHIVO NO PROPORCIONADO ###
    def test_upload_file_form_no_file(self):
        form = UploadFileForm(files={})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)

    ### ARCHIVO CON EXTENSIÓN INVÁLIDA ###
    def test_upload_file_form_invalid_extension(self):
        archivo = SimpleUploadedFile("test.txt", b"contenido de prueba", content_type="text/plain")
        form = UploadFileForm(files={'file': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)  # Asegúrate de que haya validación para tipos de archivo específicos si es necesario

    ### ARCHIVO EXCEDE EL TAMAÑO MÁXIMO ###
    def test_upload_file_form_exceeds_max_size(self):
        archivo = SimpleUploadedFile("test.csv", b"0" * 3 * 1024 * 1024, content_type="text/csv")  # 3 MB
        form = UploadFileForm(files={'file': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)  # Asegúrate de que haya una validación para el tamaño máximo si está implementada

    ### ARCHIVO JPEG NO PERMITIDO ###
    def test_upload_file_form_invalid_image_format(self):
        archivo = SimpleUploadedFile("test.jpg", b"contenido de imagen", content_type="image/jpeg")
        form = UploadFileForm(files={'file': archivo})
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
