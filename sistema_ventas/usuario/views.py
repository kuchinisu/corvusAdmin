from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from cobro.views import index

from .models import Usuarios

def iniciar_secion(request):    
    return render(request, 'pages/usuario/iniciar_secion.html')

def registrarse(request):
    return render(request, 'pages/usuario/registrarse.html')

def iniciar_secion_autentic(request):
    if request.method == 'GET':
        usuario = request.GET.get('usuario')
        contrasena = request.GET.get('contraseña')
    usuario = Usuarios.objects.filter(nombre=usuario, key=contrasena)

    if usuario.exists():
        return redirect('indexs', id=usuario[0].id_us)#
    else:
        return render(request, 'err/error_usuario.html')
