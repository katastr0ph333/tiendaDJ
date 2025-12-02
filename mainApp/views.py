from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import PedidoForm, PedidoImagenForm
from .models import Producto, Categoria, Pedido, PedidoImagen, PlataformaOrigen
from django.forms import modelformset_factory
from django.contrib import messages

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, "catalogo.html", {"productos": productos})

def get_plataforma_origen(request):
    plataformas = PlataformaOrigen.objects.get_or_create(nombre="Sitio Web")[0]
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

            # Mensaje de confirmación al crear el pedido
            messages.success(request, f"Solicitud enviada. Tu token de seguimiento es: {pedido.token_seguimiento}")

            # Redirigir a la página de seguimiento con el token
            return redirect("seguimiento_pedido", token=pedido.token_seguimiento)

    else:
        form = PedidoForm()
        formset = ImagenFormSet(queryset=PedidoImagen.objects.none())

    return render(request, "solicitud.html", {
        "form": form,
        "formset": formset,
        "producto": producto
    })

def seguimiento_pedido(request, token):
    """
    Vista pública para que los clientes realicen seguimiento de su pedido.
    Accesible a través de una URL única con el token.
    """
    pedido = get_object_or_404(Pedido, token_seguimiento=token)
    
    # Definir colores y descripciones para los estados
    estados_info = {
        'SOLICITADO': {'color': 'primary', 'descripcion': 'Tu pedido ha sido recibido'},
        'APROBADO': {'color': 'info', 'descripcion': 'Tu pedido ha sido aprobado'},
        'EN_PROCESO': {'color': 'warning', 'descripcion': 'Tu pedido está en proceso'},
        'ENTREGADO': {'color': 'success', 'descripcion': 'Tu pedido ha sido entregado'},
        'REALIZADA': {'color': 'success', 'descripcion': 'Tu pedido ha sido realizado'},
        'FINALIZADA': {'color': 'success', 'descripcion': 'Tu pedido está finalizado'},
        'CANCELADA': {'color': 'danger', 'descripcion': 'Tu pedido ha sido cancelado'},
    }
    
    estado_pago_info = {
        'PENDIENTE': {'color': 'danger', 'texto': 'Pago Pendiente'},
        'PARCIAL': {'color': 'warning', 'texto': 'Pago Parcial'},
        'COMPLETADO': {'color': 'success', 'texto': 'Pago Completado'},
    }
    
    estado_actual = estados_info.get(pedido.estado, {'color': 'secondary', 'descripcion': 'Estado desconocido'})
    pago_actual = estado_pago_info.get(pedido.estado_pago, {'color': 'secondary', 'texto': 'Estado desconocido'})
    
    contexto = {
        'pedido': pedido,
        'estado_actual': estado_actual,
        'pago_actual': pago_actual,
    }
    
    return render(request, "seguimiento.html", contexto)