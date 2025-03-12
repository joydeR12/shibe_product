from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


# from core.models import Product,Category,seller,ProductImages
# Register your models here.
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(seller)
admin.site.register(ProductImage)
admin.site.register(Debtor)

# Create groups
admin_group, _ = Group.objects.get_or_create(name='Admin')
manager_group, _ = Group.objects.get_or_create(name='Manager')
viewer_group, _ = Group.objects.get_or_create(name='Viewer')

# Assign permissions to groups (optional)
content_type = ContentType.objects.get_for_model(seller) 
permissions = Permission.objects.filter(content_type=content_type)

admin_group.permissions.set(permissions)  # Admin gets all permissions
manager_group.permissions.set(permissions.filter(codename__in=['add_seller', 'change_seller','view_product', 'add_product','delete_product', 'view_debtor', 'add_debtor', 'delete_debtor']))  # Replace modelname
viewer_group.permissions.set(permissions.filter(codename__in=['view_seller', 'add_product', 'view_product', 'add_debtor' ,'view_debtor',]))
