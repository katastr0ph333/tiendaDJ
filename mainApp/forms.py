from django import forms
from django.forms import ClearableFileInput
from .models import Pedido, PedidoImagen

class PedidoForm(forms.ModelForm):

    fecha_requerida = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Fecha requerida',
    )

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

    def save(self, commit=True):
        pedido = super().save(commit=commit)
        imagenes = self.files.getlist('imagenes_referencia')
        for imagen in imagenes:
            PedidoImagen.objects.create(pedido=pedido, imagen=imagen)
        return pedido
class PedidoImagenForm(forms.ModelForm):
    class Meta:
        model = PedidoImagen
        fields = ["imagen"]