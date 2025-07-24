#!/usr/bin/env node

/**
 * Example usage of Nelson Book Prisma Database
 * 
 * This file demonstrates common queries and operations
 * you can perform with the Nelson textbook data.
 */

const { PrismaClient } = require('@prisma/client');
require('dotenv').config();

const prisma = new PrismaClient();

async function runExamples() {
  console.log('🔍 Nelson Book Database - Example Queries\n');

  try {
    // 1. Get total count of records
    console.log('1️⃣ Database Statistics:');
    const totalRecords = await prisma.nelsonContent.count();
    const totalCategories = await prisma.medicalCategory.count();
    const totalAgeGroups = await prisma.ageGroup.count();
    
    console.log(`   📊 Total Nelson Content: ${totalRecords}`);
    console.log(`   🏥 Medical Categories: ${totalCategories}`);
    console.log(`   👶 Age Groups: ${totalAgeGroups}\n`);

    // 2. Find content by medical category
    console.log('2️⃣ Content by Medical Category:');
    const categories = await prisma.nelsonContent.groupBy({
      by: ['medicalCategory'],
      _count: { id: true },
      where: { medicalCategory: { not: null } },
      orderBy: { _count: { id: 'desc' } },
      take: 5
    });
    
    categories.forEach(cat => {
      console.log(`   🏥 ${cat.medicalCategory}: ${cat._count.id} entries`);
    });
    console.log();

    // 3. Search for specific content
    console.log('3️⃣ Search Example - "fever":');
    const feverContent = await prisma.nelsonContent.findMany({
      where: {
        OR: [
          { content: { contains: 'fever', mode: 'insensitive' } },
          { keywords: { contains: 'fever', mode: 'insensitive' } }
        ]
      },
      select: {
        id: true,
        chapter: true,
        section: true,
        medicalCategory: true,
        ageGroup: true
      },
      take: 3
    });

    feverContent.forEach(content => {
      console.log(`   📖 ID ${content.id}: ${content.chapter} - ${content.section?.substring(0, 50)}...`);
      console.log(`      Category: ${content.medicalCategory}, Age: ${content.ageGroup}`);
    });
    console.log();

    // 4. Get content for specific age group
    console.log('4️⃣ Adolescent Content:');
    const adolescentContent = await prisma.nelsonContent.findMany({
      where: { ageGroup: 'Adolescent' },
      select: {
        id: true,
        chapter: true,
        section: true,
        medicalCategory: true
      },
      take: 3,
      orderBy: { id: 'asc' }
    });

    adolescentContent.forEach(content => {
      console.log(`   👨‍⚕️ ${content.chapter}: ${content.section?.substring(0, 60)}...`);
      console.log(`      Category: ${content.medicalCategory}`);
    });
    console.log();

    // 5. Advanced search with multiple conditions
    console.log('5️⃣ Advanced Search - Pediatric Development:');
    const advancedSearch = await prisma.nelsonContent.findMany({
      where: {
        AND: [
          {
            OR: [
              { content: { contains: 'development', mode: 'insensitive' } },
              { keywords: { contains: 'development', mode: 'insensitive' } }
            ]
          },
          { medicalCategory: { not: null } },
          { ageGroup: { in: ['Child', 'Adolescent'] } }
        ]
      },
      select: {
        id: true,
        chapter: true,
        section: true,
        medicalCategory: true,
        ageGroup: true,
        keywords: true
      },
      take: 2,
      orderBy: { id: 'asc' }
    });

    advancedSearch.forEach(content => {
      console.log(`   🧠 ${content.chapter}: ${content.section?.substring(0, 50)}...`);
      console.log(`      Category: ${content.medicalCategory}, Age: ${content.ageGroup}`);
      console.log(`      Keywords: ${content.keywords?.substring(0, 80)}...`);
    });
    console.log();

    // 6. Get page statistics
    console.log('6️⃣ Page Number Statistics:');
    const pageStats = await prisma.nelsonContent.aggregate({
      _avg: { pageNumber: true },
      _min: { pageNumber: true },
      _max: { pageNumber: true },
      _count: { pageNumber: true },
      where: { pageNumber: { not: null } }
    });

    console.log(`   📄 Average Page: ${Math.round(pageStats._avg.pageNumber || 0)}`);
    console.log(`   📄 Page Range: ${pageStats._min.pageNumber} - ${pageStats._max.pageNumber}`);
    console.log(`   📄 Records with Page Numbers: ${pageStats._count.pageNumber}\n`);

    // 7. Sample medical categories
    console.log('7️⃣ Available Medical Categories:');
    const medicalCategories = await prisma.medicalCategory.findMany({
      select: { name: true },
      take: 10,
      orderBy: { name: 'asc' }
    });

    medicalCategories.forEach(cat => {
      console.log(`   🏥 ${cat.name}`);
    });
    console.log();

    // 8. Sample age groups
    console.log('8️⃣ Available Age Groups:');
    const ageGroups = await prisma.ageGroup.findMany({
      select: { name: true },
      orderBy: { name: 'asc' }
    });

    ageGroups.forEach(group => {
      console.log(`   👶 ${group.name}`);
    });

    console.log('\n✨ Example queries completed successfully!');
    console.log('\n💡 Tips:');
    console.log('   - Use Prisma Studio (npm run db:studio) for visual data exploration');
    console.log('   - Check PRISMA_SETUP.md for more query examples');
    console.log('   - Use indexes for better performance on large datasets');

  } catch (error) {
    console.error('❌ Error running examples:', error.message);
    console.error('\n🔧 Troubleshooting:');
    console.error('   1. Ensure database is set up: npm run db:setup');
    console.error('   2. Import data: npm run db:seed');
    console.error('   3. Check your .env file configuration');
  } finally {
    await prisma.$disconnect();
  }
}

// Run examples if this file is executed directly
if (require.main === module) {
  runExamples()
    .then(() => {
      console.log('\n🎉 Examples completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Examples failed:', error);
      process.exit(1);
    });
}

module.exports = { runExamples };

