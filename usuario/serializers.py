from rest_framework import serializers
from .models import Tarea # Asume que tienes un modelo llamado Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        # Campos que quieres exponer en la API
        fields = ('id', 'titulo', 'descripcion', 'completado', 'fecha_creacion')