from django.db import models

# Create your models here.
class Contacto(models.Model):

    opciones_contacto = [
        [0, 'Consulta'],
        [1, 'Envío de nómina'],
    ]

    nombre = models.CharField(max_length=30)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_contacto)
    mensaje = models.TextField(max_length=300)
    archivo = models.FileField(upload_to='nominas/')

    def __str__(self):
        return self.id