from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm, CreateUserForm
from .decorators import unauthenicated_user, allowed_users, admin_only
from .models import Expenses
from django.db.models import Sum
import datetime

@unauthenicated_user
def registerPage(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+ user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'expenseapp/register.html', context)

@unauthenicated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            
            return redirect('index')

        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'expenseapp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    expenses = Expenses.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))

    #Logic to calculate 365 days expenses
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

    expense_form = ExpenseForm()
    return render(request, 'expenseapp/index.html', 
    {'expense_form': expense_form, 'expenses': expenses, 'total_expenses': total_expenses,
        'yearly_sum': yearly_sum, 'monthly_sum': monthly_sum, 'weekly_sum': weekly_sum,
        'daily_sums': daily_sums, 'categorical_sums': categorical_sums})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def edit(request, id):
    expense = Expenses.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method == "POST":
        expense = Expenses.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'expenseapp/edit.html', {'expense_form': expense_form})



def delete(request,id):
    if request.method =='POST' and 'delete' in request.POST:
        expense = Expenses.objects.get(id=id)
        expense.delete()
    return redirect('index')
