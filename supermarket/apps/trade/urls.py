from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ShoppingCartViews
app_name = ' '

router = DefaultRouter()
router.register('shoppingcart',ShoppingCartViews,  basename ='shoppingcart')

urlpatterns = [ 
    path('',include(router.urls), name ='trade'),
]