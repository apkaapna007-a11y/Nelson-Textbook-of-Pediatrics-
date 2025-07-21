-- Pediatric Medical Resources Data Inserts
-- Sample clinical protocols, dosages, guidelines, and references

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    'e841bc65-57a7-4d40-ad69-c5b314d983d7',
    'Acute Otitis Media Treatment Protocol',
    'First-line treatment for acute otitis media in children: Amoxicillin 80-90 mg/kg/day divided twice daily for 10 days in children under 2 years or with severe symptoms. For children 2-5 years with mild symptoms, watchful waiting may be appropriate for 48-72 hours. Second-line antibiotics include amoxicillin-clavulanate 90 mg/kg/day of amoxicillin component or azithromycin 10 mg/kg on day 1, then 5 mg/kg/day for 4 days.',
    'protocol',
    'Infectious Diseases',
    '6 months - 12 years',
    '5-40 kg',
    'American Academy of Pediatrics Clinical Practice Guidelines'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '301fe43c-c212-4a49-9b8f-b41f72f7a583',
    'Pediatric Fever Management Guidelines',
    'Fever management in children: Acetaminophen 10-15 mg/kg every 4-6 hours (maximum 5 doses/24 hours) or Ibuprofen 5-10 mg/kg every 6-8 hours for children >6 months. Do not use aspirin in children due to Reye syndrome risk. Seek immediate medical attention for fever >38°C (100.4°F) in infants <3 months, or fever >39°C (102.2°F) with signs of serious illness.',
    'guideline',
    'General Pediatrics',
    '0-18 years',
    '2-80 kg',
    'WHO Pediatric Guidelines'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '29130586-916f-45b8-80d2-3ae8d8cc4d24',
    'Asthma Medication Dosing Chart',
    'Pediatric asthma medications: Albuterol inhaler 2 puffs every 4-6 hours as needed (with spacer for children <8 years). Prednisolone 1-2 mg/kg/day (maximum 60 mg) for 3-5 days for acute exacerbations. Maintenance therapy: Fluticasone 44-220 mcg twice daily depending on age and severity. Always use spacer devices for children under 8 years.',
    'dosage',
    'Respiratory',
    '2-18 years',
    '10-80 kg',
    'Global Initiative for Asthma (GINA)'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '0bef4ed1-9109-461a-825a-3d70ce7bf2da',
    'Pediatric Dehydration Assessment and Management',
    'Dehydration assessment: Mild (3-5% weight loss): slightly dry mucous membranes, normal vital signs. Moderate (6-9%): dry mucous membranes, decreased skin turgor, tachycardia. Severe (>10%): very dry mucous membranes, poor skin turgor, altered mental status. Treatment: ORS 75 mL/kg over 4 hours for mild-moderate dehydration. IV fluids: 20 mL/kg bolus for severe dehydration, then maintenance plus deficit replacement.',
    'protocol',
    'Emergency Medicine',
    '1 month - 18 years',
    '3-80 kg',
    'American Academy of Pediatrics'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '1bac4679-1007-4821-8b6a-2db88c742432',
    'Newborn Feeding Guidelines',
    'Breastfeeding: 8-12 times per day, 10-30 minutes per session. Formula feeding: 60-90 mL every 2-3 hours for term newborns. Weight gain expectations: 15-30 g/day after day 4 of life. Signs of adequate intake: 6+ wet diapers/day after day 6, regular stools, weight gain. Supplement with vitamin D 400 IU daily for breastfed infants.',
    'guideline',
    'Neonatology',
    '0-3 months',
    '2-6 kg',
    'American Academy of Pediatrics'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '335e0e6d-3ef6-4fce-bc3e-f26ce04a1732',
    'Pediatric Seizure Management Protocol',
    'Acute seizure management: Ensure airway, breathing, circulation. Lorazepam 0.1 mg/kg IV/IO (max 4 mg) or midazolam 0.2 mg/kg IM (max 10 mg). If seizure continues >5 minutes after first dose, repeat once. For status epilepticus: fosphenytoin 20 mg PE/kg IV or levetiracetam 60 mg/kg IV. Consider intubation if prolonged seizure or respiratory compromise.',
    'protocol',
    'Neurology',
    '1 month - 18 years',
    '3-80 kg',
    'Pediatric Emergency Medicine Guidelines'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '9367ac24-2413-4dd7-b9b3-e51fc143c572',
    'Growth Chart Interpretation Guide',
    'Growth assessment: Plot height, weight, and head circumference on appropriate growth charts (WHO 0-2 years, CDC 2-20 years). Normal growth velocity: 25 cm/year in first year, 12.5 cm/year in second year, 6-7 cm/year ages 3-10. Concerning findings: crossing 2+ percentile lines, height <3rd percentile, or BMI >95th percentile. Consider genetic, endocrine, or nutritional causes for growth abnormalities.',
    'reference',
    'Growth and Development',
    '0-18 years',
    '2-100 kg',
    'CDC Growth Charts'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    'b5a407e2-4bc7-483b-a62e-d4e08702ab98',
    'Pediatric Immunization Schedule',
    'Key immunizations: Hepatitis B at birth, 1-2 months, 6-18 months. DTaP at 2, 4, 6, 15-18 months, 4-6 years. Hib at 2, 4, 6, 12-15 months. PCV13 at 2, 4, 6, 12-15 months. IPV at 2, 4, 6-18 months, 4-6 years. MMR at 12-15 months, 4-6 years. Varicella at 12-15 months, 4-6 years. Annual influenza vaccine starting at 6 months.',
    'reference',
    'Preventive Medicine',
    '0-18 years',
    '2-100 kg',
    'CDC Immunization Schedule'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '97024612-2d68-42f1-bf14-0ba37c72fb32',
    'Pediatric Pain Assessment and Management',
    'Pain assessment tools: FLACC scale (0-3 years), Wong-Baker FACES (3+ years), numeric rating scale (8+ years). Mild pain: acetaminophen 10-15 mg/kg q4-6h or ibuprofen 5-10 mg/kg q6-8h. Moderate pain: add codeine 0.5-1 mg/kg q4-6h (avoid in children <12 years). Severe pain: morphine 0.1-0.2 mg/kg IV q2-4h or fentanyl 1-2 mcg/kg IV q1-2h.',
    'protocol',
    'Pain Management',
    '0-18 years',
    '2-100 kg',
    'Pediatric Pain Management Guidelines'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    'dfae3e41-68d3-4063-96e0-090a342d0ba5',
    'Adolescent Contraception Counseling',
    'Contraceptive options for adolescents: Combined oral contraceptives (if no contraindications), progestin-only pills, depot medroxyprogesterone acetate (DMPA) injection every 12 weeks, contraceptive implant (effective 3 years), IUDs (copper or hormonal). Emergency contraception: Plan B within 72 hours or ella within 120 hours of unprotected intercourse. Counsel on dual protection (condoms + hormonal method).',
    'guideline',
    'Adolescent Medicine',
    '12-18 years',
    '40-100 kg',
    'American College of Obstetricians and Gynecologists'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '75f2c591-743c-4c01-b6ee-7d6725857f81',
    'Pediatric Cardiac Arrest Algorithm',
    'CPR: 30 compressions:2 breaths (single rescuer) or 15:2 (two rescuers). Compression rate 100-120/min, depth 1/3 chest diameter. Epinephrine 0.01 mg/kg (0.1 mL/kg of 1:10,000) IV/IO every 3-5 minutes. For VF/pVT: defibrillate 2 J/kg, then 4 J/kg for subsequent shocks. Amiodarone 5 mg/kg IV/IO for refractory VF/pVT. Consider reversible causes: hypoxia, hypovolemia, hypothermia, electrolyte abnormalities.',
    'protocol',
    'Emergency Medicine',
    '1 month - 18 years',
    '3-80 kg',
    'Pediatric Advanced Life Support (PALS)'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '5b29d0e7-e315-4525-9fd1-d54ac9a00cb4',
    'Neonatal Hypoglycemia Management',
    'Definition: glucose <40 mg/dL (2.2 mmol/L) in term infants, <25 mg/dL (1.4 mmol/L) in preterm. Risk factors: maternal diabetes, IUGR, prematurity, perinatal stress. Treatment: asymptomatic - early feeding, glucose gel 40% 0.5 mL/kg buccally. Symptomatic or severe: IV dextrose 10% 2 mL/kg bolus, then continuous infusion 4-8 mg/kg/min. Monitor glucose every 30 minutes until stable.',
    'protocol',
    'Neonatology',
    '0-28 days',
    '1-5 kg',
    'Neonatal Hypoglycemia Guidelines'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    'c2bfc92d-a62b-4072-8f05-069d6415c652',
    'Pediatric Urinary Tract Infection Guidelines',
    'UTI diagnosis: clean-catch urine with >100,000 CFU/mL single organism, or catheter/suprapubic sample with >50,000 CFU/mL. Treatment: uncomplicated cystitis - trimethoprim-sulfamethoxazole 6-12 mg/kg/day (TMP component) divided q12h for 7-10 days. Pyelonephritis: ceftriaxone 50-75 mg/kg/day IV, then oral antibiotics to complete 10-14 days. Imaging: VCUG for first febrile UTI in children <2 years.',
    'guideline',
    'Nephrology/Urology',
    '2 months - 18 years',
    '4-80 kg',
    'American Academy of Pediatrics UTI Guidelines'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '70bf9bb8-f729-47d2-a2dc-df01c357dbfb',
    'Pediatric Diabetes Management',
    'Type 1 diabetes management: Insulin requirements 0.5-1.2 units/kg/day. Rapid-acting insulin before meals (lispro, aspart, glulisine). Long-acting insulin once or twice daily (glargine, detemir). Target glucose: 80-180 mg/dL most of the time. HbA1c goal <7.5% for children <18 years. Monitor for DKA: glucose >250 mg/dL, ketones, acidosis. Emergency treatment: IV fluids, insulin infusion 0.1 units/kg/hr.',
    'guideline',
    'Endocrinology',
    '1-18 years',
    '10-100 kg',
    'American Diabetes Association'
);

INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    'eb85a211-4cae-4470-b7bb-fcf37fdf0b03',
    'Pediatric Anemia Evaluation',
    'Anemia definition: Hgb <11 g/dL (6 months-5 years), <11.5 g/dL (5-12 years), <12 g/dL (12-15 years). Iron deficiency: most common cause. Screening at 12 months, then annually. Treatment: elemental iron 3-6 mg/kg/day divided 1-2 times daily on empty stomach. Recheck CBC in 4 weeks. Consider other causes if no response: thalassemia, chronic disease, lead poisoning.',
    'guideline',
    'Hematology/Oncology',
    '6 months - 18 years',
    '5-80 kg',
    'American Academy of Pediatrics'
);

