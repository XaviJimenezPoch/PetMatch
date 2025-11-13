# from django.shortcuts import render, redirect   
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .forms import LoginForm
# from .models import UserRole, Role

# def login_view(request):
    
#     if request.user.is_authenticated:
#         return redirect('dashboard')  

#     if request.method == 'POST':

#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('dashboard')  
#             else:
#                 messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        
#         else:
#             form = LoginForm()
        
#         return render(request, 'usuario/login.html', {'form': form})

# @login_required
# def logout_view(request):
#     logout(request)
#     messages.success(request, 'Has cerrado sesión correctamente.')
#     return redirect('login')          


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer, LoginSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD de usuarios via API REST
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):
        """
        Define permisos según la acción
        """
        if self.action in ['create', 'login']:
            permission_classes = [AllowAny]  # Registro y login público
        else:
            permission_classes = [IsAuthenticated]  # Resto requiere autenticación
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Devuelve el serializer apropiado según la acción
        """
        if self.action == 'create':
            return UsuarioCreateSerializer
        elif self.action == 'login':
            return LoginSerializer
        return UsuarioSerializer
    
    # CREATE - Registro de usuario
    def create(self, request, *args, **kwargs):
        """
        POST /api/usuarios/
        Crea un nuevo usuario
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Encriptar la contraseña antes de guardar
            validated_data = serializer.validated_data
            validated_data['password'] = make_password(validated_data['password'])
            
            # Crear el usuario
            usuario = Usuario.objects.create(**validated_data)
            
            # Crear token de autenticación
            token, created = Token.objects.get_or_create(user=usuario)
            
            # Devolver respuesta con usuario y token
            response_data = UsuarioSerializer(usuario).data
            response_data['token'] = token.key
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # READ - Lista de usuarios (GET /api/usuarios/)
    def list(self, request, *args, **kwargs):
        """
        GET /api/usuarios/
        Lista todos los usuarios (solo para admin)
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    # READ - Detalle de usuario (GET /api/usuarios/{id}/)
    def retrieve(self, request, *args, **kwargs):
        """
        GET /api/usuarios/{id}/
        Obtiene un usuario específico
        """
        return super().retrieve(request, *args, **kwargs)
    
    # UPDATE - Actualizar usuario (PUT /api/usuarios/{id}/)
    def update(self, request, *args, **kwargs):
        """
        PUT /api/usuarios/{id}/
        Actualiza un usuario completo
        """
        instance = self.get_object()
        
        # Solo el propio usuario puede editarse
        if instance != request.user:
            return Response({'error': 'No puedes editar otro usuario'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Si hay password en los datos, encriptarlo
        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])
        
        return super().update(request, *args, **kwargs)
    
    # UPDATE - Actualizar parcial (PATCH /api/usuarios/{id}/)
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /api/usuarios/{id}/
        Actualiza campos específicos de un usuario
        """
        instance = self.get_object()
        
        # Solo el propio usuario puede editarse
        if instance != request.user:
            return Response({'error': 'No puedes editar otro usuario'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Si hay password en los datos, encriptarlo
        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])
        
        return super().partial_update(request, *args, **kwargs)
    
    # DELETE - Eliminar usuario (DELETE /api/usuarios/{id}/)
    def destroy(self, request, *args, **kwargs):
        """
        DELETE /api/usuarios/{id}/
        Elimina un usuario
        """
        instance = self.get_object()
        
        # Solo el propio usuario puede eliminarse
        if instance != request.user:
            return Response({'error': 'No puedes eliminar otro usuario'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)
    
    # ACCIÓN PERSONALIZADA - Login
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        POST /api/usuarios/login/
        Autentica un usuario y devuelve token
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Autenticar usuario
            user = authenticate(username=username, password=password)
            
            if user:
                # Obtener o crear token
                token, created = Token.objects.get_or_create(user=user)
                
                # Devolver datos del usuario y token
                response_data = UsuarioSerializer(user).data
                response_data['token'] = token.key
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            return Response({'error': 'Credenciales inválidas'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # ACCIÓN PERSONALIZADA - Logout
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """
        POST /api/usuarios/logout/
        Cierra sesión eliminando el token
        """
        try:
            # Eliminar token del usuario actual
            request.user.auth_token.delete()
            return Response({'message': 'Sesión cerrada correctamente'}, 
                          status=status.HTTP_200_OK)
        except:
            return Response({'error': 'No hay sesión activa'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    # ACCIÓN PERSONALIZADA - Perfil actual
    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        """
        GET /api/usuarios/profile/
        Obtiene el perfil del usuario autenticado
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    # ACCIÓN PERSONALIZADA - Cambiar contraseña
    @action(detail=True, methods=['post'], url_path='change-password')
    def change_password(self, request, pk=None):
        """
        POST /api/usuarios/{id}/change-password/
        Cambia la contraseña de un usuario
        """
        user = self.get_object()
        
        # Solo el propio usuario puede cambiar su contraseña
        if user != request.user:
            return Response({'error': 'No puedes cambiar la contraseña de otro usuario'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        # Verificar contraseña actual
        if not check_password(current_password, user.password):
            return Response({'error': 'Contraseña actual incorrecta'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Cambiar contraseña
        user.password = make_password(new_password)
        user.save()
        
        return Response({'message': 'Contraseña cambiada correctamente'})
