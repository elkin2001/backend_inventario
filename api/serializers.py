from rest_framework import serializers
from .models import Categoria, Producto, Factura, FacturaProducto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    nombre_categoria = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'nombre_categoria', 'existencia', 'valor_unitario_venta', 'valor_unitario_compra']

class FacturaProductoSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), write_only=True)
    producto_detalle = ProductoSerializer(source='producto', read_only=True)

    class Meta:
        model = FacturaProducto
        fields = ['producto', 'producto_detalle', 'cantidad', 'precio_unitario']

class FacturaSerializer(serializers.ModelSerializer):
    factura_productos = FacturaProductoSerializer(many=True)

    class Meta:
        model = Factura
        fields = ['id', 'fecha', 'persona', 'compania', 'termino', 'factura_productos']

    def create(self, validated_data):
        factura_productos_data = validated_data.pop('factura_productos')
        factura = Factura.objects.create(**validated_data)
        for item in factura_productos_data:
            FacturaProducto.objects.create(factura=factura, **item)
        return factura
