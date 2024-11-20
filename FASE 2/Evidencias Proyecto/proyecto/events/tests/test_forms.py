from django.test import TestCase
from events.forms import EventoForm
from management.models import Evento
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime

class EventoFormTest(TestCase):
    
    ### FORMULARIO VÁLIDO ###
    def test_valid_form(self):
        imagen = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'nom_evento': 'Evento de prueba',
            'fec_inicio': '01/01/2024',
            'fec_termino': '31/01/2024'
        }
        form = EventoForm(data=form_data, files={'imagen': imagen})
        self.assertTrue(form.is_valid())

    ### NOMBRE DEL EVENTO VACÍO ###
    def test_nom_evento_empty(self):
        imagen = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'nom_evento': '',
            'fec_inicio': '01/01/2024',
            'fec_termino': '31/01/2024'
        }
        form = EventoForm(data=form_data, files={'imagen': imagen})
        self.assertFalse(form.is_valid())
        self.assertIn('nom_evento', form.errors)

    ### NOMBRE DEL EVENTO MUY LARGO ###
    def test_nom_evento_too_long(self):
        imagen = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'nom_evento': 'Evento' * 50,  # Más de la longitud permitida
            'fec_inicio': '01/01/2024',
            'fec_termino': '31/01/2024'
        }
        form = EventoForm(data=form_data, files={'imagen': imagen})
        self.assertFalse(form.is_valid())
        self.assertIn('nom_evento', form.errors)

    ### FECHA DE INICIO VACÍA ###
    def test_fec_inicio_empty(self):
        imagen = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'nom_evento': 'Evento de prueba',
            'fec_inicio': '',
            'fec_termino': '31/01/2024'
        }
        form = EventoForm(data=form_data, files={'imagen': imagen})
        self.assertFalse(form.is_valid())
        self.assertIn('fec_inicio', form.errors)

    ### FECHA DE TÉRMINO VACÍA ###
    def test_fec_termino_empty(self):
        imagen = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'nom_evento': 'Evento de prueba',
            'fec_inicio': '01/01/2024',
            'fec_termino': ''
        }
        form = EventoForm(data=form_data, files={'imagen': imagen})
        self.assertFalse(form.is_valid())
        self.assertIn('fec_termino', form.errors)

    ### RANGO DE FECHAS INVÁLIDO (FECHA DE INICIO DESPUÉS DE FECHA DE TÉRMINO) ###
    def test_invalid_date_range(self):
        imagen = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            'nom_evento': 'Evento de prueba',
            'fec_inicio': '31/01/2024',
            'fec_termino': '01/01/2024'  # Fecha de inicio posterior a fecha de término
        }