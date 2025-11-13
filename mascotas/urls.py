from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'mascotas', MascotaViewSet)


urlpatterns = [
    path('subir/', views.subir_mascota, name='subir_mascota'),
    path('listar/', views.listar_mascotas, name='listar_mascotas'),
     path('api/', include(router.urls)),
]