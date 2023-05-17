from django import forms
from apps.carteira.models import Carteira


class CarteiraBaixa(forms.ModelForm):
    categoria = forms.CharField(required=True, )
    class Meta:
        model = Carteira
        exclude = ['user', 'data']
