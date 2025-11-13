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
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioCreateSerializer
from django.contrib.auth.hashers import check_password 
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


#hablar con xavi: qué puede ver la gente? 
#los usuarios sólo pueden ver su propio usuario
#los usuarios pueden ver todas las protectoras
#las protectoras pueden ver todos los usuarios??????
#las protectoras pueden ver otras protectoras
#c ada uno se edita lo suyo



class UsuarioPermissions(BasePermission):
    """
    Permisos personalitzats per usuaris segons rol
    """
    
    def has_permission(self, request, view):
        # Registre i login són públics
        if view.action in ['create', 'login']:
            return True
        
        # La resta necessita autenticació
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Admin pot fer tot
        if user.role == 'admin':
            return True
        
        # Per veure perfils (GET)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            # Usuaris només poden veure:
            if user.role == 'usuario':
                # - El seu propi perfil
                if obj == user:
                    return True
                # - Perfils de protectores
                if obj.role == 'protectora':
                    return True
                # - NO altres usuaris
                return False
            
            # Protectores poden veure:
            elif user.role == 'protectora':
                # - El seu propi perfil
                if obj == user:
                    return True
                # - Altres protectores
                if obj.role == 'protectora':
                    return True
                # - Usuaris (per adopcions)
                if obj.role == 'usuario':
                    return True
                # - NO admins (llevat del seu propi si fos admin)
                return False
        
        # Per editar/eliminar (PUT, PATCH, DELETE)
        else:
            # Admin pot editar qualsevol
            if user.role == 'admin':
                return True
            # Tots els altres només poden editar-se a si mateixos
            return obj == user

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet amb sistema de permisos per rols
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [UsuarioPermissions]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer
    
    def get_queryset(self):
        """
        Filtra els usuaris segons permisos de visualització
        """
        user = self.request.user
        
        # Si no està autenticat, no retorna res
        if not user.is_authenticated:
            return Usuario.objects.none()
        
        # Admin veu tots els usuaris
        if user.role == 'admin':
            return Usuario.objects.all()
        
        # Usuaris veuen:
        elif user.role == 'usuario':
            # - Ell mateix + totes les protectores
            return Usuario.objects.filter(
                models.Q(id=user.id) | 
                models.Q(role='protectora')
            )
        
        # Protectores veuen:
        elif user.role == 'protectora':
            # - Ella mateixa + altres protectores + usuaris
            return Usuario.objects.filter(
                models.Q(id=user.id) | 
                models.Q(role='protectora') | 
                models.Q(role='usuario')
            )
        
        return Usuario.objects.none()
    
    # CREATE - Registre (públic)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            token, created = Token.objects.get_or_create(user=usuario)
            
            response_data = UsuarioSerializer(usuario).data
            response_data['token'] = token.key
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # UPDATE - Només admin o el propi usuari
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
    
        if 'password' in request.data:
            instance.set_password(request.data['password'])
            instance.save()
            request.data.pop('password')  
    
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if 'password' in request.data:
            instance.set_password(request.data['password'])
            instance.save()
            request.data.pop('password') 
        
        return super().partial_update(request, *args, **kwargs)
    
    # LOGIN
    @action(detail=False, methods=['post'], url_path='login', 
        permission_classes=[AllowAny])
    def login(self, request):
        # Login sense serializer - més simple
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username y password requeridos'}, 
                        status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
        
            response_data = UsuarioSerializer(user).data
            response_data['access'] = access_token
            response_data['refresh'] = str(refresh)
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Credenciales inválidas'}, 
                    status=status.HTTP_401_UNAUTHORIZED)
    
    # LOGOUT
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Sesión cerrada correctamente'})
        except:
            return Response({'error': 'No hay sesión activa'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    # PERFIL ACTUAL
    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    # CANVIAR PASSWORD
    @action(detail=True, methods=['post'], url_path='change-password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not check_password(current_password, user.password):
            return Response({'error': 'Contraseña actual incorrecta'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)  # Usar set_password en lloc de make_password
        user.save()
        
        return Response({'message': 'Contraseña cambiada correctamente'})