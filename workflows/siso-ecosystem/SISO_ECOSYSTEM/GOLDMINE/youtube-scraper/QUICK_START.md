# 🚀 YouTube Scraper Quick Start

## Location
```
/Users/shaansisodia/Desktop/Cursor/SISO_ECOSYSTEM/GOLDMINE/youtube-scraper/
```

## 1️⃣ Setup (One Time)

```bash
cd /Users/shaansisodia/Desktop/Cursor/SISO_ECOSYSTEM/GOLDMINE/youtube-scraper/
./setup.sh
```

## 2️⃣ Configure

### Get YouTube API Key:
1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable YouTube Data API v3
4. Create credentials → API Key
5. Copy the API key

### Get Telegram Bot:
1. Message @BotFather on Telegram
2. Send `/newbot`
3. Choose bot name and username
4. Copy the bot token

### Get Your Telegram Chat ID:
1. Message your bot
2. Visit: `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
3. Find your chat ID in the response

### Edit .env:
```bash
YOUTUBE_API_KEY=your_youtube_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

## 3️⃣ Add More Channels

Edit `config.ts` and add channel IDs:

```typescript
CHANNELS: [
  { id: 'UCxxxxx', name: 'Channel Name' },
  // ... up to 50 channels
]
```

### How to Find Channel IDs:
1. Go to YouTube channel
2. Right-click → View Page Source
3. Search for: `"channelId":"UC`
4. Copy the full UC... ID (24 characters)

## 4️⃣ Create Database Table

In Supabase SQL editor:

```sql
CREATE TABLE youtube_goldmine (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  video_id VARCHAR(255) UNIQUE NOT NULL,
  channel_id VARCHAR(255) NOT NULL,
  channel_name VARCHAR(255) NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  published_at TIMESTAMP WITH TIME ZONE NOT NULL,
  thumbnail_url TEXT,
  duration INTEGER,
  view_count INTEGER,
  url TEXT NOT NULL,
  first_seen_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_youtube_goldmine_channel_id ON youtube_goldmine(channel_id);
CREATE INDEX idx_youtube_goldmine_published_at ON youtube_goldmine(published_at);
```

## 5️⃣ Run the Scraper

```bash
npm start
```

## 📊 What It Does

- ✅ Checks all channels every hour
- ✅ Filters out YouTube Shorts
- ✅ Saves to database
- ✅ Sends to Telegram
- ✅ Handles errors gracefully

## 🔍 Monitor Progress

Check the console for:
- New videos found
- Channels being checked
- Any errors

## 💡 Tips

- Start with 10 channels to test
- Add more channels gradually
- Monitor API usage in Google Console
- Check Telegram for notifications

## 🛠️ Troubleshooting

**No videos found?**
- Check if channels have new videos
- Verify channel IDs are correct
- Check API key is valid

**Telegram not working?**
- Verify bot token
- Check chat ID
- Make sure you messaged the bot first

**API errors?**
- Check quota in Google Console
- Verify API key has YouTube Data API enabled