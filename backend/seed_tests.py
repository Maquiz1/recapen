import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from diagnostics.models import DiagnosticGroup, DiagnosticCategory, DiagnosticTest
from departments.models import Department

def seed_tests():
    lab_dept, _ = Department.objects.get_or_create(name='laboratory')
    rad_dept, _ = Department.objects.get_or_create(name='radiology')
    card_dept, _ = Department.objects.get_or_create(name='cardiology')

    # (department_obj, group_name, category_name, test_name, range_min, range_max, units, cost)
    data = [
        # Haematology
        (lab_dept, "Haematology", "Haematology", "Full Blood Picture", "0", "0", "-", 0),
        (lab_dept, "Haematology", "Haematology", "Blood Grouping and Cross matching", "0", "0", "-", 0),
        (lab_dept, "Haematology", "Haematology", "Hb Level By number", "12.5", "18.0", "g/dl", 0),
        (lab_dept, "Haematology", "Haematology", "Sickling Test", "0", "0", "-", 0),
        (lab_dept, "Haematology", "Haematology", "Peripheral Blood Smear", "0", "0", "-", 0),
        (lab_dept, "Haematology", "Haematology", "ESR By number", "0", "20", "mm/hr", 0),
        (lab_dept, "Haematology", "Haematology", "Sickle", "0", "0", "%", 0),
        
        # Serology
        (lab_dept, "Serology", "Serology", "HIV Test", "Positive", "Negative", "N/A", 0),
        (lab_dept, "Serology", "Serology", "Syphilis (VDRL/RPR)", "Reactive", "Non-Reactive", "N/A", 0),
        (lab_dept, "Serology", "Serology", "Hepatitis B", "Positive", "Negative", "N/A", 0),
        (lab_dept, "Serology", "Serology", "Hepatitis C", "0", "0", "-", 0),
        (lab_dept, "Serology", "Serology", "Widal Test Ratio", "(1:20)", "(1:640)", "N/A", 0),
        (lab_dept, "Serology", "Serology", "CD4 Count", "500", "1500", "cell/mm", 0),
        (lab_dept, "Serology", "Serology", "Viral Load", "TND", ">20", "N/A", 0),
        (lab_dept, "Serology", "Serology", "DBS Testing", "Positive", "Negative", "N/A", 0),
        (lab_dept, "Serology", "Serology", "Rheumatoid Factor", "Reactive", "Non-Reactive", "N/A", 0),
        (lab_dept, "Serology", "Serology", "Cryptococcus Ag Test", "Reactive", "Non-Reactive", "N/A", 0),
        (lab_dept, "Serology", "Serology", "H.pylori test", "Positive", "Negative", "N/A", 0),
        (lab_dept, "Serology", "Serology", "Brucella Test", "Reactive", "Non-Reactive", "N/A", 0),
        (lab_dept, "Serology", "Serology", "Covid-19", "Positive", "Negative", "N/A", 0),
        
        # Parasitology
        (lab_dept, "Parasitology", "Parasitology", "MRDT", "Positive", "Negative", "N/A", 0),
        (lab_dept, "Parasitology", "Parasitology", "B/S", "Mps", "Number of parasite count", "N/A", 0),
        (lab_dept, "Parasitology", "Parasitology", "Urine sediments", "NIL", "abnormality seen", "N/A", 0),
        (lab_dept, "Parasitology", "Parasitology", "Urinalysis", "0", "0", "-", 0),
        (lab_dept, "Parasitology", "Parasitology", "Stool analysis", "NIL", "abnormality seen", "N/A", 0),
        
        # Clinical Chemistry
        (lab_dept, "Clinical Chemistry", "Renal Function Test", "Creatinine", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Renal Function Test", "Urea", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Renal Function Test", "Uric acid", "0", "0", "-", 0),
        
        (lab_dept, "Clinical Chemistry", "Liver Function Test", "ALAT", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Liver Function Test", "ASAT", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Liver Function Test", "Bilirubin Total", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Liver Function Test", "Protein", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Liver Function Test", "Albumin", "0", "0", "-", 0),
        
        (lab_dept, "Clinical Chemistry", "Thyroid Function Test", "TSH (Thyroid Stimulating Hormone)", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Thyroid Function Test", "T3 (Triiodo Thyronine)", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Thyroid Function Test", "T4 (Thyroxine)", "0", "0", "-", 0),
        
        (lab_dept, "Clinical Chemistry", "Metabolic/Electrolytes", "Calcium", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Metabolic/Electrolytes", "Chloride", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Metabolic/Electrolytes", "Mg", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Metabolic/Electrolytes", "Zn", "0", "0", "-", 0),
        
        (lab_dept, "Clinical Chemistry", "Lipid Panel/Cardiac", "Cholesterol", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Lipid Panel/Cardiac", "LDL (Low Density Lipoprotein)", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Lipid Panel/Cardiac", "HDL (High Density)", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Lipid Panel/Cardiac", "Lipoprotein(a)", "0", "0", "-", 0),
        
        (lab_dept, "Clinical Chemistry", "Diabetes", "RBS", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Diabetes", "FBS", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Diabetes", "HbA1c", "0", "6.5%", "-", 0),
        (lab_dept, "Clinical Chemistry", "Diabetes", "C-Peptide", "0.5", "2.0", "ng/ml", 0),
        
        (lab_dept, "Clinical Chemistry", "Tumor Marker", "PSA", "0", "0", "-", 0),
        
        (lab_dept, "Clinical Chemistry", "Fertility", "LH (Luteinizing Hormone)", "0", "0", "-", 0),
        (lab_dept, "Clinical Chemistry", "Fertility", "FSH (Follicle Stimulating Hormone)", "0", "0", "-", 0),
        
        # Microbiology
        (lab_dept, "Microbiology", "Microbiology", "ZN Stain for AFB & Leprosy", "AFB seen", "N/A", "N/A", 0),
        (lab_dept, "Microbiology", "Microbiology", "Auramine O Stain for", "AFB seen", "0", "0", 0),
        (lab_dept, "Microbiology", "Microbiology", "Modified Zn Stain for AFB", "0", "0", "-", 0),
        (lab_dept, "Microbiology", "Microbiology", "Xpert MTB/RIF", "DETECTED", "NOT DETECTED", "0", 0),
        
        # Bacteriology
        (lab_dept, "Bacteriology", "Bacteriology", "Gram Stain", "Positive", "Negative", "N/A", 0),
        (lab_dept, "Bacteriology", "Bacteriology", "Blood for C/S", "No Growth", "Identification", "N/A", 0),
        (lab_dept, "Bacteriology", "Bacteriology", "Urine for C/S", "No Growth", "Identification", "0", 0),
        (lab_dept, "Bacteriology", "Bacteriology", "Body fluid culture", "No Growth", "Identification", "N/A", 0),
        (lab_dept, "Bacteriology", "Bacteriology", "Pus swab culture", "No Growth", "Identification", "N/A", 0),
        (lab_dept, "Bacteriology", "Bacteriology", "HVS for C/S", "No Growth", "Identification", "N/A", 0),
        (lab_dept, "Bacteriology", "Bacteriology", "Skin scraping", "0", "0", "-", 0),
        (lab_dept, "Bacteriology", "Bacteriology", "Seminal analysis", "No Growth", "Identification", "N/A", 0),
    ]

    rad_investigations = {
        "X-ray": [
            "Chest X-ray", "Abdomen X-ray", "Skull X-ray", "Cervical Spine X-ray", 
            "Thoracic Spine X-ray", "Lumbar Spine X-ray", "Pelvis X-ray", "Hip X-ray", 
            "Shoulder X-ray", "Humerus X-ray", "Elbow X-ray", "Forearm X-ray", 
            "Wrist X-ray", "Hand X-ray", "Femur X-ray", "Knee X-ray", 
            "Tibia/Fibula X-ray", "Ankle X-ray", "Foot X-ray"
        ],
        "Ultrasound (USS)": [
            "Abdominal Ultrasound", "Pelvic Ultrasound", "Obstetric Ultrasound", 
            "Renal Ultrasound", "Hepatobiliary Ultrasound", "Thyroid Ultrasound", 
            "Breast Ultrasound", "Scrotal Ultrasound", "Soft Tissue Ultrasound", 
            "Doppler Ultrasound (Arterial)", "Doppler Ultrasound (Venous)", 
            "Carotid Doppler", "Echocardiography (if managed under imaging)"
        ],
        "Computed Tomography (CT)": [
            "CT Brain", "CT Head", "CT Chest", "CT Abdomen", "CT Pelvis", 
            "CT Abdomen & Pelvis", "CT Cervical Spine", "CT Thorax", 
            "CT Angiography (CTA)", "CT Pulmonary Angiography (CTPA)", 
            "CT Coronary Angiography", "CT Urogram"
        ],
        "Magnetic Resonance Imaging (MRI)": [
            "MRI Brain", "MRI Spine", "MRI Cervical Spine", "MRI Lumbar Spine", 
            "MRI Knee", "MRI Shoulder", "MRI Hip", "MRI Abdomen", "MRI Pelvis", 
            "MRI Cardiac", "MR Angiography (MRA)"
        ],
        "Fluoroscopy": [
            "Barium Swallow", "Barium Meal", "Barium Enema", 
            "Hysterosalpingography (HSG)", "Micturating Cystourethrogram (MCUG)"
        ],
        "Mammography": [
            "Screening Mammogram", "Diagnostic Mammogram"
        ],
        "Nuclear Medicine": [
            "Bone Scan", "Thyroid Scan", "Renal Scan", "PET-CT"
        ]
    }
    for group, tests in rad_investigations.items():
        for t in tests:
            data.append((rad_dept, group, "General", t, "", "", "", 0))

    card_investigations = {
        "Electrocardiography": [
            "Resting 12-Lead ECG", "Serial ECG", "Rhythm Strip"
        ],
        "Echocardiography": [
            "Transthoracic Echocardiogram (TTE)", "Transesophageal Echocardiogram (TEE)", 
            "Stress Echocardiogram", "Contrast Echocardiogram", "Fetal Echocardiogram"
        ],
        "Cardiac Monitoring": [
            "24-Hour Holter Monitor", "48-Hour Holter Monitor", "72-Hour Holter Monitor", 
            "Event Monitor", "Ambulatory ECG Monitoring"
        ],
        "Stress Testing": [
            "Exercise Stress Test (Treadmill Test)", "Bicycle Stress Test", "Pharmacological Stress Test"
        ],
        "Blood Pressure Monitoring": [
            "24-Hour Ambulatory Blood Pressure Monitoring (ABPM)"
        ],
        "Cardiac Imaging": [
            "Cardiac CT", "CT Coronary Angiography (CTCA)", "Cardiac MRI", "Myocardial Perfusion Scan"
        ],
        "Cardiac Catheterization": [
            "Coronary Angiography", "Left Heart Catheterization", "Right Heart Catheterization"
        ],
        "Vascular Studies": [
            "Carotid Doppler (Cardiology)", "Peripheral Arterial Doppler", "Peripheral Venous Doppler", "Ankle-Brachial Index (ABI)"
        ]
    }
    for group, tests in card_investigations.items():
        for t in tests:
            data.append((card_dept, group, "General", t, "", "", "", 0))

    print("Seeding diagnostic tests...")
    
    for dept_obj, group_name, category_name, test_name, range_min, range_max, units, cost in data:
        group, _ = DiagnosticGroup.objects.get_or_create(
            name=group_name,
            defaults={'department': dept_obj}
        )
        
        category = None
        if category_name and category_name != "General":
            category, _ = DiagnosticCategory.objects.get_or_create(
                group=group,
                name=category_name
            )

        slug = slugify(test_name)
        # Ensure code uniqueness by truncating or modifying
        code = slug[:45]
        counter = 1
        while DiagnosticTest.objects.filter(code=code).exists() and not DiagnosticTest.objects.filter(test_name=test_name).exists():
            code = f"{slug[:40]}-{counter}"
            counter += 1
            
        test, created = DiagnosticTest.objects.get_or_create(
            test_name=test_name,
            defaults={
                'department': dept_obj,
                'diagnostic_group': group,
                'diagnostic_category': category,
                'code': code,
                'range_min': range_min,
                'range_max': range_max,
                'units': units,
                'cost': cost
            }
        )
        if created:
            print(f"Created: {test_name} ({dept_obj.name})")

    print("Finished seeding database!")

if __name__ == '__main__':
    seed_tests()
