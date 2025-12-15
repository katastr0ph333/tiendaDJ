from django.db import models
from django.utils.text import slugify
from uuid import uuid4
# Create your models here.


ESTADO_PEDIDO_CHOICES = [
    ('APROBADO', 'Aprobado'),
    ('ENVIADO', 'Enviado'),
    ('ENTREGADO', 'Entregado'), 
    ('CANCELADO', 'Cancelado'),
    ('SOLICITADO', 'Solicitado'),
    ('EN_PROCESO', 'En Proceso'),
    ('FINALIZADO', 'Finalizado')
]

ESTADO_PAGO_CHOICES = [
    ('PENDIENTE', 'Pendiente'),
    ('COMPLETADO', 'Completado'),
    ('PARCIAL', 'Parcial'),
    
]

RED_SOCIAL_CHOICES = [
    ('WHATSAPP', 'WhatsApp'),
    ('INSTAGRAM', 'Instagram'),
    ('FACEBOOK', 'Facebook'),
    ('PRESENCIAL', 'Presencial'),
    ('SITIO_WEB', 'Sitio Web'),
    ('OTRO', 'Otro')]

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    destacado = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
    
    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Producto"

class Insumo(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    cantidad_disponible = models.IntegerField(default=0)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad_disponible} {self.unidad})"
    
    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
    
    
class PlataformaOrigen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Plataforma de Origen"
        verbose_name_plural = "Plataformas de Origen"
    
class Pedido(models.Model):
    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField(blank=True, null=True)
    cliente_telefono = models.CharField(max_length=20, blank=True, null=True)
    cliente_red_social = models.CharField(max_length=100, blank=True, null=True)
    producto_referencia = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True)
    descripcion_solicitud = models.TextField(blank=True, verbose_name='descripción de la solicitud')
    fecha_requerida = models.DateTimeField(blank=True, null=True, verbose_name='fecha requerida')
    plataforma_origen = models.ForeignKey(PlataformaOrigen, on_delete=models.PROTECT)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO_CHOICES, default='SOLICITADO')
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='PENDIENTE')
    medio_contacto = models.CharField(max_length=20, choices=RED_SOCIAL_CHOICES, blank=True, null=True)
    token_seguimiento = models.CharField(max_length=100, unique=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.token_seguimiento:
            self.token_seguimiento = str(uuid4())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido {self.id} - {self.cliente_nombre}"
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_solicitud']

class PedidoImagen(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='pedidos/referencia/')
    
    def __str__(self):
        return f"Imagen del Pedido {self.pedido.id}"
    
    class Meta:
        verbose_name = "Imagen de Pedido"
        verbose_name_plural = "Imágenes de Pedido"
