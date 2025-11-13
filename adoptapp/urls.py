
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
     path('usuario/', include('usuario.urls')),
    path('mascotas/', include('mascotas.urls')), 
    path('api/', include('usuario.urls'))
]
