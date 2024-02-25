from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Usuarios(models.Model):
    nombre = models.TextField(default = " " , max_length = 30)

    id_us = models.IntegerField(default=1, validators=[
        MaxValueValidator(99999),
        MinValueValidator(0)
    ], unique=True)

    key = models.TextField(default = " ", unique = True, max_length = 30)

    def __str__(self):
        return str(self.nombre)


class HistorialDeCompras(models.Model):
    id_prducto =  models.IntegerField(default=1, validators=[
        MaxValueValidator(99999),
        MinValueValidator(0)
    ])

    id_historial = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_prducto)