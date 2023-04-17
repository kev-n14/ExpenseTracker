from django.forms import ModelForm
from .models import Expenses
from django import forms

# create an form for expense model
class ExpenseForm(ModelForm):
    class Meta:
        model = Expenses # model to be used is 'Expenses' model
        fields = ('name', 'amount', 'category')# fields to be accept from user

