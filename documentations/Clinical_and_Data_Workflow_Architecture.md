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

**10. Retrospective & Dynamic Visit Generation**
To optimize database performance and maintain clinical relevance, the system employs an intelligent, step-wise visit generation algorithm rather than bulk-creating an exhaustive multi-year schedule upfront. 
*   **Retrospective Catch-up:** If a patient is enrolled retrospectively (i.e., the enrollment date is more than one month in the past), the system automatically computes and generates all historical monthly visits spanning from the date of enrollment up to the current date, plus exactly one future scheduled visit.
*   **Forward Generation:** For standard prospective enrollments, the system strictly generates only the immediate next anticipated visit following a completed encounter.

**11. Patient Status & Visit Outcome Management**
The architecture provides Data Managers and Administrators with highly dynamic, granular controls over the patient lifecycle and visit outcomes:
*   **Visit Status Attribution:** Individual visits can be categorized securely with specific outcomes, including *Missed*, *Unscheduled*, or *Not Applicable*, ensuring data integrity across the longitudinal record.
*   **Administrative Follow-Up Controls:** Administrators retain the authority to manually delete or override scheduled follow-up visits when necessary.
*   **Terminal & Exclusionary Statuses:** The automated visit generation engine can be immediately halted if a patient undergoes a status change to *Deceased* (derived via date of death), *Loss to Follow-Up (LTFU)*, *Withdrawn Consent*, *Transferred Out*, or *Defaulted*.
*   **Re-activation:** The system fully supports bidirectional status management, allowing patients who were previously designated as LTFU to be seamlessly re-activated and returned to active follow-up generation upon re-engaging with clinical care.
