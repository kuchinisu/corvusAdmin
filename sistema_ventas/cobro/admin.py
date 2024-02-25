from django.contrib import admin

from .models import (
    Categoria, Producto, Year, Mes, Dia, Hora, Caja, Reserva, CajaFuerte, Bolsillo, 
    InversionEnProductos, InversionLocal, Servicio, GastosA, GuardadoAServicios, GuardadoASurtir, 
    DiasDeGanancias,DiasDeClientes,ColoresGraf, Marca
)
admin.site.register(Categoria)
admin.site.register(Producto) 
admin.site.register(Year)
admin.site.register(Mes)
admin.site.register(Dia)
admin.site.register(Hora)
admin.site.register(Caja)
admin.site.register(Reserva)
admin.site.register(CajaFuerte)
admin.site.register(Bolsillo)
admin.site.register(InversionEnProductos)
admin.site.register(InversionLocal)
admin.site.register(Servicio)
admin.site.register(GastosA)
admin.site.register(GuardadoAServicios)
admin.site.register(GuardadoASurtir)
admin.site.register(DiasDeGanancias)
admin.site.register(DiasDeClientes)
admin.site.register(ColoresGraf)
admin.site.register(Marca)
