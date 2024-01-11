from django import forms

from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'cost', 'category')

    
class ProductFilterForm(forms.Form):
    name = forms.CharField(max_length=150, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="All Categories")


class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', required=True)
    expiration_date = forms.DateField(label='Expiration Date', required=True)
    cvc = forms.CharField(label='CVC', required=True)