from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ShoppingCart

class ShoppingCartSerializer(serializers.ModelSerializer):
    product_classify = serializers.CharField(source='products.product_classify.name',read_only=True)

    class Meta:
        model = ShoppingCart
        fields = "__all__"