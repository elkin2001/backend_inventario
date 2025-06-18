from django.contrib import admin
from .models import Producto, Factura, Categoria

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'existencia', 'valor_unitario_venta', 'valor_unitario_compra')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'persona', 'compania', 'termino')
    search_fields = ('persona', 'compania')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
