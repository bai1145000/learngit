from rest_framework import serializers
from .models import Collect
from product.models import Product

class CollectSerializer(serializers.ModelSerializer):
    '''收藏'''
    user = serializers.CharField(read_only=True)
    product_name = serializers.CharField(source='product.product_name',read_only=True) #商品名字
    id = serializers.IntegerField(source='product',write_only=True)

    class Meta:
        fields = ['id','product_name','user']
        model = Collect

    # def create(self, validated_data):
    #     is_collect = Collect.objects.filter(**validated_data )
    #     if not is_collect:
    #         is_collect.delete()
    #     return super().create(validated_data)
        


    
        

