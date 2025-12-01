from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from mainApp.forms import PedidoForm
from .models import Producto, Categoria, Pedido, PedidoImagen, PlataformaOrigen

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, "catalogo.html", {"productos": productos})

def get_plataforma_origen(request):
    plataformas = PlataformaOrigen.objects.get_or_create(nombre="sitio_web")[0]
    return plataformas

def catalogo_producto(request):
    query = request.GET.get('q')
    categoria_slug = request.GET.get('categoria')
    productos = Producto.objects.filter(id__isnull=False)
    
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)
        
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        ).distinct()
        
    categorias = Categoria.objects.all()
    
    contexto = {
        'productos': productos,
        'categorias': categorias,
        'query_busqueda': query,
        'categoria_activa': categoria_slug,
    }
    return render(request, "catalogo.html", contexto)
def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.prefetch_related('imagenes'), 
        slug=slug
    )

    contexto = {
        'producto': producto,
    }
    return render(request, "detalle_producto.html", contexto)
def solicitud_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    plataforma = PlataformaOrigen.objects.get_or_create(nombre="Sitio Web")[0]

    if request.method == "POST":
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.producto_referencia = producto
            pedido.plataforma_origen = plataforma
            pedido.save()

            for img in request.FILES.getlist("imagenes_referencia"):
                PedidoImagen.objects.create(pedido=pedido, imagen=img)

            return redirect("catalogo")

    else:
        form = PedidoForm()

    return render(request, "solicitud.html", {
        "form": form,
        "producto_referencia": producto
    })