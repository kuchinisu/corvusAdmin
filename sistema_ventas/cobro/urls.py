from django.urls import path
from django.conf.urls.static import static

from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:categoria>/', views.index, name='index_con_categoria'),
    

    path('producto/<int:codigo>', views.producto, name='producto'),
    path("lista_de_productos", views.lista_de_productos, name="productos"),
    path('comprado/<int:codigo>', views.comprado, name='comprado'),
    path('comprar_carrito', views.cobrar_desde_carrito, name='comprarc'),
    path('panel', views.panel_financiero, name='panel'),
    path('corte_de_caja', views.corte, name='corte'),
    path('corte_realizado', views.realizar_corte, name='corte_realizado')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)