from django.urls import path

from payroll import views

urlpatterns = [
    path('api/ride-income/', views.RideIncomeView.as_view(), name='RideIncome'),
]