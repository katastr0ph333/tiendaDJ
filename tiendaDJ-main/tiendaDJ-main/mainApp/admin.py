from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Categoria,
    Producto,
    ProductoImagen,
    Insumo,
    PlataformaOrigen,
    Pedido,
    PedidoImagen
)


def miniatura(obj):
    if hasattr(obj, "imagen") and obj.imagen and obj.imagen.url:
        return format_html(
            '<img src="{}" style="height:70px; border-radius:4px;" />',
            obj.imagen.url
        )
    return "—"

miniatura.short_description = "Vista previa"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "slug")
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("nombre",)


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    readonly_fields = ("preview",)
    fields = ("imagen", "preview")

    def preview(self, obj):
        return miniatura(obj)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "categoria", "precio_base", "destacado")
    list_filter = ("categoria", "destacado")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    inlines = [ProductoImagenInline]




@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "tipo", "cantidad_disponible", "marca", "unidad")
    list_filter = ("tipo", "marca", "unidad")
    search_fields = ("nombre", "tipo", "marca")
    ordering = ("nombre",)


@admin.register(PlataformaOrigen)
class PlataformaOrigenAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


class PedidoImagenInline(admin.TabularInline):
    model = PedidoImagen
    extra = 1
    readonly_fields = ("preview",)
    fields = ("imagen", "preview")

    def preview(self, obj):
        return miniatura(obj)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente_nombre",
        "producto_referencia",
        "plataforma_origen",
        "estado",
        "estado_pago",
        "fecha_requerida",
        "fecha_solicitud",
    )

    list_filter = (
        "estado",
        "estado_pago",
        "plataforma_origen",
        "fecha_requerida",
        "fecha_solicitud",
    )

    search_fields = (
        "cliente_nombre",
        "cliente_telefono",
        "cliente_red_social",
        "descripcion_solicitud",
    )

    date_hierarchy = "fecha_solicitud"

    inlines = [PedidoImagenInline]

    readonly_fields = ("fecha_solicitud",)

    fieldsets = (
        ("Datos del cliente", {
            "fields": (
                "cliente_nombre",
                "cliente_telefono",
                "cliente_red_social",
            )
        }),
        ("Producto y solicitud", {
            "fields": (
                "producto_referencia",
                "descripcion_solicitud",
                "fecha_requerida",
            )
        }),
        ("Origen y estado", {
            "fields": (
                "plataforma_origen",
                ("estado", "estado_pago"),
            )
        }),
        ("Información del sistema", {
            "classes": ("collapse",),
            "fields": ("fecha_solicitud",),
        }),
    )

    # regla de negocio: no permitir finalizar sin pago
    def save_model(self, request, obj, form, change):
        if obj.estado == "ENTREGADO" and obj.estado_pago != "COMPLETADO":
            from django.core.exceptions import ValidationError
            raise ValidationError("No se puede marcar como ENTREGADO si el pago no está COMPLETADO.")
        super().save_model(request, obj, form, change)
