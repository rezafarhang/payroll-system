import celery
from datetime import date, timedelta

from django.db import transaction
from django.db.models import Sum

from payroll import models as payroll_models
from payroll.utils import DateDataManager


@celery.shared_task()
def calculate_weekly_incomes(courier_ids):

    closest_specific_date = DateDataManager.get_closest_specific_date(date.today())
    weekly_incomes = []
    for courier_id in courier_ids:
        weekly_income = payroll_models.DailyIncomes.objects.filter(
            courier_id=courier_id,
            date__gte=closest_specific_date,
            date__lte=closest_specific_date + timedelta(days=7)
        ).aggregate(Sum('income'))['income__sum']

        weekly_income = payroll_models.WeeklyIncomes(
            courier_id=courier_id,
            start_date=closest_specific_date,
            end_date=closest_specific_date + timedelta(days=7),
            income=weekly_income
        )
        weekly_incomes.append(weekly_income)

    with transaction.atomic():
        payroll_models.WeeklyIncomes.objects.bulk_create(weekly_incomes)

    return weekly_incomes

