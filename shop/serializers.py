from rest_framework import serializers
from shop.models import Product, CompanyConfig, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"

class CompanyConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyConfig
        fields = "__all__"