from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_mascota, name='subir_mascota'),
    path('listar/', views.listar_mascotas, name='listar_mascotas'),
    path('<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('mis-mascotas/', views.mis_mascotas, name='mis_mascotas'),
    path('eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
]