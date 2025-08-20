// YouTube Scraper Database Integration

import { supabase } from '@/integrations/supabase/client';
import { YouTubeVideo } from './types';
import { YOUTUBE_CONFIG } from './config';

/**
 * Initialize YouTube goldmine table if it doesn't exist
 */
export async function initializeDatabase() {
  // Note: In production, this table should be created via Supabase migrations
  // This is just for reference of the schema
  /*
  CREATE TABLE IF NOT EXISTS youtube_goldmine (
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
  */
}

/**
 * Check if a video has already been processed
 */
export async function isVideoProcessed(videoId: string): Promise<boolean> {
  const { data, error } = await supabase
    .from(YOUTUBE_CONFIG.DB_TABLE_NAME)
    .select('video_id')
    .eq('video_id', videoId)
    .single();
  
  if (error && error.code !== 'PGRST116') { // PGRST116 = not found
    console.error('Error checking video:', error);
    return false;
  }
  
  return !!data;
}

/**
 * Save new videos to database
 */
export async function saveVideos(videos: YouTubeVideo[]): Promise<void> {
  if (videos.length === 0) return;
  
  const records = videos.map(video => ({
    video_id: video.videoId,
    channel_id: video.channelId,
    channel_name: video.channelName,
    title: video.title,
    description: video.description,
    published_at: video.publishedAt.toISOString(),
    thumbnail_url: video.thumbnailUrl,
    duration: video.duration,
    view_count: video.viewCount,
    url: video.url
  }));
  
  const { error } = await supabase
    .from(YOUTUBE_CONFIG.DB_TABLE_NAME)
    .upsert(records, {
      onConflict: 'video_id',
      ignoreDuplicates: false
    });
  
  if (error) {
    console.error('Error saving videos:', error);
    throw error;
  }
}

/**
 * Get videos published since a specific date
 */
export async function getVideosSince(since: Date, channelId?: string): Promise<YouTubeVideo[]> {
  let query = supabase
    .from(YOUTUBE_CONFIG.DB_TABLE_NAME)
    .select('*')
    .gte('published_at', since.toISOString())
    .order('published_at', { ascending: false });
  
  if (channelId) {
    query = query.eq('channel_id', channelId);
  }
  
  const { data, error } = await query;
  
  if (error) {
    console.error('Error fetching videos:', error);
    return [];
  }
  
  return data.map(record => ({
    videoId: record.video_id,
    channelId: record.channel_id,
    channelName: record.channel_name,
    title: record.title,
    description: record.description,
    publishedAt: new Date(record.published_at),
    thumbnailUrl: record.thumbnail_url,
    duration: record.duration,
    viewCount: record.view_count,
    url: record.url
  }));
}

/**
 * Get scraper state from database
 */
export async function getScraperState(): Promise<{
  lastCheckTime: Map<string, Date>;
  processedVideos: Set<string>;
}> {
  // In a production system, you might want to store this state in a separate table
  // For now, we'll derive it from the existing data
  
  const lastCheckTime = new Map<string, Date>();
  const processedVideos = new Set<string>();
  
  // Get all unique video IDs
  const { data: videos } = await supabase
    .from(YOUTUBE_CONFIG.DB_TABLE_NAME)
    .select('video_id, channel_id, created_at')
    .order('created_at', { ascending: false });
  
  if (videos) {
    videos.forEach(video => {
      processedVideos.add(video.video_id);
      
      // Track last check time per channel
      const channelTime = lastCheckTime.get(video.channel_id);
      const videoTime = new Date(video.created_at);
      if (!channelTime || videoTime > channelTime) {
        lastCheckTime.set(video.channel_id, videoTime);
      }
    });
  }
  
  return { lastCheckTime, processedVideos };
}