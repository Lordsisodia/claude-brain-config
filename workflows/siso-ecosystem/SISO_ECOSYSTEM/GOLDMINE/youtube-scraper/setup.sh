#!/bin/bash

echo "🚀 YouTube Scraper Setup"
echo "======================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  Please edit .env and add:"
    echo "   - YouTube API Key"
    echo "   - Telegram Bot Token"
    echo "   - Telegram Chat ID"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Node.js is installed: $(node --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm init -y > /dev/null 2>&1
npm install --save \
    @supabase/supabase-js \
    node-fetch \
    dotenv \
    @types/node \
    typescript \
    tsx

# Create package.json scripts
echo ""
echo "📝 Adding npm scripts..."
npm pkg set scripts.start="tsx scraper.ts"
npm pkg set scripts.test="tsx test-scraper.ts"
npm pkg set scripts.build="tsc"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Add remaining YouTube channels to config.ts"
echo "3. Create the database table in Supabase (see README.md)"
echo "4. Run: npm start"
echo ""
echo "💡 To find YouTube channel IDs:"
echo "   - Visit the YouTube channel"
echo "   - View page source (Ctrl+U)"
echo "   - Search for 'channelId'"
echo "   - Copy the UC... ID (24 characters)"