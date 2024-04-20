from datetime import datetime, timedelta
from django.utils.dateparse import parse_date

from rest_framework.exceptions import ValidationError


class DateDataManager:

    def get_specific_weekdays(self, start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        specific_weekday_dates = []
        closest_date = self.closest_date_for_calculation(start_date)

        while closest_date <= end_date:
            specific_weekday_dates.append(closest_date)
            closest_date += timedelta(days=7)

        return specific_weekday_dates

    def closest_date_for_calculation(self, date):
        days_since_specific_weekday = date.weekday()
        days_to_subtract = (days_since_specific_weekday + 2) % 7
        return date - timedelta(days=days_to_subtract)

    def validate_date(self, value):
        if not value:
            raise ValidationError('Date parameter is required')
        try:
            date_obj = parse_date(value)
            if date_obj is None:
                raise ValidationError('Invalid date format. Please use YYYY-MM-DD format.')
        except ValueError:
            raise ValidationError('Invalid date value. Please provide a valid date.')

        return value
