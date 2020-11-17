from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductListViews, ProductImagesViews, ProductClassifyViews, ProductCenterViews, SlideshowViews
app_name = 'product'

router = DefaultRouter()
router.register('list', ProductListViews, basename='list')
router.register('image', ProductImagesViews, basename='image')
router.register('classify', ProductClassifyViews, basename='classify')
router.register('center',ProductCenterViews, basename='center')
router.register('slideshow',SlideshowViews, basename='slideshow')


urlpatterns = [ 
    path('',include(router.urls), name ='product'),
]