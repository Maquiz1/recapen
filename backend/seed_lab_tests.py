import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from laboratory.models import LaboratoryCategory, LaboratoryType, LaboratoryTest
from django.utils.text import slugify

data = [
    # Haematology
    ("Haematology", "Haematology", "Full Blood Picture", "0-0", "-", 0),
    ("Haematology", "Haematology", "Blood Grouping and Cross matching", "0-0", "-", 0),
    ("Haematology", "Haematology", "Hb Level By number", "12.5 - 18.0", "g/dl", 0),
    ("Haematology", "Haematology", "Sickling Test", "0-0", "-", 0),
    ("Haematology", "Haematology", "Peripheral Blood Smear", "0-0", "-", 0),
    ("Haematology", "Haematology", "ESR By number", "0-20", "mm/hr", 0),
    ("Haematology", "Haematology", "Sickle", "0-0", "%", 0),
    
    # Serology
    ("Serology", "Serology", "HIV Test", "Positive or Negative", "N/A", 0),
    ("Serology", "Serology", "Syphilis (VDRL/RPR)", "Reactive or Non-Reactive", "N/A", 0),
    ("Serology", "Serology", "Hepatitis B", "Positive or Negative", "N/A", 0),
    ("Serology", "Serology", "Hepatitis C", "0-0", "-", 0),
    ("Serology", "Serology", "Widal Test Ratio", "(1:20, 1:40, 1:80, 1:160, 1:320, 1:640)", "N/A", 0),
    ("Serology", "Serology", "CD4 Count", "500 - 1500", "cell/mm", 0),
    ("Serology", "Serology", "Viral Load", "TND or Number >20", "N/A", 0),
    ("Serology", "Serology", "DBS Testing", "Positive or Negative", "N/A", 0),
    ("Serology", "Serology", "Rheumatoid Factor", "Reactive or Non-Reactive", "N/A", 0),
    ("Serology", "Serology", "Cryptococcus Ag Test", "Reactive or Non-Reactive", "N/A", 0),
    ("Serology", "Serology", "H.pylori test", "Positive or Negative", "N/A", 0),
    ("Serology", "Serology", "Brucella Test", "Reactive or Non-Reactive", "N/A", 0),
    ("Serology", "Serology", "Covid-19", "Positive or Negative", "N/A", 0),
    
    # Parasitology
    ("Parasitology", "Parasitology", "MRDT", "Positive or Negative", "N/A", 0),
    ("Parasitology", "Parasitology", "B/S", "Mps or Number of parasite count", "N/A", 0),
    ("Parasitology", "Parasitology", "Urine sediments", "NIL or any abnormality seen", "N/A", 0),
    ("Parasitology", "Parasitology", "Urinalysis", "0-0", "-", 0),
    ("Parasitology", "Parasitology", "Stool analysis", "NIL or any abnormality seen", "N/A", 0),
    
    # Clinical Chemistry
    ("Clinical Chemistry", "Renal Function Test", "Creatinine", "0-0", "-", 0),
    ("Clinical Chemistry", "Renal Function Test", "Urea", "0-0", "-", 0),
    ("Clinical Chemistry", "Renal Function Test", "Uric acid", "0-0", "-", 0),
    
    ("Clinical Chemistry", "Liver Function Test", "ALAT", "0-0", "-", 0),
    ("Clinical Chemistry", "Liver Function Test", "ASAT", "0-0", "-", 0),
    ("Clinical Chemistry", "Liver Function Test", "Bilirubin Total", "0-0", "-", 0),
    ("Clinical Chemistry", "Liver Function Test", "Protein", "0-0", "-", 0),
    ("Clinical Chemistry", "Liver Function Test", "Albumin", "0-0", "-", 0),
    
    ("Clinical Chemistry", "Thyroid Function Test", "TSH (Thyroid Stimulating Hormone)", "0-0", "-", 0),
    ("Clinical Chemistry", "Thyroid Function Test", "T3 (Triiodo Thyronine)", "0-0", "-", 0),
    ("Clinical Chemistry", "Thyroid Function Test", "T4 (Thyroxine)", "0-0", "-", 0),
    
    ("Clinical Chemistry", "Metabolic/Electrolytes", "Calcium", "0-0", "-", 0),
    ("Clinical Chemistry", "Metabolic/Electrolytes", "Chloride", "0-0", "-", 0),
    ("Clinical Chemistry", "Metabolic/Electrolytes", "Mg", "0-0", "-", 0),
    ("Clinical Chemistry", "Metabolic/Electrolytes", "Zn", "0-0", "-", 0),
    
    ("Clinical Chemistry", "Lipid Panel/Cardiac", "Cholesterol", "0-0", "-", 0),
    ("Clinical Chemistry", "Lipid Panel/Cardiac", "LDL (Low Density Lipoprotein)", "0-0", "-", 0),
    ("Clinical Chemistry", "Lipid Panel/Cardiac", "HDL (High Density)", "0-0", "-", 0),
    ("Clinical Chemistry", "Lipid Panel/Cardiac", "Lipoprotein(a)", "0-0", "-", 0),
    
    ("Clinical Chemistry", "Diabetes", "RBS", "0-0", "-", 0),
    ("Clinical Chemistry", "Diabetes", "FBS", "0-0", "-", 0),
    ("Clinical Chemistry", "Diabetes", "HbA1c", "0 - 6.5%", "-", 0),
    ("Clinical Chemistry", "Diabetes", "C-Peptide", "0.5 - 2.0", "ng/ml", 0),
    
    ("Clinical Chemistry", "Tumor Marker", "PSA", "0-0", "-", 0),
    
    ("Clinical Chemistry", "Fertility", "LH (Luteinizing Hormone)", "0-0", "-", 0),
    ("Clinical Chemistry", "Fertility", "FSH (Follicle Stimulating Hormone)", "0-0", "-", 0),
    
    # Microbiology
    ("Microbiology", "Microbiology", "ZN Stain for AFB & Leprosy", "AFB seen by counting +, ++, +++", "N/A", 0),
    ("Microbiology", "Microbiology", "Auramine O Stain for", "AFB seen by counting +, ++, +++", "0-0", 0),
    ("Microbiology", "Microbiology", "Modified Zn Stain for AFB", "0-0", "-", 0),
    ("Microbiology", "Microbiology", "Xpert MTB/RIF", "MTB DETECTED or NOT DETECTED", "0-0", 0),
    
    # Bacteriology
    ("Bacteriology", "Bacteriology", "Gram Stain", "Identification of Gram Positive or Gram Negative", "N/A", 0),
    ("Bacteriology", "Bacteriology", "Blood for C/S", "No Growth or Identification of bacteria + DST", "N/A", 0),
    ("Bacteriology", "Bacteriology", "Urine for C/S", "No Growth or Identification of bacteria + DST", "0-0", 0),
    ("Bacteriology", "Bacteriology", "Body fluid culture", "No Growth or Identification of bacteria + DST", "N/A", 0),
    ("Bacteriology", "Bacteriology", "Pus swab culture", "No Growth or Identification of bacteria + DST", "N/A", 0),
    ("Bacteriology", "Bacteriology", "HVS for C/S", "No Growth or Identification of bacteria + DST", "N/A", 0),
    ("Bacteriology", "Bacteriology", "Skin scraping", "0-0", "-", 0),
    ("Bacteriology", "Bacteriology", "Seminal analysis", "No Growth or Identification of bacteria + DST", "N/A", 0),
]

for cat_name, sub_name, test_name, ref_range, units, cost in data:
    cat, _ = LaboratoryCategory.objects.get_or_create(name=cat_name)
    sub, _ = LaboratoryType.objects.get_or_create(name=sub_name)
    
    slug = slugify(test_name)
    # create or update
    test, created = LaboratoryTest.objects.get_or_create(name=test_name, defaults={
        'code': slug,
        
        'laboratory_category': cat,
        'laboratory_type': sub,
        'reference_range': ref_range,
        'units': units,
        'cost': cost
    })
    if not created:
        test.laboratory_category = cat
        test.laboratory_type = sub
        test.reference_range = ref_range
        test.units = units
        test.cost = cost
        if not test.code:
            test.code = slug
        test.save()

print(f"Successfully seeded {len(data)} tests!")
