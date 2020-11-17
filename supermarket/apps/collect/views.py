from django.shortcuts import render
from rest_framework import viewsets
from .models import Collect
from product.models import Product
from .serializer import CollectSerializer
from db.baseviews import BaseModelViewSet
from rest_framework.response import Response

class ColectViews(BaseModelViewSet):
    '''收藏中心'''
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    def create(self,request,*args, **kwargs):
        product_id = self.request.data.get('id')
        product = self.queryset.filter(product_id = product_id).last()
        if product:
            product.delete()
            return Response({'code':200 , 'status':'取消收藏'})
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.request.data.get('id')
        # is_product = Collect.objects.filter(product_id=product_id,user=user)
        # if is_product.last():
        #     is_product.delete()
        product = Product.objects.filter(id=product_id).last()
        serializer.save(user = user, product= product)

    def perform_destroy(self, instance):
        '''物理删除'''
        instance.delete()