from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Pedido, PedidoImagen, PlataformaOrigen

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, "catalogo.html", {"productos": productos})