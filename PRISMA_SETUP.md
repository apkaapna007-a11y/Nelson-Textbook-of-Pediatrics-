# Nelson Book - Prisma Database Setup

This guide will help you set up a Prisma database to store and query Nelson Textbook data from the CSV file.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- A PostgreSQL, MySQL, or SQLite database
- Database credentials ready

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Database Connection
Copy the example environment file and update with your database credentials:
```bash
cp .env.example .env
```

Edit `.env` file with your database connection string:
```env
# For PostgreSQL (recommended)
DATABASE_URL="postgresql://username:password@localhost:5432/nelson_book_db?schema=public"

# For MySQL
DATABASE_URL="mysql://username:password@localhost:3306/nelson_book_db"

# For SQLite (development only)
DATABASE_URL="file:./dev.db"
```

### 3. Set Up Database
```bash
npm run db:setup
```

### 4. Import Nelson Data
```bash
npm run db:seed
```

### 5. Explore Your Data
```bash
npm run db:studio
```

## 📊 Database Schema

The Prisma schema includes three main models:

### NelsonContent
Main table storing Nelson textbook content:
- `id` - Auto-incrementing primary key
- `chapter` - Chapter name/number
- `section` - Section title or description
- `pageNumber` - Page number in the textbook
- `content` - Full text content
- `keywords` - Pipe-separated keywords
- `medicalCategory` - Medical specialty category
- `ageGroup` - Target age group
- `createdAt` / `updatedAt` - Timestamps

### MedicalCategory
Reference table for medical specialties:
- `id` - Primary key
- `name` - Category name (unique)
- `description` - Optional description

### AgeGroup
Reference table for age groups:
- `id` - Primary key
- `name` - Age group name (unique)
- `description` - Optional description
- `minAge` / `maxAge` - Age range (optional)

## 🛠️ Available Commands

| Command | Description |
|---------|-------------|
| `npm run db:generate` | Generate Prisma Client |
| `npm run db:migrate` | Run database migrations (development) |
| `npm run db:migrate:prod` | Deploy migrations (production) |
| `npm run db:studio` | Open Prisma Studio (database GUI) |
| `npm run db:seed` | Import Nelson data from CSV |
| `npm run db:setup` | Complete database setup |
| `npm run db:reset` | Reset database and optionally reimport data |

## 📝 Usage Examples

### Basic Queries

```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Find content by medical category
const pediatricContent = await prisma.nelsonContent.findMany({
  where: {
    medicalCategory: 'Pediatrics'
  },
  select: {
    id: true,
    chapter: true,
    section: true,
    content: true,
    keywords: true
  }
});

// Search content by keywords
const searchResults = await prisma.nelsonContent.findMany({
  where: {
    OR: [
      { content: { contains: 'fever', mode: 'insensitive' } },
      { keywords: { contains: 'fever', mode: 'insensitive' } }
    ]
  }
});

// Get content for specific age group
const adolescentContent = await prisma.nelsonContent.findMany({
  where: {
    ageGroup: 'Adolescent'
  },
  orderBy: {
    chapter: 'asc'
  }
});

// Count content by category
const categoryStats = await prisma.nelsonContent.groupBy({
  by: ['medicalCategory'],
  _count: {
    id: true
  },
  orderBy: {
    _count: {
      id: 'desc'
    }
  }
});
```

### Advanced Queries

```javascript
// Full-text search across multiple fields
const complexSearch = await prisma.nelsonContent.findMany({
  where: {
    AND: [
      {
        OR: [
          { content: { contains: searchTerm, mode: 'insensitive' } },
          { keywords: { contains: searchTerm, mode: 'insensitive' } },
          { section: { contains: searchTerm, mode: 'insensitive' } }
        ]
      },
      { medicalCategory: { not: null } },
      { ageGroup: targetAgeGroup }
    ]
  },
  take: 20,
  skip: page * 20,
  orderBy: [
    { chapter: 'asc' },
    { pageNumber: 'asc' }
  ]
});

// Get statistics
const stats = await prisma.$transaction([
  prisma.nelsonContent.count(),
  prisma.medicalCategory.count(),
  prisma.ageGroup.count(),
  prisma.nelsonContent.aggregate({
    _avg: { pageNumber: true },
    _max: { pageNumber: true },
    _min: { pageNumber: true }
  })
]);
```

## 🔧 Troubleshooting

### Common Issues

**Database Connection Failed**
- Verify your DATABASE_URL in `.env`
- Ensure database server is running
- Check firewall/network settings
- Verify database exists

**Migration Errors**
- Try `npx prisma db push` instead of migrate
- Check database permissions
- Ensure schema is compatible with your database type

**Import Errors**
- Verify `dataset.csv` exists in root directory
- Check CSV format matches expected structure
- Look for encoding issues (should be UTF-8)

**Performance Issues**
- Ensure indexes are created (run migrations)
- Consider adding custom indexes for your query patterns
- Use `take` and `skip` for pagination

### Database-Specific Notes

**PostgreSQL (Recommended)**
- Best performance and feature support
- Full-text search capabilities
- JSON field support for future enhancements

**MySQL**
- Good performance
- Wide compatibility
- Change `provider = "mysql"` in schema.prisma

**SQLite**
- Great for development/testing
- Single file database
- Limited concurrent access

## 🚀 Production Deployment

### Environment Setup
```env
NODE_ENV=production
DATABASE_URL="your-production-database-url"
```

### Deployment Steps
1. Set up production database
2. Update DATABASE_URL in production environment
3. Run migrations: `npm run db:migrate:prod`
4. Import data: `npm run db:seed`

### Performance Optimization
- Enable connection pooling
- Add custom indexes for your query patterns
- Consider read replicas for high-traffic applications
- Monitor query performance with Prisma Studio

## 📚 Additional Resources

- [Prisma Documentation](https://www.prisma.io/docs/)
- [Prisma Client API Reference](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- [Database Connection Troubleshooting](https://www.prisma.io/docs/reference/database-reference/connection-urls)

## 🤝 Support

If you encounter issues:
1. Check this documentation
2. Review error messages carefully
3. Verify your database connection and credentials
4. Check the GitHub repository for updates

---

**Happy querying! 🎉**

