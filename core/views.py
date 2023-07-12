import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from .serializers import *
from rest_framework import viewsets
import requests
from django.contrib.auth import authenticate, login
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import Group
from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
from django.templatetags.static import static
import os
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist


#funcion generica qeu valida el grupo del usuario
def grupo_requerido(nombre_grupo):
    def decorator(view_fuc):
        @user_passes_test(lambda user: user.groups.filter(name=nombre_grupo).exists())
        def wrapper(requests, *arg, **kwargs):
            return view_fuc(requests, *arg, **kwargs)
        return wrapper
    return decorator

#se usa like @grupo_requerido('nombre del grupo')
#cuando se crea el usuario para asignar a un grupo es con
#grupo = Group.objects.get(name='cliente')
#user.groups.add(grupo)

#NOS PERMITE MOSTRAR LA INFO
class ProductoViewset(viewsets.ModelViewSet):
    #para poder filtrar queryset = Producto.objects.filter(tipo=1)
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class TipoProductoViewset(viewsets.ModelViewSet):
    #para poder filtrar queryset = Producto.objects.filter(tipo=1)
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer

class TipoSubViewsets(viewsets.ModelViewSet):
    queryset = Suscripcion.objects.all()
    serializer_class = TipoSubSerializer

class HistorialViewsets(viewsets.ModelViewSet):
    queryset = HistorialCompra.objects.all()
    serializer_class = HistorialSerializer  


# Create your views here.

@grupo_requerido('cliente')
def historial(request):
    respuesta = requests.get('https://mindicador.cl/api').json()
    historial = HistorialCompra.objects.filter(usuario=request.user)
    paginator = Paginator(historial, 3)
    page = request.GET.get('page', 1)

    try:
        historial = paginator.page(page)
    except EmptyPage:
        historial = paginator.page(1)
    except PageNotAnInteger:
        historial = paginator.page(1)

    data = {
        'monedas': respuesta,
        'historial': historial,
        'paginator': paginator
    }
    
    return render(request, 'core/historial.html', data)

def index(request):
    productosAll = Producto.objects.all() #SELECT * FROM producto
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    respuesta = requests.get('https://mindicador.cl/api').json()
    
    try:
        paginator = Paginator(productosAll, 4)
        productosAll = paginator.page(page)
    except:
        raise Http404

    data = {
        'monedas': respuesta,
        'listado': productosAll,
        'paginator': paginator
    }

    if request.method == 'POST':
        carrito = ItemsCarrito()
        carrito.NombreProducto = request.POST.get('NombreProducto')
        carrito.PrecioProducto = request.POST.get('PrecioProducto')
        carrito.imagen = request.POST.get('imagenProducto')
        carrito.save()
        
    return render(request, 'core/index.html', data)

def base(request):
    respuesta = requests.get('https://mindicador.cl/api').json()
    
    data = {
        'monedas': respuesta,
         }
    
    return render(request, 'core/base.html', data)

def product(request):
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    productos = respuesta.json()
    #productosAll = Producto.objects.all() #SELECT * FROM producto
    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    respuesta1 = requests.get('https://mindicador.cl/api').json()
    
    try:
        paginator = Paginator(productos, 8)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'monedas': respuesta1,
        'listado': productos,
        'paginator': paginator
    }
    
    if request.method == 'POST':
        carrito = ItemsCarrito()
        carrito.NombreProducto = request.POST.get('NombreProducto')
        carrito.PrecioProducto = request.POST.get('PrecioProducto')
        carrito.imagen = request.POST.get('imagenProducto')
        carrito.save()

    return render(request, 'core/product.html', data)

@grupo_requerido('cliente')
def seguimiento(request):
    if request.user.is_superuser:  # Verifica si el usuario es un administrador
        pedidos = Pedido.objects.all()  # Obtiene todos los pedidos
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)  # Filtra los pedidos del usuario actual

    return render(request, 'core/seguimiento.html', {'pedidos': pedidos})

def seguimientoCompra(request):
    respuesta = requests.get('https://mindicador.cl/api').json()
    data = {
        'monedas': respuesta,
         }
    return render(request, 'core/seguimientoCompra.html',data)

def contacto(request):
    respuesta = requests.get('https://mindicador.cl/api').json()

    data = {
        'monedas': respuesta,
         }
    return render(request, 'core/contacto.html',data)

@login_required
def details(request, id):
    producto = Producto.objects.get(id=id)
    respuesta = requests.get('https://mindicador.cl/api').json()
    data = {'Productos': producto}

    if request.method == 'POST':
        carrito, created = ItemsCarrito.objects.get_or_create(usuario=request.user, producto=producto)
        cantidad_agregada = int(request.POST.get('cantidad_agregada', 1))
        carrito.cantidad_agregada += cantidad_agregada
        carrito.save()

        producto.stock -= cantidad_agregada
        producto.save()

        messages.success(request, "Producto almacenado correctamente")

    carrito_usuario = ItemsCarrito.objects.filter(usuario=request.user)
    data['ListaCarrito'] = carrito_usuario

    return render(request, 'core/details.html', data)

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            grupo = Group.objects.get(name="cliente")
            user.groups.add(grupo)
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            #redirigir al home
            return redirect(to="subs")
        data["form"] = formulario    
    return render(request, 'registration/registro.html',data)

@login_required
def compra(request):
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']
    carrito = ItemsCarrito.objects.filter(usuario=request.user)
    total_price_without_discount = sum(item.producto.precio * item.cantidad_agregada for item in carrito)

    for item in carrito:
        item.total_producto = item.producto.precio * item.cantidad_agregada
        item.save()  # Guardar los cambios realizados en los objetos ItemsCarrito
    
    total_price_with_discount = total_price_without_discount
    if request.user.is_authenticated:
        total_price_with_discount *= 0.95
        suscripcion = Suscripcion.objects.filter(usuario=request.user, estado=True).first()
        if suscripcion:
            total_price_with_discount -= total_price_with_discount * 0.05  # Aplicar descuento del 5%

    total_price_without_discount = int(total_price_without_discount)  # Convertir el precio sin descuento a entero
    total_price_with_discount = int(total_price_with_discount)  # Convertir el precio con descuento a entero
    discount_amount = total_price_without_discount - total_price_with_discount
    valor_total = total_price_with_discount / valor_usd

    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            # Guardar historial de compras para cada item en el carrito
            for item in carrito:
                historial = HistorialCompra.objects.create(
                    codigo_compra=item.codigo_compra,
                    usuario=request.user,
                    producto=item.producto,
                    cantidad=item.cantidad_agregada,
                    precio=item.producto.precio
                )
                # Restar la cantidad comprada del stock del producto
                item.producto.stock -= item.cantidad_agregada
                item.producto.save()

            # Vaciar el carrito del usuario
            carrito.delete()

            messages.success(request, "Compra realizada correctamente")
            return redirect('index')
    else:
        form = CompraForm(initial={'valor_total': round(valor_total, 2)})

    # Obtener el historial de compras del usuario
    historial_compras = HistorialCompra.objects.filter(usuario=request.user)

    datos = {
        'monedas': respuesta,
        'ListaCarrito': carrito,
        'total_price_without_discount': total_price_without_discount,
        'valor_total': round(valor_total, 2),
        'discount_amount': discount_amount,
        'total_price_with_discount': total_price_with_discount,
        'historial': historial_compras,
        'form': form,
    }

    return render(request, 'core/compra.html', datos)


#def aprobado(request):
 #   respuesta = requests.get('https://mindicador.cl/api').json()
  #  carrito = ItemsCarrito.objects.filter(usuario=request.user)  # Filtrar por el usuario actual

    # Guardar historial de compras para cada item en el carrito
   # for item in carrito:
    #    historial = HistorialCompra.objects.create(
     #       usuario=request.user,
      #      producto=item.producto,
       #     cantidad=item.cantidad_agregada,
        #    precio=item.producto.precio
      #  )

        # Restar la cantidad comprada del stock del producto
        #item.producto.stock -= item.cantidad_agregada
        #item.producto.save()

    #historial_compras = HistorialCompra.objects.filter(usuario=request.user)  # Obtener el historial de compras del usuario
    #carrito.delete()  # Borrar los elementos del carrito

    #data = {
     #   'monedas': respuesta,
      #  'historial_compras': historial_compras  # Pasar el historial de compras a la plantilla
    #}

    #return render(request, 'core/aprobado.html', data)

@grupo_requerido('cliente')
def subs(request):
    suscripcion = Suscripcion.objects.filter(usuario=request.user).first()
    is_suscribed = True if suscripcion else False
    
    if request.method == 'POST':
        if is_suscribed:
            # Acción de desuscripción
            suscripcion.delete()
            return render(request, 'core/desuscripcion_exitosa.html')
        else:
            form = SuscripcionForm(request.POST)
            if form.is_valid():
                suscripcion = form.save(commit=False)
                suscripcion.usuario = request.user
                suscripcion.fecha_inicio = date.today()
                suscripcion.fecha_vencimiento = suscripcion.fecha_inicio + timedelta(days=30)
                suscripcion.estado = True  # Establecer el estado de suscripción como True
                suscripcion.save()

                return render(request, 'core/pagoSubs.html')
    else:
        form = SuscripcionForm(initial={'fecha_inicio': date.today()})

    return render(request, 'core/subs.html', {'form': form, 'is_suscribed': is_suscribed})



def cambiar_estado_pedido(request, pedido_id):
    # Obtener el pedido específico
    pedido = Pedido.objects.get(pk=pedido_id)

    if request.method == 'POST':
        # Obtener el nuevo estado seleccionado
        nuevo_estado = request.POST.get('nuevo_estado')

        # Actualizar el estado del pedido
        pedido.estado = nuevo_estado
        pedido.save()
        return redirect('seguimiento')
    return render(request, 'core/seguimiento.html', {'pedido': pedido})

@grupo_requerido('cliente')
def pagoSubs(request):
    return render(request, 'core/pagoSubs.html')

@grupo_requerido('cliente')
def subsAprobada(request):
    return render(request, 'core/subsAprobada.html')

@grupo_requerido('cliente')
def subsModificada(request):
    suscripcion = get_object_or_404(Suscripcion, usuario=request.user)
    suscripcion.delete()

    return render(request, 'core/subsModificada.html')

######################## CRUD ########################
@grupo_requerido('Vendedor')
def add(request):
    respuesta = requests.get('https://mindicador.cl/api').json()
    data ={
        'monedas': respuesta,
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) #OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() #INSERT INTO...
            #data['msj'] = "Producto guardado correctamente"
            messages.success(request, "Producto almacenado correctamente")

    return render(request, 'core/add-product.html', data)

@grupo_requerido('Vendedor')
def update(request, id):
    respuesta = requests.get('https://mindicador.cl/api').json()
    producto = Producto.objects.get(id=id) #OBTIENE UN PRODUCTO POR EL ID
    data ={
        'form' : ProductoForm(instance=producto) #CARGAMOS EL PRODUCTO EN EL FORMULARIO
    }

    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, instance=producto, files=request.FILES) #OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save() #INSERT INTO...
            #data['msj'] = "Producto actualizado correctamente"
            messages.success(request, "Producto almacenado correctamente")
            data['form'] = formulario #CAGRA LA NUEVA INFO EN EL FORMULARIO
            
    return render(request, 'core/update-product.html', data)

@grupo_requerido('Vendedor')
def delete(request, id):
    respuesta = requests.get('https://mindicador.cl/api').json()
    producto = Producto.objects.get(id=id) #OBTIENE UN PRODUCTO POR EL ID
    producto.delete()

    data ={
        'monedas': respuesta,
        'form' : ProductoForm()
    }
    
    return redirect(to = 'index',)

def indexapi(request):
    #obtiene productos api
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api')
    #apis mas complejas con arreglos
    respuesta3 = requests.get('https://rickandmortyapi.com/api/character')
    #Transformar JSON
    productos = respuesta.json()
    monedas = respuesta2.json()
    #utilizamos 2 variables para las apis mas coplejas
    envolvente = respuesta3.json()
    personajes = envolvente['results']

    data = {
        'listado': productos,
        'monedas': monedas,
        'personajes': personajes,
        
    }

        
    return render(request, 'core/indexapi.html', data)

def EliminaProd(request, id):
    carrito = ItemsCarrito.objects.get(id=id)
    producto = carrito.producto

    #devolver stock
    producto.stock += carrito.cantidad_agregada
    producto.save()

    carrito.delete()

    return redirect ("compra")


def vaciar_carrito(request):
    productos_carrito = ItemsCarrito.objects.filter(usuario=request.user)
    productos_carrito.delete()

    return redirect('/')


import random
def checkout(request):
    if request.method == 'POST':
        carrito = ItemsCarrito.objects.filter(usuario=request.user)
        respuesta2 = requests.get('https://mindicador.cl/api/dolar').json()
        valor_usd = respuesta2['serie'][0]['valor']
        total_precio = Decimal(str(sum(item.producto.precio * item.cantidad_agregada for item in carrito)))
        total_en_dolar = round(total_precio / Decimal(str(valor_usd)), 2)

        # Definir valores predeterminados para descuento y total_dolares
        descuento = Decimal('0.0')
        total_con_descuento = total_precio
        total_dolares = Decimal('0.0')
        iva = round(total_precio * Decimal('0.19'))    
        total_iva = round(total_precio + iva)
        total_envio = round(total_iva + 5000)  

        # Verificar si el usuario está suscrito
        if hasattr(request.user, 'suscripcion'):
            descuento_porcentaje = Decimal('0.1')
            descuento = round(total_precio * descuento_porcentaje)
            total_con_descuento = round(total_iva - descuento)
            total_dolares = round(total_con_descuento / Decimal(str(valor_usd)), 2)

        total = total_dolares or total_en_dolar

        fecha_entrega = datetime.now().date() + timedelta(days=5)
        fecha_compra = datetime.today()

        # Generar un solo número aleatorio de pedido para el usuario actual
        numero_pedido = str(random.randint(1000, 9999))

        # Crear una lista para almacenar los objetos de HistorialCompra y Pedidos
        historiales = []
        pedidos = []

        for item in carrito:
            item.total_producto = item.producto.precio * item.cantidad_agregada
            item.save()  

            historial = HistorialCompra(
                usuario=request.user,
                producto=item.producto,
                cantidad=item.cantidad_agregada,
                precio=item.producto.precio
            )
            historiales.append(historial)

            pedido = Pedido(
                usuario=request.user,
                producto=item.producto,
                cantidad=item.cantidad_agregada,
                nombre_completo=request.POST.get('nombre_completo'),
                region=request.POST.get('region'),
                comuna=request.POST.get('comuna'),
                direccion=request.POST.get('direccion'),
                nro_casa_departamento=request.POST.get('nro_casa_departamento'),
                celular=request.POST.get('celular'),
                correo=request.POST.get('correo'),
                comentario=request.POST.get('comentario'),
                fecha_entrega=fecha_entrega,
                numero_pedido=numero_pedido
            )
            pedidos.append(pedido)

            BoletaCompra.objects.create(
                usuario=request.user,
                producto=item.producto,
                cantidad=item.cantidad_agregada,
                fecha_compra=timezone.now(),
                precio_unitario=item.producto.precio,              
                precio_total=total_precio,
                monto_neto=total_con_descuento,
                iva=iva,
                descuento=descuento
            )

        # Crear los registros de historial de compra en una sola operación
        HistorialCompra.objects.bulk_create(historiales)

        # Crear los registros de pedidos en una sola operación
        Pedido.objects.bulk_create(pedidos)

        datos = {
            'listarproductos': carrito,
            'total_precio': total_precio,
            'total_envio': total_envio,
            'descuento': descuento,
            'total_con_descuento': total_con_descuento,
            'total_dolares': total_dolares,
            'total_en_dolar': total_en_dolar,
            'total': total,
            'iva': iva,
            'total_iva': total_iva,
            'suscrito': hasattr(request.user, 'suscripcion')
        }
        return render(request, 'core/checkout.html', datos)

    else:
        # Código para la solicitud GET (cuando se carga la página)
        carrito = ItemsCarrito.objects.filter(usuario=request.user)
        total_precio = Decimal('0')

        for item in carrito:
            item.total_producto = item.producto.precio * item.cantidad_agregada
            total_precio += item.total_producto

        iva = round(total_precio * Decimal('0.19'))    
        total_iva = total_precio + iva
        total_envio = total_iva + 5000      

        respuesta2 = requests.get('https://mindicador.cl/api/dolar').json()
        valor_usd = respuesta2['serie'][0]['valor']
        total_en_dolar = round(total_envio / Decimal(str(valor_usd)), 2)

        descuento = Decimal('0.0')
        total_con_descuento = total_envio
        total_dolares = Decimal('0.0')

        if hasattr(request.user, 'suscripcion'):
            descuento_porcentaje = Decimal('0.1')
            descuento = round(total_precio * descuento_porcentaje)
            total_con_descuento = round(total_iva - descuento)
            total_dolares = round(total_con_descuento / Decimal(str(valor_usd)), 2)

        total = total_dolares or total_en_dolar

        datos = {
            'listarproductos': carrito,
            'total_precio': total_precio,
            'total_envio': total_envio,
            'descuento': descuento,
            'total_con_descuento': total_con_descuento,
            'total_dolares': total_dolares,
            'total_en_dolar': total_en_dolar,
            'total': total,
            'iva': iva,
            'total_iva': total_iva,
            'suscrito': hasattr(request.user, 'suscripcion')
        }
        return render(request, 'core/checkout.html', datos)




######################################################

