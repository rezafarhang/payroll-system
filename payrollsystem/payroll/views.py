from rest_framework import permissions, generics

from payroll import models as payroll_models
from payroll import serializers as payroll_serializers
from payroll.managers import DateDataManager


class RideIncomeView(generics.ListCreateAPIView):
    queryset = payroll_models.RideIncome.objects.all()
    permission_classes = (permissions.IsAdminUser, )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return payroll_serializers.RideIncomeListSerializer
        return payroll_serializers.RideIncomeSerializer


class DailyIncomeList(generics.ListAPIView):
    queryset = payroll_models.DailyIncome.objects.all()
    serializer_class = payroll_serializers.DailyIncomeSerializer
    permission_classes = (permissions.IsAdminUser, )


class DailyIncomeItem(generics.RetrieveAPIView):
    serializer_class = payroll_serializers.DailyIncomeSerializer
    permission_classes = (permissions.IsAdminUser, )
    lookup_field = 'courier_id'

    def get_queryset(self):
        return payroll_models.DailyIncome.objects.filter(
            courier_id=self.kwargs['courier_id'],
            date=self.request.query_params.get('date')
        )


class WeeklyIncomeList(generics.ListAPIView):
    serializer_class = payroll_serializers.WeeklyIncomeSerializer
    permission_classes = (permissions.IsAdminUser, )


    def __init__(self):
        super(WeeklyIncomeList, self).__init__()
        self.date_manager = DateDataManager()
    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        self.date_manager.validate_date(start_date)
        self.date_manager.validate_date(end_date)
        report_dates = self.date_manager.get_specific_weekdays(start_date, end_date)

        self.date_manager.calculate_weekly_income(report_dates, self.kwargs['courier_id'])

        return payroll_models.WeeklyIncome.objects.filter(
            courier_id=self.kwargs['courier_id'],
            start_date__in=report_dates
        )
