from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("cobro/", include("cobro.urls")),
    path('usuario/', include("usuario.urls")),
    path('', views.index, name="indexp"),
    path('ensesion/<str:id>/', views.index, name="indexs"),
    
    path('a_iniciar', views.a_inicar, name='ainiciar'),
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)