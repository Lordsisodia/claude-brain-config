// Telegram Notification Service

import { YOUTUBE_CONFIG, TELEGRAM_RATE_LIMITS } from './config';
import { YouTubeVideo } from './types';
import { formatVideoForTelegram, chunk, sleep } from './utils';

/**
 * Send a message to Telegram
 */
async function sendTelegramMessage(message: string): Promise<void> {
  if (!YOUTUBE_CONFIG.TELEGRAM_BOT_TOKEN || !YOUTUBE_CONFIG.TELEGRAM_CHAT_ID) {
    console.warn('Telegram credentials not configured');
    return;
  }
  
  const url = `https://api.telegram.org/bot${YOUTUBE_CONFIG.TELEGRAM_BOT_TOKEN}/sendMessage`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      chat_id: YOUTUBE_CONFIG.TELEGRAM_CHAT_ID,
      text: message,
      parse_mode: 'Markdown',
      disable_web_page_preview: false
    })
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Telegram API error: ${response.status} - ${error}`);
  }
}

/**
 * Send multiple videos to Telegram with rate limiting
 */
export async function sendVideosToTelegram(videos: YouTubeVideo[]): Promise<void> {
  if (videos.length === 0) return;
  
  console.log(`Sending ${videos.length} new videos to Telegram...`);
  
  // Group videos by channel for better organization
  const videosByChannel = videos.reduce((acc, video) => {
    if (!acc[video.channelName]) {
      acc[video.channelName] = [];
    }
    acc[video.channelName].push(video);
    return acc;
  }, {} as Record<string, YouTubeVideo[]>);
  
  // Create batches to respect rate limits
  const messages: string[] = [];
  
  for (const [channelName, channelVideos] of Object.entries(videosByChannel)) {
    if (channelVideos.length === 1) {
      // Single video from channel
      messages.push(formatVideoForTelegram(channelVideos[0]));
    } else {
      // Multiple videos from same channel - send summary
      const summary = `
🎬 *${channelVideos.length} new videos from ${channelName}*

${channelVideos.map((v, i) => `${i + 1}. [${v.title}](${v.url})`).join('\n')}
      `.trim();
      messages.push(summary);
    }
  }
  
  // Send messages in batches with rate limiting
  const messageBatches = chunk(messages, YOUTUBE_CONFIG.TELEGRAM_MAX_MESSAGES_PER_BATCH);
  
  for (const batch of messageBatches) {
    // Send messages in current batch
    await Promise.all(
      batch.map(async (message, index) => {
        // Add small delay between messages in same batch
        await sleep(index * TELEGRAM_RATE_LIMITS.RECOMMENDED_DELAY_MS);
        await sendTelegramMessage(message);
      })
    );
    
    // Delay before next batch
    if (messageBatches.indexOf(batch) < messageBatches.length - 1) {
      await sleep(YOUTUBE_CONFIG.TELEGRAM_BATCH_DELAY_MS);
    }
  }
  
  console.log('✅ Telegram notifications sent successfully');
}

/**
 * Send error notification to Telegram
 */
export async function sendErrorNotification(error: Error, context: string): Promise<void> {
  const errorMessage = `
🚨 *YouTube Scraper Error*

*Context:* ${context}
*Error:* ${error.message}
*Time:* ${new Date().toLocaleString()}

Please check the logs for more details.
  `.trim();
  
  try {
    await sendTelegramMessage(errorMessage);
  } catch (telegramError) {
    console.error('Failed to send error notification to Telegram:', telegramError);
  }
}

/**
 * Send daily summary to Telegram
 */
export async function sendDailySummary(stats: {
  totalVideos: number;
  videosByChannel: Record<string, number>;
  totalDuration: number;
}): Promise<void> {
  const channelStats = Object.entries(stats.videosByChannel)
    .sort(([, a], [, b]) => b - a)
    .map(([channel, count]) => `• ${channel}: ${count} videos`)
    .join('\n');
  
  const summary = `
📊 *Daily YouTube Summary*

*Total Videos:* ${stats.totalVideos}
*Total Duration:* ${Math.round(stats.totalDuration / 3600)} hours

*By Channel:*
${channelStats}

*Generated:* ${new Date().toLocaleString()}
  `.trim();
  
  await sendTelegramMessage(summary);
}