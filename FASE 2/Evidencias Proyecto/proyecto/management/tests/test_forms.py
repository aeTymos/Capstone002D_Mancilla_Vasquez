from django.test import TestCase
from management.forms import AcreditadoForm
from management.models import Acreditado, Empresa, Acceso, Rol
from django.core.exceptions import ValidationError
from datetime import datetime

class AcreditadoFormTest(TestCase):
    def setUp(self):
        # Crear instancias de apoyo para los campos de relación
        self.empresa = Empresa.objects.create(nombre="Empresa de prueba")
        self.acceso = Acceso.objects.create(tipo_acceso="WP")
        self.rol = Rol.objects.create(tipo_rol="Cargador")

    ### FORMULARIO VÁLIDO ###
    def test_valid_form(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertTrue(form.is_valid())

    ### RUT VACÍO ###
    def test_rut_empty(self):
        form_data = {
            'rut': '',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    ### RUT CON FORMATO INCORRECTO ###
    def test_rut_invalid_format(self):
        form_data = {
            'rut': '12345678',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    ### NOMBRE VACÍO ###
    def test_nombre_empty(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': '',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### NOMBRE CON CARACTERES NO PERMITIDOS ###
    def test_nombre_with_invalid_characters(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis123!',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### APELLIDO PATERNO VACÍO ###
    def test_app_paterno_empty(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis',
            'app_paterno': '',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('app_paterno', form.errors)

    ### FECHA DE INICIO VACÍA ###
    def test_fec_inicio_empty(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fec_inicio', form.errors)

    ### FECHA DE TÉRMINO VACÍA ###
    def test_fec_termino_empty(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fec_termino', form.errors)

    ### RANGO DE FECHAS INVÁLIDO (FECHA DE INICIO DESPUÉS DE FECHA DE TÉRMINO) ###
    def test_invalid_date_range(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': 'Ana',
            'app_paterno': 'López',
            'app_materno': 'Santos',
            'fec_inicio': '2024-12-31',
            'fec_termino': '2024-01-01',  # Fecha de inicio después de la fecha de término
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('La fecha de inicio no puede ser mayor a la fecha de término.', form.errors['__all__'])

    ### EMPRESA VACÍA ###
    def test_empresa_empty(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': '',  # Empresa vacía
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('empresa', form.errors)

    ### ACCESO VACÍO ###
    def test_acceso_empty(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': '',  # Acceso vacío
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('acceso', form.errors)

    ### ROL VACÍO ###
    def test_rol_empty(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': 'Luis',
            'app_paterno': 'Gómez',
            'app_materno': 'Martínez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': '',  # Rol vacío
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rol', form.errors)

    ### FORMULARIO CON DATOS FALTANTES ###
    def test_missing_required_field(self):
        form_data = {
            'rut': '12.345.678-9',
            'nombre': '',
            'app_paterno': 'Gómez',
            'fec_inicio': '2024-01-01',
            'fec_termino': '2024-12-31',
            'empresa': self.empresa.id,
            'acceso': self.acceso.id,
            'rol': self.rol.id,
        }
        form = AcreditadoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)