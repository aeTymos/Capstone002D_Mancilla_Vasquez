from django.test import TestCase
from django.contrib.auth.models import User
from management.forms import CustomUserCreationForm
from management.models import Acreditador

class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        # Crear un usuario y acreditador existente para las pruebas de validación
        Acreditador.objects.create(rut_acreditador='12.345.678-9', 
                                   nombre='Juan', 
                                   apellido_paterno='Pérez',
                                   apellido_materno='',
                                   correo='existente@example.com', 
                                   password1 = 'testpassword123', 
                                   password2= 'testpassword123') 
    ### RUT VACÍO ###
    def test_rut_empty(self):
        form_data = {
            'rut': '',
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    ### RUT CON 1 DÍGITO MENOS ###
    def test_rut_with_one_digit_less(self):
        form_data = {
            'rut': '12.345.678-',
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    ### RUT CON 1 DÍGITO MÁS ###
    def test_rut_with_one_digit_more(self):
        form_data = {
            'rut': '123.456.789-01',
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    ### RUT YA EXISTENTE ###
    def test_rut_already_exists(self):
        form_data = {
            'rut': '12.345.678-9',  # RUT ya existente
            'nombre': 'María',
            'apellido_paterno': 'López',
            'apellido_materno': 'Gómez',
            'email': 'maria.lopez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('El RUT ingresado ya existe.', form.errors['rut'])

    ### RUT CON FORMATO INVÁLIDO (CARACTERES) ###
    def test_rut_with_invalid_characters(self):
        form_data = {
            'rut': '12.34A.678-9',
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    ### RUT SIN GUIONES ###
    def test_rut_without_dashes(self):
        form_data = {
            'rut': '123456789',
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    ### NOMBRE VACÍO ###
    def test_nombre_empty(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': '',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### NOMBRE CON CARACTERES ESPECIALES ###
    def test_nombre_with_special_characters(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': 'Juan$#',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### NOMBRE CON NÚMEROS ###
    def test_nombre_with_numbers(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': 'Juan123',
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### NOMBRE DEMASIADO LARGO ###
    def test_nombre_too_long(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': 'J' * 51,  # 51 caracteres
            'apellido_paterno': 'Pérez',
            'apellido_materno': 'López',
            'email': 'juan.perez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    ### APELLIDO PATERNO VACÍO ###
    def test_apellido_paterno_empty(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': 'Carlos',
            'apellido_paterno': '',
            'apellido_materno': 'López',
            'email': 'carlos.martinez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido_paterno', form.errors)

    ### APELLIDO PATERNO CON FORMATO INVÁLIDO ###
    def test_apellido_paterno_with_invalid_format(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': 'Carlos',
            'apellido_paterno': '12345',
            'apellido_materno': 'López',
            'email': 'carlos.martinez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido_paterno', form.errors)

    ### APELLIDO PATERNO DEMASIADO CORTO ###
    def test_apellido_paterno_too_short(self):
        form_data = {
            'rut': '98.765.432-1',
            'nombre': 'Carlos',
            'apellido_paterno': 'P',
            'apellido_materno': 'López',
            'email': 'carlos.martinez@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido_paterno', form.errors)

    ### EMAIL FORMATO INCORRECTO ###
    def test_email_invalid_format(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'correo-invalido',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    ### EMAIL VACÍO ###
    def test_email_empty(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    ### EMAIL SIN DOMINIO ###
    def test_email_without_domain(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'correo@',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    ### EMAIL SIN PARTE LOCAL ###
    def test_email_without_local_part(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': '@dominio.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    ### EMAIL YA EXISTENTE ###
    def test_email_already_exists(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'existente@example.com',  # Email ya existente
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('El correo ingresado ya existe.', form.errors['email'])

    ### CONTRASEÑAS NO COINCIDENTES ###
    def test_passwords_do_not_match(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': 'testpassword123',
            'password2': 'diferentepassword456',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    ### CONTRASEÑA DÉBIL ###
    def test_weak_password(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': '12345',
            'password2': '12345',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    ### CONTRASEÑA SOLO CON LETRAS ###
    def test_password_only_letters(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': 'passwordonly',
            'password2': 'passwordonly',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    ### CONTRASEÑA SOLO CON NÚMEROS ###
    def test_password_only_numbers(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': '1234567890',
            'password2': '1234567890',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    ### CONTRASEÑA DEMASIADO LARGA ###
    def test_password_too_long(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': 'A' * 129,  # 129 caracteres
            'password2': 'A' * 129,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    ### CONTRASEÑA SIN MAYÚSCULAS ###
    def test_password_without_uppercase(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    ### CONTRASEÑA SIN MINÚSCULAS ###
    def test_password_without_lowercase(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': 'TESTPASSWORD123',
            'password2': 'TESTPASSWORD123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    ### CONTRASEÑA SIN NÚMEROS ###
    def test_password_without_numbers(self):
        form_data = {
            'rut': '87.654.321-0',
            'nombre': 'Carlos',
            'apellido_paterno': 'Martínez',
            'apellido_materno': 'González',
            'email': 'nuevo@example.com',
            'password1': 'TestPassword',
            'password2': 'TestPassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)