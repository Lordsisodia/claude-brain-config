// YouTube Scraper Main Entry Point

export { YouTubeScraper, youtubeScraper } from './scraper';
export { YOUTUBE_CONFIG, TELEGRAM_RATE_LIMITS } from './config';
export * from './types';
export { sendDailySummary } from './telegram';
export { getVideosSince } from './database';

// Usage example:
/*
import { youtubeScraper } from '@/automations/youtube-scraper';

// Initialize and start the scraper
await youtubeScraper.initialize();
await youtubeScraper.start();

// Check stats
const stats = youtubeScraper.getStats();
console.log('Scraper stats:', stats);

// Stop when needed
youtubeScraper.stop();
*/