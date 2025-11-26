from django.db import models
from django.utils.text import slugify
# Create your models here.


ESTADO_PEDIDO_CHOICES = [
    ('APROBADO', 'Aprobado'),
    ('ENVIADO', 'Enviado'),
    ('ENTREGADO', 'Entregado'), 
    ('CANCELADO', 'Cancelado'),
    ('SOLICITADO', 'Solicitado'),
]

ESTADO_PAGO_CHOICES = [
    ('PENDIENTE', 'Pendiente'),
    ('COMPLETADO', 'Completado'),
    ('FALLIDO', 'Fallido'),
]

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.nombre
    
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
    
class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class Insumo(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    cantidad_disponible = models.IntegerField(default=0)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.cantidad_disponible} {self.unidad})"
    
    
class PlataformaOrigen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    cliente_nombre = models.CharField(max_length=200)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20, blank=True, null=True)
    cliente_red_social = models.CharField(max_length=100, blank=True, null=True)
    producto_referencia = models.ForeignKey(Producto, related_name='producto del catalogo', on_delete=models.SET_NULL, blank=True, null=True)
    descripcion_solicitud = models.TextField(blank=True, related_name='descripcion de la solicitud')
    fecha_requerida = models.DateTimeField(blank=True, null=True, related_name='fecha requerida')
    plataforma_origen = models.ForeignKey(PlataformaOrigen, related_name='plataforma de origen', on_delete=models.PROTECT)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO_CHOICES, default='SOLICITADO', related_name='estado del pedido')
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='PENDIENTE', related_name='estado del pago')
    def __str__(self):
        return f"Pedido {self.id} - {self.cliente_nombre}"

class PedidoImagen(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='imagen del pedido', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='pedidos/referencia/')

    