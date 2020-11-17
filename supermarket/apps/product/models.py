from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from db.basemodels import BaseModel
from product.tests import get_image_path

class Product(BaseModel):
    '''商品模型'''
    
    product_name = models.CharField(max_length=20, unique=True, verbose_name='商品名称')
    Product_desc = models.CharField(max_length=256, null=True, blank=True, verbose_name ='商品简介')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    product_stock = models.IntegerField(default=1, verbose_name='商品库存')
    product_sales = models.IntegerField(default=0, verbose_name='商品销量')
    product_is_putaway = models.BooleanField(default=False, verbose_name='是否发布商品中心')
    create_user = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='createUser',verbose_name='创建管理员')
    product_classify = models.ForeignKey('ProductClassify',on_delete=models.CASCADE,related_name='classify',null=True,blank=True)
    # product_create_time = 
    class Meta:
        db_table = 'products' 
        verbose_name = '商品'

    def __str__(self):
        return self.product_name
    
class ProductImages(BaseModel):
    '''商品图片'''
    image_url = models.ImageField(upload_to=get_image_path, blank=True, verbose_name='图片路由')
    product = models.ForeignKey('Product', related_name='productImages', on_delete=models.CASCADE, verbose_name='商品')
    class Meta:
        db_table ='product_images'
        verbose_name = '商品图片'

    def __str__(self):
        return self.product.product_name
    
class ProductClassify(BaseModel):
    '''商品分类'''
    name = models.CharField(max_length=20,verbose_name='商品分类名称',unique=True)
    # classify = models.CharField(max_length=20,verbose_name='商品分类',null=True,blank=True,unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parentClassify', null=True,blank=True,verbose_name = '商品上级分类')
    class Meta:
        db_table = 'product_classify'
        verbose_name = '商品分类'

    def __str__(self):
        return self.name
    

