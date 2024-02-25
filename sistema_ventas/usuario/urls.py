from django.urls import path
from django.conf.urls.static import static

from django.conf import settings

from . import views

urlpatterns = [
    path("iniciar", views.iniciar_secion, name="iniciar"),
    path("registrarse", views.registrarse, name="registrarse"),
    path("entrar", views.iniciar_secion_autentic, name="entrar")
]