from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from mainApp.models import Insumo, Pedido
from .serializers import InsumoSerializer, PedidoSerializer 
from rest_framework.decorators import api_view
from django.db.models import Q
from datetime import datetime

@api_view(['GET','POST', 'PUT', 'DELETE'])
def insumo_list(request):
    if request.method == 'GET':
        insumos = Insumo.objects.all()
        serializer = InsumoSerializer(insumos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = InsumoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        insumo_id = request.data.get('id')
        insumo = Insumo.objects.get(id=insumo_id)
        serializer = InsumoSerializer(insumo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        insumo_id = request.data.get('id')
        insumo = Insumo.objects.get(id=insumo_id)
        insumo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','POST', 'PUT', 'DELETE'])
def pedido_list(request):
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        pedido_id = request.data.get('id')
        pedido = Pedido.objects.get(id=pedido_id)
        serializer = PedidoSerializer(pedido, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pedido_id = request.data.get('id')
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def pedido_list_filtrado(request):
    
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')
    estados = request.query_params.getlist('estados')
    max_resultados = request.query_params.get('max_resultados', 100)

    try:
        max_resultados = int(max_resultados)
        if max_resultados < 1:
            max_resultados = 100
    except ValueError:
        max_resultados = 100

    pedidos = Pedido.objects.all()

    if fecha_inicio or fecha_fin:
        try:
            fecha_inicio_dt = datetime.fromisoformat(fecha_inicio) if fecha_inicio else None
        except ValueError:
            return Response({'error': 'Formato de fecha_inicio inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fecha_fin_dt = datetime.fromisoformat(fecha_fin) if fecha_fin else None
        except ValueError:
            return Response({'error': 'Formato de fecha_fin inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)
        
        if fecha_inicio_dt and fecha_fin_dt:
            pedidos = pedidos.filter(
                Q(fecha_solicitud__date__gte=fecha_inicio_dt.date(),
                fecha_solicitud__date__lte=fecha_fin_dt.date())
            )
        elif fecha_inicio_dt:
            pedidos = pedidos.filter(
                Q(fecha_solicitud__date__gte=fecha_inicio_dt.date()) 
    
            )
        elif fecha_fin_dt:
            pedidos = pedidos.filter(
                Q(fecha_solicitud__date__lte=fecha_fin_dt.date())
            )

    if estados:
        pedidos = pedidos.filter(estado__in=estados)

    pedidos = pedidos.select_related('producto_referencia').order_by('-id')[:max_resultados]
    
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)