from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from learning.models import Document
from shopping.models import Order, Cart


User = get_user_model()




def add_to_cart_view(request, slug):
  shopper = request.user
  product = get_object_or_404(Document, slug=slug)
  cart, _ = Cart.objects.get_or_create(shopper=shopper)

  order, created = Order.objects.get_or_create(shopper=shopper, ordered = False, document=product)

  if created:
    cart.orders.add(order)
    cart.save()
  else:
    #order.quantity += 1
    order.save()

  cart = Cart.objects.get(shopper=request.user)
  return redirect('documents-list')



def cart_view(request):
  cart = request.user.cart
  cost = 0.0
  for order in cart.orders.all():
    cost = cost + order.order_cost

  total_cost = cost

  return render(request, 'shopping/cart.html', {'orders':cart.orders.all, 'total_cost':total_cost, 'cart':cart})


def delete_cart_view(request):
  if cart := request.user.cart:
    cart.delete()

  return redirect('documents-list')