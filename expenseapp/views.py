from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ExpenseForm
from .models import Expenses
from django.db.models import Sum
import datetime


def index(request):
    return render(request, 'expenseapp/index.html')

def home(request):
    if request.method == "POST": # when the request is post
        expense = ExpenseForm(request.POST)  # get data from ExpenseForm from post request
        if expense.is_valid(): # check if data is valid
            expense.save() # save data in the database
    expenses = Expenses.objects.all() # to get access to the expenses. alll expense objects from the Expense Model
    total_expenses = expenses.aggregate(Sum('amount')) # take all objects(expenses) together calculate the sum of expenses

    #Logic to calculate 365 days expenses.
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expenses.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

    #Logic to calculate 30 days expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expenses.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

    #Logic to calculate 7 days expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expenses.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sums = Expenses.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))

    categorical_sums = Expenses.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm() # create an instance of ExpenseForm
    return render(request, 'expenseapp/home.html',
    {'expense_form': expense_form, 'expenses': expenses,
        'total_expenses': total_expenses,
        'yearly_sum': yearly_sum, 'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums, 'categorical_sums': categorical_sums, })


def edit(request, id): # to render form to edit a paticular expense.
    expense = Expenses.objects.get(id=id)# store the id of a particular url id expense
    expense_form = ExpenseForm(instance=expense)# pass expence as an instance to form
    if request.method == "POST": # when the request is post
        expense = Expenses.objects.get(id=id)# to get same id as above
        form = ExpenseForm(request.POST, instance=expense) # to store new data that is been passed to form
        if form.is_valid():
            form.save()# save from
            return redirect('home')
    return render(request, 'expenseapp/edit.html',
    {'expense_form': expense_form})


def delete(request, id): # passing in id of item to be deleted
    if request.method == 'POST' and 'delete' in request.POST:
        expense = Expenses.objects.get(id=id)# get the expense id
        expense.delete()# delete that id
    return redirect('home')
