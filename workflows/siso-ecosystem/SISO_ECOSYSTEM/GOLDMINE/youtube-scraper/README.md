# YouTube Scraper Automation

A standalone YouTube scraper that monitors 50+ channels for new long-form content and sends notifications to Telegram.

## Features

- 🎥 Monitors multiple YouTube channels via RSS feeds
- ⏱️ Filters out YouTube Shorts (only videos > 60 seconds)
- 📊 Uses YouTube Data API v3 for video duration checking
- 💾 Stores all data in Supabase (youtube_goldmine table)
- 📱 Sends notifications to Telegram
- 🔄 Runs automatically every hour
- 🛡️ Resilient with retry logic and error handling

## Setup

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
YOUTUBE_API_KEY=your_youtube_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

### 2. Database Setup

Create the YouTube goldmine table in Supabase:

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
  duration INTEGER, -- in seconds
  view_count INTEGER,
  url TEXT NOT NULL,
  first_seen_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_youtube_goldmine_channel_id ON youtube_goldmine(channel_id);
CREATE INDEX idx_youtube_goldmine_published_at ON youtube_goldmine(published_at);
```

### 3. Add Your Channels

Edit `config.ts` and add your 50 channels:

```typescript
CHANNELS: [
  { id: 'UCPGrgwfbkjTIgPoOh2q1BAg', name: 'David Ondrej' },
  { id: 'UC...', name: 'Channel Name' },
  // ... add all 50 channels
]
```

## Usage

```typescript
import { youtubeScraper } from '@/automations/youtube-scraper';

// Initialize and start
await youtubeScraper.initialize();
await youtubeScraper.start();

// Check stats
const stats = youtubeScraper.getStats();

// Stop when needed
youtubeScraper.stop();
```

## Rate Limits

### YouTube
- RSS Feeds: No official limit, we check hourly (safe)
- API: 10,000 units/day (we use ~10-500 units/day)

### Telegram
- To yourself: 30 messages/second (we use 10/second max)
- Batch delay: 3 seconds between batches
- Max 10 messages per batch

## API Usage Calculation

With 50 channels, 10 new videos per channel per day:
- Videos to check: 500/day
- API calls (batched): 10 calls/day
- API units used: 10 units/day
- **Usage: 0.1% of daily quota**

## Error Handling

- Automatic retry with exponential backoff
- Error notifications sent to Telegram
- Channels with 3+ consecutive errors trigger alerts
- State persisted across restarts

## Monitoring

The scraper provides real-time stats:
- Running status
- Total processed videos
- Channels with errors
- Last check time per channel