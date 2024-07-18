from django.db import models
from decimal import Decimal

# Create your models here.
class Account(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def transfer(self, amount: Decimal, to_account):
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        to_account.balance += amount
        self.save()
        to_account.save()