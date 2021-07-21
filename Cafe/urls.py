from django.conf.urls.static import static
from django.urls import path
from django.views.generic import *

from Cafe_Django import settings
from .views import *

app_name = 'Cafe'
urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('about', About.as_view(), name='about'),
    path('contactus', ContactUs.as_view(), name='contactus'),
    path('menu', Menu.as_view(), name='menu'),
    path('order-list', OrderList.as_view(), name='order-list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
