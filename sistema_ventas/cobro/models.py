from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre#id

class Marca(models.Model):
    nombre = models.CharField(default="blanca", max_length=50)
    def __str__(self):
        return self.nombre
    

class Producto(models.Model):
    nombre = models.CharField(default='',max_length=100)
    descripcion = models.CharField(default='', max_length=150)
    marcaP = models.ForeignKey(Marca, on_delete=models.CASCADE, default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='media/img/', null=True, blank=True)

    codigo = models.IntegerField(
        default = 0,
        unique=True,
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(0)
        ]
    )

    costo = models.DecimalField(default = 0 , max_digits=10, decimal_places=2)
    
    cantidad = models.IntegerField(default=0,validators=[
            MaxValueValidator(99999),
            MinValueValidator(0)])
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Year(models.Model):
    anio = models.IntegerField(default=24, validators=[
        MaxValueValidator(99999),
        MinValueValidator(24)
    ])

    def __str__(self):
        return str(self.anio) 

class Mes(models.Model):
    mes = models.IntegerField(default=1, validators=[
        MaxValueValidator(12),
        MinValueValidator(1)
    ])
    del_anio = models.ForeignKey(Year, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.mes)

class Dia(models.Model):
    dia = models.IntegerField(default=1, validators=[
        MaxValueValidator(31),
        MinValueValidator(1)
    ])
    
    del_mes = models.ForeignKey(Mes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dia)

class Hora(models.Model):
    hora = models.IntegerField(default=0, validators=[
        MaxValueValidator(1440),
        MinValueValidator(0)
    ])
    producto_vendido = models.CharField(default='', max_length=50)
    del_dia = models.ForeignKey(Dia, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.hora)
    



class DiaDeVentas(models.Model):
    year = models.IntegerField(default=24, validators=[
        MaxValueValidator(99999),
        MinValueValidator(24)
    ])
    mes = models.IntegerField(default=24, validators=[
        MaxValueValidator(99999),
        MinValueValidator(24)
    ])

    dia = models.IntegerField(default=24, validators=[
        MaxValueValidator(99999),
        MinValueValidator(24)
    ])

    entradas = models.CharField(default="0", max_length=500)
    salidas = models.CharField(default="0", max_length=500)

    cantidad_dinero_neto = models.DecimalField(max_digits=10, decimal_places=2)

    promedio_ventas =  models.DecimalField(max_digits=10, decimal_places=2)


# todos los objetos financieros del negocio
    #dinero positivo

class Caja(models.Model):
    nombre = models.CharField(default=("caja"), max_length=50)
    dinero = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    dinero_a_surtir = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    dinero_a_servicios = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    dinero_de_reserva = models.DecimalField(default = 100.00, max_digits=10, decimal_places=2)
    
    def __str__(self):
        return str(self.nombre)

class EspacioEnCaja(models.Model):
    nombre = models.CharField(default="espacio en caja", max_length=50)

    def __str__(self):
            return str(self.nombre)
    
class Reserva(models.Model):
    nombre = models.CharField(default="reserva", max_length = 50)
    dinero = models.DecimalField(max_digits=10, decimal_places=2)
    #categoria = models.ForeignKey(EspacioEnCaja, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.nombre)
    
class CajaFuerte(models.Model):
    nombre=models.CharField(default="caja_fuerte", max_length = 50)
    dinero = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return str(self.nombre)
    
class Bolsillo(models.Model):
    nombre=models.CharField(default="bolsillo", max_length = 50)
    dinero = models.DecimalField(max_digits=10, decimal_places=2)
    destinado = models.DecimalField(default=10, max_digits=10, decimal_places=2)
    def __str__(self):
        return str(self.nombre)


class DiasDeGanancias(models.Model):
    
    nombre = models.CharField(default = "dia_ganancias", max_length=50)

    dia = models.IntegerField(default=1, validators=[
        MaxValueValidator(31),
        MinValueValidator(1)])
    mes = models.IntegerField(default=1, validators=[
        MaxValueValidator(12),
        MinValueValidator(1)])
    anio = models.IntegerField(default=2024, validators=[
        MaxValueValidator(9999),
        MinValueValidator(2024)])
    
    ganancias_netas = models.DecimalField(default=10, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre
    
class DiasDeClientes(models.Model):
    nombre=models.CharField(default = "clientes por dia", max_length=50)
    dia = models.IntegerField(default=1, validators=[
        MaxValueValidator(31),
        MinValueValidator(1)])
    mes = models.IntegerField(default=1, validators=[
        MaxValueValidator(12),
        MinValueValidator(1)])
    anio = models.IntegerField(default=2024, validators=[
        MaxValueValidator(9999),
        MinValueValidator(2024)])

    cantidad_de_clientes = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    def __str__(self):
        return self.nombre
    
    #dinero negativo
class InversionEnProductos(models.Model):
    nombre = models.CharField(default = "inversion", max_length=50)
    dinero = models.DecimalField(max_digits=10, decimal_places=2)
    destinado = models.DecimalField(default=10, max_digits=10, decimal_places=2)
    #categoria=models.ForeignKey(EspacioEnCaja, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.nombre)

class GuardadoASurtir(models.Model):
    nombre = models.CharField(default="surtir", max_length = 20)
    cantidad = models.DecimalField(default = 0,max_digits=10, decimal_places=2)
    #categoria=models.ForeignKey(EspacioEnCaja, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)
    
class GuardadoAServicios(models.Model):
    nombre = models.CharField(default="servicio", max_length=20)
    cantidad = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    destinado = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    #categoria = models.ForeignKey(EspacioEnCaja, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)


class GastosA(models.Model):
    nombre = models.CharField(default=" ", max_length=20)

    def __str__(self):
        return str(self.nombre)


class ColoresGraf(models.Model):
    nomre = models.CharField(default=" ", max_length = 10)
    
    def __str__(self):
        return str(self.nomre)


class Servicio(models.Model):
    nombre = models.CharField(default="", max_length=50)

    monto = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    meta = models.DecimalField(default = 0, max_digits=10, decimal_places=2)

    fecha = models.IntegerField(default=30, validators=[
        MaxValueValidator(99999),
        MinValueValidator(0)
    ])
 
    a_partir_de = models.DateTimeField()

    dias_de_atraso = models.IntegerField(default=30, validators=[
        MaxValueValidator(99999),
        MinValueValidator(0)
    ])

    destinado = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])

    categoria = models.ForeignKey(GastosA, on_delete=models.CASCADE)
    color = models.ForeignKey(ColoresGraf, on_delete=models.CASCADE, default=0)


    def __str__(self):
        return str(self.nombre)
    

class InversionLocal(models.Model):
    nombre = models.CharField(default="local", max_length=50)
    inmueble = models.DecimalField(max_digits=10, decimal_places=2)
    muebles = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return str(self.nombre)
