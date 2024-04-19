from django.urls import path

from payroll import views

urlpatterns = [
    path('api/ride-income/', views.RideIncomeView.as_view(), name='ride-income'),
    path('api/daily-income/', views.DailyIncomeList.as_view(), name='daily-income-list'),
    path('api/daily-income/<int:courier_id>/', views.DailyIncomeItem.as_view(), name='daily-income-item'),
    path('api/weekly-income/<int:courier_id>/', views.WeeklyIncomeList.as_view(), name='weekly-income-item'),

]