// YouTube Scraper Configuration
export const YOUTUBE_CONFIG = {
  // API Configuration
  API_KEY: process.env.YOUTUBE_API_KEY || '',
  API_BASE_URL: 'https://www.googleapis.com/youtube/v3',
  
  // RSS Configuration
  RSS_BASE_URL: 'https://www.youtube.com/feeds/videos.xml',
  
  // Scraping Configuration
  CHECK_INTERVAL_MS: 60 * 60 * 1000, // 1 hour
  MIN_VIDEO_DURATION_SECONDS: 61, // Filter out shorts (> 1 minute)
  BATCH_SIZE: 50, // YouTube API max batch size
  
  // Rate Limiting
  DELAY_BETWEEN_BATCHES_MS: 2000, // 2 seconds
  MAX_RETRIES: 3,
  RETRY_DELAY_MS: 5 * 60 * 1000, // 5 minutes
  
  // Telegram Configuration
  TELEGRAM_BOT_TOKEN: process.env.TELEGRAM_BOT_TOKEN || '',
  TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID || '',
  TELEGRAM_MAX_MESSAGES_PER_BATCH: 10, // Send in batches to avoid rate limits
  TELEGRAM_BATCH_DELAY_MS: 3000, // 3 seconds between batches
  
  // Database
  DB_TABLE_NAME: 'youtube_goldmine',
  
  // 13 VERIFIED WORKING CHANNELS (Start with these, add more later)
  CHANNELS: [
    // Claude Code Specialists
    { id: 'UCPGrgwfbkjTIgPoOh2q1BAg', name: 'David Ondrej' },
    
    // Web Development Elite
    { id: 'UCsBjURrPoezykLs9EqgamOA', name: 'Fireship' },
    { id: 'UC29ju8bIPH5as8OGnQzwJyA', name: 'Traversy Media' },
    { id: 'UCFbNIlppjAuEX4znoulh0Cw', name: 'Web Dev Simplified' },
    { id: 'UCW5YeuERMmlnqo4oq8vwUpg', name: 'The Net Ninja' },
    
    // Modern Stack Masters
    { id: 'UCbRP3c757lWg9M-U7TyEkXA', name: 'Theo - t3.gg' },
    { id: 'UC-8QAzbLcRglXeN_MY9blyw', name: 'Ben Awad' },
    
    // AI Research & Education
    { id: 'UCbfYPyITQ-7l4upoX8nvctg', name: 'Two Minute Papers' },
    { id: 'UCSHZKyawb77ixDdsGog4iWA', name: 'Lex Fridman' },
    { id: 'UCYO_jab_esuFRV4b17AJtAw', name: '3Blue1Brown' },
    { id: 'UCZHmQk67mSJgfCCTn7xBfew', name: 'Yannic Kilcher' },
    
    // Programming Education
    { id: 'UC8butISFwT-Wl7EV0hUK0BQ', name: 'freeCodeCamp.org' },
    { id: 'UCWv7vMbMWH4-V0ZXdmDpPBA', name: 'Programming with Mosh' }
    
    // TODO: Add remaining verified channels as we fix their IDs
    // See verified-working-channels.json for testing other channels
  ]
};

// Telegram Rate Limits Reference:
// - To yourself (saved messages): No strict limit, but ~30 msgs/second recommended
// - To groups: 20 messages per minute
// - To users: 30 messages per second per chat
// - Bulk messages: 30 messages per second overall
export const TELEGRAM_RATE_LIMITS = {
  MESSAGES_PER_SECOND: 30,
  MESSAGES_PER_MINUTE_GROUP: 20,
  RECOMMENDED_DELAY_MS: 100, // 10 messages per second to be safe
};