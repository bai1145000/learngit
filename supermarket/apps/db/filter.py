import django_filters
from django_filters import rest_framework  as filters
from product.models import ProductClassify, Product
from rest_framework import filters as fs

# class ProductClassifyFilter(django_filters.FilterSet):

#     class Meta:
#         model = Producclassify
#         fields = ['id','name','catpid'] #需要过滤的字段
#         filter_fields = {
#             'id': ['exact'],
#             "name": ['exact','icontains'],
#             'catpid':['exact']
#         }

class ProductFilter(filters.FilterSet):
    # 区间查询,指定区间的最大最小值
    price_min = filters.NumberFilter(field_name="product_price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="product_price", lookup_expr='lte')
    # 模糊查询,这里带i是忽略大小写
    name = filters.CharFilter(field_name="product_name", lookup_expr="icontains")
    classify = filters.CharFilter(field_name="product_classify")

    class Meta:
        model = Product
        fields = ['name', 'price_min','price_max','classify'] #需要过滤的字段
        filter_fields = {
            "name": ['exact','icontains'],
            'price_min': ['exact'],
            'price_max': ['exact'],
        }