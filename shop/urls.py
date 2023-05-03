from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('fill-database/', views.fill_database, name='fill_database')
]

