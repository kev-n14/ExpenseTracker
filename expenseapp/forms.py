from django.forms import ModelForm
from .models import Expenses

class ExpenseForm(ModelForm):
    class Meta:
        model = Expenses
        fields = ('name', 'amount', 'category')