#!/usr/bin/env node

const { execSync } = require('child_process');
const { PrismaClient } = require('@prisma/client');
require('dotenv').config();

async function setupDatabase() {
  console.log('🚀 Setting up Nelson Book Prisma Database...');
  
  try {
    // Check if DATABASE_URL is configured
    if (!process.env.DATABASE_URL) {
      throw new Error('DATABASE_URL environment variable is not set. Please configure your .env file.');
    }

    console.log('📋 Database URL configured:', process.env.DATABASE_URL.replace(/:[^:@]*@/, ':****@'));

    // Generate Prisma Client
    console.log('🔧 Generating Prisma Client...');
    execSync('npx prisma generate', { stdio: 'inherit' });

    // Run database migrations
    console.log('🗄️  Running database migrations...');
    try {
      execSync('npx prisma migrate dev --name init', { stdio: 'inherit' });
    } catch (error) {
      console.log('⚠️  Migration failed, trying to push schema directly...');
      execSync('npx prisma db push', { stdio: 'inherit' });
    }

    // Test database connection
    console.log('🔌 Testing database connection...');
    const prisma = new PrismaClient();
    
    try {
      await prisma.$connect();
      console.log('✅ Database connection successful!');
      
      // Check if tables exist
      const tableCount = await prisma.$queryRaw`
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('nelson_content', 'medical_categories', 'age_groups')
      `;
      
      console.log(`📊 Database tables created: ${tableCount[0]?.count || 0}/3`);
      
    } catch (error) {
      throw new Error(`Database connection failed: ${error.message}`);
    } finally {
      await prisma.$disconnect();
    }

    console.log('\n🎉 Database setup completed successfully!');
    console.log('\n📝 Next steps:');
    console.log('   1. Update your .env file with correct database credentials');
    console.log('   2. Run: npm run db:seed (to import Nelson data from CSV)');
    console.log('   3. Run: npm run db:studio (to open Prisma Studio)');
    console.log('\n💡 Available commands:');
    console.log('   npm run db:generate  - Generate Prisma Client');
    console.log('   npm run db:migrate   - Run database migrations');
    console.log('   npm run db:studio    - Open Prisma Studio');
    console.log('   npm run db:seed      - Import Nelson data from CSV');
    console.log('   npm run db:reset     - Reset database and reimport data');

  } catch (error) {
    console.error('❌ Database setup failed:', error.message);
    
    if (error.message.includes('DATABASE_URL')) {
      console.log('\n🔧 To fix this:');
      console.log('   1. Copy .env.example to .env');
      console.log('   2. Update DATABASE_URL with your database credentials');
      console.log('   3. Run this setup script again');
    }
    
    if (error.message.includes('connect')) {
      console.log('\n🔧 Database connection troubleshooting:');
      console.log('   1. Ensure your database server is running');
      console.log('   2. Verify database credentials in .env file');
      console.log('   3. Check if the database exists');
      console.log('   4. Verify network connectivity to database server');
    }
    
    process.exit(1);
  }
}

// Run the setup
if (require.main === module) {
  setupDatabase()
    .then(() => {
      console.log('✨ Setup process completed');
      process.exit(0);
    })
    .catch((error) => {
      console.error('💥 Setup process failed:', error);
      process.exit(1);
    });
}

module.exports = { setupDatabase };

