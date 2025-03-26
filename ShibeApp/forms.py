from django import forms
from .models import Product
from .models import Debtor


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','price']
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Select Product'
        self.fields['price']







class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = [
            'debtor_name',
            'debtor_phone',

        ]

    def __init__(self, *args, **kwargs):
        super(DebtorForm, self).__init__(*args, **kwargs)
        self.fields['debtor_name'].widget.attrs['placeholder'] = 'Debitor Name'
        self.fields['debtor_phone'].widget.attrs['placeholder'] = 'Debtor Phone Number'

    def clean(self):
        cleaned_data = super(DebtorForm, self).clean()
        return cleaned_data
    


    # ShibeApp/forms.py
from django import forms
from .models import Debtor, DebitorProduct, Product

class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = ['debtor_name', 'debtor_phone']
        widgets = {
            'debtor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'debtor_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DebtorProductForm(forms.ModelForm):
    class Meta:
        model = DebitorProduct
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(DebtorProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

class PaymentForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )