from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from .forms import PedidoForm, PedidoImagenForm
from .models import Producto, Categoria, Pedido, PedidoImagen, PlataformaOrigen
from django.forms import modelformset_factory
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
        Producto.objects.prefetch_related("imagenes"),
        slug=slug
    )
    return render(request, "detalle_producto.html", {"producto": producto})


def solicitud_producto(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)
    plataforma = PlataformaOrigen.objects.get_or_create(nombre="Sitio Web")[0]

    ImagenFormSet = modelformset_factory(
        PedidoImagen,
        form=PedidoImagenForm,
        extra=5,
        can_delete=False
    )

    if request.method == "POST":
        form = PedidoForm(request.POST)
        formset = ImagenFormSet(request.POST, request.FILES, queryset=PedidoImagen.objects.none())

        if form.is_valid() and formset.is_valid():

            pedido = form.save(commit=False)
            pedido.producto_referencia = producto
            pedido.plataforma_origen = plataforma
            pedido.save()

            # Guardar imágenes
            for f in formset.cleaned_data:
                if f and f.get("imagen"):
                    PedidoImagen.objects.create(
                        pedido=pedido,
                        imagen=f["imagen"]
                    )

            return redirect("catalogo")

    else:
        form = PedidoForm()
        formset = ImagenFormSet(queryset=PedidoImagen.objects.none())

    return render(request, "solicitud.html", {
        "form": form,
        "formset": formset,
        "producto": producto
    })