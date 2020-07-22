from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('home/', views.home, name='home'),
    path('category/<slug:category_slug>', views.product_list, name='product_list_category'),
    path('<slug:product_slug>', views.product_detail, name='product_detail'),
]
