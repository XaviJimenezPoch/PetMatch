from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_mascota, name='subir_mascota'),
    path('listar/', views.listar_mascotas, name='listar_mascotas'),
]