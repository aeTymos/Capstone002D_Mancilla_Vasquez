from django.urls import path, include
from rest_framework import routers
from .views import AcreditadoViewset, AcreditacionViewset, AcreditadorViewset, RolViewset, AccesoViewset, \
    EmpresaViewset, EncargadoViewset, EventoViewset

router = routers.DefaultRouter()
router.register('acreditado', AcreditadoViewset)
router.register('acreditacion', AcreditacionViewset)
router.register('acreditador', AcreditadorViewset)
router.register('acceso', AccesoViewset)
router.register('rol', RolViewset)
router.register('empresa', EmpresaViewset)
router.register('encargado', EncargadoViewset)
router.register('evento', EventoViewset)

urlpatterns = [
    path('api/', include(router.urls)),
]