const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  connectionTimeoutMillis: 5000,
});

console.log('\n🔍 Testing connection to Mobile POS PostgreSQL database...\n');
console.log('Configuration:');
console.log(`  Host: ${process.env.DB_HOST}`);
console.log(`  Port: ${process.env.DB_PORT}`);
console.log(`  Database: ${process.env.DB_NAME}`);
console.log(`  User: ${process.env.DB_USER}`);
console.log('\n');

async function testConnection() {
  try {
    // Test basic connection
    const client = await pool.connect();
    console.log('✅ Successfully connected to PostgreSQL!\n');

    // Test database version
    const versionResult = await client.query('SELECT version()');
    console.log('📊 Database Info:');
    console.log(`  ${versionResult.rows[0].version}\n`);

    // Test current time
    const timeResult = await client.query('SELECT NOW() as current_time');
    console.log(`  Current database time: ${timeResult.rows[0].current_time}\n`);

    // List all tables
    const tablesResult = await client.query(`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);

    console.log('📋 Available tables:');
    if (tablesResult.rows.length === 0) {
      console.log('  No tables found. You may need to run the schema creation script.\n');
    } else {
      tablesResult.rows.forEach(row => {
        console.log(`  - ${row.table_name}`);
      });
      console.log('');
    }

    // Count products
    try {
      const productsResult = await client.query('SELECT COUNT(*) as count FROM products');
      console.log(`  Products: ${productsResult.rows[0].count} records`);
    } catch (err) {
      console.log('  Products table: Not found or empty');
    }

    // Count sales
    try {
      const salesResult = await client.query('SELECT COUNT(*) as count FROM sales');
      console.log(`  Sales: ${salesResult.rows[0].count} records`);
    } catch (err) {
      console.log('  Sales table: Not found or empty');
    }

    console.log('\n✅ Connection test completed successfully!\n');

    client.release();
    await pool.end();
    process.exit(0);

  } catch (error) {
    console.error('❌ Connection failed!\n');
    console.error('Error details:');
    console.error(`  ${error.message}\n`);

    console.log('💡 Troubleshooting steps:\n');
    console.log('1. Verify both devices are on the same network (192.168.254.x)');
    console.log('2. On Mobile POS laptop, check PostgreSQL is running:');
    console.log('   - Open Services (services.msc)');
    console.log('   - Find "postgresql-x64-16"');
    console.log('   - Ensure it\'s "Running"\n');
    console.log('3. Check PostgreSQL allows network connections:');
    console.log('   - Edit C:\\Program Files\\PostgreSQL\\16\\data\\postgresql.conf');
    console.log('   - Set: listen_addresses = \'*\'');
    console.log('   - Restart PostgreSQL service\n');
    console.log('4. Check firewall allows PostgreSQL port 5432:');
    console.log('   - Windows Firewall → Advanced Settings');
    console.log('   - Inbound Rules → Allow TCP port 5432\n');
    console.log('5. Check pg_hba.conf allows connections from your network:');
    console.log('   - Edit C:\\Program Files\\PostgreSQL\\16\\data\\pg_hba.conf');
    console.log('   - Add: host    all    all    192.168.254.0/24    md5\n');

    await pool.end();
    process.exit(1);
  }
}

testConnection();
