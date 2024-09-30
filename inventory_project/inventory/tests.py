# inventory/tests.py

from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient, force_authenticate
from .models import Item
from .views import create_item, read_item, update_item, delete_item

class ApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='Adil',
            password='Adil@111'
        )
        self.token = Token.objects.create(user=self.user)
        print(f"Token created: {self.token.key}") 

        # Force authenticate the client with the user and token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Creating an initial item for testing purposes
        self.item = Item.objects.create(name='Test Item', description='Test Description', quantity=10)
        print(f"Initial item created: {self.item.name}")  

    def test_create_item(self):
        """Test creating a new item."""
        item_data = {
            'name': 'New Item',
            'description': 'New Description',
            'quantity': 5,
            'price': 15.00
        }
        response = self.client.post('/items/', item_data, format='json')
        print(f"Create response: {response.status_code}, {response.data}")  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2) 
        self.assertEqual(Item.objects.last().name, 'New Item')

    def test_read_item(self):
        """Test retrieving an item."""
        response = self.client.get(f'/items/{self.item.id}/', format='json')
        print(f"Read response: {response.status_code}, {response.data}")  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)
        self.assertEqual(response.data['description'], self.item.description)
        self.assertEqual(response.data['quantity'], self.item.quantity)

    def test_update_item(self):
        """Test updating an item."""
        update_data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'quantity': 20,
            'price': 25.00
        }
        response = self.client.put(f'/items/{self.item.id}/update/', update_data, format='json')
        print(f"Update response: {response.status_code}, {response.data}")  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

       
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')
        self.assertEqual(self.item.description, 'Updated Description')
        self.assertEqual(self.item.quantity, 20)
        self.assertEqual(self.item.price, 25.00)

    def test_delete_item(self):
        """Test deleting an item."""
        response = self.client.delete(f'/items/{self.item.id}/delete/', format='json')
        print(f"Delete response: {response.status_code}, {response.data}") 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)  
