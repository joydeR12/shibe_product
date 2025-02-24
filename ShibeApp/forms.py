from django import forms
from .models import Product
from .models import Debtor
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'image', 'description', 'price','old_price', 'user' ]

class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = '__all__'