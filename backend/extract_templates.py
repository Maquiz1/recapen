import re
import os

def extract_app_body(filename):
    with open(filename, "r") as f:
        content = f.read()
    match = re.search(r'<div class="app-body">(.*?)</div>\s*<!-- App body ends -->', content, re.DOTALL)
    if not match:
        match = re.search(r'<div class="app-body">(.*?)</div>\s*</div>\s*<!-- App wrapper ends -->', content, re.DOTALL)
    if not match:
        match = re.search(r'<div class="app-body">(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
    if match:
        return '<div class="app-body">' + match.group(1) + '</div>'
    return 'Not found in ' + filename

base_dir = "/home/maquiz/New_Templates/hospital/appollo/www.bootstrapget.com/demos/apollo-medical-admin-template/"
templates = [
    "doctors-grid.html",
    "doctors-cards.html",
    "doctors-profile.html",
    "add-doctors.html",
    "doctor-dashboard.html"
]

out_dir = "/home/maquiz/Documents/FINAL_PROJECTS/recapen/backend/templates/accounts/"

for t in templates:
    body = extract_app_body(base_dir + t)
    
    t_name = t.replace("add-", "")
    t_name = t_name.replace("doctors.html", "doctor_form.html")
    t_name = t_name.replace("-", "_")
    
    out_file = os.path.join(out_dir, t_name)
    
    django_content = '{% extends "base.html" %}\n{% load static %}\n{% block content %}\n' + body + '\n{% endblock content %}\n'
    
    with open(out_file, "w") as f:
        f.write(django_content)
    print(f"Written {out_file}")
