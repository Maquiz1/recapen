# Clinical and Data Workflow Architecture

**1. Patient Registration**
The workflow initiates with the formal registration of the patient into the system, capturing essential demographic and identifying information to establish their longitudinal electronic record.

**2. Initial Screening**
A preliminary screening is performed (capturing presenting complaints, medical history, vital signs) to identify suspected diseases. This assessment dictates the specific diagnostic investigations required.

**3. Investigation Requests**
Based on the screening indications, clinical staff electronically request targeted diagnostic investigations (e.g., Laboratory, Radiology, Cardiology tests) tailored to the suspected pathologies.

**4. Investigation Completion**
The respective ancillary departments (Laboratory, Radiology, Cardiology) conduct the requested investigations and input the diagnostic results directly into the system.

**5. Clinical Assessment & Diagnosis**
Attending physicians review the aggregated history, examination findings, and diagnostic results to formulate and confirm a definitive clinical diagnosis.

**6. Eligibility Assessment**
Following a confirmed diagnosis, the physician evaluates the patient against the study/program's inclusion criteria to determine if they are eligible for longitudinal cohort follow-up.

**7. Study/Program Enrollment**
If the patient is eligible, they provide consent and the physician assigns the patient to one or multiple corresponding study cohorts (e.g., Diabetes, Sickle Cell Disease, Cardiac).

**8. Disease Baseline**
Clinical staff fill out disease-specific baseline forms corresponding to the cohorts the patient was enrolled in, capturing essential initial clinical metrics.

**9. Baseline Assessment**
The initial encounter is finalized as the Baseline Assessment. This completes the patient's onboarding and baseline documentation.

**10. Follow Up Assessments Cadence & Scheduling**
Upon successful study enrollment, the clinical team establishes a personalized follow-up schedule. The system defaults to a standard one-month cadence from the date of enrollment, with the flexibility to configure alternative intervals (e.g., bi-monthly, quarterly, or annually) based on protocol or clinical necessity.

**11. eCRF Configuration & Visit Typology**
System Administrators and Data Managers configure the data collection requirements by mapping specific Electronic Case Report Forms (eCRFs) to distinct visit types. The system accommodates both *Scheduled* and *Unscheduled* clinical encounters to ensure comprehensive data capture.

**12. Longitudinal Visit Nomenclature**
The system adheres to standard clinical trial nomenclature: the initial enrollment encounter is designated as the *Baseline Assessment*, with the subsequent scheduled encounters documented as *Follow Up Assessments*, continuing sequentially.

**13. Retrospective & Dynamic Visit Generation**
To optimize database performance and maintain clinical relevance, the system employs an intelligent, step-wise visit generation algorithm rather than bulk-creating an exhaustive multi-year schedule upfront. 
*   **Retrospective Catch-up:** If a patient is enrolled retrospectively (i.e., the enrollment date is more than one month in the past), the system automatically computes and generates all historical monthly visits spanning from the date of enrollment up to the current date, plus exactly one future scheduled visit.
*   **Forward Generation:** For standard prospective enrollments, the system strictly generates only the immediate next anticipated visit following a completed encounter.

**14. Patient Status & Visit Outcome Management**
The architecture provides Data Managers and Administrators with highly dynamic, granular controls over the patient lifecycle and visit outcomes:
*   **Visit Status Attribution:** Individual visits can be categorized securely with specific outcomes, including *Missed*, *Unscheduled*, or *Not Applicable*, ensuring data integrity across the longitudinal record.
*   **Intra-Month Visit Conflicts:** In scenarios where multiple visits transpire within a single calendar month, the system permits manual adjustment of the *Visit Nature*—enabling clinicians or data managers to accurately classify one visit as the primary *Scheduled* encounter and the other as an *Unscheduled* or ad-hoc encounter.
*   **Individualized Follow Up Frequency & Audit Trailing:** While cohort-level default schedules exist, administrators possess per-patient control to dynamically alter the follow up frequency (e.g., escalating from a one-month cadence to a two-month cadence, or vice versa) in response to evolving clinical presentations. The system maintains a strict **Audit Trail**, immutably recording the timestamp, the responsible user, and the rationale every time a schedule frequency is modified.
*   **Administrative Follow Up Controls:** Administrators retain the authority to manually delete or override scheduled follow up visits when necessary.
*   **Terminal & Exclusionary Statuses:** The automated visit generation engine can be immediately halted if a patient undergoes a status change to *Deceased* (derived via date of death), *Loss to Follow Up (LTFU)*, *Withdrawn Consent*, *Transferred Out*, or *Defaulted*.
*   **Re-activation:** The system fully supports bidirectional status management, allowing patients who were previously designated as LTFU to be seamlessly re-activated and returned to active follow up generation upon re-engaging with clinical care.
