from django.test import TestCase, Client
from django.urls import reverse
from .models import LaboratoryTest
from patients.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()

class LaboratoryTests(TestCase):
    def setUp(self):
        # Create a user to avoid auth issues if views require it
        self.user = User.objects.create_user(username='testadmin', password='password')
        
        self.client = Client()
        self.client.login(username='testadmin', password='password')
        
        # We need a patient
        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            gender='M',
            phone_number='123456789'
        )

    def test_create_lab_test(self):
        url = reverse('laboratory:create')
        data = {
            'name': 'New Special Test',
            'code': 'new_special_test',
            
            'is_active': True
        }
        response = self.client.post(url, data)
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        test_exists = LaboratoryTest.objects.filter(code='new_special_test').exists()
        self.assertTrue(test_exists)
        test_obj = LaboratoryTest.objects.get(code='new_special_test')
        self.assertEqual(test_obj.name, 'New Special Test')

    def test_edit_lab_test(self):
        test_obj = LaboratoryTest.objects.create(
            name='Old Name',
            code='old_name',
            
        )
        url = reverse('laboratory:edit', kwargs={'pk': test_obj.pk})
        data = {
            'name': 'Updated Name',
            'code': 'old_name',
            
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        test_obj.refresh_from_db()
        self.assertEqual(test_obj.name, 'Updated Name')
        
    def test_test_edit_redirect_no_tests(self):
        """
        test_edit_redirect view should now redirect 
        to the first available lab test.
        """
        LaboratoryTest.objects.all().delete()
        
        url = reverse('laboratory:edit_no_pk')
        response = self.client.get(url)
        # Should render empty dashboard or warning since no tests exist
        self.assertEqual(response.status_code, 200) 
        
        test_obj = LaboratoryTest.objects.create(
            name='Some Test',
            code='some_test',
            
        )
        response = self.client.get(url)
        # Now it should redirect to that test's edit view
        self.assertEqual(response.status_code, 302)
        first_test = LaboratoryTest.objects.filter(is_active=True).first()
        self.assertEqual(response.url, reverse('laboratory:edit', kwargs={'pk': first_test.pk}))
