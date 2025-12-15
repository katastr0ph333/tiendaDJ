from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from mainApp.models import Insumo, Pedido
from .serializers import InsumoSerializer 
from rest_framework.decorators import api_view

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
    