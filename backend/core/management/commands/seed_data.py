from django.core.management.base import BaseCommand
from diseases.models import Disease
from laboratory.models import LabTest
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Seeds initial core data into the database (Diseases, Lab Tests, Radiology, Cardiology, Roles)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data seeding...")

        # 1. Seed Roles (Django Groups)
        roles = [
            'National Coordinator',
            'Regional Coordinator',
            'District Coordinator',
            'Facility Doctor/Nurse',
            'Mentor/Trainer',
            'Principal Investigator',
            'Data Clerk'
        ]
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Role (Group): {role}"))

        # 2. Seed Diseases
        diseases_data = [
            {'code': 'SCD', 'name': 'Sickle Cell Disease', 'description': 'Sickle Cell Disease'},
            {'code': 'DM', 'name': 'Diabetes Mellitus', 'description': 'Diabetes Mellitus'},
            {'code': 'CARDIAC', 'name': 'Cardiac Diseases', 'description': 'Cardiovascular and Heart Diseases'},
        ]
        
        disease_objs = {}
        for d in diseases_data:
            disease, created = Disease.objects.get_or_create(
                code=d['code'],
                defaults={'name': d['name'], 'description': d['description']}
            )
            disease_objs[d['code']] = disease
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Disease: {d['name']}"))

        # 3. Seed Laboratory Tests
        lab_tests_data = [
            {'code': 'hba1c', 'name': 'HbA1c', 'category': 'lab', 'disease': 'DM'},
            {'code': 'c_peptide', 'name': 'C-Peptide', 'category': 'lab', 'disease': 'DM'},
            {'code': 'creatinine', 'name': 'Creatinine', 'category': 'lab', 'disease': 'DM'},
            {'code': 'urea', 'name': 'Urea', 'category': 'lab', 'disease': 'DM'},
            {'code': 'fbg', 'name': 'Fasting Blood Glucose (FBG)', 'category': 'lab', 'disease': 'DM'},
            {'code': 'rbg', 'name': 'Random Blood Glucose (RBG)', 'category': 'lab', 'disease': 'DM'},
            {'code': 'scd_lab', 'name': 'SCD Routine Lab', 'category': 'lab', 'disease': 'SCD'},
            {'code': 'cardiac_lab', 'name': 'Cardiac Enzymes', 'category': 'lab', 'disease': 'CARDIAC'},
        ]

        # 4. Seed Radiology & Imaging
        radiology_data = [
            {'code': 'scd_xray', 'name': 'Bone X-Ray', 'category': 'radiology', 'disease': 'SCD'},
            {'code': 'chest_xray', 'name': 'Chest X-Ray', 'category': 'radiology', 'disease': 'CARDIAC'},
            {'code': 'scd_screening', 'name': 'SCD Screening (TCD)', 'category': 'radiology', 'disease': 'SCD'},
        ]

        # 5. Seed Cardiology Tests
        cardiology_data = [
            {'code': 'ecg', 'name': 'Electrocardiogram (ECG)', 'category': 'cardiology', 'disease': 'CARDIAC'},
            {'code': 'echo', 'name': 'Echocardiogram', 'category': 'cardiology', 'disease': 'CARDIAC'},
            {'code': 'scd_echo', 'name': 'SCD Echocardiogram', 'category': 'cardiology', 'disease': 'SCD'},
        ]

        # Combine all tests
        all_tests = lab_tests_data + radiology_data + cardiology_data

        for t in all_tests:
            test, created = LabTest.objects.get_or_create(
                code=t['code'],
                defaults={'name': t['name'], 'category': t['category']}
            )
            # Link disease if created or if we want to ensure it's linked
            if t['disease'] in disease_objs:
                test.diseases.add(disease_objs[t['disease']])
                
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created {t['category'].title()} Test: {t['name']}"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
