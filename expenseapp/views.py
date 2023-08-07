from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ExpenseForm
from .models import Expenses
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import datetime


def index(request):
    return render(request, 'expenseapp/index.html')


@login_required(login_url='signin')
def home(request):
    if request.method == "POST": # when the request is post
        expense = ExpenseForm(request.POST)  # get data from ExpenseForm from post request
        if expense.is_valid():
            new_expense = expense.save(commit=False)
            new_expense.user = request.user 
            messages.success(request, 'Expense Has Been Added')
            new_expense.save() # save data in the database
        else:
            messages.error(request, 'Expense Has Not Been Added')
    user_expenses = Expenses.objects.filter(user=request.user)
    user_expenses = Expenses.objects.filter(user=request.user)
    #expenses = Expenses.objects.all() # to get access to the expenses. alll expense objects from the Expense Model
    
    total_expenses = user_expenses.aggregate(Sum('amount')) # take all objects(expenses) together calculate the sum of expenses

    #Logic to calculate 365 days expenses.
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expenses.objects.filter(date__gt=last_year)
    yearly_sum = user_expenses.filter(date__gt=last_year).aggregate(Sum('amount'))

    #Logic to calculate 30 days expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expenses.objects.filter(date__gt=last_month)
    monthly_sum = user_expenses.filter(date__gt=last_month).aggregate(Sum('amount'))

    #Logic to calculate 7 days expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expenses.objects.filter(date__gt=last_week)
    weekly_sum = user_expenses.filter(date__gt=last_week).aggregate(Sum('amount'))

    daily_sums = user_expenses.values('date').order_by('date').annotate(sum=Sum('amount'))

    categorical_sums = user_expenses.values('category').order_by('category').annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()

    expense_form = ExpenseForm() # create an instance of ExpenseForm
    return render(request, 'expenseapp/home.html',
    {'expense_form': expense_form, 
        'user_expenses': user_expenses,
        'total_expenses': total_expenses,
        'yearly_sum': yearly_sum, 
        'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums, 
        'categorical_sums': categorical_sums, })


@login_required(login_url='signin')
def edit(request, id): # to render form to edit a paticular expense.
    expense = Expenses.objects.get(id=id)# store the id of a particular url id expense
    expense_form = ExpenseForm(instance=expense)# pass expence as an instance to form
    if request.method == "POST": # when the request is post
        expense = Expenses.objects.get(id=id)# to get same id as above
        form = ExpenseForm(request.POST, instance=expense) # to store new data that is been passed to form
        if form.is_valid():
            form.save()# save from
            messages.success(request, 'Expense Has Been Updated')
            return redirect('home')
        else:
            messages.error(request, 'Expense Could Not Be Updated.')
    return render(request, 'expenseapp/edit.html',
    {'expense_form': expense_form})


@login_required(login_url='signin')
def delete(request, id): # passing in id of item to be deleted
    if request.method == 'POST' and 'delete' in request.POST:
        expense = Expenses.objects.get(id=id)# get the expense id
        messages.success(request, 'Expense Has Been Deleted')
        expense.delete()# delete that id
    else:
        messages.error(request, 'Expense Has Not Been Deleted')
    return redirect('home')


def expense_list(request):
    expenses = Expenses.objects.filter(user=request.user)
    return render(request, 'expenseapp/home.html', {'expenses': expenses})