from django.contrib import admin

from payroll import models as payroll_models


@admin.register(payroll_models.RideIncome)
class RideIncomeAdmin(admin.ModelAdmin):
    list_display = ['courier', 'income', 'type', 'date']
    list_filter = ['type']
    search_fields = ['courier__username', 'type', 'date']
    date_hierarchy = 'date'


@admin.register(payroll_models.DailyIncome)
class DailyIncomeAdmin(admin.ModelAdmin):
    list_display = ['courier', 'income', 'date']
    search_fields = ['courier__username', 'date']
    date_hierarchy = 'date'
