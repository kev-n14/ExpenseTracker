from django.forms import ModelForm
from .models import Expenses
from django import forms


class ExpenseForm(ModelForm):
    class Meta:
        model = Expenses
        fields = ('name', 'amount', 'category')

