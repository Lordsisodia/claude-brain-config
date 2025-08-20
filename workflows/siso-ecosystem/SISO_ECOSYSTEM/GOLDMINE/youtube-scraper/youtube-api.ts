// YouTube Data API v3 Integration

import { YOUTUBE_CONFIG } from './config';
import { YouTubeAPIVideoDetails } from './types';
import { chunk, parseISO8601Duration, retryWithBackoff } from './utils';

/**
 * Get video details from YouTube API (including duration)
 */
export async function getVideoDetails(videoIds: string[]): Promise<Map<string, YouTubeAPIVideoDetails>> {
  if (!YOUTUBE_CONFIG.API_KEY) {
    throw new Error('YouTube API key not configured');
  }
  
  const videoDetailsMap = new Map<string, YouTubeAPIVideoDetails>();
  
  // YouTube API allows max 50 video IDs per request
  const batches = chunk(videoIds, YOUTUBE_CONFIG.BATCH_SIZE);
  
  for (const batch of batches) {
    const batchDetails = await fetchVideoBatch(batch);
    batchDetails.forEach(detail => {
      videoDetailsMap.set(detail.id, detail);
    });
  }
  
  return videoDetailsMap;
}

/**
 * Fetch a batch of video details from YouTube API
 */
async function fetchVideoBatch(videoIds: string[]): Promise<YouTubeAPIVideoDetails[]> {
  const url = new URL(`${YOUTUBE_CONFIG.API_BASE_URL}/videos`);
  url.searchParams.append('part', 'contentDetails,statistics');
  url.searchParams.append('id', videoIds.join(','));
  url.searchParams.append('key', YOUTUBE_CONFIG.API_KEY);
  
  return retryWithBackoff(async () => {
    const response = await fetch(url.toString());
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`YouTube API error: ${response.status} - ${error}`);
    }
    
    const data = await response.json();
    return data.items || [];
  }, YOUTUBE_CONFIG.MAX_RETRIES);
}

/**
 * Check if video is a YouTube Short based on duration
 */
export function isYouTubeShort(durationISO: string): boolean {
  const durationSeconds = parseISO8601Duration(durationISO);
  return durationSeconds < YOUTUBE_CONFIG.MIN_VIDEO_DURATION_SECONDS;
}

/**
 * Get channel's upload playlist ID
 * YouTube channel IDs can be converted to playlist IDs by replacing 'UC' with 'UU'
 */
export function getUploadsPlaylistId(channelId: string): string {
  return channelId.replace('UC', 'UU');
}

/**
 * Check API quota usage (for monitoring)
 */
export async function checkQuotaUsage(): Promise<{ used: number; limit: number }> {
  // Note: YouTube doesn't provide a direct quota check endpoint
  // This is a placeholder - you'd need to track usage manually
  return {
    used: 0,
    limit: 10000 // Default daily quota
  };
}