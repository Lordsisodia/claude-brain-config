# 🤖 Telegram Optimizer Notification Setup

## Quick Setup (5 minutes)

### 1. Create Your Telegram Bot
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` 
3. Choose a name (e.g., "Claude Optimizer Bot")
4. Choose a username (e.g., `claude_optimizer_bot`)
5. **Save the bot token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Get Your Chat ID
1. Start a chat with your new bot
2. Send any message to it
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat ID in the response (looks like: `123456789`)

### 3. Configure the Script

Option A - Edit the script directly:
```bash
nano ~/.claude/scripts/telegram-optimizer-notifier.sh
# Replace YOUR_BOT_TOKEN_HERE and YOUR_CHAT_ID_HERE
```

Option B - Use environment variables:
```bash
# Add to ~/.zshrc or ~/.bashrc
export TELEGRAM_BOT_TOKEN="your_actual_bot_token"
export TELEGRAM_CHAT_ID="your_actual_chat_id"
```

### 4. Start the Notifier
```bash
# Run in background
~/.claude/scripts/telegram-optimizer-notifier.sh &

# Or in a dedicated terminal
~/.claude/scripts/telegram-optimizer-notifier.sh
```

### 5. Test It!
```bash
# Trigger a test optimization
~/.claude/scripts/openai-prompt-optimizer-gpt5.sh "test telegram notifications"
```

## What You'll Receive

Every time ANY optimizer runs, you'll get a Telegram message with:
- 🧠 Which agent optimized the prompt
- ⏰ Timestamp
- 📊 Expansion percentage
- 📝 Original prompt preview
- #️⃣ Hashtags for filtering

## Monitored Agents
- GPT-5 Optimizer
- Standard OpenAI Optimizer
- Prompt Enhancer
- Security Validator
- Intelligent Session
- Any new agents added to the system!

## Advanced Features

### Auto-start on Login
Add to your shell profile:
```bash
# ~/.zshrc or ~/.bashrc
~/.claude/scripts/telegram-optimizer-notifier.sh > /dev/null 2>&1 &
```

### View History
```bash
cat ~/.claude/telegram-notifications/history.log
```

### Stop Notifications
```bash
pkill -f telegram-optimizer-notifier
```

## Troubleshooting
- Make sure bot token and chat ID are correct
- Check if the script is running: `ps aux | grep telegram-optimizer`
- View logs: `tail -f ~/.claude/logs/*.log`