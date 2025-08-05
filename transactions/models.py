from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator
from django.contrib.auth .models import User

class Categories(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name}'


class Transactions(models.Model):
    class TransactionType(models.TextChoices):
        INCOMNIG = "I", "Incoming"
        OUTGOING = "O", "Outgoing"

    transaction_type = models.CharField(
        max_length = 2,
        choices = TransactionType
    )

    transaction_timestamp = models.DateTimeField(default = datetime.now)
    created_at = models.DateTimeField(auto_now_add = True)

    amount  = models.DecimalField(
    max_digits = 10,
    decimal_places = 2,
    validators=[MinValueValidator(0.00)],
    default = 0.00
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE)

    category = models.ForeignKey(Categories, on_delete = models.SET_NULL, null = True)

class Balance(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)

    amount  = models.DecimalField(
    max_digits = 10,
    decimal_places = 2,
    default = 0.00
    )

class Budget(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)

    month_year = models.CharField(max_length = 6)

    amount  = models.DecimalField(
    max_digits = 10,
    decimal_places = 2,
    default = 0.00
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'month_year'],
                name = 'user_month_year'
            )
        ]