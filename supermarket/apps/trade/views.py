from django.shortcuts import render
from .models import ShoppingCart
from . serializers import ShoppingCartSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class ShoppingCartViews(ModelViewSet):
    '''购物车'''
    serializer_class =  ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()


