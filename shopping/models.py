from django.db import models
from django.contrib import admin
from learning.models import Inscrit, Document
from mlgsite.settings import AUTH_USER_MODEL
from django.utils import timezone


# With class Document as product already exists


class Order(models.Model):
  shopper = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
  quantity = models.IntegerField(default=1)
  ordered = models.BooleanField(default=False)
  unit_price = models.FloatField(default=0.0)
  order_cost = models.FloatField(default=0.0)
  ordered_date = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return self.document.title+"("+str(self.quantity)+")"

  def save(self, *args, **kwargs):
    if (self.order_cost==0.0 and self.unit_price==0.0):
      self.unit_price = (self.document.price)
      self.order_cost = (self.document.price) * (self.quantity)

    else:
      self.order_cost = (self.document.price) * (self.quantity)
    super().save(*args, **kwargs)



class OrderAdmin(admin.ModelAdmin):
  list_display = ('id', 'quantity', 'document', 'unit_price', 'ordered_date' )



class Cart(models.Model):
  shopper = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  orders = models.ManyToManyField(Order)



  def __str__(self):
    return "Panier de "+self.shopper.username


  def delete(self, *args, **kwargs):
    #if cart := request.user.cart:
    orders = self.orders.all()
    for order in orders:
      order.ordered = True
      order.ordered_date = timezone.now()
      order.save()

    self.orders.clear()

    super().delete(*args, **kwargs)