from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction

# Create your models here.
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Company Name")
    balance = models.IntegerField(verbose_name="Company Account Balance", validators=[MinValueValidator(0)] )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class Employee(models.Model):
    name = models.CharField(max_length=50, verbose_name="Employee Name")
    surname = models.CharField(max_length=50, verbose_name="Employee Surname")
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + self.surname


class BudgetChoices(models.IntegerChoices):
    LOW = 300, 'Low $300'
    HIGH = 500, 'High $400'


class Card(models.Model):
    BUDGET_CHOICES = (
        (300, 'Low ( $300 )'),
        (500, 'High ( $500 )'),
    )
    employee = models.OneToOneField(Employee, related_name="card", verbose_name="Employee", on_delete=models.CASCADE)
    budget = models.IntegerField(default=BudgetChoices.LOW, choices=BudgetChoices.choices)
    balance = models.IntegerField(verbose_name="Card Balance", default=0, validators=[MinValueValidator(0)] )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            budget_per_day = self.budget / 30
            created_day = datetime.now().day
            ## money is deposited for the remaining days until the end of the month
            self.balance = (31 - created_day) * budget_per_day
        super(Card, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.employee}'s card"

class Restaurant(models.Model):
    name = models.CharField(max_length=50, verbose_name= "Restaurant Name")
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField(verbose_name="Restaurant Balance", default=0, validators=[MinValueValidator(0)] )

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE = (('top-up', 'Top-Up'), ('purchase', 'Purchase'))
    card = models.ForeignKey(Card, related_name="transactions", verbose_name="Card", on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=20, verbose_name="Transaction Type")

    amount = models.IntegerField(verbose_name="Amount", default=0)
    restaurant = models.ForeignKey(Restaurant, related_name="transactions", verbose_name="Restaurant", on_delete=models.CASCADE, null=True, blank=True)
    is_success = models.BooleanField(verbose_name="Was the transaction successful?", default=False)
    status_message = models.CharField(max_length=100, verbose_name="Status Message", default="-Status message goes here-")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            card = self.card
            company = self.card.employee.company
            if self.transaction_type == "top-up":
                if card.budget > company.balance:
                    self.is_success=False
                    self.status_message = "Top-Up failed. I think the company went bankrupt :("
                else:
                    card.balance = card.budget
                    company.balance -= card.budget
                    self.is_success = True
                    self.status_message = "The card is fulled"
            elif self.transaction_type == "purchase":
                if self.amount > card.balance:
                    self.is_success = False
                    self.status_message = "Insufficient balance."
                else:
                    card.balance -= self.amount
                    self.restaurant.balance += self.amount
                    self.is_success = True
                    self.status_message = "Purchase successful."
                    self.restaurant.save()
            card.save()
            company.save()

        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.transaction_type


class Refund(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                restaurant = self.transaction.restaurant
                restaurant.balance -= self.transaction.amount
                self.transaction.card.balance += self.transaction.amount
                restaurant.save()
                self.transaction.card.save()




