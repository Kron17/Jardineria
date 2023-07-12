from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#ES DONDE SE CREAN LAS TABLAS
class TipoProducto(models.Model):
    descripcion = models.CharField(max_length = 50)

    def __str__(self):
        return self.descripcion

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=250)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    vencimiento = models.DateField()
    imagen = models.ImageField(null=True, blank=True)
    vigente = models.BooleanField()
    usuarios = models.ManyToManyField(User, through='ItemsCarrito')

    def __str__(self):
        return self.nombre

class ItemsCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_agregada = models.IntegerField(default=0)

    class Meta:
        db_table = "db_items_carrito"


class HistorialCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)

    
class Suscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField(null=True)
    estado = models.BooleanField(default=False)

import random


class Pedido(models.Model):



    ESTADO_CHOICES = (
        ('validacion', 'Validación'),
        ('preparacion', 'Preparación'),
        ('reparto', 'Reparto'),
        ('entregado', 'Entregado'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    fecha_entrega = models.DateField(null=True)
    nombre_completo = models.CharField(max_length=100, blank=True)
    cantidad = models.IntegerField(default=0, null=True)
    region = models.CharField(max_length=100, blank=True)
    comuna = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    nro_casa_departamento = models.CharField(max_length=50, blank=True)
    celular = models.CharField(max_length=100, blank=True)
    correo = models.CharField(max_length=100, blank=True)
    comentario = models.TextField(blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='validacion')
    numero_pedido = models.CharField(max_length=50, default='')

    def save(self, *args, **kwargs):
        if not self.numero_pedido:  # Si no se ha asignado un número de pedido
            max_numero_pedido = Pedido.objects.filter(usuario=self.usuario).aggregate(models.Max('numero_pedido'))
            ultimo_numero_pedido = max_numero_pedido.get('numero_pedido__max')
            if ultimo_numero_pedido:
                self.numero_pedido = ultimo_numero_pedido
            else:
                self.numero_pedido = str(random.randint(1000, 9999))  # Genera un número aleatorio de pedido
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.numero_pedido} - {self.usuario.username}"






class BoletaCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    monto_neto = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)