from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, date

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

class Acreditador(AbstractUser):
    # TODO: Cambiar a int y agregar dv
    # rut = models.IntegerField(unique=True)
    # dv = models.IntegerField()
    rut = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.rut

class Acreditado(models.Model):
    # TODO: Cambiar a int y agregar dv
    # rut = models.IntegerField(unique=True)
    # dv = models.IntegerField()
    rut = models.CharField(max_length=12, unique=True)
    id_pulsera = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=40)
    app_paterno = models.CharField(max_length=40)
    app_materno = models.CharField(max_length=40)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    acceso = models.ForeignKey(Acceso, on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def __str__(self):
        return self.rut    

    def dias_de_trabajo(self):
        return Asistencia.objects.filter(acreditado=self).values_list('dia', flat=True)

class Asistencia(models.Model):
    dia = models.DateField()
    acreditado = models.ForeignKey(Acreditado, on_delete=models.CASCADE)

    @classmethod
    def create_from_date(cls, fecha, acreditado):
        return cls(
            dia=fecha,
            acreditado=acreditado
        )

    def __str__(self):
        return f"{self.acreditado.nombre} - {self.dia.day}/{self.dia.month}/{self.dia.year}"

class Evento(models.Model):
    nom_evento = models.CharField(max_length=50)
    fec_inicio = models.DateField()
    fec_termino = models.DateField()
    imagen = models.ImageField(upload_to='event_images', null=True, blank=True)
    activo = models.BooleanField(default=True)
    accmax = models.IntegerField()
    accmin = models.IntegerField()

    def __str__(self):
        return self.nom_evento


class Acreditacion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT)
    acreditador = models.ForeignKey(Acreditador, on_delete=models.PROTECT)
    acreditado = models.ForeignKey(Acreditado, on_delete=models.CASCADE)
    fecha_acreditacion = models.DateField()

    def __str__(self):
        return f'{self.acreditador} - {self.acreditado} - {self.evento}'