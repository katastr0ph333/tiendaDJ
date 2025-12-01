from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import PedidoForm
from .models import Producto, Categoria, Pedido, PedidoImagen,PlataformaOrigen


def get_plataforma_web():
    plataforma, created = PlataformaOrigen.objects.get_or_create(nombre="Sitio Web")
    return plataforma

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
        Producto.objects.prefetch_related("imagenes"),
        slug=slug
    )
    return render(request, "detalle_producto.html", {"producto": producto})


def solicitud_pedido(request, producto_id=None):

    producto_referencia= None 
    if producto_id:
        producto_referencia = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        form = PedidoForm(request.POST, request.FILES)
        
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.producto_referencia = producto_referencia
            pedido.plataforma_origen = get_plataforma_web()
            pedido.save()
            
            imagenes = request.FILES.getlist('imagenes_referencia')
            for imagen_archivo in imagenes:
                PedidoImagen.objects.create(
                    pedido=pedido,
                    imagen=imagen_archivo
                )
                
            return render(
                request,
                "solicitud_exitosa.html",
                {'token': pedido.token_seguimiento},
                {"pedido": pedido})
            
    else:
        form = PedidoForm()
        
    contexto = {
        'form': form,
        'producto_referencia': producto_referencia
    }
    return render(request, "solicitud.html", contexto)

 

def seguimiento_pedido(request, token):
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related('pedidoimagen_set'), 
        token_seguimiento=token
    )
    
    contexto= {
        'pedido': pedido
    }
    
    return render(request, 'seguimiento_pedido.html', contexto)
