
-- Sample SQL queries for testing the Nelson Pediatric Database

-- 1. Get all infectious disease content
SELECT chapter, section, content 
FROM nelson_textbook 
WHERE medical_category = 'Infectious Diseases' 
LIMIT 5;

-- 2. Search for fever-related content
SELECT chapter, section, content 
FROM nelson_textbook 
WHERE 'fever' = ANY(keywords) 
LIMIT 5;

-- 3. Get content appropriate for infants
SELECT chapter, section, content 
FROM nelson_textbook 
WHERE age_group IN ('Infant (1-12 months)', 'All Ages') 
LIMIT 5;

-- 4. Get emergency protocols
SELECT title, content, age_range 
FROM pediatric_medical_resources 
WHERE resource_type = 'protocol' 
  AND category = 'Emergency Medicine';

-- 5. Get medication dosing information
SELECT title, content, age_range, weight_range 
FROM pediatric_medical_resources 
WHERE resource_type = 'dosage' 
ORDER BY category;

-- 6. Search content by multiple keywords
SELECT * FROM search_by_keywords(
  ARRAY['antibiotic', 'infection', 'pediatric'], 
  10
);

-- 7. Get respiratory content for school-age children
SELECT * FROM get_age_appropriate_content(
  'School Age (5-12 years)', 
  'Respiratory', 
  5
);

-- 8. Database statistics
SELECT * FROM database_statistics;

-- 9. Count records by category
SELECT medical_category, COUNT(*) as record_count
FROM nelson_textbook 
GROUP BY medical_category 
ORDER BY record_count DESC;

-- 10. Find content with most keywords
SELECT chapter, section, array_length(keywords, 1) as keyword_count
FROM nelson_textbook 
WHERE keywords IS NOT NULL
ORDER BY keyword_count DESC 
LIMIT 10;
