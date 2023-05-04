from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'shop'

urlpatterns = [
    
    path('fill-database/', views.fill_database, name='fill_database'),
    path('', TemplateView.as_view(template_name='shop/shop.html'), name='shop'),
    path('cart_view/',  TemplateView.as_view(template_name='shop/cart.html'), name='cart_view'),
    path('detail/<int:pk>/',  TemplateView.as_view(template_name='shop/shop-details.html'), name='shop_detail')
]

