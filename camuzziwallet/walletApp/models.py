from datetime import date

from django.conf import settings
from django.db import models

from decimal import *

from functools import cmp_to_key


# Create your models here.
class Wallet(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userLimit = models.DecimalField(max_digits=18, decimal_places=2, null=True)

    objects = models.Manager()

    def get_cards(self):
        # Return QuerySet for all cards within this wallet
        return Card.objects.filter(wallet=self)

    def add_card(self, number, duedate, validthru, name, securecode, creditlimit, balance):
        # Add a new card to the wallet.
        new_card = Card(wallet=self, number=number, dueDate=duedate, validThru=validthru, name=name,
                        secureCode=securecode, creditLimit=creditlimit, balance=balance)
        new_card.save()

    def rm_card(self, card):
        # Remove a card from the wallet (and from the database), reset userLimit if greater than new max_limit
        card.delete()
        if self.userLimit > self.get_max_limit():
            self.userLimit = None
            self.save()

    def set_user_limit(self, value):
        # Set Wallet userLimit, must be below maxLimit or an exception is raised.
        # If set to "None", maxLimit will be used instead user_limit
        if value and value > self.get_max_limit():
            raise Exception('User limit can not be greater than max limit')
        else:
            self.userLimit = value
            self.save()

    def get_max_limit(self):
        # Sum of all its cards limit
        max_limit = Decimal('0')
        for card in self.get_cards():
            max_limit += card.creditLimit
        return max_limit

    def get_available_credit(self):
        # Return available credit for the wallet, limited to userLimit if defined
        limit = self.userLimit or self.get_max_limit()
        total_balance = self.get_balance()
        return limit - total_balance

    def get_balance(self):
        # Return total balance of the Wallet
        total_balance = Decimal('0')
        for card in self.get_cards():
            total_balance += card.balance
        return total_balance

    def add_purchase(self, value):
        # Add a purchase to the wallet, must choose cards according to specified priorities and split the purchase if
        # no card have sufficient credit limit. If value is greater than user defined limit raise exception
        if value > self.get_available_credit():
            raise Exception('Not possible to add purchase with value greater than user available credit.')

        cards = sorted(self.get_cards(), key=cmp_to_key(Card.compare))
        for card in cards:
            # Iterate over all cards sorted by priority, buy with first that have enough limit
            if value <= card.get_available_credit():
                card.add_purchase(value)
                return

        for card in cards:
            if value <= card.get_available_credit():
                # If remaining value fits on this card available credit, add purchase and return
                card.add_purchase(value)
                return
            else:
                # Add purchase with maximum available credit and continue the loop with remaining value
                available_credit = card.get_available_credit()
                card.add_purchase(available_credit)
                value -= available_credit

        if value > Decimal('0'):
            # The execution shall never reach this point with remaining value.
            raise Exception('There is still remaining value to process but no available credit.')


class Card(models.Model):

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    number = models.CharField(max_length=19, unique=True)
    dueDate = models.DateField('due date')
    validThru = models.DateField('valid thru')
    name = models.CharField(max_length=40)
    secureCode = models.CharField(max_length=4)
    creditLimit = models.DecimalField(max_digits=18, decimal_places=2)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)

    objects = models.Manager()

    def __str__(self):
        return self.number

    def get_available_credit(self):
        # Return available credit for the card
        return self.creditLimit - self.balance

    def add_purchase(self, purchase_value):
        # Add a purchase to the card, if there is not available limit raise exception
        if self.get_available_credit() < purchase_value:
            raise Exception('Not available credit for this purchase.')
        else:
            self.balance += purchase_value
            self.save()

    def release_credit(self, payment_value):
        # Release credit on the card, if payment value is greater than balance, raise exception.
        if payment_value > self.balance:
            raise Exception('Not possible to release more credit than card balance.')
        else:
            self.balance -= payment_value
            self.save()

    @staticmethod
    def compare(card1, card2):
        if card1.dueDate.day == card2.dueDate.day:
            return card1.get_available_credit() - card2.get_available_credit()
        else:
            d1 = card1.dueDate.day - date.today().day \
                if card1.dueDate.day > date.today().day \
                else 31 + date.today().day - card1.dueDate.day
            d2 = card2.dueDate.day - date.today().day \
                if card2.dueDate.day > date.today().day \
                else 31 + date.today().day - card2.dueDate.day
            return d2 - d1

