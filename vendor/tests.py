from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class VendorModelTestCase(TestCase):
    def setUp(self):
        # Creating a Vendor for testing
        self.vendor = Vendor.objects.create(
            name='Vendor 1',
            contact_details='Contact info 1',
            address='Address 1',
            vendor_code='VC001',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=24.5,
            fulfillment_rate=90.0
        )

    def test_vendor_creation(self):
        # Testing Vendor creation
        vendor = Vendor.objects.get(vendor_code='VC001')
        self.assertEqual(vendor.name, 'Vendor 1')

class VendorEndpointTestCase(TestCase):
    def setUp(self):
        # Setting up the test client and user
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # Creating a Vendor for endpoint testing
        self.vendor = Vendor.objects.create(
            name='Vendor 1',
            contact_details='Contact info 1',
            address='Address 1',
            vendor_code='VC001',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=24.5,
            fulfillment_rate=90.0
        )

    def test_get_vendor(self):
        # Testing GET request for Vendor details
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        # Testing POST request to create a new Vendor
        url = reverse('vendor-list')  
        data = {
            'name': 'New Vendor',
            'contact_details': 'Contact info',
            'address': 'New Address',
            'vendor_code': 'VC002',
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
