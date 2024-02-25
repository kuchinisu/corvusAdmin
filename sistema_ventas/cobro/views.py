from django.shortcuts import render,redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import pandas as pd
import numpy as np
from datetime import date
import matplotlib
#matplotlib.use("TkAgg")
matplotlib.use('agg')
import matplotlib.pyplot as plt


from django.http import HttpResponse, JsonResponse
from decimal import Decimal
from .models import (Producto, 
                     Year, Mes, Dia, Hora, Caja, CajaFuerte, 
                     Reserva, Bolsillo, InversionEnProductos, 
                     InversionLocal, InversionEnProductos, Servicio, DiasDeGanancias,
                     DiasDeClientes, Categoria)


def index(request, categoria=""):
    
    if categoria:
        categoria = Categoria.objects.filter(nombre=categoria).first()
        productos = Producto.objects.filter(categoria=categoria)
    else:
        productos = Producto.objects.all()

    icon_url = "\static\icon\caja-registradora.png"
    if 'q' in request.GET:
        query = request.GET['q']
        productos = Producto.objects.filter(nombre__icontains=query)
        if not productos.exists():
            productos = Producto.objects.filter(codigo__icontains=query)
    caja = Caja.objects.filter(nombre = "caja")
    return render(request, 'cobro.html', {'productos': productos, "url":icon_url, "caja":caja})


def lista_de_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})



def comprado(request, codigo):
    productos = Producto.objects.all()
    pr = productos.filter(codigo__icontains=codigo)

    producto = get_object_or_404(Producto, codigo__icontains=codigo)

    if producto.cantidad > 0:
        producto.cantidad -= 1
        producto.save()

        return render(request, 'pages/comprado.html', {'producto': pr})
    else:
        return render(request, 'err/compra_fallida.html', {'mensaje': 'No hay suficiente cantidad disponible para comprar.'})

    


def producto(request, codigo):
    productos = Producto.objects.all()
    pr = productos.filter(codigo__icontains=codigo)
    
    return render(request, 'pages/producto.html', {'producto': pr})

def add_al_carrito(request, codigo):
    return HttpResponse("Producto agregado al carrito")



@api_view(["GET", "POST"])
def cobrar_desde_carrito(request):
    if request.method == 'POST':
        datos = request.data  
        print(datos)

        productos = Producto.objects.all()
        caja = Caja.objects.all()
        fecha = datetime.now()

        for key, value in datos.items():
            try:
                pr = productos.get(codigo__icontains=value)
                pr.cantidad -= 1
                pr.save()

                
                
                caja_ = caja.get(nombre__icontains="caja")
                ganancia_bruta = pr.precio - pr.costo
                servicios = Servicio.objects.all()

                
                for servicio in servicios:
                    pago_al_servicio = (Decimal(servicio.destinado) / Decimal(100)) * Decimal(ganancia_bruta)

                    servicio.monto += pago_al_servicio
                    ganancia_bruta -= pago_al_servicio
                    caja_.dinero_a_servicios += pago_al_servicio
                    
                    servicio.save()
                    print("destinado a serivicos")
                    print(servicio.nombre)
                    print(servicio.monto)
                    print("ya")
                
                
                ganancia_neta = ganancia_bruta

                inversion = InversionEnProductos.objects.first()
                a_reinversion_a_surtir = (inversion.destinado / 100) * ganancia_neta
                ganancia_neta - a_reinversion_a_surtir

                caja_.dinero += ganancia_neta
                caja_.dinero_a_surtir += pr.costo + a_reinversion_a_surtir
                caja_.save()

                hoy = datetime.now()

                clientes_del_dia = DiasDeClientes.objects.filter(dia=hoy.day, mes=hoy.month, anio=hoy.year)

                if not clientes_del_dia.exists():
                    nuevo_cliente = DiasDeClientes(dia=hoy.day, mes=hoy.month, anio=hoy.year)
                    nuevo_cliente.cantidad_de_clientes += 1
                    clientes_del_dia = nuevo_cliente
                    clientes_del_dia.save()
                else:
                    clientes_del_dia = clientes_del_dia.first()
                    clientes_del_dia.cantidad_de_clientes += 1
                    clientes_del_dia.save()


                try:
                    anio = fecha.year
                    mes = fecha.month
                    dia = fecha.day
                    hora = (fecha.hour * 60) + fecha.minute + (fecha.second / 60)
                    #pandas_excel(anio, mes, dia, pr,hora)
                except KeyError as e:
                    return Response({"error": str(e)})
                
            except Producto.DoesNotExist:
                
                return Response({"mensaje": f"El producto con código {value} no existe"}, status=400)
        

        return Response(datos)
    else:
        return Response({"mensaje": "Método no permitido"}, status=405)


def pandas_excel(year, mes, dia, producto, hora):
    anio_existente = Year.objects.filter(anio=year).exists()
    if not anio_existente:
        nuevo_anio = Year(anio=year)
        nuevo_anio.save()

    anio_instancia = Year.objects.get(anio=year)

    mes_del_anio = Mes.objects.filter(del_anio=anio_instancia, mes=mes).first()
    if not mes_del_anio:
        nuevo_mes = Mes(mes=mes, del_anio=anio_instancia)
        nuevo_mes.save()
        mes_del_anio = nuevo_mes

    dia_del_mes = Dia.objects.filter(del_mes=mes_del_anio, dia=dia).first()
    if not dia_del_mes:
        nuevo_dia = Dia(dia=dia, del_mes=mes_del_anio)
        nuevo_dia.save()
        dia_del_mes = nuevo_dia

    nueva_hora = Hora(del_dia=dia_del_mes, hora=hora, producto_vendido = producto)
    nueva_hora.save()    

    years = Year.objects.all()

    data_dict = {}

    for year in years:
        data_dict[year.anio] = {}

        for month in Mes.objects.filter(del_anio=year):
            data_dict[year.anio][month.mes] = {}

            for day in Dia.objects.filter(del_mes=month):
                data_dict[year.anio][month.mes][day.dia] = []

                for hour in Hora.objects.filter(del_dia=day):
                    data_dict[year.anio][month.mes][day.dia].append(hour.hora)

    df = pd.DataFrame(data_dict)

    df = df.transpose()

    df.to_excel('sistema_ventas/static/xlsx/registro_ventas.xlsx', index=True)


###area de las finanzas

def plot_grafico(categorias, alturas, reunido, meta, porcentaje_completado, servicio_nombre, grafica, color, dias_faltantes, dias_de_atraso):
    plt.style.use('fivethirtyeight')

    plt.figure(figsize=(10, 13))

    porcentaje_completado = round(porcentaje_completado, 2)
    plt.bar(categorias, alturas, color=color)

    plt.xlabel(f'Reunido: {reunido}MXN de: {meta}MXN, {porcentaje_completado}% Completado')
    plt.ylabel('Meta')
    plt.title(str(servicio_nombre))

    for i, altura in enumerate(alturas):
        plt.text(i, altura + Decimal(0.1), f'${altura}', ha='center', va='bottom')

    plt.text(0.1, max(alturas) + 1, f'{porcentaje_completado}%', ha='center', va='bottom', color='red', fontweight='bold')
    
    plt.ylim(0, meta + 5)
    plt.grid(False)

    # Agregar texto con información adicional
    texto_informacion = f'Días Faltantes: {dias_faltantes}\nDías de Atraso: {dias_de_atraso}'
    plt.text(0.1, max(alturas) + 2, texto_informacion, ha='center', va='bottom', color='black', fontsize=10)

    plt.savefig(f'sistema_ventas/static/img/graf/{grafica}')

    plt.close()



def calcular_dias_faltantes(desde_cuando, cada_cuantos):
    fecha_actual = datetime.now()
    if fecha_actual.month == desde_cuando.month:
        dias_pasados = desde_cuando.day + fecha_actual.day
        dias_faltantes = cada_cuantos - dias_pasados  
        
    else:
        restante_de_mes = 30 - desde_cuando.day
        dias_avanzados = fecha_actual.day
        dias_pasados = restante_de_mes +  dias_avanzados

        for i in range((desde_cuando + 1), fecha_actual.month):
            dias_pasados =+ 30

        dias_faltantes = dias_pasados  - cada_cuantos 

    if dias_faltantes < 0:
        dias_de_atraso = dias_faltantes * -1
    else:
        dias_de_atraso = 0
    
    return dias_faltantes, dias_de_atraso

def panel_financiero(request):
    bolsillo = Bolsillo.objects.filter(nombre = "bolsillo")
    caja_fuerte = CajaFuerte.objects.filter(nombre = "caja_fuerte")
    caja = Caja.objects.filter(nombre="caja")
    inversion_productos = InversionEnProductos.objects.filter(nombre = "inversion")
    inversion_local = InversionLocal.objects.filter(nombre = "local")

    dias_de_ganancias = DiasDeGanancias.objects.all()

    icon_url = '/static/icon'

    cant_dias = len(dias_de_ganancias)
    if cant_dias > 1:
        ultimo_dia = dias_de_ganancias[cant_dias - 1 ]
        penultimo_dia = dias_de_ganancias[cant_dias - 2]

        diferencia_cant =ultimo_dia.ganancias_netas -  penultimo_dia.ganancias_netas 
        print(diferencia_cant)
        if diferencia_cant < 0:
            sube_o_baja = False
        elif diferencia_cant > 0:
            sube_o_baja = True
        else:
            sube_o_baja = 1
    else:
        diferencia_cant = 0
        sube_o_baja = False

    print(sube_o_baja)
    true = True
    false = False
    uno = 1

    url_img = '/static/img/graf'#black
    graficas = []
    
    servicios = Servicio.objects.all()
    num = 0
    for servicio in servicios:
        
        meta = servicio.meta
        reunido = servicio.monto

        if reunido >= meta:
            meta = reunido-1
            porcentaje_completado = "100"
        else:
            porcentaje_completado = (reunido / meta) * 100

        categorias = ['reunido']
        alturas = [reunido]
        servicio_nombre = servicio.nombre

        
        grafica = f"grafica_{num}.png"
        graficas.append(grafica)
        color = str(servicio.color.nomre)
        
        a_partir_de = servicio.a_partir_de
        cada_cuantos = servicio.fecha
        #print(a_partir_de.date().day)
        dias_faltantes, dias_de_atraso = calcular_dias_faltantes(a_partir_de, cada_cuantos)
        plot_grafico(categorias, alturas, reunido, meta, porcentaje_completado, servicio_nombre, 
                     grafica, color, dias_faltantes, dias_de_atraso)


        num+=1

    clientes_per_dia = DiasDeClientes.objects.all()
    return render(request, 'pages/panel.html' , {"bolsillo": bolsillo, 
                                                 "caja_fuerte": caja_fuerte, 
                                                 "caja": caja,
                                                 "inversion_productos": inversion_productos,
                                                 "inversion_local": inversion_local,
                                                 'dias_de_ganancia': dias_de_ganancias,
                                                 'icon': icon_url,
                                                 'antier_hoy': diferencia_cant,
                                                 'sube_o_baja': sube_o_baja,
                                                 'true':true,
                                                 'false':false,
                                                 'uno':uno,
                                                 'clientes_per_dia': clientes_per_dia,
                                                 'servicios':servicios,
                                                 'url_img':url_img,
                                                 'graficas': graficas})



def corte(request):
    return render(request, 'pages/corte.html')

def realizar_corte(request):
    caja = Caja.objects.filter(nombre="caja").first()
    caja_fuerte = CajaFuerte.objects.filter(nombre="caja_fuerte").first()

    dinero = caja.dinero
    caja_fuerte.dinero += dinero
    caja.dinero = 0
    dinero_de_caja_fuerte = caja_fuerte.dinero
    bolsillo = Bolsillo.objects.first()
    le_toca_a_bolsillo = (bolsillo.destinado / 100) * dinero_de_caja_fuerte
    bolsillo.dinero += le_toca_a_bolsillo
    caja_fuerte.dinero -= le_toca_a_bolsillo

    hoy = datetime.now()
    ganancias_del_dia = DiasDeGanancias.objects.filter(dia=hoy.day, mes=hoy.month, anio=hoy.year)

    if not ganancias_del_dia.exists():
        nueva_ganancia = DiasDeGanancias(dia=hoy.day, mes=hoy.month, anio=hoy.year, ganancias_netas = le_toca_a_bolsillo)
        nueva_ganancia.save()
    else:
        ganancias_del_dia = ganancias_del_dia.first()
        ganancias_del_dia.ganancias_netas = le_toca_a_bolsillo
        ganancias_del_dia.save()

    caja.save()
    bolsillo.save()
    caja_fuerte.save()
    return render(request, 'pages/corte_realizado.html')