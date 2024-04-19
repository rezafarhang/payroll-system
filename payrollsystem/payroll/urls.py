from django.urls import path

from payroll import views

urlpatterns = [
    path('api/ride-income/', views.RideIncomeView.as_view(), name='RideIncome'),
    path('api/daily-income/', views.DailyIncomeList.as_view(), name='DailyIncome'),
    path('api/daily-income/<int:courier_id>/', views.DailyIncomeItem.as_view(), name='dailyincome-item'),

]