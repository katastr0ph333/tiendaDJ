from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    
class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
    
    
class PlataformaOrigen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    estado = models.CharField(max_length=50)
    estado_pago = models.CharField(max_length=50)
    plataforma_origen = models.ForeignKey(PlataformaOrigen, on_delete=models.PROTECT)

    def __str__(self):
        return f"Pedido de {self.cantidad} x {self.producto.nombre} desde {self.plataforma_origen.nombre}"