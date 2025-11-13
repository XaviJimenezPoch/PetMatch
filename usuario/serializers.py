from rest_framework import serializers
from .models import Usuario # Asume que tienes un modelo llamado Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    #recoge los datos del usuario, no debemos mostrar la contraseña
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'city', 'role', 'date_joined',
            'telefono', 'data_nacimiento', 'descripcion', 'foto_perfil',
            'genero', 'necesidades_esp', 'mascota_previa', 'tipo_vivienda',
            'nombre_protectora', 'direccion_completa', 'web', 'nucleo_zoologico')
        read_only_fields = ('id', 'date_joined')

        
class UsuarioCreateSerializer(serializers.ModelSerializer):
    #para crear los nuevos usuarios
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Usuario
        fields = ('username', 'password', 'email', 'city', 'role',
            'telefono', 'data_nacimiento', 'descripcion', 'foto_perfil',
            'genero', 'necesidades_esp', 'mascota_previa', 'tipo_vivienda',
            'nombre_protectora', 'direccion_completa', 'web', 'nucleo_zoologico')
    
    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value
    
    def validate_username(self, value):
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este username ya está registrado.")
        return value

    def validate_nucleo_zoologico(self, value):
        if value and not re.match(r'^ES\d{2}\d{3}C\d{6}$', value):
            raise serializers.ValidationError(
                'Formato inválido. Ejemplo: ES12345C000123'
            )
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
class LoginUsuario(serializers.Serializer):
    #login 
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    """
    Serializer per login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)