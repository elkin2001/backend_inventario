from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Producto, Categoria

class ProductoAPITestCase(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Categoria Test")
        self.producto = Producto.objects.create(
            nombre="Producto Test",
            categoria=self.categoria,
            existencia=10,
            valor_unitario_venta=100.0,
            valor_unitario_compra=80.0
        )
        self.producto_detail_url = reverse('producto-detail', kwargs={'pk': self.producto.pk})
        self.non_existent_detail_url = reverse('producto-detail', kwargs={'pk': 9999})

    def test_edit_producto(self):
        data = {
            "nombre": "Producto Editado",
            "categoria": self.categoria.id,
            "existencia": 20,
            "valor_unitario_venta": 150.0,
            "valor_unitario_compra": 120.0
        }
        response = self.client.put(self.producto_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Producto Editado")
        self.assertEqual(self.producto.existencia, 20)
        self.assertEqual(float(self.producto.valor_unitario_venta), 150.0)
        self.assertEqual(float(self.producto.valor_unitario_compra), 120.0)

    def test_delete_producto(self):
        response = self.client.delete(self.producto_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Producto.DoesNotExist):
            Producto.objects.get(pk=self.producto.pk)

    def test_edit_non_existent_producto(self):
        data = {
            "nombre": "No Existe",
            "categoria": self.categoria.id,
            "existencia": 0,
            "valor_unitario_venta": 0.0,
            "valor_unitario_compra": 0.0
        }
        response = self.client.put(self.non_existent_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_producto(self):
        response = self.client.delete(self.non_existent_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_producto_invalid_data(self):
        data = {
            "nombre": "",  # Assuming nombre is required and cannot be empty
            "categoria": self.categoria.id,
            "existencia": -10,  # Invalid negative stock
            "valor_unitario_venta": -100.0,  # Invalid negative price
            "valor_unitario_compra": -80.0  # Invalid negative price
        }
        response = self.client.put(self.producto_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
