from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Mascota
import json

@csrf_exempt
def subir_mascota(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo', 'perro')
            descripcion = request.POST.get('descripcion', '')
            edad = request.POST.get('edad', 1)
            ubicacion = request.POST.get('ubicacion', 'Ciudad')
            foto = request.FILES.get('foto')
            
            # Validar que haya una foto
            if not foto:
                return JsonResponse({
                    'success': False,
                    'error': 'Debes subir una foto de la mascota'
                }, status=400)
            
            # Crear la mascota (por ahora con el primer usuario)
            from django.contrib.auth.models import User
            usuario = User.objects.first()  # En producción usarías request.user
            
            mascota = Mascota.objects.create(
                nombre=nombre,
                tipo=tipo,
                descripcion=descripcion,
                edad=edad,
                ubicacion=ubicacion,
                foto=foto,
                propietario=usuario
            )
            
            return JsonResponse({
                'success': True,
                'mascota_id': mascota.id,
                'foto_url': mascota.foto.url,
                'message': 'Mascota creada exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def listar_mascotas(request):
    """Vista para obtener todas las mascotas"""
    mascotas = Mascota.objects.all().order_by('-fecha_creacion')
    
    mascotas_data = []
    for mascota in mascotas:
        mascotas_data.append({
            'id': mascota.id,
            'nombre': mascota.nombre,
            'tipo': mascota.tipo,
            'foto_url': mascota.foto.url,
            'descripcion': mascota.descripcion,
            'edad': mascota.edad,
            'ubicacion': mascota.ubicacion,
            'propietario': mascota.propietario.username
        })
    
    return JsonResponse({
        'success': True,
        'mascotas': mascotas_data
    })