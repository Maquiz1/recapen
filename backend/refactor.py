import os
import shutil

base = '/home/maquiz/Documents/FINAL_PROJECTS/recapen/backend/laboratory'

# Read models
with open(os.path.join(base, 'models.py'), 'r') as f:
    models_content = f.read()

# Write models
with open(os.path.join(base, 'models', 'tests.py'), 'w') as f:
    f.write(models_content)

with open(os.path.join(base, 'models', '__init__.py'), 'w') as f:
    f.write('from .tests import *\n')

os.remove(os.path.join(base, 'models.py'))

# Read views
with open(os.path.join(base, 'views.py'), 'r') as f:
    views_content = f.read()

# Write views
with open(os.path.join(base, 'views', 'tests.py'), 'w') as f:
    f.write(views_content)

with open(os.path.join(base, 'views', '__init__.py'), 'w') as f:
    f.write('from .tests import *\n')

os.remove(os.path.join(base, 'views.py'))

print("Refactor complete")
