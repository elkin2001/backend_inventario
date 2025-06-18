from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoListCreateAPIView, ProductoRetrieveUpdateDestroyAPIView, FacturaListCreateAPIView, FacturaRetrieveUpdateDestroyAPIView

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', include(router.urls)),
    path('productos/', ProductoListCreateAPIView.as_view(), name='producto-list-create'),
    path('productos/<int:pk>/', ProductoRetrieveUpdateDestroyAPIView.as_view(), name='producto-detail'),
    path('factura/', FacturaListCreateAPIView.as_view(), name='factura-list-create'),
    path('factura/<int:pk>/', FacturaRetrieveUpdateDestroyAPIView.as_view(), name='factura-detail'),
]
