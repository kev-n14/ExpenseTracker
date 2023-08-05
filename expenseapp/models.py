from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account

class Expense(models.Model):
    expense_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.expense_id



class Expenses(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
