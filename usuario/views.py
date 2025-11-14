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
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario, PerfilUsuario, PerfilProtectora
from .serializers import (
    UsuarioSerializer, 
    UsuarioCreateSerializer,
    PerfilUsuarioSerializer,
    PerfilProtectoraSerializer,
    LoginSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UsuarioSerializer(user).data
                })
            
            return Response(
                {'error': 'Credenciales inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Obtener perfil del usuario actual"""
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para perfiles de usuario"""
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Cada usuario solo ve su propio perfil"""
        return PerfilUsuario.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        """Asociar el perfil al usuario actual"""
        serializer.save(usuario=self.request.user)

class PerfilProtectoraViewSet(viewsets.ModelViewSet):
    """ViewSet para perfiles de protectora"""
    queryset = PerfilProtectora.objects.all()
    serializer_class = PerfilProtectoraSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Solo protectoras pueden acceder a estos perfiles"""
        if self.request.user.role == 'protectora':
            return PerfilProtectora.objects.filter(usuario=self.request.user)
        return PerfilProtectora.objects.none()
    
    def perform_create(self, serializer):
        """Asociar el perfil al usuario actual"""
        if self.request.user.role == 'protectora':
            serializer.save(usuario=self.request.user)