from django.core.management.base import BaseCommand
from diseases.models import Disease
from laboratory.models import LaboratoryTest
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
            # Comprehensive Chemistry Panel (Available to all)
            {'code': 'na', 'name': 'Sodium (Na)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'k', 'name': 'Potassium (K)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'cl', 'name': 'Chloride (Cl)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'bun', 'name': 'Blood Urea Nitrogen (BUN)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'cre', 'name': 'Creatinine (Cre)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'ca', 'name': 'Calcium (Ca)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'ast', 'name': 'AST', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'alt', 'name': 'ALT', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'alp', 'name': 'ALP', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'tbil', 'name': 'Total Bilirubin', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'bnp', 'name': 'Brain Natriuretic Peptide (BNP)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'inr', 'name': 'International Normalized Ratio (INR)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'chemistry_panel', 'name': 'Comprehensive Chemistry Panel', 'category': 'lab', 'disease': 'ALL', 'is_panel': True},
            # Hematology Parameters
            {'code': 'hb', 'name': 'Hemoglobin (Hb)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'wbc', 'name': 'White Blood Cells (WBC)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'plt', 'name': 'Platelets (PLT)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'hct', 'name': 'Hematocrit (Hct)', 'category': 'lab', 'disease': 'ALL'},
            {'code': 'hematology_panel', 'name': 'Hematology Panel', 'category': 'lab', 'disease': 'ALL', 'is_panel': True},
        ]

        # 4. Seed Radiology & Imaging
        radiology_data = [
            {'code': 'bone_xray', 'name': 'Bone X-Ray', 'category': 'radiology', 'disease': 'ALL'},
            {'code': 'chest_xray', 'name': 'Chest X-Ray', 'category': 'radiology', 'disease': 'ALL'},
            {'code': 'tcd', 'name': 'Transcranial Doppler (TCD)', 'category': 'radiology', 'disease': 'ALL'},
        ]

        # 5. Seed Cardiology Tests
        cardiology_data = [
            {'code': 'ecg', 'name': 'Electrocardiogram (ECG)', 'category': 'cardiology', 'disease': 'ALL'},
            {'code': 'echo', 'name': 'Echocardiogram', 'category': 'cardiology', 'disease': 'ALL'},
        ]

        # Combine all tests
        all_tests = lab_tests_data + radiology_data + cardiology_data

        for t in all_tests:
            try:
                # We use update_or_create to prevent UniqueConstraint errors if name exists
                test, created = LaboratoryTest.objects.update_or_create(
                    code=t['code'],
                    defaults={
                        'name': t['name'], 
                        'category': t['category'],
                        'is_panel': t.get('is_panel', False),
                    }
                )
                # Link disease if created or if we want to ensure it's linked
                if t['disease'] == 'ALL':
                    for d_code, d_obj in disease_objs.items():
                        test.diseases.add(d_obj)
                elif t['disease'] in disease_objs:
                    test.diseases.add(disease_objs[t['disease']])
                    
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created {t['category'].title()} Test: {t['name']}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to create/update {t['name']}: {str(e)}"))

        # 6. Associate Panel Sub-Tests
        try:
            chem_panel = LaboratoryTest.objects.get(code='chemistry_panel')
            subtest_codes = ['na', 'k', 'cl', 'bun', 'cre', 'ca', 'ast', 'alt', 'alp', 'tbil', 'bnp', 'inr']
            for st_code in subtest_codes:
                st = LaboratoryTest.objects.filter(code=st_code).first()
                if st:
                    st.parent_panel = chem_panel
                    st.save()
            self.stdout.write(self.style.SUCCESS("Associated sub-tests to Comprehensive Chemistry Panel."))
        except LaboratoryTest.DoesNotExist:
            pass
            
        try:
            hem_panel = LaboratoryTest.objects.get(code='hematology_panel')
            hem_codes = ['hb', 'wbc', 'plt', 'hct']
            for st_code in hem_codes:
                st = LaboratoryTest.objects.filter(code=st_code).first()
                if st:
                    st.parent_panel = hem_panel
                    st.save()
            self.stdout.write(self.style.SUCCESS("Associated sub-tests to Hematology Panel."))
        except LaboratoryTest.DoesNotExist:
            pass

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
