from django.db import transaction
from django.contrib.auth.models import User

from rest_framework import serializers

from payroll import models as payroll_models


class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', )


class RideIncomeListSerializer(serializers.ModelSerializer):
    courier = CourierSerializer()

    class Meta:
        model = payroll_models.RideIncome
        fields = ('courier', 'income', 'type', 'date', )


class RideIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = payroll_models.RideIncome
        fields = ('courier', 'income', 'type', 'date', )

    def validate(self, attrs):
        income, type = attrs.get('income'), attrs.get('type')
        if type == payroll_models.RideIncomeType.DEFICIT:
            if income >= 0:
                raise serializers.ValidationError('deficit income cannot be greater than 0')
        else:
            if income <= 0:
                raise serializers.ValidationError('income cannot be less than 1')

        return attrs
        
    def create(self, validated_data):
        ride_income_instance = super().create(validated_data)
        with transaction.atomic():
            daily_income_instance, created = payroll_models.DailyIncome.objects.get_or_create(
                courier=ride_income_instance.courier,
                date=ride_income_instance.date,
                defaults={
                    'income': ride_income_instance.income
                }
            )
            if not created:
                daily_income_instance.income += ride_income_instance.income
                daily_income_instance.save()

        return ride_income_instance


class DailyIncomeSerializer(serializers.ModelSerializer):
    courier = CourierSerializer()

    class Meta:
        model = payroll_models.DailyIncome
        fields = ('courier', 'income', 'date', )


class WeeklyIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = payroll_models.WeeklyIncome
        fields = ('courier', 'income', 'start_date', 'end_date', )

