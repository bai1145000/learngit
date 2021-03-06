# Generated by Django 3.0.7 on 2020-11-19 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_auto_20201119_0956'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nums', models.IntegerField(default=0, verbose_name='购买数量')),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name='添加时间')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车喵',
                'verbose_name_plural': '购物车喵',
                'unique_together': {('user', 'products')},
            },
        ),
    ]
