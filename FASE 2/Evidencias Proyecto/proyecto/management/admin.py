from django.contrib import admin
from .models import Acreditador, Acreditado, Encargado, Acceso, Empresa, Rol

# Register your models here.
admin.site.register(Acreditador)
admin.site.register(Acreditado)
admin.site.register(Encargado)
admin.site.register(Acceso)
admin.site.register(Empresa)
admin.site.register(Rol)