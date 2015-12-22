from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from kas.models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ('user', 'date', 'valid')
