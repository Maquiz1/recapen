# Model Name Changes and Mappings Reference

This document tracks the conversion, mapping, and renaming of data models imported from older clinical systems into the **Recapen** database schema.

| Old System / Form Name | Recapen Database Model Name | Description & Key Fields | App Module | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Demographics** / **Demographic** | `SchoolHomeAssessment` | Tracks school grade alignment, NCD school limitations, missed school days, household size, referral sources, home visit consent, and Community Health Worker (CHW) details. | `clinical` | **Migrated & Renamed** |
| **VT** / **SCDVitals** | `Vitals` | Clinical vital signs: Systolic/Diastolic BP, Heart Rate, SpO2 (Oxygen Saturation), Pain Score, and notes. | `clinical` | **Migrated & Renamed** |
| **Initial Screening** | `Baseline` | Renamed the encounter type database value `'initial'` to display as `'Baseline'` in the UI. | `encounters`, `study_config` | **Renamed** |
| **History** | `History` | Newly added model for clinical assessment: past medical history, family history, and surgical history text details. | `clinical` | **New Model Added** |
| **Symptom** | `Symptom` | Newly added model for patient-reported symptoms: description list, severity scale (mild/moderate/severe), and duration in days. | `clinical` | **New Model Added** |
| **Complications** | `Complications` | Newly added model tracking NCD complications: Stroke, Kidney Disease, Retinopathy, Neuropathy, Diabetic Foot, and Cardiovascular Disease. | `clinical` | **New Model Added** |
| **Socioeconomic** | `Socioeconomic` | Tracks patient education level, employment status, monthly income range, clean water access, and health insurance coverage. | `clinical` | **Existing Model** |
| **Hospitalization** | `Hospitalization` | Admissions, NCD admissions, school days missed, transfusions, Bed Net, Folic Acid, and Malaria/Penicillin prophylaxis. | `clinical` | **Existing Model** |
| **treatment_plan** | `Treatment` | Future plan: vaccinations needed, transfusions needed, patient education checklists, social support, and referrals. | `clinical` | **Migrated & Renamed** |
