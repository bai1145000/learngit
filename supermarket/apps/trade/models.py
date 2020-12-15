from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    nums = models.IntegerField("购买数量",default=0)
    add_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")

    class Meta:
        verbose_name = '购物车喵'
        verbose_name_plural = verbose_name
        unique_together = ("user", "products")

    def __str__(self):
        return "%s(%d)".format(self.products.name, self.nums)