from django.contrib import admin
from .models import Acreditador, Acreditado, Encargado, Acceso, Empresa, Rol, Evento, Acreditacion, \
    Asistencia

# Register your models here.
admin.site.register(Acreditador)
admin.site.register(Acreditado)
admin.site.register(Asistencia)
admin.site.register(Acreditacion)
admin.site.register(Encargado)
admin.site.register(Acceso)
admin.site.register(Empresa)
admin.site.register(Rol)
admin.site.register(Evento)