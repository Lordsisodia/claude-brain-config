# 🔧 Fix YouTube Channel IDs

## ❌ **Broken Channel IDs Found:**
- Anthropic: `UCJmJgKCYrNvK3pgIgLyC4aQ` (404 error)
- Matthew Berman: `UCqRlEXn0Z_0pIYvxm8dGamw` (404 error)
- Some others may need verification

## ✅ **Working Channel IDs:**
- David Ondrej: `UCPGrgwfbkjTIgPoOh2q1BAg` ✅
- Fireship: `UCsBjURrPoezykLs9EqgamOA` ✅
- Traversy Media: `UC29ju8bIPH5as8OGnQzwJyA` ✅
- Theo - t3.gg: `UCbRP3c757lWg9M-U7TyEkXA` ✅
- Ben Awad: `UC-8QAzbLcRglXeN_MY9blyw` ✅

## 🔍 **How to Find Correct Channel IDs:**

### Method 1: YouTube Channel Page Source
1. Go to the YouTube channel (e.g., `youtube.com/@anthropic`)
2. Right-click → View Page Source
3. Search for: `"channelId":"UC`
4. Copy the full ID: `UC...` (24 characters total)

### Method 2: YouTube URL Inspector
1. Go to any video from the channel
2. Right-click → View Page Source  
3. Search for: `"channelId":"UC`
4. This will show the correct channel ID

### Method 3: Browser Console
1. Go to the YouTube channel page
2. Open Developer Tools (F12)
3. Go to Console tab
4. Paste this code:
```javascript
document.documentElement.innerHTML.match(/"channelId":"(UC[^"]+)"/)?.[1]
```
5. Press Enter - it will return the channel ID

## 🎯 **Channels That Need Fixing:**

### High Priority (AI Companies):
- **Anthropic** - Check: `youtube.com/@anthropic`
- **OpenAI** - Check: `youtube.com/@openai` 
- **Google DeepMind** - Check: `youtube.com/@googledeepmind`
- **Hugging Face** - Check: `youtube.com/@huggingface`

### Medium Priority (AI News):
- **Matthew Berman** - Check: `youtube.com/@matthew_berman`
- **The AI Advantage** - Check: `youtube.com/@theaiadvantage`
- **Wes Roth** - Check: `youtube.com/@wesroth`

### Tech Companies:
- **Vercel** - Check: `youtube.com/@vercel`
- **Supabase** - Check: `youtube.com/@supabase`

## 🚀 **Quick Fix Process:**

1. **Test each channel RSS feed:**
```bash
# Test format: https://www.youtube.com/feeds/videos.xml?channel_id=UC...
curl "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA"
```

2. **If 404 error, get correct ID:**
   - Visit channel page
   - Use Method 1, 2, or 3 above
   - Update config.ts

3. **Update config.ts with correct IDs**

## 📋 **Verification Checklist:**

Create this script to test all channels:

```javascript
// test-channels.js
const channels = [
  { id: 'UCJmJgKCYrNvK3pgIgLyC4aQ', name: 'Anthropic' },
  { id: 'UCXZCJLdBC09xxGZ6gcdrc6A', name: 'OpenAI' },
  // ... all your channels
];

async function testChannel(channel) {
  const url = `https://www.youtube.com/feeds/videos.xml?channel_id=${channel.id}`;
  try {
    const response = await fetch(url);
    console.log(`${channel.name}: ${response.status === 200 ? '✅' : '❌'}`);
  } catch (error) {
    console.log(`${channel.name}: ❌ Error`);
  }
}

channels.forEach(testChannel);
```

## 🔧 **Common Issues:**

1. **Custom URLs vs Channel IDs:**
   - `youtube.com/@username` ≠ channel ID
   - Must find the actual `UC...` ID

2. **Old vs New URLs:**
   - Some channels changed their URLs
   - Always verify with recent video

3. **Private/Deleted Channels:**
   - Some channels may no longer exist
   - Remove from config if confirmed deleted

## ✅ **Next Steps:**

1. Run through the high-priority channels first
2. Get correct IDs for Anthropic, OpenAI, Matthew Berman
3. Test each new ID with RSS feed
4. Update config.ts with working IDs
5. Remove any channels that no longer exist

This will fix your scraper and ensure you get content from all the channels you want!