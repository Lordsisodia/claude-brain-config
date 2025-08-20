# Secure Multi-Account API Setup Instructions

## ⚠️ IMMEDIATE SECURITY ACTIONS

1. **REGENERATE EXPOSED KEYS NOW**
   - Go to https://console.groq.com and regenerate your Groq API key
   - Go to https://aistudio.google.com/apikey and regenerate your Gemini key
   - These keys have been exposed and could be compromised

## 🚀 Quick Start Setup

### 1. Install Dependencies
```bash
pip install python-dotenv aiohttp asyncio
```

### 2. Create Your .env File
```bash
# Copy the template
cp .env.example .env

# Edit .env and add your actual keys
# NEVER share or commit this file!
```

### 3. Team Member Setup
Have each team member:
1. Create their own account on each platform
2. Generate their API key
3. Send you ONLY the masked version for tracking (first 4 and last 4 chars)
4. They keep the full key secure

### 4. Run the Manager
```bash
python secure_multi_api_manager.py
```

## 📊 Current Capacity Calculator

Based on the providers and team size:

### Solo Developer (1 person)
```
Google Gemini:  6M tokens/day
Groq:          1M tokens/day
GitHub Models: 1M tokens/day
Total:         8M tokens/day
```

### Small Team (5 people)
```
Google Gemini:  30M tokens/day
Groq:           5M tokens/day
GitHub Models:  5M tokens/day
Total:         40M tokens/day
```

### Medium Team (10 people)
```
Google Gemini:  60M tokens/day
Groq:          10M tokens/day
GitHub Models: 10M tokens/day
Total:         80M tokens/day
```

### Large Team (50 people)
```
Google Gemini: 300M tokens/day
Groq:          50M tokens/day
GitHub Models: 50M tokens/day
Total:        400M tokens/day
```

## 🔑 Getting API Keys

### Google Gemini
1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key starting with "AIza..."

### Groq
1. Go to https://console.groq.com/keys
2. Click "Create API Key"
3. Copy the key starting with "gsk_"

### GitHub Models
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `read:packages`
4. Copy the token starting with "ghp_"

### Cerebras
1. Go to https://cloud.cerebras.ai/
2. Sign up for free account
3. Generate API key in dashboard

### OpenRouter
1. Go to https://openrouter.ai/
2. Sign up and add $10 credit
3. Get API key from settings

## 🛡️ Security Best Practices

### DO ✅
- Store keys in environment variables
- Use .gitignore to exclude .env files
- Rotate keys regularly
- Monitor usage for anomalies
- Use different emails for each account

### DON'T ❌
- Share keys in chat/email/slack
- Commit keys to git
- Use same key across multiple apps
- Share keys between team members
- Exceed rate limits

## 📈 Scaling Strategy

### Phase 1: Foundation (Week 1)
- Set up 5 team members
- Test with ~40M tokens/day
- Monitor for any issues

### Phase 2: Scale (Week 2)
- Add 5 more team members
- Reach ~80M tokens/day
- Implement monitoring dashboard

### Phase 3: Optimize (Week 3)
- Add academic accounts if eligible
- Optimize routing algorithms
- Add caching layer

### Phase 4: Production (Week 4)
- Scale to full team size
- Add paid tier overflow
- Deploy monitoring and alerts

## 🎯 Monitoring Dashboard

The manager provides real-time metrics:
- Total daily capacity
- Current usage per provider
- Per-key utilization
- Failure tracking
- Automatic recommendations

## 🚨 Troubleshooting

### "No available keys"
- Check daily limits haven't been exceeded
- Verify keys are valid
- Check rate limiting

### "API call failed"
- Verify key is active
- Check provider status page
- Review error logs

### "Rate limit exceeded"
- Reduce requests per minute
- Add more team members
- Implement request queuing

## 📝 Example Usage

```python
from secure_multi_api_manager import MultiAccountAPIManager
import asyncio

async def run_agents():
    manager = MultiAccountAPIManager()
    
    # Make a request with automatic key selection
    result = await manager.make_request(
        provider=Provider.GROQ,
        prompt="Write a business plan outline",
        max_tokens=2000
    )
    
    if result['success']:
        print(f"Success! Used {result['tokens_used']} tokens")
        print(f"Response: {result['response']}")
    else:
        print(f"Failed: {result['error']}")

asyncio.run(run_agents())
```

## 📊 Daily Operations

### Morning Checklist
1. Check usage summary
2. Verify all keys active
3. Review failure counts
4. Check remaining quotas

### Evening Review
1. Analyze usage patterns
2. Identify bottlenecks
3. Plan next day capacity
4. Rotate keys if needed

## 🎯 Goal Achievement

To reach **1 Billion tokens/day**:
- Need ~125 team members with current providers
- OR add academic credits (100M+ tokens)
- OR implement hybrid free+paid strategy

Current realistic target with 10-person team: **80-100M tokens/day**

## Need Help?

Common issues and solutions:
1. **Keys not loading**: Check .env file format
2. **Rate limits hit**: Add delays between requests
3. **Provider down**: System auto-fails over to backup

Remember: **NEVER SHARE REAL API KEYS** - Only use environment variables!