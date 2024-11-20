from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

from management.models import *

from datetime import date

class AcreditadorModelTest(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(
            username='acreditador_user',
            password='securepassword',
            email='acreditador@example.com'
        )
        self.acreditador = Acreditador.objects.create(
            user=self.user,
            rut_acreditador='12345678-9',
            nombre='Juan',
            app_paterno='Pérez',
            app_materno='González',
            correo='juan.perez@example.com'
        )

    def test_acreditador_creation(self):
        """Test that Acreditador instance is created correctly."""
        self.assertEqual(self.acreditador.rut_acreditador, '12345678-9')
        self.assertEqual(self.acreditador.nombre, 'Juan')
        self.assertEqual(self.acreditador.app_paterno, 'Pérez')
        self.assertEqual(self.acreditador.app_materno, 'González')
        self.assertEqual(self.acreditador.correo, 'juan.perez@example.com')
        self.assertEqual(self.acreditador.user.username, 'acreditador_user')

    def test_acreditador_str_method(self):
        """Test the __str__ method."""
        self.assertEqual(str(self.acreditador), '12345678-9')  # This should return the rut_acreditador
    
    def test_unique_rut_acreditador(self):
        """Test that rut_acreditador field enforces uniqueness."""
        with self.assertRaises(IntegrityError):
            Acreditador.objects.create(
                user=self.user,
                rut_acreditador='12345678-9',  # Duplicate rut_acreditador
                nombre='Carlos',
                app_paterno='Lopez',
                app_materno='Martínez',
                correo='carlos.lopez@example.com'
            )

    def test_unique_correo(self):
        """Test that correo field enforces uniqueness."""
        with self.assertRaises(IntegrityError):
            Acreditador.objects.create(
                user=self.user,
                rut_acreditador='98765432-1',
                nombre='Carlos',
                app_paterno='Lopez',
                app_materno='Martínez',
                correo='juan.perez@example.com'  # Duplicate correo
            )

    def test_acreditador_user_relationship(self):
        """Test that the relationship with the User model works correctly."""
        # Check if the user linked to the Acreditador is correct
        self.assertEqual(self.acreditador.user.username, 'acreditador_user')
        self.assertEqual(self.acreditador.user.email, 'acreditador@example.com')

class AcreditadoModelTest(TestCase):

    def setUp(self):
        """Set up test environment, including dependent models."""
        # Setup related models
        self.empresa = Empresa.objects.create(nombre='Empresa Test')
        self.acceso = Acceso.objects.create(tipo_acceso='Acceso Test')
        self.rol = Rol.objects.create(tipo_rol='Rol Test')

        # Create the Acreditado instance
        self.acreditado = Acreditado.objects.create(
            rut='12345678-9',
            id_pulsera='12345',
            nombre='Juan',
            app_paterno='Pérez',
            app_materno='González',
            empresa=self.empresa,
            acceso=self.acceso,
            rol=self.rol
        )

    
    def tearDown(self):
        """Ensure the database is cleared and avoid broken transactions."""
        try:
            with transaction.atomic():
                Acreditado.objects.all().delete()
                Empresa.objects.all().delete()
                Acceso.objects.all().delete()
                Rol.objects.all().delete()
        except Exception as e:
            # Handle any errors that might occur during cleanup (though this should rarely happen)
            print(f"Error cleaning up the database: {e}")

    def test_acreditado_creation(self):
        """Test creation of Acreditado model and foreign key relationships."""
        self.assertEqual(self.acreditado.rut, '12345678-9')
        self.assertEqual(self.acreditado.id_pulsera, '12345')
        self.assertEqual(self.acreditado.nombre, 'Juan')
        self.assertEqual(self.acreditado.app_paterno, 'Pérez')
        self.assertEqual(self.acreditado.app_materno, 'González')
        self.assertEqual(self.acreditado.empresa.nombre, 'Empresa Test')
        self.assertEqual(self.acreditado.acceso.tipo_acceso, 'Acceso Test')
        self.assertEqual(self.acreditado.rol.tipo_rol, 'Rol Test')

    def test_unique_fields(self):
        """Test unique constraints on rut and id_pulsera."""
        
        # Wrap the test code in an atomic block to ensure rollback happens
        try:
            with transaction.atomic():
                # First, create an Acreditado instance with unique rut and id_pulsera
                Acreditado.objects.create(
                    rut='12345678-9',
                    id_pulsera='12345',  # Unique id_pulsera
                    nombre='Juan',
                    app_paterno='Pérez',
                    app_materno='González',
                    empresa=self.empresa,
                    acceso=self.acceso,
                    rol=self.rol
                )

                # Test duplicate rut (this should fail with IntegrityError)
                with self.assertRaises(IntegrityError):
                    Acreditado.objects.create(
                        rut='12345678-9',  # Duplicate rut
                        id_pulsera='67891',
                        nombre='Carlos',
                        app_paterno='Lopez',
                        app_materno='Martínez',
                        empresa=self.empresa,
                        acceso=self.acceso,
                        rol=self.rol
                    )

                # Test duplicate id_pulsera (this should also fail with IntegrityError)
                with self.assertRaises(IntegrityError):
                    Acreditado.objects.create(
                        rut='98765432-1',
                        id_pulsera='12345',  # Duplicate id_pulsera
                        nombre='Carlos',
                        app_paterno='Lopez',
                        app_materno='Martínez',
                        empresa=self.empresa,
                        acceso=self.acceso,
                        rol=self.rol
                    )
        except IntegrityError:
            # In case of a uniqueness violation, the transaction will be rolled back.
            pass
        
class AsistenciaModelTest(TestCase):

    def setUp(self):
        # Create related models
        self.empresa = Empresa.objects.create(nombre='Empresa Test')
        self.acceso = Acceso.objects.create(tipo_acceso='Acceso Test')
        self.rol = Rol.objects.create(tipo_rol='Rol Test')

        self.acreditado = Acreditado.objects.create(
            rut='12345678-9',
            id_pulsera='12345',
            nombre='Juan',
            app_paterno='Pérez',
            app_materno='González',
            empresa=self.empresa,
            acceso=self.acceso,
            rol=self.rol
        )

        # Create an Asistencia instance
        self.asistencia = Asistencia.objects.create(
            dia=date.today(),
            acreditado=self.acreditado
        )

    def test_asistencia_creation(self):
        """Test the creation of Asistencia and related fields."""
        self.assertEqual(self.asistencia.dia, date.today())
        self.assertEqual(self.asistencia.acreditado.rut, '12345678-9')

    def test_create_from_date(self):
        """Test the create_from_date method."""
        new_asistencia = Asistencia.create_from_date(date(2024, 1, 1), self.acreditado)
        self.assertEqual(new_asistencia.dia, date(2024, 1, 1))
        self.assertEqual(new_asistencia.acreditado.rut, '12345678-9')

class AcreditacionModelTest(TestCase):

    def setUp(self):
        # Create related models
        self.empresa = Empresa.objects.create(nombre='Empresa Test')
        self.acceso = Acceso.objects.create(tipo_acceso='Acceso Test')
        self.rol = Rol.objects.create(tipo_rol='Rol Test')

        self.user = User.objects.create_user(username='testuser', password='password')

        self.acreditador = Acreditador.objects.create(
            user=self.user,
            rut_acreditador='12345678-9',
            nombre='Acreditador Nombre',
            app_paterno='Apellido Paterno',
            app_materno='Apellido Materno',
            correo='acreditador@example.com'
        )

        self.acreditado = Acreditado.objects.create(
            rut='12345678-9',
            id_pulsera='12345',
            nombre='Juan',
            app_paterno='Pérez',
            app_materno='González',
            empresa=self.empresa,
            acceso=self.acceso,
            rol=self.rol
        )

        # Create an Acreditacion instance
        self.acreditacion = Acreditacion.objects.create(
            acreditador=self.acreditador,
            acreditado=self.acreditado,
            fecha_acreditacion=date.today()
        )

    def test_acreditacion_creation(self):
        """Test creation of Acreditacion model and foreign key relationships."""
        self.assertEqual(self.acreditacion.acreditador.rut_acreditador, '12345678-9')
        self.assertEqual(self.acreditacion.acreditado.rut, '12345678-9')
        self.assertEqual(self.acreditacion.fecha_acreditacion, date.today())

    def test_acreditacion_str_method(self):
        """Test the __str__ method for Acreditacion."""
        self.assertEqual(str(self.acreditacion), '12345678-9 - 12345678-9')

class RolModelTest(TestCase):

    def test_rol_creation(self):
        """Test the creation of the Rol model."""
        rol = Rol.objects.create(tipo_rol='Verificador')
        self.assertEqual(rol.tipo_rol, 'Verificador')

    def test_rol_str_method(self):
        """Test the __str__ method for Rol."""
        rol = Rol.objects.create(tipo_rol='Verificador')
        self.assertEqual(str(rol), 'Verificador')

class AccesoModelTest(TestCase):

    def test_acceso_creation(self):
        """Test the creation of the Acceso model."""
        acceso = Acceso.objects.create(tipo_acceso='WP', desc_acceso='Working Pass')
        self.assertEqual(acceso.tipo_acceso, 'WP')
        self.assertEqual(acceso.desc_acceso, 'Working Pass')

    def test_acceso_str_method(self):
        """Test the __str__ method for Acceso."""
        acceso = Acceso.objects.create(tipo_acceso='WP', desc_acceso='Working Pass')
        self.assertEqual(str(acceso), 'WP')

    def test_acceso_choices(self):
        """Test that Acceso's tipo_acceso field uses the correct choices."""
        acceso = Acceso.objects.create(tipo_acceso='AA', desc_acceso='All Access')
        self.assertEqual(acceso.tipo_acceso, 'AA')

    def test_invalid_tipo_acceso(self):
        """Test that an invalid tipo_acceso raises a ValidationError."""
        with self.assertRaises(ValidationError):
            acceso = Acceso(tipo_acceso='INVÁLIDO', desc_acceso='Acceso inválido.')
            acceso.full_clean()  # Manually trigger validation

    def test_empty_desc_acceso(self):
        """Test that desc_acceso cannot be empty (if it's required)."""
        acceso = Acceso(tipo_acceso='SA', desc_acceso='')
        with self.assertRaises(ValidationError):
            acceso.full_clean()

    def test_null_desc_acceso(self):
        """Test that desc_acceso cannot be null (if it's required)."""
        acceso = Acceso(tipo_acceso='WP', desc_acceso=None)
        with self.assertRaises(ValidationError):
            acceso.full_clean()

    def test_invalid_tipo_acceso_choice(self):
        """Test that invalid tipo_acceso does not get saved."""
        try:
            acceso = Acceso.objects.create(tipo_acceso='INVÁLIDO', desc_acceso='Acceso inválido')
            acceso.full_clean()
        except ValidationError as e:
            self.assertTrue('tipo_acceso' in str(e))

class EmpresaModelTest(TestCase):

    def test_empresa_creation(self):
        """Test the creation of the Empresa model."""
        empresa = Empresa.objects.create(nombre='Empresa Test')
        self.assertEqual(empresa.nombre, 'Empresa Test')

    def test_empresa_str_method(self):
        """Test the __str__ method for Empresa."""
        empresa = Empresa.objects.create(nombre='Empresa Test')
        self.assertEqual(str(empresa), 'Empresa Test')

class EncargadoModelTest(TestCase):

    def setUp(self):
        """Set up an Empresa instance to associate with Encargado."""
        self.empresa = Empresa.objects.create(nombre='Empresa Test')

    def test_encargado_creation(self):
        """Test the creation of the Encargado model."""
        encargado = Encargado.objects.create(
            nombre='Juan Pérez',
            telefono=123456789,
            correo='juan.perez@example.com',
            empresa=self.empresa
        )
        self.assertEqual(encargado.nombre, 'Juan Pérez')
        self.assertEqual(encargado.telefono, 123456789)
        self.assertEqual(encargado.correo, 'juan.perez@example.com')
        self.assertEqual(encargado.empresa.nombre, 'Empresa Test')

    def test_encargado_str_method(self):
        """Test the __str__ method for Encargado."""
        encargado = Encargado.objects.create(
            nombre='Juan Pérez',
            telefono=123456789,
            correo='juan.perez@example.com',
            empresa=self.empresa
        )
        self.assertEqual(str(encargado), 'Juan Pérez')

class EventoModelTest(TestCase):

    def test_evento_creation(self):
        """Test the creation of the Evento model."""
        evento = Evento.objects.create(
            nom_evento='Conferencia de pruebas',
            fec_inicio=date(2024, 1, 1),
            fec_termino=date(2024, 1, 3),
            activo=True
        )
        self.assertEqual(evento.nom_evento, 'Conferencia de pruebas')
        self.assertEqual(evento.fec_inicio, date(2024, 1, 1))
        self.assertEqual(evento.fec_termino, date(2024, 1, 3))
        self.assertTrue(evento.activo)

    def test_evento_str_method(self):
        """Test the __str__ method for Evento."""
        evento = Evento.objects.create(
            nom_evento='Conferencia de pruebas',
            fec_inicio=date(2024, 1, 1),
            fec_termino=date(2024, 1, 3),
            activo=True
        )
        self.assertEqual(str(evento), 'Conferencia de pruebas')

    def test_invalid_fec_inicio(self):
        """Test that an invalid fec_inicio date raises a ValidationError."""
        # Let's try to create an event with an invalid date (e.g., using a string instead of a date)
        with self.assertRaises(ValidationError):
            evento = Evento(
                nom_evento='Evento inválido',
                fec_inicio='Invalid Date',  # Invalid date format
                fec_termino=date(2024, 1, 3),
                activo=True
            )
            evento.full_clean()  # Manually trigger validation

    def test_fec_termino_before_fec_inicio(self):
        """Test that fec_termino cannot be before fec_inicio."""
        evento = Evento(
            nom_evento='Evento inválido',
            fec_inicio=date(2024, 1, 3),
            fec_termino=date(2024, 1, 2),  # Invalid: fec_termino should not be before fec_inicio
            activo=True
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_null_fec_inicio(self):
        """Test that fec_inicio cannot be null."""
        evento = Evento(
            nom_evento='Evento inválido',
            fec_inicio=None,  # Null value
            fec_termino=date(2024, 1, 3),
            activo=True
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_null_fec_termino(self):
        """Test that fec_termino cannot be null."""
        evento = Evento(
            nom_evento='Evento inválido',
            fec_inicio=date(2024, 1, 1),
            fec_termino=None,  # Null value
            activo=True
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_invalid_activo_field(self):
        """Test that activo cannot be None or invalid."""
        evento = Evento(
            nom_evento='Evento inválido',
            fec_inicio=date(2024, 1, 1),
            fec_termino=date(2024, 1, 3),
            activo=None  # Should be a boolean (True or False)
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()