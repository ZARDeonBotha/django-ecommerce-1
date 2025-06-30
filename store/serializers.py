# store/serializers.py
from rest_framework import serializers
from .models import Store, Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at', 'verified_purchase']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)  # Shows reviews for each product
    class Meta:
        model = Product
        fields = ['id', 'store', 'name', 'price', 'stock', 'image', 'description', 'reviews']

class StoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # Shows products for each store
    class Meta:
        model = Store
        fields = ['id', 'owner', 'name', 'created_at', 'products']
