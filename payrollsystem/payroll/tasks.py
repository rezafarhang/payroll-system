import celery
from datetime import date, timedelta

from django.db import transaction
from django.db.models import Sum

from payroll import models as payroll_models
from payroll.managers import DateDataManager


@celery.shared_task()
def calculate_weekly_incomes(courier_ids):
    manager = DateDataManager()
    closest_specific_date = manager.closest_date_for_calculation(date.today())
    weekly_incomes = payroll_models.DailyIncome.objects.filter(
        courier_id__in=courier_ids,
        date__gte=closest_specific_date,
        date__lte=closest_specific_date + timedelta(days=6)
    ).values('courier_id').annotate(weekly_income=Sum('income'))

    weekly_incomes_list = [
        payroll_models.WeeklyIncome(
            courier_id=item['courier_id'],
            start_date=closest_specific_date,
            end_date=closest_specific_date + timedelta(days=6),
            income=item['weekly_income']
        )
        for item in weekly_incomes
    ]

    with transaction.atomic():
        payroll_models.WeeklyIncome.objects.bulk_create(weekly_incomes_list)

    return weekly_incomes

