# VAMOS A CREAR UN FORMULARIO QUE SE REUTILIZA EN EL AGREGAR Y ACTUALIZAR
from datetime import date
from django import forms
from django.forms import ModelForm
from .models import *
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductoForm(ModelForm):

    nombre = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10,max_length=250,widget=forms.Textarea(attrs={"rows":4}))

    class Meta:
        model = Producto
        #fields = ['nombre','precio','stock','descripcion','tipo']
        fields = '__all__'

        widgets = {
            'vencimiento' : forms.SelectDateWidget(years=range(1940,2024))
        }

class CarritoForm(forms.ModelForm):
    class Meta:
        model = ItemsCarrito
        fields = ['producto', 'cantidad_agregada']

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
class ItemsCarritoForm(forms.ModelForm):
    class Meta:
        model = ItemsCarrito
        fields = ['usuario', 'producto', 'cantidad_agregada']
        widgets = {
            'usuario': forms.HiddenInput(),
        }

class CompraForm(forms.Form):
    valor_total = forms.DecimalField(label='Valor Total')

    def clean_valor_total(self):
        valor_total = self.cleaned_data['valor_total']
        if valor_total <= 0:
            raise forms.ValidationError("El valor total debe ser mayor que cero.")
        return valor_total

class SuscripcionForm(forms.ModelForm):
    class Meta:
        model = Suscripcion
        fields = []


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'




class BoletaCompraForm(forms.ModelForm):
    class Meta:
        model = BoletaCompra
        fields = '__all__'