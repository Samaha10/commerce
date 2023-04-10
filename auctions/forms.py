from django import forms
from .models import Listing


class ListForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'price', 'image', 'category')
