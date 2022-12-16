from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Stock, Product
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title']
    search_fields = ['description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [SearchFilter]
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']
