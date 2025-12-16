from rest_framework import serializers
from mainApp.models import Insumo, Pedido, PedidoImagen

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        
        read_only_fields = ['estado', 'token_pedido','estado_pago']
        
        
class PedidoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'insumos', 'total', 'direccion_envio', 'metodo_pago']
        read_only_fields = ['estado', 'token_pedido','estado_pago']

