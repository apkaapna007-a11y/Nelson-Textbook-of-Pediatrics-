#!/usr/bin/env node

const fs = require('fs');
const csv = require('csv-parser');
const { PrismaClient } = require('@prisma/client');
require('dotenv').config();

const prisma = new PrismaClient();

async function importNelsonData() {
  console.log('🚀 Starting Nelson data import...');
  
  try {
    // Check if CSV file exists
    if (!fs.existsSync('./dataset.csv')) {
      throw new Error('dataset.csv file not found in the root directory');
    }

    const records = [];
    let totalRecords = 0;
    let processedRecords = 0;
    let errorRecords = 0;

    // Read and parse CSV file
    console.log('📖 Reading CSV file...');
    
    await new Promise((resolve, reject) => {
      fs.createReadStream('./dataset.csv')
        .pipe(csv())
        .on('data', (row) => {
          totalRecords++;
          
          try {
            // Parse and validate the row data
            const record = {
              chapter: row.chapter || null,
              section: row.section || null,
              pageNumber: row.page_number ? parseInt(row.page_number) : null,
              content: row.content || '',
              keywords: row.keywords || null,
              medicalCategory: row.medical_category || null,
              ageGroup: row.age_group || null,
              createdAt: row.created_at ? new Date(row.created_at) : new Date(),
              updatedAt: row.updated_at ? new Date(row.updated_at) : new Date()
            };

            // Basic validation
            if (!record.content.trim()) {
              console.warn(`⚠️  Warning: Empty content for record ${totalRecords}, skipping...`);
              errorRecords++;
              return;
            }

            records.push(record);
          } catch (error) {
            console.error(`❌ Error processing row ${totalRecords}:`, error.message);
            errorRecords++;
          }
        })
        .on('end', resolve)
        .on('error', reject);
    });

    console.log(`📊 CSV parsing complete:`);
    console.log(`   Total rows: ${totalRecords}`);
    console.log(`   Valid records: ${records.length}`);
    console.log(`   Error records: ${errorRecords}`);

    if (records.length === 0) {
      throw new Error('No valid records found to import');
    }

    // Clear existing data (optional - comment out if you want to append)
    console.log('🗑️  Clearing existing data...');
    await prisma.nelsonContent.deleteMany({});

    // Import data in batches for better performance
    const batchSize = 100;
    const batches = [];
    
    for (let i = 0; i < records.length; i += batchSize) {
      batches.push(records.slice(i, i + batchSize));
    }

    console.log(`📦 Importing data in ${batches.length} batches...`);

    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      
      try {
        await prisma.nelsonContent.createMany({
          data: batch,
          skipDuplicates: true
        });
        
        processedRecords += batch.length;
        console.log(`   ✅ Batch ${i + 1}/${batches.length} completed (${processedRecords}/${records.length} records)`);
      } catch (error) {
        console.error(`❌ Error in batch ${i + 1}:`, error.message);
        
        // Try to insert records individually to identify problematic ones
        for (const record of batch) {
          try {
            await prisma.nelsonContent.create({ data: record });
            processedRecords++;
          } catch (individualError) {
            console.error(`❌ Failed to insert record:`, {
              chapter: record.chapter,
              section: record.section?.substring(0, 50) + '...',
              error: individualError.message
            });
            errorRecords++;
          }
        }
      }
    }

    // Create medical categories and age groups for reference
    console.log('📋 Creating reference data...');
    
    const uniqueCategories = [...new Set(records
      .map(r => r.medicalCategory)
      .filter(Boolean)
    )];
    
    const uniqueAgeGroups = [...new Set(records
      .map(r => r.ageGroup)
      .filter(Boolean)
    )];

    // Insert medical categories
    for (const category of uniqueCategories) {
      try {
        await prisma.medicalCategory.upsert({
          where: { name: category },
          update: {},
          create: { name: category }
        });
      } catch (error) {
        console.warn(`⚠️  Warning: Could not create medical category '${category}':`, error.message);
      }
    }

    // Insert age groups
    for (const ageGroup of uniqueAgeGroups) {
      try {
        await prisma.ageGroup.upsert({
          where: { name: ageGroup },
          update: {},
          create: { name: ageGroup }
        });
      } catch (error) {
        console.warn(`⚠️  Warning: Could not create age group '${ageGroup}':`, error.message);
      }
    }

    // Final statistics
    const finalCount = await prisma.nelsonContent.count();
    const categoryCount = await prisma.medicalCategory.count();
    const ageGroupCount = await prisma.ageGroup.count();

    console.log('\n🎉 Import completed successfully!');
    console.log(`📊 Final Statistics:`);
    console.log(`   Nelson Content Records: ${finalCount}`);
    console.log(`   Medical Categories: ${categoryCount}`);
    console.log(`   Age Groups: ${ageGroupCount}`);
    console.log(`   Processing Errors: ${errorRecords}`);

    // Sample queries to verify data
    console.log('\n🔍 Sample data verification:');
    
    const sampleRecord = await prisma.nelsonContent.findFirst({
      select: {
        id: true,
        chapter: true,
        section: true,
        medicalCategory: true,
        ageGroup: true,
        content: true
      }
    });

    if (sampleRecord) {
      console.log('   Sample record:', {
        id: sampleRecord.id,
        chapter: sampleRecord.chapter,
        section: sampleRecord.section?.substring(0, 50) + '...',
        medicalCategory: sampleRecord.medicalCategory,
        ageGroup: sampleRecord.ageGroup,
        contentLength: sampleRecord.content?.length || 0
      });
    }

  } catch (error) {
    console.error('❌ Import failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
}

// Run the import
if (require.main === module) {
  importNelsonData()
    .then(() => {
      console.log('✨ Import process completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Import process failed:', error);
      process.exit(1);
    });
}

module.exports = { importNelsonData };

