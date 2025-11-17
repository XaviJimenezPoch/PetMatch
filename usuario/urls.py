from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, login_view, logout_view, profile_view


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Endpoints CRUD bàsics
    path('login/', login_view, name='login'),  # Endpoint per login
    path('logout/', logout_view, name='logout'),  # Endpoint per logout
    path('profile/', profile_view, name='profile'),  # Endpoint per obtenir el perfil
]



""""

=== API REST USUARIS (Recomanat per React) ===
GET       /api/usuarios/                          → Llistar usuaris (segons permisos)
POST      /api/usuarios/                          → Registrar usuari nou
GET       /api/usuarios/{id}/                     → Obtenir usuari específic
PUT       /api/usuarios/{id}/                     → Actualitzar usuari complet
PATCH     /api/usuarios/{id}/                     → Actualitzar camps específics
DELETE    /api/usuarios/{id}/                     → Eliminar usuari
POST      /api/usuarios/login/                    → Login (retorna token)
POST      /api/usuarios/logout/                   → Logout
GET       /api/usuarios/profile/                  → Perfil usuari actual
POST      /api/usuarios/{id}/change-password/     → Canviar contrasenya

"""