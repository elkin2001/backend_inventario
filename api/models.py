from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    existencia = models.PositiveIntegerField()
    valor_unitario_venta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario_compra = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        try:
            logger.info(f"Deleting Producto id={self.id}")
            super().delete(*args, **kwargs)
            logger.info(f"Deleted Producto id={self.id} successfully")
        except Exception as e:
            logger.error(f"Error deleting Producto id={self.id}: {e}")
            raise

class Factura(models.Model):
    fecha = models.DateField()
    persona = models.CharField(max_length=100)
    compania = models.CharField(max_length=100, null=True, blank=True)
    termino = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Factura {self.id} - {self.persona}"

class FacturaProducto(models.Model):
    factura = models.ForeignKey(Factura, related_name='factura_productos', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, related_name='factura_productos')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
