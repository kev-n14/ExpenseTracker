from django.db import models


class Expenses(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
