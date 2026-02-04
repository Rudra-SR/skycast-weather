from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class WeatherAssistantTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    @patch('requests.get')
    def test_packing_assistant_hot(self, mock_get):
        """Verify that the packing assistant suggests sunscreen in hot weather."""
        mock_get.return_value.json.return_value = {
            'cod': 200, 'name': 'Mumbai', 'main': {'temp': 35, 'humidity': 40},
            'weather': [{'description': 'clear sky', 'icon': '01d'}], 'wind': {'speed': 10}
        }
        response = self.client.post(self.url, {'city': 'Mumbai'})
        self.assertContains(response, 'Sunscreen')
        self.assertContains(response, 'Stay hydrated')