from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Expenses
from django import forms


class ExpenseForm(ModelForm):
    class Meta:
        model = Expenses
        fields = ('name', 'amount', 'category')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
