from rest_framework import viewsets
from .models import Categoria, Producto, Factura, FacturaProducto
from .serializers import CategoriaSerializer, ProductoSerializer, FacturaSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import AllowAny

from rest_framework import viewsets

import logging
logger = logging.getLogger(__name__)

class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting category {instance.id}: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductoListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        producto = self.get_object(pk)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    def put(self, request, pk):
        producto = self.get_object(pk)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = self.get_object(pk)
        try:
            producto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting product {producto.id}: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Factura, FacturaProducto
from .serializers import FacturaSerializer

class FacturaListCreateAPIView(APIView):
    def get(self, request):
        facturas = Factura.objects.all()
        serializer = FacturaSerializer(facturas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacturaSerializer(data=request.data)
        if serializer.is_valid():
            factura = serializer.save()
            return Response(FacturaSerializer(factura).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FacturaRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Factura.objects.get(pk=pk)
        except Factura.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        factura = self.get_object(pk)
        serializer = FacturaSerializer(factura)
        return Response(serializer.data)

    def put(self, request, pk):
        factura = self.get_object(pk)
        serializer = FacturaSerializer(factura, data=request.data)
        if serializer.is_valid():
            factura = serializer.save()
            return Response(FacturaSerializer(factura).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        factura = self.get_object(pk)
        factura.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
