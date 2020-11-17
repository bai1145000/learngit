from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ColectViews
app_name = 'collect'

router = DefaultRouter()
router.register('coll', ColectViews, basename='collect')

urlpatterns = [
    path('',include(router.urls))
]