# Nelson Textbook of Pediatrics Database Dataset

This repository contains a structured dataset prepared from the Nelson Textbook of Pediatrics, designed for use with PostgreSQL and pgvector for AI-powered pediatric medical assistance systems.

## 🚀 NEW: Prisma Database Integration

**Quick Start with Prisma:**
```bash
npm install
npm run db:setup
npm run db:seed
npm run db:studio
```

📖 **[Complete Prisma Setup Guide](PRISMA_SETUP.md)** - Full documentation for database setup, queries, and usage examples.

## 📊 Dataset Overview

The dataset includes:
- **34,313 records** extracted from Nelson Textbook of Pediatrics
- **15 sample pediatric medical resources** (protocols, dosages, guidelines)
- Complete PostgreSQL schema with vector search capabilities
- Utility functions for content retrieval and search

## 🗄️ Database Schema

### Tables

#### 1. `nelson_textbook`
Contains parsed content from the Nelson Textbook with the following structure:
- `id`: Unique identifier (UUID)
- `chapter`: Chapter reference (e.g., "Chapter 150")
- `section`: Section title within the chapter
- `page_number`: Page reference (when available)
- `content`: Full text content
- `embedding`: Vector embedding (1536 dimensions for OpenAI)
- `keywords`: Array of extracted medical keywords
- `medical_category`: Categorized medical specialty
- `age_group`: Target age group for the content
- `created_at`, `updated_at`: Timestamps

#### 2. `pediatric_medical_resources`
Clinical protocols, dosing guidelines, and reference materials:
- `id`: Unique identifier (UUID)
- `title`: Resource title
- `content`: Full resource content
- `resource_type`: Type (protocol, dosage, guideline, reference)
- `category`: Medical category
- `age_range`: Applicable age range
- `weight_range`: Applicable weight range
- `embedding`: Vector embedding (1536 dimensions)
- `source`: Source reference
- `created_at`, `last_updated`: Timestamps

#### 3. `chat_sessions` & `chat_messages`
Support tables for chat functionality in AI applications.

## 📈 Data Distribution

### Medical Categories
- **General Pediatrics**: 10,334 records
- **Infectious Diseases**: 4,552 records
- **Neurology**: 3,633 records
- **Respiratory**: 3,130 records
- **Gastroenterology**: 2,533 records
- **Cardiovascular**: 1,823 records
- **Growth and Development**: 1,526 records
- **Hematology/Oncology**: 1,526 records
- **Dermatology**: 1,298 records
- **Nephrology/Urology**: 1,177 records
- **Endocrinology**: 1,160 records
- **Adolescent Medicine**: 1,014 records
- **Neonatology**: 607 records

### Age Groups
- **All Ages**: 20,903 records
- **School Age (5-12 years)**: 7,586 records
- **Infant (1-12 months)**: 2,331 records
- **Newborn (0-28 days)**: 2,311 records
- **Adolescent (12-18 years)**: 1,011 records
- **Preschool (3-5 years)**: 114 records
- **Toddler (1-3 years)**: 57 records

## 🚀 Setup Instructions

### Prerequisites
- PostgreSQL 12+ with pgvector extension
- Python 3.8+ (for data processing scripts)

### Database Setup

1. **Install pgvector extension**:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

2. **Run the complete setup script**:
   ```bash
   psql -d your_database -f setup_nelson_database.sql
   ```

3. **Load the Nelson textbook data**:
   ```bash
   psql -d your_database -f nelson_textbook_inserts.sql
   ```

4. **Load the pediatric resources data**:
   ```bash
   psql -d your_database -f pediatric_resources_inserts.sql
   ```

### Data Processing Scripts

#### Parse Nelson Textbook Files
```bash
python3 improved_nelson_parser.py
```
This script processes the raw text files and generates structured data.

#### Generate Pediatric Resources
```bash
python3 generate_pediatric_resources.py
```
This script creates sample clinical protocols and guidelines.

## 🔍 Usage Examples

### Vector Similarity Search
```sql
-- Search for similar content using embeddings
SELECT * FROM match_documents(
  '[your_query_embedding_vector]'::vector(1536),
  'nelson_textbook',
  5,
  0.7
);
```

### Keyword Search
```sql
-- Search by medical keywords
SELECT * FROM search_by_keywords(
  ARRAY['fever', 'antibiotic', 'pediatric'],
  10
);
```

### Category-based Retrieval
```sql
-- Get content by medical category
SELECT * FROM get_content_by_category('Infectious Diseases', 20);
```

### Age-appropriate Content
```sql
-- Get content for specific age group
SELECT * FROM get_age_appropriate_content(
  'Infant (1-12 months)',
  'Respiratory',
  15
);
```

### Clinical Protocols
```sql
-- Get emergency protocols
SELECT * FROM pediatric_emergency_protocols;

-- Get medication dosing information
SELECT * FROM medication_dosing_guide WHERE category = 'Respiratory';
```

## 📁 File Structure

```
├── README.md                          # This documentation
├── setup_nelson_database.sql          # Complete database schema and setup
├── improved_nelson_parser.py          # Script to parse Nelson textbook files
├── generate_pediatric_resources.py    # Script to generate clinical resources
├── nelson_textbook_inserts.sql        # SQL inserts for Nelson textbook data
├── pediatric_resources_inserts.sql    # SQL inserts for clinical resources
├── nelson_textbook_data.json          # JSON format of Nelson data
├── pediatric_resources_data.json      # JSON format of clinical resources
├── parsing_summary.md                 # Summary of parsing results
├── part1 (1).txt                      # Raw Nelson textbook file 1
├── part2.txt                          # Raw Nelson textbook file 2
└── part3.txt                          # Raw Nelson textbook file 3
```

## 🔧 Utility Functions

The database includes several utility functions:

- `match_documents()`: Vector similarity search
- `get_content_by_category()`: Filter by medical category
- `search_by_keywords()`: Keyword-based search
- `get_age_appropriate_content()`: Age-specific content retrieval

## 📊 Database Views

Pre-built views for common queries:
- `pediatric_emergency_protocols`: Emergency medicine protocols
- `medication_dosing_guide`: Medication dosing information
- `database_statistics`: Dataset statistics

## 🎯 Use Cases

This dataset is ideal for:
- **AI-powered pediatric medical assistants**
- **Clinical decision support systems**
- **Medical education applications**
- **Research in pediatric medicine**
- **Vector-based semantic search applications**

## ⚠️ Important Notes

1. **Medical Disclaimer**: This dataset is for educational and research purposes only. Always consult qualified healthcare professionals for medical decisions.

2. **Data Quality**: The parsing process may introduce some inconsistencies. Review and validate data before production use.

3. **Embeddings**: Vector embeddings are not included in the SQL files. You'll need to generate them using your preferred embedding model (e.g., OpenAI's text-embedding-ada-002).

4. **Licensing**: Ensure compliance with Nelson Textbook of Pediatrics licensing terms for your use case.

## 🤝 Contributing

To improve the dataset:
1. Report parsing issues or data quality problems
2. Suggest additional clinical resources
3. Contribute utility functions or views
4. Improve categorization accuracy

## 📞 Support

For questions or issues with this dataset, please create an issue in the repository or contact the maintainers.

---

**Generated from Nelson Textbook of Pediatrics content for AI-powered pediatric medical assistance systems.**
