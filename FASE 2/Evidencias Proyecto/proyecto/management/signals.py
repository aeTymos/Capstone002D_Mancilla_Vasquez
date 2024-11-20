from django.db.models.signals import post_save
from django.dispatch import receiver
from management.models import Acreditado, Acreditacion, Evento, Acreditador
from django.contrib.auth.models import User
from datetime import date

@receiver(post_save, sender=Acreditado)
def crear_acreditacion(sender, instance, created, **kwargs):
    if created:
        # Obtén el evento al que se debe asociar (puedes ajustar esto según tu lógica)
        evento = Evento.objects.last() 

        # Obtén el acreditador 
        acreditador = Acreditador.objects.first()  # Cambia esto por tu lógica para obtener el acreditador

        # Crea un nuevo registro en la tabla Acreditacion
        Acreditacion.objects.create(
            evento=evento,
            acreditador=acreditador,
            acreditado=instance,
            fecha_acreditacion=instance.dias_de_trabajo().first() or date.today()  # Ajusta la fecha si es necesario
        )
