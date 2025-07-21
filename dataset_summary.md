# Nelson Textbook Dataset Summary

## Overview
This dataset was created from three Nelson Textbook of Pediatrics text files (`part1 (1).txt`, `part2.txt`, `part3.txt`) and formatted according to the PostgreSQL schema for the `nelson_textbook` table.

## Files Created

### 1. dataset.csv
- **Total Entries**: 700 records (plus header)
- **Source Files**: part1 (1).txt, part2.txt, part3.txt
- **Schema Compliance**: Follows the nelson_textbook table structure

### 2. create_dataset.py
- Python script used to process the text files
- Extracts chapters, sections, and medical content
- Automatically categorizes content by medical specialty
- Generates keywords and determines age groups

## Dataset Schema

The CSV follows this structure matching the PostgreSQL table:

```sql
CREATE TABLE nelson_textbook (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  chapter VARCHAR(255) NOT NULL,
  section VARCHAR(500) NOT NULL,
  page_number INTEGER,
  content TEXT NOT NULL,
  embedding vector(1536), -- Will be generated separately
  keywords TEXT[],
  medical_category VARCHAR(100),
  age_group VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## CSV Columns

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Sequential ID (1-700) |
| chapter | String | Chapter reference (e.g., "Chapter 150") |
| section | String | Section title |
| page_number | Integer | Estimated page number |
| content | Text | Medical content excerpt |
| keywords | String | Pipe-separated medical keywords |
| medical_category | String | Medical specialty category |
| age_group | String | Target age group |
| created_at | Timestamp | ISO 8601 timestamp |
| updated_at | Timestamp | ISO 8601 timestamp |

## Medical Categories Included

- Adolescent Medicine
- Growth and Development  
- Urology
- Infectious Diseases
- Cardiology
- Pulmonology
- Neurology
- General Pediatrics

## Age Groups

- Neonatal
- Infant
- Pediatric
- Adolescent

## Usage

To import this data into PostgreSQL:

```sql
COPY nelson_textbook(id, chapter, section, page_number, content, keywords, medical_category, age_group, created_at, updated_at)
FROM '/path/to/dataset.csv'
DELIMITER ','
CSV HEADER;
```

Note: The `embedding` column will need to be populated separately using an embedding service like OpenAI's text-embedding-ada-002.

## Data Quality

- All entries have substantial content (>200 characters)
- Medical keywords automatically extracted
- Content properly escaped for CSV format
- Timestamps in ISO 8601 format
- Categories based on content analysis

