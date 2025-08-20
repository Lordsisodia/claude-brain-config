// Main YouTube Scraper Logic

import { YOUTUBE_CONFIG } from './config';
import { YouTubeChannel, YouTubeVideo, ScraperState } from './types';
import { fetchChannelRSSFeed, rssEntryToVideo } from './rss-parser';
import { getVideoDetails, isYouTubeShort } from './youtube-api';
import { saveVideos, isVideoProcessed, getScraperState } from './database';
import { sendVideosToTelegram, sendErrorNotification } from './telegram';
import { chunk, sleep, parseISO8601Duration } from './utils';

export class YouTubeScraper {
  private state: ScraperState;
  private isRunning: boolean = false;
  private intervalId: NodeJS.Timeout | null = null;
  
  constructor() {
    this.state = {
      lastCheckTime: new Map(),
      processedVideos: new Set(),
      errors: new Map()
    };
  }
  
  /**
   * Initialize the scraper
   */
  async initialize(): Promise<void> {
    console.log('🚀 Initializing YouTube Scraper...');
    
    // Load state from database
    const dbState = await getScraperState();
    this.state.lastCheckTime = dbState.lastCheckTime;
    this.state.processedVideos = dbState.processedVideos;
    
    console.log(`✅ Loaded ${this.state.processedVideos.size} processed videos`);
  }
  
  /**
   * Start the scraper
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      console.log('⚠️ Scraper is already running');
      return;
    }
    
    this.isRunning = true;
    console.log('▶️ Starting YouTube Scraper...');
    
    // Run immediately
    await this.runScrapeIteration();
    
    // Schedule regular runs
    this.intervalId = setInterval(
      () => this.runScrapeIteration(),
      YOUTUBE_CONFIG.CHECK_INTERVAL_MS
    );
  }
  
  /**
   * Stop the scraper
   */
  stop(): void {
    if (!this.isRunning) return;
    
    this.isRunning = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    
    console.log('⏹️ YouTube Scraper stopped');
  }
  
  /**
   * Run a single scrape iteration
   */
  private async runScrapeIteration(): Promise<void> {
    console.log(`\n🔄 Starting scrape iteration at ${new Date().toLocaleString()}`);
    
    const startTime = Date.now();
    const allNewVideos: YouTubeVideo[] = [];
    
    try {
      // Process channels in batches to avoid overwhelming APIs
      const channelBatches = chunk(YOUTUBE_CONFIG.CHANNELS, 5);
      
      for (const batch of channelBatches) {
        const batchVideos = await Promise.all(
          batch.map(channel => this.processChannel(channel))
        );
        
        allNewVideos.push(...batchVideos.flat());
        
        // Small delay between batches
        if (channelBatches.indexOf(batch) < channelBatches.length - 1) {
          await sleep(YOUTUBE_CONFIG.DELAY_BETWEEN_BATCHES_MS);
        }
      }
      
      // Send notifications for all new videos
      if (allNewVideos.length > 0) {
        console.log(`📹 Found ${allNewVideos.length} new long-form videos`);
        await sendVideosToTelegram(allNewVideos);
      } else {
        console.log('✅ No new videos found');
      }
      
      const duration = Date.now() - startTime;
      console.log(`✅ Scrape iteration completed in ${Math.round(duration / 1000)}s`);
      
    } catch (error) {
      console.error('❌ Scrape iteration failed:', error);
      await sendErrorNotification(error as Error, 'Scrape iteration');
    }
  }
  
  /**
   * Process a single YouTube channel
   */
  private async processChannel(channel: YouTubeChannel): Promise<YouTubeVideo[]> {
    try {
      console.log(`📡 Checking ${channel.name}...`);
      
      // Fetch RSS feed
      const feedEntries = await fetchChannelRSSFeed(channel.id);
      if (feedEntries.length === 0) {
        return [];
      }
      
      // Filter out already processed videos
      const newEntries = feedEntries.filter(
        entry => !this.state.processedVideos.has(entry.videoId)
      );
      
      if (newEntries.length === 0) {
        return [];
      }
      
      console.log(`  Found ${newEntries.length} potential new videos`);
      
      // Convert to video objects
      const videos = newEntries.map(entry => rssEntryToVideo(entry, channel.name));
      
      // Get video details from YouTube API (including duration)
      const videoIds = videos.map(v => v.videoId);
      const videoDetails = await getVideoDetails(videoIds);
      
      // Filter out shorts and enrich with duration data
      const longFormVideos: YouTubeVideo[] = [];
      
      for (const video of videos) {
        const details = videoDetails.get(video.videoId);
        if (!details) continue;
        
        // Skip if it's a short
        if (isYouTubeShort(details.contentDetails.duration)) {
          console.log(`  Skipping short: "${video.title}"`);
          continue;
        }
        
        // Enrich video with duration and stats
        const enrichedVideo: YouTubeVideo = {
          ...video,
          duration: parseISO8601Duration(details.contentDetails.duration),
          viewCount: details.statistics ? parseInt(details.statistics.viewCount) : undefined
        };
        
        longFormVideos.push(enrichedVideo);
      }
      
      // Save to database
      if (longFormVideos.length > 0) {
        await saveVideos(longFormVideos);
        
        // Update processed videos set
        longFormVideos.forEach(v => this.state.processedVideos.add(v.videoId));
        
        console.log(`  ✅ Found ${longFormVideos.length} new long-form videos`);
      }
      
      // Update last check time
      this.state.lastCheckTime.set(channel.id, new Date());
      
      // Reset error count on success
      this.state.errors.delete(channel.id);
      
      return longFormVideos;
      
    } catch (error) {
      console.error(`  ❌ Error processing ${channel.name}:`, error);
      
      // Track errors
      const errorCount = (this.state.errors.get(channel.id) || 0) + 1;
      this.state.errors.set(channel.id, errorCount);
      
      // Send notification if channel has consistent errors
      if (errorCount >= 3) {
        await sendErrorNotification(
          error as Error,
          `Channel ${channel.name} has failed ${errorCount} times`
        );
      }
      
      return [];
    }
  }
  
  /**
   * Get scraper statistics
   */
  getStats(): {
    isRunning: boolean;
    processedVideos: number;
    channelsWithErrors: number;
    lastCheckTimes: Record<string, string>;
  } {
    const lastCheckTimes: Record<string, string> = {};
    
    for (const [channelId, time] of this.state.lastCheckTime) {
      const channel = YOUTUBE_CONFIG.CHANNELS.find(c => c.id === channelId);
      if (channel) {
        lastCheckTimes[channel.name] = time.toLocaleString();
      }
    }
    
    return {
      isRunning: this.isRunning,
      processedVideos: this.state.processedVideos.size,
      channelsWithErrors: this.state.errors.size,
      lastCheckTimes
    };
  }
}

// Export singleton instance
export const youtubeScraper = new YouTubeScraper();