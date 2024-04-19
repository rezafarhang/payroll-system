from rest_framework import permissions, generics

from payroll import models as payroll_models
from payroll import serializers as payroll_serializers


class RideIncomeView(generics.ListCreateAPIView):
    queryset = payroll_models.RideIncome.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return payroll_serializers.RideIncomeListSerializer
        return payroll_serializers.RideIncomeSerializer

