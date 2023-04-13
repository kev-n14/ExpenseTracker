from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm


def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    expense_form = ExpenseForm()
    return render(request, 'expenseapp/index.html', {'expense_form':expense_form})
