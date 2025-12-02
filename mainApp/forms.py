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
            "cliente_email",
            "cliente_telefono",
            "cliente_red_social",
            "descripcion_solicitud",
            "fecha_requerida",
        ]
        labels = {
            "cliente_nombre": "Nombre completo",
            "cliente_email": "Correo electrónico",
            "cliente_telefono": "Número de teléfono",
            "cliente_red_social": "Usuario o red social",
        }
        widgets = {
            "cliente_nombre": forms.TextInput(attrs={"style": "width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;"}),
            "cliente_email": forms.EmailInput(attrs={"style": "width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;"}),
            "cliente_telefono": forms.TextInput(attrs={"style": "width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;"}),
            "cliente_red_social": forms.TextInput(attrs={"style": "width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;"}),
            "descripcion_solicitud": forms.Textarea(attrs={"style": "width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;", "rows": 3}),
            "fecha_requerida": forms.DateTimeInput(attrs={"style": "width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;", "type": "datetime-local"}),
        }

    def save(self, commit=True):
        pedido = super().save(commit=commit)
        imagenes = self.files.getlist('imagenes_referencia')
        for imagen in imagenes:
            PedidoImagen.objects.create(pedido=pedido, imagen=imagen)
        return pedido

    def clean(self):
        cleaned = super().clean()
        fecha = cleaned.get('fecha_requerida')
        if fecha:
            from django.utils import timezone
            now = timezone.now()
            # If fecha is naive, compare in naive form by converting now to naive in current timezone
            if hasattr(fecha, 'tzinfo') and fecha.tzinfo is None:
                # make now naive in current timezone
                try:
                    import datetime
                    now_naive = now.replace(tzinfo=None)
                except Exception:
                    now_naive = now
                compare_now = now_naive
            else:
                compare_now = now

            if fecha < compare_now:
                from django.core.exceptions import ValidationError
                raise ValidationError({'fecha_requerida': 'La fecha requerida no puede ser anterior a la fecha y hora actual.'})
        return cleaned

class PedidoImagenForm(forms.ModelForm):
    class Meta:
        model = PedidoImagen
        fields = ["imagen"]
