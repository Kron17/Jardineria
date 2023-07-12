from django.urls import path, include
from .views import *
from rest_framework import routers

#rutas del API tienen rutas propias

router = routers.DefaultRouter()
router.register('productos', ProductoViewset)
router.register('tipoproductos', TipoProductoViewset)
router.register('tiposubs', TipoSubViewsets)
router.register('historialviewsets', HistorialViewsets)

urlpatterns = [
    #api
    path('api/', include(router.urls)),
    #RUTAS
    path('', index, name="index"),
    path('base/', base, name="base"),
    path('product/', product, name="productos"),
    path('contacto/', contacto, name="contacto"),
    path('registro/', registro, name="registro"),
    path('seguimiento/', seguimiento, name="seguimiento"),
    path('compra/', compra, name="compra"),
    #path('aprobado/', aprobado, name="aprobado"),
    path('seguimientoCompra/', seguimientoCompra, name="seguimientoCompra"),
    path('indexapi', indexapi, name="indexapi"),
    path('subs/', subs, name="subs"),
    path('subsModificada/', subsModificada, name="subsModificada"),
    path('subsAprobada/', subsAprobada, name="subsAprobada"),
    path('details/<id>/', details, name='details'),
    path('EliminaProd/<id>/', EliminaProd, name="EliminaProd"),
    path('historial/', historial, name="historial"),
    path('pagoSubs/', pagoSubs, name="pagoSubs"),
    path('checkout/', checkout, name="checkout"),
    path('cambiar_estado/<int:pedido_id>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('vaciar_carrito/', vaciar_carrito, name='vaciar_carrito'),

    #CRUD
    path('add/', add, name='add'),
    path('update/<id>/', update, name="update"),
    path('delete/<id>/', delete, name="delete"),
    
]