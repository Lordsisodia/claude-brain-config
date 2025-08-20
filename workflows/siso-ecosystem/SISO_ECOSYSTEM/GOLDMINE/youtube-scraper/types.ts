// YouTube Scraper Types

export interface YouTubeChannel {
  id: string;
  name: string;
}

export interface YouTubeVideo {
  videoId: string;
  channelId: string;
  channelName: string;
  title: string;
  description: string;
  publishedAt: Date;
  thumbnailUrl: string;
  duration?: number; // in seconds
  viewCount?: number;
  url: string;
}

export interface RSSFeedEntry {
  id: string;
  videoId: string;
  channelId: string;
  title: string;
  link: string;
  author: {
    name: string;
    uri: string;
  };
  published: string;
  updated: string;
  description?: string;
  thumbnailUrl?: string;
  viewCount?: number;
}

export interface YouTubeAPIVideoDetails {
  id: string;
  contentDetails: {
    duration: string; // ISO 8601 duration format (e.g., "PT4M13S")
  };
  statistics?: {
    viewCount: string;
    likeCount: string;
    commentCount: string;
  };
}

export interface ScraperState {
  lastCheckTime: Map<string, Date>; // channelId -> lastCheckTime
  processedVideos: Set<string>; // Set of videoIds already processed
  errors: Map<string, number>; // channelId -> error count
}