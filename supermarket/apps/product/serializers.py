from rest_framework import serializers
from django.contrib.auth.models import User
from collect.models import Collect
from .models import ProductClassify, ProductImages, Product

class  ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='image_url')
    # product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = ProductImages
        # fields = '__all__'
        fields  = ['image']

class ProductListSerializer(serializers.ModelSerializer):
    '''我的商品'''
    product_create_time = serializers.DateTimeField(source='create_time',read_only=True)
    product_id = serializers.IntegerField(source='id',read_only=True)
    product_classify = serializers.CharField(read_only=True)
    create_user = serializers.CharField(read_only=True)
    product_url = serializers.SerializerMethodField()
    product_status_nums = serializers.SerializerMethodField()
    product_is_collection  = serializers.SerializerMethodField()
    product_url = serializers.SerializerMethodField()
    files = serializers.ImageField(write_only=True)
    class Meta:
        model = Product
        # fields ="__all__"
        exclude = ['update_time','Product_desc','is_delete','create_time']

    def get_product_status_nums(self,obj):
        '''收藏次数'''
        self.couts = len(obj.collectProduct.all())
        return self.couts

    def get_product_is_collection(self,obj):
        '''是否被收藏'''
        request = self.context.get('request')
        user = request.user
        collect  = Collect.objects.filter(user =user,product = obj )
        return True if collect.last() else False  

    def get_product_url(self, obj):
        image_url = ProductImageSerializer(instance = obj.productImages.all().filter(is_delete=True),many=True,context={'request':self.context['request']}).data
        # image_url = [self.context['request']._current_scheme_host + i.image_url.url for i in obj.productImages.all()]
        # return dict(zip(range(len(image_url)),image_url))
        return image_url

    def create(self, validated_data):
        images = self.context['request'].data.getlist('files')
        product_classify = self.context['request'].data.get('product_classify')
        validated_data['product_classify'] = ProductClassify.objects.filter(id=product_classify).last()
        del validated_data['files']
        instance = super().create(validated_data)
        for i in images :
            ProductImages.objects.create(image_url=i,product=instance)
        return instance

    def update(self,instance,validated_data):
        product_classify = self.context['request'].data.get('product_classify')
        if product_classify:
            validated_data['product_classify'] = ProductClassify.objects.filter(name=product_classify).last()
        return super().update(instance,validated_data)
    

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'format': self.format_kwarg,
            'view': self
        }

class ProductClassifySerializer(serializers.ModelSerializer):
    '''商品分类'''
    parent = serializers.IntegerField(source='parent_id',allow_null=True)
    children = serializers.SerializerMethodField()
    label =  serializers.CharField(source='name')
    value = serializers.CharField(source='id',read_only=True)
    class Meta:
        model = ProductClassify
        fields = ['id','label','value','children','parent']
        # fields = "__all__"
        # read_only_fields = ['name','values']
        depth = 5

    def get_children(self, obj):
        '''递归获取下级分类'''
        if hasattr(obj,'parentClassify'):
            return ProductClassifySerializer(obj.parentClassify.all(), many=True).data
    
    def create(self,validated_data):
        return super().create(validated_data)


class SlideshowViewsSerializer(serializers.ModelSerializer):
    '''轮播'''

    class Meta:

        model = Product
        fields ="__all__"
  

    