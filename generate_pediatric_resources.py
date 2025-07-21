#!/usr/bin/env python3
"""
Script to generate sample pediatric medical resources data for the pediatric_medical_resources table.
"""

import json
import uuid
from typing import List, Dict

def generate_pediatric_resources() -> List[Dict]:
    """Generate sample pediatric medical resources."""
    
    resources = [
        {
            'id': str(uuid.uuid4()),
            'title': 'Acute Otitis Media Treatment Protocol',
            'content': 'First-line treatment for acute otitis media in children: Amoxicillin 80-90 mg/kg/day divided twice daily for 10 days in children under 2 years or with severe symptoms. For children 2-5 years with mild symptoms, watchful waiting may be appropriate for 48-72 hours. Second-line antibiotics include amoxicillin-clavulanate 90 mg/kg/day of amoxicillin component or azithromycin 10 mg/kg on day 1, then 5 mg/kg/day for 4 days.',
            'resource_type': 'protocol',
            'category': 'Infectious Diseases',
            'age_range': '6 months - 12 years',
            'weight_range': '5-40 kg',
            'source': 'American Academy of Pediatrics Clinical Practice Guidelines'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Fever Management Guidelines',
            'content': 'Fever management in children: Acetaminophen 10-15 mg/kg every 4-6 hours (maximum 5 doses/24 hours) or Ibuprofen 5-10 mg/kg every 6-8 hours for children >6 months. Do not use aspirin in children due to Reye syndrome risk. Seek immediate medical attention for fever >38°C (100.4°F) in infants <3 months, or fever >39°C (102.2°F) with signs of serious illness.',
            'resource_type': 'guideline',
            'category': 'General Pediatrics',
            'age_range': '0-18 years',
            'weight_range': '2-80 kg',
            'source': 'WHO Pediatric Guidelines'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Asthma Medication Dosing Chart',
            'content': 'Pediatric asthma medications: Albuterol inhaler 2 puffs every 4-6 hours as needed (with spacer for children <8 years). Prednisolone 1-2 mg/kg/day (maximum 60 mg) for 3-5 days for acute exacerbations. Maintenance therapy: Fluticasone 44-220 mcg twice daily depending on age and severity. Always use spacer devices for children under 8 years.',
            'resource_type': 'dosage',
            'category': 'Respiratory',
            'age_range': '2-18 years',
            'weight_range': '10-80 kg',
            'source': 'Global Initiative for Asthma (GINA)'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Dehydration Assessment and Management',
            'content': 'Dehydration assessment: Mild (3-5% weight loss): slightly dry mucous membranes, normal vital signs. Moderate (6-9%): dry mucous membranes, decreased skin turgor, tachycardia. Severe (>10%): very dry mucous membranes, poor skin turgor, altered mental status. Treatment: ORS 75 mL/kg over 4 hours for mild-moderate dehydration. IV fluids: 20 mL/kg bolus for severe dehydration, then maintenance plus deficit replacement.',
            'resource_type': 'protocol',
            'category': 'Emergency Medicine',
            'age_range': '1 month - 18 years',
            'weight_range': '3-80 kg',
            'source': 'American Academy of Pediatrics'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Newborn Feeding Guidelines',
            'content': 'Breastfeeding: 8-12 times per day, 10-30 minutes per session. Formula feeding: 60-90 mL every 2-3 hours for term newborns. Weight gain expectations: 15-30 g/day after day 4 of life. Signs of adequate intake: 6+ wet diapers/day after day 6, regular stools, weight gain. Supplement with vitamin D 400 IU daily for breastfed infants.',
            'resource_type': 'guideline',
            'category': 'Neonatology',
            'age_range': '0-3 months',
            'weight_range': '2-6 kg',
            'source': 'American Academy of Pediatrics'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Seizure Management Protocol',
            'content': 'Acute seizure management: Ensure airway, breathing, circulation. Lorazepam 0.1 mg/kg IV/IO (max 4 mg) or midazolam 0.2 mg/kg IM (max 10 mg). If seizure continues >5 minutes after first dose, repeat once. For status epilepticus: fosphenytoin 20 mg PE/kg IV or levetiracetam 60 mg/kg IV. Consider intubation if prolonged seizure or respiratory compromise.',
            'resource_type': 'protocol',
            'category': 'Neurology',
            'age_range': '1 month - 18 years',
            'weight_range': '3-80 kg',
            'source': 'Pediatric Emergency Medicine Guidelines'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Growth Chart Interpretation Guide',
            'content': 'Growth assessment: Plot height, weight, and head circumference on appropriate growth charts (WHO 0-2 years, CDC 2-20 years). Normal growth velocity: 25 cm/year in first year, 12.5 cm/year in second year, 6-7 cm/year ages 3-10. Concerning findings: crossing 2+ percentile lines, height <3rd percentile, or BMI >95th percentile. Consider genetic, endocrine, or nutritional causes for growth abnormalities.',
            'resource_type': 'reference',
            'category': 'Growth and Development',
            'age_range': '0-18 years',
            'weight_range': '2-100 kg',
            'source': 'CDC Growth Charts'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Immunization Schedule',
            'content': 'Key immunizations: Hepatitis B at birth, 1-2 months, 6-18 months. DTaP at 2, 4, 6, 15-18 months, 4-6 years. Hib at 2, 4, 6, 12-15 months. PCV13 at 2, 4, 6, 12-15 months. IPV at 2, 4, 6-18 months, 4-6 years. MMR at 12-15 months, 4-6 years. Varicella at 12-15 months, 4-6 years. Annual influenza vaccine starting at 6 months.',
            'resource_type': 'reference',
            'category': 'Preventive Medicine',
            'age_range': '0-18 years',
            'weight_range': '2-100 kg',
            'source': 'CDC Immunization Schedule'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Pain Assessment and Management',
            'content': 'Pain assessment tools: FLACC scale (0-3 years), Wong-Baker FACES (3+ years), numeric rating scale (8+ years). Mild pain: acetaminophen 10-15 mg/kg q4-6h or ibuprofen 5-10 mg/kg q6-8h. Moderate pain: add codeine 0.5-1 mg/kg q4-6h (avoid in children <12 years). Severe pain: morphine 0.1-0.2 mg/kg IV q2-4h or fentanyl 1-2 mcg/kg IV q1-2h.',
            'resource_type': 'protocol',
            'category': 'Pain Management',
            'age_range': '0-18 years',
            'weight_range': '2-100 kg',
            'source': 'Pediatric Pain Management Guidelines'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Adolescent Contraception Counseling',
            'content': 'Contraceptive options for adolescents: Combined oral contraceptives (if no contraindications), progestin-only pills, depot medroxyprogesterone acetate (DMPA) injection every 12 weeks, contraceptive implant (effective 3 years), IUDs (copper or hormonal). Emergency contraception: Plan B within 72 hours or ella within 120 hours of unprotected intercourse. Counsel on dual protection (condoms + hormonal method).',
            'resource_type': 'guideline',
            'category': 'Adolescent Medicine',
            'age_range': '12-18 years',
            'weight_range': '40-100 kg',
            'source': 'American College of Obstetricians and Gynecologists'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Cardiac Arrest Algorithm',
            'content': 'CPR: 30 compressions:2 breaths (single rescuer) or 15:2 (two rescuers). Compression rate 100-120/min, depth 1/3 chest diameter. Epinephrine 0.01 mg/kg (0.1 mL/kg of 1:10,000) IV/IO every 3-5 minutes. For VF/pVT: defibrillate 2 J/kg, then 4 J/kg for subsequent shocks. Amiodarone 5 mg/kg IV/IO for refractory VF/pVT. Consider reversible causes: hypoxia, hypovolemia, hypothermia, electrolyte abnormalities.',
            'resource_type': 'protocol',
            'category': 'Emergency Medicine',
            'age_range': '1 month - 18 years',
            'weight_range': '3-80 kg',
            'source': 'Pediatric Advanced Life Support (PALS)'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Neonatal Hypoglycemia Management',
            'content': 'Definition: glucose <40 mg/dL (2.2 mmol/L) in term infants, <25 mg/dL (1.4 mmol/L) in preterm. Risk factors: maternal diabetes, IUGR, prematurity, perinatal stress. Treatment: asymptomatic - early feeding, glucose gel 40% 0.5 mL/kg buccally. Symptomatic or severe: IV dextrose 10% 2 mL/kg bolus, then continuous infusion 4-8 mg/kg/min. Monitor glucose every 30 minutes until stable.',
            'resource_type': 'protocol',
            'category': 'Neonatology',
            'age_range': '0-28 days',
            'weight_range': '1-5 kg',
            'source': 'Neonatal Hypoglycemia Guidelines'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Urinary Tract Infection Guidelines',
            'content': 'UTI diagnosis: clean-catch urine with >100,000 CFU/mL single organism, or catheter/suprapubic sample with >50,000 CFU/mL. Treatment: uncomplicated cystitis - trimethoprim-sulfamethoxazole 6-12 mg/kg/day (TMP component) divided q12h for 7-10 days. Pyelonephritis: ceftriaxone 50-75 mg/kg/day IV, then oral antibiotics to complete 10-14 days. Imaging: VCUG for first febrile UTI in children <2 years.',
            'resource_type': 'guideline',
            'category': 'Nephrology/Urology',
            'age_range': '2 months - 18 years',
            'weight_range': '4-80 kg',
            'source': 'American Academy of Pediatrics UTI Guidelines'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Diabetes Management',
            'content': 'Type 1 diabetes management: Insulin requirements 0.5-1.2 units/kg/day. Rapid-acting insulin before meals (lispro, aspart, glulisine). Long-acting insulin once or twice daily (glargine, detemir). Target glucose: 80-180 mg/dL most of the time. HbA1c goal <7.5% for children <18 years. Monitor for DKA: glucose >250 mg/dL, ketones, acidosis. Emergency treatment: IV fluids, insulin infusion 0.1 units/kg/hr.',
            'resource_type': 'guideline',
            'category': 'Endocrinology',
            'age_range': '1-18 years',
            'weight_range': '10-100 kg',
            'source': 'American Diabetes Association'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Pediatric Anemia Evaluation',
            'content': 'Anemia definition: Hgb <11 g/dL (6 months-5 years), <11.5 g/dL (5-12 years), <12 g/dL (12-15 years). Iron deficiency: most common cause. Screening at 12 months, then annually. Treatment: elemental iron 3-6 mg/kg/day divided 1-2 times daily on empty stomach. Recheck CBC in 4 weeks. Consider other causes if no response: thalassemia, chronic disease, lead poisoning.',
            'resource_type': 'guideline',
            'category': 'Hematology/Oncology',
            'age_range': '6 months - 18 years',
            'weight_range': '5-80 kg',
            'source': 'American Academy of Pediatrics'
        }
    ]
    
    return resources

def generate_sql_inserts(resources: List[Dict], output_file: str):
    """Generate SQL INSERT statements for pediatric resources."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Pediatric Medical Resources Data Inserts\n")
        f.write("-- Sample clinical protocols, dosages, guidelines, and references\n\n")
        
        for resource in resources:
            # Escape single quotes
            title = resource['title'].replace("'", "''")
            content = resource['content'].replace("'", "''")
            source = resource['source'].replace("'", "''")
            
            sql = f"""INSERT INTO pediatric_medical_resources (id, title, content, resource_type, category, age_range, weight_range, source) VALUES (
    '{resource['id']}',
    '{title}',
    '{content}',
    '{resource['resource_type']}',
    '{resource['category']}',
    '{resource['age_range']}',
    '{resource['weight_range']}',
    '{source}'
);

"""
            f.write(sql)

def main():
    print("Generating pediatric medical resources...")
    resources = generate_pediatric_resources()
    
    print(f"Generated {len(resources)} pediatric medical resources")
    
    # Generate SQL inserts
    generate_sql_inserts(resources, 'pediatric_resources_inserts.sql')
    
    # Generate JSON output
    with open('pediatric_resources_data.json', 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)
    
    print("\nSample resources:")
    for i, resource in enumerate(resources[:3]):
        print(f"\nResource {i+1}:")
        print(f"Title: {resource['title']}")
        print(f"Type: {resource['resource_type']}")
        print(f"Category: {resource['category']}")
        print(f"Age Range: {resource['age_range']}")
        print(f"Content preview: {resource['content'][:150]}...")
    
    print(f"\nFiles generated:")
    print(f"- pediatric_resources_inserts.sql ({len(resources)} INSERT statements)")
    print(f"- pediatric_resources_data.json (JSON format)")

if __name__ == "__main__":
    main()

