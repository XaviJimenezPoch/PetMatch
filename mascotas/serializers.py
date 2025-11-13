from rest_framework import serializers
from .models import Mascota

class MascotaSerializer(serializers.ModelSerializer):
    propietario_username = serializers.CharField(source='propietario.username', read_only=True)
    
    class Meta:
        model = Mascota
        fields = '__all__'
        read_only_fields = ('propietario', 'fecha_creacion', 'fecha_actualizacion')