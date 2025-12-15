from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages


MODELS_AVAILABLE = True
try:
    from .models import (
        Categoria,
        Producto,
        ProductoImagen,
        Insumo,
        PlataformaOrigen,
        Pedido,
        PedidoImagen,
    )
except Exception as _err:
    print(f"WARNING: mainApp.models could not be imported: {_err}")
    MODELS_AVAILABLE = False


def miniatura(obj):
    if hasattr(obj, "imagen") and obj.imagen and obj.imagen.url:
        return format_html(
            '<img src="{}" style="height:70px; border-radius:4px;" />',
            obj.imagen.url
        )
    return "—"

if MODELS_AVAILABLE:
    class ProductoImagenInline(admin.TabularInline):
        model = ProductoImagen
        extra = 1
        readonly_fields = ("preview",)
        fields = ("imagen", "preview")

        def preview(self, obj):
            return miniatura(obj)


    class PedidoImagenInline(admin.TabularInline):
        model = PedidoImagen
        extra = 1
        readonly_fields = ("preview",)
        fields = ("imagen", "preview")

        def preview(self, obj):
            return miniatura(obj)


    @admin.register(Categoria)
    class CategoriaAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre", "slug")
        ordering = ("nombre",)


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

        def save_model(self, request, obj, form, change):
            if obj.estado == "ENTREGADO" and obj.estado_pago != "COMPLETADO":
                from django.core.exceptions import ValidationError
                raise ValidationError("No se puede marcar como ENTREGADO si el pago no está COMPLETADO.")
            super().save_model(request, obj, form, change)

        @admin.action(description="Marcar pagos como COMPLETADO")
        def marcar_pago_completado(self, request, queryset):
            """Marca el campo `estado_pago` como 'COMPLETADO' para los pedidos seleccionados."""
            actualizado = 0
            for pedido in queryset:
                if pedido.estado_pago != 'COMPLETADO':
                    pedido.estado_pago = 'COMPLETADO'
                    pedido.save()
                    actualizado += 1

            if actualizado:
                messages.success(request, f'{actualizado} pedido(s) marcado(s) como pago COMPLETADO.')
            else:
                messages.info(request, 'No se actualizaron pedidos (ya estaban COMPL ETADO).')

        actions = ['marcar_pago_completado']
