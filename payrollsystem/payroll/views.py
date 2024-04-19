from rest_framework import permissions, generics

from payroll import models as payroll_models
from payroll import serializers as payroll_serializers


class RideIncomeView(generics.ListCreateAPIView):
    queryset = payroll_models.RideIncome.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return payroll_serializers.RideIncomeListSerializer
        return payroll_serializers.RideIncomeSerializer


class DailyIncomeList(generics.ListAPIView):
    queryset = payroll_models.DailyIncome.objects.all()
    serializer_class = payroll_serializers.DailyIncomeSerializer


class DailyIncomeItem(generics.RetrieveAPIView):
    serializer_class = payroll_serializers.DailyIncomeSerializer
    lookup_field = 'courier_id'

    def get_queryset(self):
        return payroll_models.DailyIncome.objects.filter(courier_id=self.kwargs['courier_id'])
