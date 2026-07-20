from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date
from .models import Patient, Screening, Enrollment, Diagnosis

User = get_user_model()

class PatientWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testdoctor', password='password123', role_type='facility')
        
    def test_patient_model_creation(self):
        patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1995, 5, 15),
            gender='male',
            phone_number='1234567890',
            national_id='ID99999',
            created_by=self.user
        )
        self.assertEqual(str(patient), "John Doe")
        self.assertEqual(patient.status, 'registered')
        self.assertEqual(patient.created_by, self.user)
        self.assertFalse(patient.is_deleted)

    def test_patient_list_view(self):
        response = self.client.get(reverse('patients:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/patient_list.html')

    def test_patient_register_view(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1990-10-20',
            'gender': 'female',
            'phone_number': '0987654321',
            'national_id': 'ID88888'
        }
        response = self.client.post(reverse('patients:register'), data)
        self.assertEqual(response.status_code, 302) # Redirects to screening
        
        patient = Patient.objects.get(national_id='ID88888')
        self.assertEqual(patient.status, 'registered')
        
    def test_screening_progression(self):
        patient = Patient.objects.create(
            first_name='Alice',
            last_name='Green',
            date_of_birth=date(1988, 4, 12),
            gender='female',
            national_id='ID77777'
        )
        
        # Test Screening View with ordered tests
        data = {
            'suspect_scd': False,
            'suspect_dm': True,
            'suspect_cardiac': False,
            'order_dm_hba1c': 'on',
            'order_dm_fbg': 'on',
            'screening_notes': 'Suspect diabetes'
        }
        response = self.client.post(reverse('patients:screening', args=[patient.pk]), data)
        self.assertEqual(response.status_code, 302) # Redirects to investigation
        
        patient.refresh_from_db()
        self.assertEqual(patient.status, 'screened')
        
        screening = Screening.objects.get(patient=patient)
        self.assertTrue(screening.suspect_dm)
        self.assertTrue(screening.order_dm_hba1c)
        self.assertFalse(screening.order_dm_c_peptide) # Omitted
        
    def test_investigation_and_diagnosis_flow(self):
        patient = Patient.objects.create(
            first_name='Bob',
            last_name='Blue',
            date_of_birth=date(1985, 2, 22),
            gender='male',
            national_id='ID66666',
            status='screened'
        )
        screening = Screening.objects.create(patient=patient)
        from diseases.models import Disease
        from laboratory.models import LabTest
        screening.suspected_diseases.add(Disease.objects.get(code='DM'))
        screening.ordered_tests.add(LabTest.objects.get(code='hba1c'))
        screening.ordered_tests.add(LabTest.objects.get(code='fbg'))
        
        # Post DM Investigation values for ordered tests
        data = {
            'dm-hba1c': '7.5',
            'dm-fbg': '8.2'
        }
        response = self.client.post(reverse('patients:investigation', args=[patient.pk]), data)
        self.assertEqual(response.status_code, 302) # Redirects to diagnosis
        
        dm_inv = patient.dm_investigation
        self.assertEqual(float(dm_inv.hba1c), 7.5)
        self.assertIsNone(dm_inv.c_peptide) # Not ordered
        
        # Post Diagnosis (Doctor Dx, Confirmed Disease & Eligibility)
        consult_data = {
            'consult-diagnosis': 'Type 2 Diabetes Mellitus',
            'consult-confirmed_dm': 'on',
            'consult-comments': 'Eligible for PEN-Plus cohort program.',
            'enroll-is_eligible': 'on', # Checkbox checked
            'enroll-cohort': 'dm'
        }
        response = self.client.post(reverse('patients:diagnosis', args=[patient.pk]), consult_data)
        self.assertEqual(response.status_code, 302) # Redirects to enrollment
        
        patient.refresh_from_db()
        self.assertEqual(patient.status, 'diagnosed')
        
        consult = Diagnosis.objects.get(patient=patient)
        self.assertTrue(consult.confirmed_dm)
        self.assertFalse(consult.confirmed_scd)
        
        enrollment = Enrollment.objects.get(patient=patient)
        self.assertTrue(enrollment.is_eligible)
        
        # Post Enrollment finalization
        enroll_data = {
            'enroll-cohort': 'dm',
            'enroll-is_eligible': 'on'
        }
        response = self.client.post(reverse('patients:enrollment', args=[patient.pk]), enroll_data)
        self.assertEqual(response.status_code, 302) # Redirects back to patient list
        
        patient.refresh_from_db()
        self.assertEqual(patient.status, 'enrolled')
        self.assertEqual(patient.enrollment.cohort, 'dm')

    def test_cardiac_type_validation_error(self):
        patient = Patient.objects.create(
            first_name='Charlie',
            last_name='Brown',
            date_of_birth=date(1999, 1, 1),
            gender='male',
            national_id='ID55555',
            status='screened'
        )
        screening = Screening.objects.create(patient=patient)
        from diseases.models import Disease
        from laboratory.models import LabTest
        screening.suspected_diseases.add(Disease.objects.get(code='CARDIAC'))
        screening.ordered_tests.add(LabTest.objects.get(code='ecg'))
        
        # Post Cardiac diagnosis confirmation but omit confirmed_cardiac_type
        consult_data = {
            'consult-diagnosis': 'Cardiac problem',
            'consult-confirmed_cardiac': 'on', # Checked confirmed cardiac
            # omitted confirmed_cardiac_type
            'enroll-is_eligible': 'on',
            'enroll-cohort': 'cardiac'
        }
        response = self.client.post(reverse('patients:diagnosis', args=[patient.pk]), consult_data)
        # Should stay on page and fail validation
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'c_form', 'confirmed_cardiac_type', 'Please select a cardiac condition type.')

    def test_patient_profile_view(self):
        patient = Patient.objects.create(
            first_name='David',
            last_name='Grey',
            date_of_birth=date(2000, 3, 3),
            gender='male',
            national_id='ID11111'
        )
        response = self.client.get(reverse('patients:profile', args=[patient.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/patient_profile.html')

    def test_my_patients_view(self):
        response = self.client.get(reverse('patients:my_patients'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/my_patients.html')

    def test_patient_dashboard_view(self):
        patient = Patient.objects.create(
            first_name='Eva',
            last_name='Yellow',
            date_of_birth=date(2001, 4, 4),
            gender='female',
            national_id='ID22222'
        )
        response = self.client.get(reverse('patients:dashboard', args=[patient.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/patient_profile.html')

    def test_patient_edit_view(self):
        patient = Patient.objects.create(
            first_name='Francis',
            last_name='Orange',
            date_of_birth=date(1992, 5, 25),
            gender='male',
            national_id='ID33333'
        )
        # GET edit form
        response = self.client.get(reverse('patients:edit', args=[patient.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patients/patient_edit.html')
        
        # POST edit form changes
        edit_data = {
            'first_name': 'Francis Updated',
            'last_name': 'Orange',
            'date_of_birth': '1992-05-25',
            'gender': 'male',
            'national_id': 'ID33333-updated'
        }
        response = self.client.post(reverse('patients:edit', args=[patient.pk]), edit_data)
        self.assertEqual(response.status_code, 302) # Redirects to list
        
        patient.refresh_from_db()
        self.assertEqual(patient.first_name, 'Francis Updated')
        self.assertEqual(patient.national_id, 'ID33333-updated')

    def test_patient_dashboard_redirect_no_patient(self):
        response = self.client.get(reverse('patients:dashboard_no_pk'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patients:list'))

    def test_patient_dashboard_redirect_with_patient(self):
        patient = Patient.objects.create(
            first_name='George',
            last_name='Purple',
            date_of_birth=date(1996, 6, 6),
            gender='male',
            national_id='ID44444'
        )
        response = self.client.get(reverse('patients:dashboard_no_pk'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('patients:dashboard', args=[patient.pk]))
