from django.test import TestCase, Client
from django.urls import reverse
from .models import LabTest
from diseases.models import Disease

class LaboratoryWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.disease = Disease.objects.get(code='DM')

    def test_test_list_view(self):
        response = self.client.get(reverse('laboratory:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laboratory/test_list.html')

    def test_test_create_view(self):
        # GET form
        response = self.client.get(reverse('laboratory:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laboratory/test_form.html')
        
        # POST valid form data
        data = {
            'name': 'New Special Lab Test',
            'code': 'new_special_test',
            'category': 'lab',
            'diseases': [self.disease.pk],
            'description': 'Reference range 0-10.',
            'is_active': 'on'
        }
        response = self.client.post(reverse('laboratory:create'), data)
        self.assertEqual(response.status_code, 302) # Redirects to list
        
        test_exists = LabTest.objects.filter(code='new_special_test').exists()
        self.assertTrue(test_exists)
        test_obj = LabTest.objects.get(code='new_special_test')
        self.assertEqual(test_obj.diseases.first(), self.disease)

    def test_test_edit_view(self):
        test_obj = LabTest.objects.create(
            name='Editable Test',
            code='editable_test',
            category='lab'
        )
        # GET edit form
        response = self.client.get(reverse('laboratory:edit', args=[test_obj.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'laboratory/test_form.html')
        
        # POST edit update
        data = {
            'name': 'Editable Test Updated',
            'code': 'editable_test_updated',
            'category': 'lab',
            'diseases': [],
            'description': 'Updated reference.',
            'is_active': 'on'
        }
        response = self.client.post(reverse('laboratory:edit', args=[test_obj.pk]), data)
        self.assertEqual(response.status_code, 302)
        
        test_obj.refresh_from_db()
        self.assertEqual(test_obj.name, 'Editable Test Updated')
        self.assertEqual(test_obj.code, 'editable_test_updated')

    def test_test_edit_redirect_no_tests(self):
        # Delete default seeded tests
        LabTest.objects.all().delete()
        response = self.client.get(reverse('laboratory:edit_no_pk'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('laboratory:list'))

    def test_test_edit_redirect_with_tests(self):
        test_obj = LabTest.objects.create(
            name='First Test',
            code='first_test',
            category='lab'
        )
        response = self.client.get(reverse('laboratory:edit_no_pk'))
        self.assertEqual(response.status_code, 302)
        first_test = LabTest.objects.filter(is_active=True).first()
        self.assertRedirects(response, reverse('laboratory:edit', args=[first_test.pk]))
