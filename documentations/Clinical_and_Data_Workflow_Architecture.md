# Clinical and Data Workflow Architecture

**1. Patient Registration & Demographics Intake**
The workflow initiates with the formal registration of the patient into the system, capturing essential demographic and identifying information to establish their longitudinal electronic record.

**2. Pre-Screening & Eligibility Assessment**
A preliminary eligibility checklist is utilized to stratify the patient’s clinical profile. This assessment directly dictates the specific diagnostic screening pathways required for the patient.

**3. Clinical Orders & Sample Collection**
Based on the pre-screening indications (e.g., suspected Diabetes, Sickle Cell Disease [SCD], or Cardiac conditions), clinical staff (physicians or nurses) acquire biological samples and electronically request targeted diagnostic investigations. These may include laboratory, radiological, or cardiological tests tailored to the suspected pathologies.

**4. Diagnostic Execution & Departmental Data Entry**
The respective ancillary departments (Laboratory, Radiology, Cardiology) conduct the requested investigations. Upon completion, technicians or specialists input the diagnostic results directly into the system via department-specific electronic forms.

**5. Clinical Review & Diagnostic Confirmation**
Attending physicians review the aggregated diagnostic results within the system to formulate a definitive clinical diagnosis. 

**6. Study Enrollment & Cohort Assignment**
Following a confirmed diagnosis (e.g., Diabetes, SCD, or a Cardiac condition), the physician evaluates the patient against the study’s inclusion criteria. If the patient presents with multiple comorbidities, the physician holds the authority to assign the patient to one or multiple corresponding study cohorts based on their specific eligibility.

**7. Follow-up Cadence & Scheduling**
Upon successful study enrollment, the clinical team establishes a personalized follow-up schedule. The system defaults to a standard one-month cadence from the date of enrollment, with the flexibility to configure alternative intervals (e.g., bi-monthly, quarterly, or annually) based on protocol or clinical necessity.

**8. eCRF Configuration & Visit Typology**
System Administrators and Data Managers configure the data collection requirements by mapping specific Electronic Case Report Forms (eCRFs) to distinct visit types. The system accommodates both *Scheduled* and *Unscheduled* clinical encounters to ensure comprehensive data capture.

**9. Longitudinal Visit Nomenclature**
The system adheres to standard clinical trial nomenclature: the initial enrollment encounter is designated as the *Baseline (Visit 0)*, with the subsequent scheduled encounter documented as *Visit 1*, continuing sequentially.

**10. Dynamic Visit Generation & Patient Status Management**
To optimize database performance and clinical relevance, the system employs dynamic, step-wise visit generation (creating only the immediate next visit rather than an exhaustive multi-year schedule). Furthermore, the system provides Data Managers with robust administrative controls to:
*   Modify follow-up intervals dynamically (e.g., transitioning from a 1-month to a 2-month cadence).
*   Manually adjust scheduled follow-up dates.
*   Manage terminal or exclusionary patient statuses (e.g., Withdrawn Consent, Transferred Out, or Deceased), thereby halting automated visit generation.
*   Handle "Loss to Follow-Up" (LTFU) protocols, including the capability to seamlessly re-activate patients returning to clinical care.
