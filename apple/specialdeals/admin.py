from django.contrib import admin

# Register your models here.

from .models import ModelLine
from .models import Product
from .models import Offer

class ModelLineAdmin(admin.ModelAdmin):
    fields = ['name', 'url']
    list_display = ('name', 'url')

class ProductAdmin(admin.ModelAdmin):
    fields = ['model_line',
              'product_id',
              'model_year',
              'size','cpu',
              'ram', 'disk',
              'other','url',
              ]
    list_display = ['product_id','model_line','size','cpu','ram','disk']

class OfferAdmin(admin.ModelAdmin):
    fields = ['product', 'start', 'end', 'price', 'sold']
    list_display = ['product','start','end','price', 'sold']

admin.site.register(ModelLine, ModelLineAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Offer,OfferAdmin)
