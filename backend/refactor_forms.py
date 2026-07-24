import os

base = '/home/maquiz/Documents/FINAL_PROJECTS/recapen/backend/laboratory'
os.makedirs(os.path.join(base, 'forms'), exist_ok=True)

# Read forms
with open(os.path.join(base, 'forms.py'), 'r') as f:
    forms_content = f.read()

with open(os.path.join(base, 'forms_order.py'), 'r') as f:
    forms_order_content = f.read()

# Write to forms directory
with open(os.path.join(base, 'forms', 'tests.py'), 'w') as f:
    f.write(forms_content)

with open(os.path.join(base, 'forms', 'orders.py'), 'w') as f:
    f.write(forms_order_content)

with open(os.path.join(base, 'forms', '__init__.py'), 'w') as f:
    f.write('from .tests import *\n')
    f.write('from .orders import *\n')

# Clean up
os.remove(os.path.join(base, 'forms.py'))
os.remove(os.path.join(base, 'forms_order.py'))

print("Forms refactored successfully")
