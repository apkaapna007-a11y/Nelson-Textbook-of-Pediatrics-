#!/usr/bin/env node

const { PrismaClient } = require('@prisma/client');
const { importNelsonData } = require('./import-nelson-data');
require('dotenv').config();

async function resetDatabase() {
  console.log('🔄 Resetting Nelson Book Database...');
  
  const prisma = new PrismaClient();
  
  try {
    // Clear all data
    console.log('🗑️  Clearing existing data...');
    
    await prisma.nelsonContent.deleteMany({});
    console.log('   ✅ Nelson content cleared');
    
    await prisma.medicalCategory.deleteMany({});
    console.log('   ✅ Medical categories cleared');
    
    await prisma.ageGroup.deleteMany({});
    console.log('   ✅ Age groups cleared');

    // Reset auto-increment sequences (PostgreSQL specific)
    try {
      await prisma.$executeRaw`ALTER SEQUENCE nelson_content_id_seq RESTART WITH 1`;
      await prisma.$executeRaw`ALTER SEQUENCE medical_categories_id_seq RESTART WITH 1`;
      await prisma.$executeRaw`ALTER SEQUENCE age_groups_id_seq RESTART WITH 1`;
      console.log('   ✅ ID sequences reset');
    } catch (error) {
      console.log('   ⚠️  Could not reset sequences (this is normal for non-PostgreSQL databases)');
    }

    console.log('\n📊 Database reset completed');
    
    // Ask user if they want to reimport data
    const readline = require('readline');
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const answer = await new Promise((resolve) => {
      rl.question('🤔 Do you want to reimport Nelson data from CSV? (y/N): ', resolve);
    });
    
    rl.close();

    if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
      console.log('\n🚀 Starting data reimport...');
      await importNelsonData();
    } else {
      console.log('\n✅ Database reset completed. Run "npm run db:seed" to import data later.');
    }

  } catch (error) {
    console.error('❌ Database reset failed:', error.message);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
}

// Run the reset
if (require.main === module) {
  resetDatabase()
    .then(() => {
      console.log('✨ Reset process completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Reset process failed:', error);
      process.exit(1);
    });
}

module.exports = { resetDatabase };

