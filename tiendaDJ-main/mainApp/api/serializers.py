from rest_framework import serializers
from mainApp.models import Insumo, Pedido, PedidoImagen

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ('id', 'cliente_nombre', 'cliente_email', 'producto', 'cantidad', 'fecha_solicitud')
        read_only_fields = ('id', 'fecha_solicitud')
        