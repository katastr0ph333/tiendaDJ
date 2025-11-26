from django.contrib import admin
from .models import Categoria, Producto, ProductoImagen, PlataformaOrigen, Pedido
from django.utils.html import format_html

class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    readonly_fields = ('imagen_admin',)
    fields = ('imagen', 'imagen_admin',)

    def imagen_admin(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.imagen.url)
        return "No Image"
    imagen_admin.short_description = 'vista previa'
    
