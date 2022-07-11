
from . import views
from django.urls import path

urlpatterns = [


    path('cart/', views.cart_view, name='cart'),
    path('cart/delete/', views.delete_cart_view, name='delete-cart'),
    path('document/<str:slug>/add_to_cart', views.add_to_cart_view, name="add-to-cart"),

]