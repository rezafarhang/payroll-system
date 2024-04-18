from datetime import date

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class RideIncome(models.Model):
    INCOME_TYPE_CHOICES = (
        (1, 'income'),
        (2, 'deficit'),
        (3, 'increment'),
    )
    courier = models.ForeignKey(User, related_name='ride_incomes', on_delete=models.CASCADE)
    income = models.IntegerField(validators=[MinValueValidator(1)])
    type = models.IntegerField(choices=INCOME_TYPE_CHOICES)
    date = models.DateField(default=date.today())


class DailyIncome(models.Model):
    courier = models.ForeignKey(User, related_name='daily_incomes', on_delete=models.CASCADE)
    income = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField(default=date.today(), unique=True, db_index=True)
