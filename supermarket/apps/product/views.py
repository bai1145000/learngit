from django.shortcuts import render
from rest_framework.mixins import ListModelMixin
from db.baseviews import BaseModelViewSet, ResponseTemplate
from .models import ProductClassify, ProductImages, Product
from .serializers import ProductListSerializer, ProductClassifySerializer, ProductImageSerializer, SlideshowViewsSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from db.filter import ProductFilter
import json, uuid, random
from django.contrib.admin.models import LogEntry
from itertools import chain
from django.db.models import Q
import asyncio
# Create your views here.

class ProductListViews(BaseModelViewSet):
    """商品列表页"""

    # filter_class = ProductFilter
    serializer_class = ProductListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(is_delete = False).filter(create_user_id=user.id).order_by('-create_time')
        return queryset

    def create(self,request,*args, **kwargs):
        product_name = request.data.get('product_name')
        if self.get_queryset().filter(product_name = product_name):
            return Response(ResponseTemplate(code = 400, status = '已存在').template())
        return super().create( request, *args, **kwargs)
        
    def perform_create(self, serializer):
        '''自动为当前创建商品加上用户'''
        create_user = self.request.user
        serializer.save(create_user=create_user)

    def perform_update(self, serializer):
        '''判断传输数据为空,为上架货品'''
        if not serializer.initial_data:
            serializer.instance.product_is_putaway = False if serializer.instance.product_is_putaway else True
        serializer.save()


class ProductImagesViews(BaseModelViewSet):
    '''商品图片'''
    queryset = ProductImages.objects.all()
    serializer_class = ProductImageSerializer

    def create(self, request, *args, **kwargs):
        data = dict()
        image_list = self.request.data.getlist('image')
        data['Product'] = self.request.data.get('Product')
        for image in image_list:
            data['image_url'] = image
            serializer = self.get_serializer(data=data) #序列化输入每张图片
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)   #保存
        else:
            return Response(ResponseTemplate(code=200, status='添加成功').template())
        return Response(ResponseTemplate(code=400, data = serializer.errors).template())


class ProductClassifyViews(BaseModelViewSet):
    '''商品分类'''
    queryset = ProductClassify.objects.filter(is_delete = False).filter(parent_id=None)
    serializer_class = ProductClassifySerializer

    search_fields = ('=name')
    ordering_fields = ['name','parent_id']

    def get_object(self):
        self.queryset = ProductClassify.objects.filter(is_delete = False)
        return super().get_object()

    def create(self,request,*args, **kwargs):
        label = self.request.data.get('label')
        classify = ProductClassify.objects.filter(is_delete = False).filter(name = label).last()
        if classify:
            return Response({'code':400,'status':'已存在'})
        return super().create(request,*args, **kwargs)

class ProductCenterViews(BaseModelViewSet):
    '''商品中心'''
    serializer_class = ProductListSerializer
    ordering_fields = ('product_price','[-,+](.*?)_create_time') 
    filter_class = ProductFilter

    def get_queryset(self):
        '''筛选出已上架的'''
        user = self.request.user
        queryset = Product.objects.filter(is_delete = False).filter(product_is_putaway=True)

        '''根据开头[-,+]product_create_time,-为时间排序'''
        ordering = self.request.query_params.get('ordering')
        if ordering is not None and  'create_time' in ordering:
            queryset = queryset.order_by('{}create_time'.format( '' if ordering[0] !='-' else ordering[0]))
        return queryset

class SlideshowViews(viewsets.ReadOnlyModelViewSet):
    '''首页推荐轮播图'''
   
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        # LogEntry
        filters = keyword()
        max_product = {}
        queryset = Product.objects.filter(is_delete = False).filter(product_is_putaway=True)
        #查找每组数据总出现次数最多的
        for k,v in filters.items():
            count = 0
            for i in v:
                count = v.count(i) if v.count(i)>count else count
                if count > len(v)/2: #数据大于总数的1/2则中断
                    break
            max_product.update({k:i})

        data_name = queryset.filter(Q(product_name= max_product.get('name'))| Q(product_classify = max_product.get('classify')))
        data_price = queryset.filter(Q(product_price__lte=max_product.get('price_max'))&Q(product_price__gt=max_product.get('price_min',0)))
        # data_price = queryset.raw('select * from product_manage.products where product_price <%s',params=[max_product.get('price_max')])
        data_price = random.choices(data_price,k=2) #随机返回2条

        data = data_price + list(data_name)
        data = data + random.choices(queryset,k=(6-len(data))) if len(data)<6 else data
        #保证6条数据全是不一样的
        while len(set(data))<6:
            data.append(random.choice(queryset))
            data = list(set(data))
        return data
    
    def list(self,request,*args,**kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        return Response(ResponseTemplate(status='成功', code=200, data = data, kwargs=kwargs).template())

def keyword():
    '''寻找出筛选分组的数据
    {
        name:[....],
        price:[....]
    }
    '''
    # log = LogEntry.objects.filter(object_id=request.resolver_match.url_name) #基于该视图的所有loging
    log =  LogEntry.objects.filter(object_id="center-list").order_by('-action_time')[:10] #基于该视图的最近10条loging
    classify_dict = {}
    for i in log:
        import_u = eval(i.change_message).get('import')
        classify = list(import_u.keys())
        for k in classify:
            if k not in classify_dict:
                classify_dict[k] = [import_u.get(k)]
                continue 
            classify_dict[k].append(import_u.get(k))
    return classify_dict




