from django.conf import settings
from django.db import models


# Create your models here.
class Wallet(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userLimit = models.DecimalField(max_digits=18, decimal_places=2, null=True)


class Card(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    number = models.CharField(max_length=19, unique=True)
    dueDate = models.DateField('due date')
    validThru = models.DateField('valid thru')
    name = models.CharField(max_length=40)
    secureCode = models.CharField(max_length=4)
    creditLimit = models.DecimalField(max_digits=18, decimal_places=2)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)

    def __str__(self):
        return self.number

