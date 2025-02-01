from django.contrib import admin
from .models import *
# from core.models import Product,Category,seller,ProductImages
# Register your models here.
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(seller)
admin.site.register(ProductImage)


