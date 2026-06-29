from django import forms
from .models import CoffeeProduct


class ProductForm(forms.ModelForm):

    class Meta:

        model = CoffeeProduct

        fields = "__all__"