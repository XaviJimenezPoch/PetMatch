from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    # AbstractUser ya incluye id, password y username (pero username lo dejo)
    #REGISTRO RÁPIDO
    # user_id = models.AutoField(primary_key=True)
    # password = models.CharField(max_length=128)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('usuario', 'Usuario'),
        ('protectora', 'Protectora')
    ]
    
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario')
    USERNAME_FIELD = 'username'
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_usuario')
    #REGISTRO COMPLETO
    #camps a consensuar entre tots
    telefono = models.CharField(max_length=15, blank=True, null=True)
    data_nacimiento = models.DateField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfils/', blank=True, null=True)
    GENERO_CHOICES = [
        ('M', 'Masculí'),
        ('F', 'Femení'),
        ('O', 'Altres'),
        ('N', 'Preferisc no dir-ho')
    ]

    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True, null=True)
    necesidades_esp = models.BooleanField(default=False)
    mascota_previa = models.BooleanField(default=False)
    CASA_CHOICES = [
        ('apartamento', 'Apartamento'),
        ('casa_pequeña', 'Casa pequeña'),
        ('casa_grande', 'Casa grande'),
        ('casa_con_jardin', 'Casa con jardín'),
        ('finca', 'Finca/Casa rural')
    ]
    tipo_vivienda = models.CharField( max_length=20, choices=CASA_CHOICES, blank=True, null=True)


    class Meta:
        db_table = 'perfil_usuario'
        verbose_name = 'Perfil Usuario'
        verbose_name_plural = 'Perfiles Usuarios'
        
class PerfilProtectora(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_protectora')
        # Camps específics per protectores
    nombre_protectora = models.CharField(max_length=200, blank=True, null=True)
    direccion_completa = models.TextField(blank=True, null=True)
    web = models.URLField(blank=True, null=True)
    nucleo_zoologico = models.CharField(max_length=20, blank=True, null=True )
    



    class Meta:
        db_table = 'perfil_protectora'
        verbose_name = 'Protectora'
        verbose_name_plural = 'Protectoras'
        
        


# class Role(models.Model):
#     PERMISION_CHOICES = [
#         (0, 'Admin'),
#         (1, 'Usuario'),
#         (2, 'Protectora'),
# ]
    
#     role_name = models.CharField(max_length=50, primary_key=True)
#     admin = models.IntegerField(choices= PERMISION_CHOICES, default=0)
#     usuario = models.IntegerField(choices= PERMISION_CHOICES, default=0)
#     protectora = models.IntegerField(choices= PERMISION_CHOICES, default=0)

#     class Meta:
#         db_table = 'roles'
#         verbose_name = 'Rol'
#         verbose_name_plural = 'Roles'
    
#     def __str__(self):
#         return self.role_name
    
# class UserRole(models.Model):

#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'user_roles'
#         verbose_name = 'Rol de usuario'
#         verbose_name_plural = 'Roles de usuario'
#         unique_together = ('usuario', 'role') # No se le puede poner el mismo rol dos veces al mismo usuario

#     def __str__(self):
#         return f"{self.user_id.username} - {self.role.role_name}"