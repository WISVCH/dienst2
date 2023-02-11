from django import forms
from django_select2 import forms as s2forms

from post.models import Item


class ContactWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains"]
class CategoryWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains"]
    
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        widgets = {
            "sender": ContactWidget,
            "recipient": ContactWidget,
            "category": CategoryWidget,
        }
