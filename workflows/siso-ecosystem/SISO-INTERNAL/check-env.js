// Quick script to check environment variables
const fs = require('fs');
const path = require('path');

console.log('🔍 Checking SISO-CORE Environment Configuration\n');

// Check .env files
const envFiles = ['.env', '.env.local', '.env.development'];

envFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`📄 Found ${file}:`);
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.split('\n').filter(line => line && !line.startsWith('#'));
    lines.forEach(line => {
      if (line.includes('SUPABASE')) {
        const [key, value] = line.split('=');
        console.log(`   ${key} = ${value ? value.substring(0, 50) + '...' : 'NOT SET'}`);
      }
    });
    console.log('');
  }
});

console.log('✅ To fix the infinite loading issue:\n');
console.log('1. Make sure the VITE_SUPABASE_ANON_KEY in .env.local matches the one in .env');
console.log('2. The key in .env looks correct (starts with eyJ...)');
console.log('3. Delete .env.local or update it with the correct key');
console.log('\nRun this to fix:');
console.log('cp .env .env.local');