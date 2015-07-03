from django.db import models

from django.utils import timezone

# Create your models here.

class ModelLine(models.Model):
    name = models.CharField(null=True,max_length=50)
    url  = models.URLField(null=True,max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    model_line = models.ForeignKey(ModelLine)
    product_id = models.CharField(null=True,max_length=20)
    model_year = models.CharField(null=True,max_length=50)
    size       = models.CharField(null=True,max_length=10)
    cpu        = models.CharField(null=True,max_length=50)
    ram        = models.CharField(null=True,max_length=50)
    disk       = models.CharField(null=True,max_length=50)
    other      = models.CharField(null=True,max_length=100)
    url        = models.URLField(null=True,max_length=200)

    def __str__(self):
        return self.product_id

class Offer(models.Model):
    product    = models.ForeignKey(Product)
    start      = models.DateTimeField(null=True,default=timezone.now())
    end        = models.DateTimeField(null=True)
    price      = models.CharField(null=True,max_length=10)
    sold       = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_id  + "(" + self.product.model_line.name + ")"
