from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auths/', include('user.urls', namespace='user')), 
    path('api/v1/product/', include('product.urls', namespace='product')),
    path('api/v1/collection/',include('collect.urls', namespace='collect')),
    path('', include('rest_framework.urls')),
    path('api/v1/trade/', include('trade.urls', namespace= 'trade'))
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)