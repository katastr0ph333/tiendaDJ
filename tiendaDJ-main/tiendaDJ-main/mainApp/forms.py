from django import forms
from .models import Pedido, PedidoImagen

class PedidoForm(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 
            'medio_contacto_preferido', 
            'cliente_email', 
            'cliente_telefono',
            'cliente_usuario_red_social',
            'descripcion_solicitud',
            'fecha_necesita',]
        
    imagenes_referencia =  forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label='Imágenes de referencia',
        help_text='Puedes subir múltiples imágenes que ayuden a entender tu solicitud.',
        required=False
    )
    
    fecha_necesita = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha en que se necesita el pedido',
    )
    
    descripcion_solicitud = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Descripción detallada de la solicitud',
    )
    
    labels = {
        'cliente_nombre': 'Nombre completo',  
        'medio_contacto_preferido': 'Medio de contacto preferido',
        'cliente_email': 'Correo electrónico',
        'cliente_telefono': 'Número de teléfono',
        'cliente_usuario_red_social': 'Usuario de red social'
    }
    
    class PedidoImagenForm(forms.ModelForm):
        class Meta:
            model = PedidoImagen
            fields = ['imagen']