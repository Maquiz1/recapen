import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from diseases.models import Disease

def seed_diseases():
    diseases = [
        {'code': 'DM', 'name': 'Diabetes Mellitus', 'description': 'A disease in which the body’s ability to produce or respond to the hormone insulin is impaired.'},
        {'code': 'CARDIAC', 'name': 'Cardiac Disease', 'description': 'General term for heart conditions, including congenital and acquired diseases.'},
        {'code': 'SCD', 'name': 'Sickle Cell Disease', 'description': 'A group of inherited red blood cell disorders.'},
        {'code': 'RHD', 'name': 'Rheumatic Heart Disease', 'description': 'Permanent damage to heart valves caused by rheumatic fever.'},
        {'code': 'EPILEPSY', 'name': 'Epilepsy', 'description': 'A central nervous system (neurological) disorder in which brain activity becomes abnormal, causing seizures.'},
        {'code': 'ASTHMA', 'name': 'Asthma', 'description': 'A condition in which a person\'s airways become inflamed, narrow and swell, and produce extra mucus.'},
        {'code': 'HTN', 'name': 'Hypertension', 'description': 'A condition in which the force of the blood against the artery walls is too high.'},
        {'code': 'HF', 'name': 'Heart Failure', 'description': 'A chronic condition in which the heart doesn\'t pump blood as well as it should.'},
    ]

    for i, item in enumerate(diseases):
        disease, created = Disease.objects.update_or_create(
            code=item['code'],
            defaults={
                'name': item['name'],
                'description': item['description'],
                'order': i + 1
            }
        )
        if created:
            print(f"Created disease: {disease.name} ({disease.code})")
        else:
            print(f"Updated disease: {disease.name} ({disease.code})")

if __name__ == '__main__':
    seed_diseases()
