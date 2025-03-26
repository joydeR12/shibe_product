from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



admin.site.register(Product)
admin.site.register(Debtor)

# Create an inline for DebitorProduct
class DebitorProductInline(admin.TabularInline):  # Use StackedInline for a different layout
    model = DebitorProduct
    extra = 1  # Number of empty forms to display for new entries
    fields = ['product', 'quantity', 'is_ordered']  # Fields to show in admin panel

# Register DebitorOrder with the inline
@admin.register(DebitorOrder)
class DebitorOrderAdmin(admin.ModelAdmin):
    list_display = ['debitor', 'status', 'total_price', 'debt_paid', 'debt_pending', 'date_created']
    inlines = [DebitorProductInline]  # Link the inline to DebitorOrder

