from django.shortcuts import render, redirect
from usuario.views import iniciar_secion
from usuario.models import Usuarios

def index(request, id="",):
    imagenes_url = '/static/img'

    nombre = ""
    if id:
        id = int(id)
        try:
            usuario = Usuarios.objects.get(id_us=id)
            nombre = usuario.nombre
        except Usuarios.DoesNotExist:
            nombre = ""
    if type(id) is str:
        como_cajero = False
    else:
        if id == 1:
            como_cajero = True
        else:
            como_cajero = False
    true = True
    false = False    

    return render(request, 'index.html',{"url":imagenes_url,
                                         "como_cajero": como_cajero,
                                         "true":true,
                                         "false": false,
                                         "nombre":nombre,
                                         "id": id})



def a_inicar(request):
    return redirect(iniciar_secion)