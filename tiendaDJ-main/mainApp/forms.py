from django import forms
from django.forms import ClearableFileInput
from .models import Pedido, PedidoImagen

class PedidoForm(forms.ModelForm):

    fecha_requerida = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Fecha requerida'
    )
    imagenes_referencia = forms.FileField(
        required=False,
        label='Imágenes de Referencia (Sube tus diseños)',
        widget=ClearableFileInput(attrs={'multiple': True}))

    descripcion_solicitud = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        label='Descripción de la solicitud',
    )

    class Meta:
        model = Pedido
        fields = [
            "cliente_nombre",
            "cliente_telefono",
            "cliente_red_social",
            "descripcion_solicitud",
            "fecha_requerida",
        ]
        labels = {
            "cliente_nombre": "Nombre completo",
            "cliente_telefono": "Número de teléfono",
            "cliente_red_social": "Usuario o red social",
        }
        widgets = {
            "cliente_nombre": forms.TextInput(attrs={"class": "form-control"}),
            "cliente_telefono": forms.TextInput(attrs={"class": "form-control"}),
            "cliente_red_social": forms.TextInput(attrs={"class": "form-control"})
            }


   #def save(self, commit=True):
      ##  pedido = super().save(commit=commit)
       ####  for imagen in imagenes:
        ## PedidoImagen.objects.create(pedido=pedido, imagen=imagen)
        ##return pedido
    def limpiar():
        data_clean= super().clean()
        telefono= data_clean.get('cliente_telefono')
        red_social= data_clean.get('cliente_red_social')
        if not telefono and not red_social:
            from django.core.exceptions import ValidationError
            raise ValidationError("Debe proporcionar al menos un método de contacto: teléfono o red social.")
        return data_clean
    
        
class PedidoImagenForm(forms.ModelForm):
    class Meta:
        model = PedidoImagen
        fields = ["imagen"]
        labels = {
            "imagen": "Imagen de referencia",
        }
        widgets = {
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        } 
    def limpiar_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                from django.core.exceptions import ValidationError
                raise ValidationError("El tamaño de la imagen no debe exceder los 5MB.")
        return imagen
    class Meta:
        model = PedidoImagen
        fields = ["imagen"]
        labels = {
            "imagen": "Imagen de referencia",
        }
        widgets = {
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }

