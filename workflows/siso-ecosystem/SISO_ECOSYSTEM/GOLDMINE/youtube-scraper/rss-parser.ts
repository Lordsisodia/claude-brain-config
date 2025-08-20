// YouTube RSS Feed Parser

import { YOUTUBE_CONFIG } from './config';
import { RSSFeedEntry, YouTubeVideo } from './types';
import { retryWithBackoff } from './utils';

/**
 * Parse RSS feed XML to extract video entries
 */
function parseRSSFeed(xmlText: string): RSSFeedEntry[] {
  const parser = new DOMParser();
  const doc = parser.parseFromString(xmlText, 'text/xml');
  const entries = doc.querySelectorAll('entry');
  const feedEntries: RSSFeedEntry[] = [];
  
  entries.forEach(entry => {
    const videoId = entry.querySelector('videoId')?.textContent || '';
    const channelId = entry.querySelector('channelId')?.textContent || '';
    const title = entry.querySelector('title')?.textContent || '';
    const link = entry.querySelector('link')?.getAttribute('href') || '';
    const authorName = entry.querySelector('author > name')?.textContent || '';
    const authorUri = entry.querySelector('author > uri')?.textContent || '';
    const published = entry.querySelector('published')?.textContent || '';
    const updated = entry.querySelector('updated')?.textContent || '';
    const description = entry.querySelector('media\\:description, description')?.textContent || '';
    const thumbnail = entry.querySelector('media\\:thumbnail, thumbnail')?.getAttribute('url') || '';
    const viewCountStr = entry.querySelector('media\\:statistics')?.getAttribute('views') || '0';
    
    if (videoId && channelId) {
      feedEntries.push({
        id: `yt:video:${videoId}`,
        videoId,
        channelId,
        title,
        link,
        author: { name: authorName, uri: authorUri },
        published,
        updated,
        description,
        thumbnailUrl: thumbnail,
        viewCount: parseInt(viewCountStr) || 0
      });
    }
  });
  
  return feedEntries;
}

/**
 * Fetch RSS feed for a YouTube channel
 */
export async function fetchChannelRSSFeed(channelId: string): Promise<RSSFeedEntry[]> {
  const url = `${YOUTUBE_CONFIG.RSS_BASE_URL}?channel_id=${channelId}`;
  
  return retryWithBackoff(async () => {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`RSS fetch failed: ${response.status} ${response.statusText}`);
    }
    
    const xmlText = await response.text();
    return parseRSSFeed(xmlText);
  }, YOUTUBE_CONFIG.MAX_RETRIES);
}

/**
 * Convert RSS entry to YouTubeVideo object
 */
export function rssEntryToVideo(entry: RSSFeedEntry, channelName: string): Omit<YouTubeVideo, 'duration'> {
  return {
    videoId: entry.videoId,
    channelId: entry.channelId,
    channelName,
    title: entry.title,
    description: entry.description || '',
    publishedAt: new Date(entry.published),
    thumbnailUrl: entry.thumbnailUrl || '',
    viewCount: entry.viewCount,
    url: entry.link
  };
}