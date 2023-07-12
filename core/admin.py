from django.contrib import admin
from .models import *

# Register your models here.

# DEJA EN MODO TABLA LA VISUALIZACION EN EL ADMIN
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo', 'vigente', 'vencimiento']
    search_fields = ['nombre']
    list_per_page = 10
    list_filter = ['tipo', 'precio']
    list_editable = ['precio','stock','descripcion','tipo','vigente', 'vencimiento']

#class CarritoAdmin(admin.ModelAdmin):
    #list_display = ['NombreProducto','PrecioProducto']
    #search_fields = ['NombreProducto']
    #list_per_page = 10
    #list_filter = ['PrecioProducto']
'''
class HistorialComraAdmin(admin.ModelAdmin):
    list_display = ['codigo_compra','usuario','producto','cantidad','precio', 'fecha_compra']
    search_fields = ['nombre']
    list_per_page = 10
    list_filter = ['codigo_compra', 'usaurio']
'''
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['usuario','fecha_inicio','fecha_vencimiento','estado']
    search_fields = ['nombre']
    list_per_page = 10
    list_filter = ['usuario', 'fecha_inicio']


admin.site.register(TipoProducto)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(HistorialCompra)
#admin.site.register(ItemsCarrito, CarritoAdmin)
admin.site.register(Suscripcion, SuscripcionAdmin)
admin.site.register(Pedido)