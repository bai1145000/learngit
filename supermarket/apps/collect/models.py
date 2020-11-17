from django.db import models
from db.basemodels import BaseModel
from product.models import Product
# Create your models here.

class Collect(models.Model):
    '''收藏模型'''
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE ,related_name = 'collectUser',verbose_name='收藏人')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name ='collectProduct',verbose_name='收藏商品')

    class Meta:
        db_table = 'collect' 
        verbose_name = '收藏'

    def __str__(self):
        return self.user.username
    