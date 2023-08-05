from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account


class Expenses(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
