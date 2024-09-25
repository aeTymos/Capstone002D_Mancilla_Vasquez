from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.
class Rol(models.Model):
    tipo_rol = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo_rol

ACCESOS = {
    'SA': 'Seleccionar acceso',
    'WP': 'Working Pass',
    'AA': 'All Access',
    'AAA': 'All Areas Access',
    'S': 'Seguridad',
}

class Acceso(models.Model):
    tipo_acceso = models.CharField(max_length=3, choices=ACCESOS, default='SA')
    desc_acceso = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo_acceso
    
class Empresa(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Encargado(models.Model):
    nombre = models.CharField(max_length=40)
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=40, unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Acreditador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut_acreditador = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    app_paterno = models.CharField(max_length=40)
    app_materno = models.CharField(max_length=40)
    correo = models.EmailField(max_length=40, unique=True)

    def __str__(self):
        return self.rut_acreditador

class Acreditado(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    id_pulsera = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=40)
    app_paterno = models.CharField(max_length=40)
    app_materno = models.CharField(max_length=40)
    fec_inicio = models.DateField()
    fec_termino = models.DateField()
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    acceso = models.ForeignKey(Acceso, on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def __str__(self):
        return self.rut

    def dias_de_trabajo(self):
        fecha_inicio = self.fec_inicio
        dias_de_trabajo = []

        while fecha_inicio <= self.fec_termino:
            dias_de_trabajo.append(fecha_inicio)
            fecha_inicio += timedelta(days=1)
        
        return dias_de_trabajo

class Acreditacion(models.Model):
    acreditador = models.ForeignKey(Acreditador, on_delete=models.PROTECT)
    acreditado = models.ForeignKey(Acreditado, on_delete=models.PROTECT)
    fecha_acreditacion = models.DateField()

    def __str__(self):
        return f'{self.acreditador} - {self.acreditado}'

class Evento(models.Model):
    nom_evento = models.CharField(max_length=50)
    fec_inicio = models.DateField()
    fec_termino = models.DateField()
    imagen = models.ImageField(upload_to='event_images', null=True, blank=True)

    def __str__(self):
        return self.nom_evento

