from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from payroll import models as payroll_models

class DailyIncomeListTestCase(APITestCase):

    def setUp(self):
        self.courier_id = 1
        self.courier_username = 'admin'
        self.date = '2024-01-01'
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_staff=True)

    def test_get_daily_income_item(self):
        self.client.force_authenticate(self.admin_user)

        ride_income_url = reverse('ride-income')
        list_of_ride_income_data = [
            {'courier': 1, 'income': 100, 'type': 2, 'date': '2024-01-01'},
            {'courier': 1, 'income': 500, 'type': 1, 'date': '2024-01-01'},
            {'courier': 1, 'income': -200, 'type': 3, 'date': '2024-01-01'},
            {'courier': 2, 'income': 150, 'type': 1, 'date': '2024-01-01'}
        ]

        for data in list_of_ride_income_data:
            self.client.post(ride_income_url, data, format='json')


        daily_income_url = reverse('daily-income-item', kwargs={'courier_id': self.courier_id})
        daily_income_url += f'?date={self.date}'  # Add date query parameter to the URL
        response = self.client.get(daily_income_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['courier']['username'], self.courier_username)
        self.assertEqual(response.data['income'], 400)
        self.assertEqual(response.data['date'], self.date)
        self.assertEqual(
            payroll_models.DailyIncome.objects.filter(date=self.date, courier_id=self.courier_id).count(), 1
        )



