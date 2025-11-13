from django.db import models
from django.contrib.auth.models import User

class Mascota(models.Model):
    # Tipos de mascota
    TIPO_MASCOTA = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_MASCOTA, default='perro')
    foto = models.ImageField(upload_to='mascotas/')
    descripcion = models.TextField()
    edad = models.PositiveIntegerField(help_text="Edad en años")
    ubicacion = models.CharField(max_length=100, default="Ciudad")
    
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"