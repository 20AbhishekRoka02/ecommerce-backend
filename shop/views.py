from rest_framework.viewsets import ReadOnlyModelViewSet
from shop.models import Product, Category, CompanyConfig
from shop.serializers import ProductSerializer, CategorySerializer, CompanyConfigSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ComapanyConfigViewSet(ReadOnlyModelViewSet):
    queryset = CompanyConfig.objects.all()
    serializer_class = CompanyConfigSerializer