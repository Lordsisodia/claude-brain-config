# 🔄 Multi-Device Setup Guide

> **Sync Claude Brain Config across all your Macs automatically**

This guide shows you how to set up Claude Brain Config on multiple devices with automatic synchronization.

## 🚀 Quick Setup for New Device (Mac Mini)

### **One-Command Setup**
```bash
# Run this single command on your Mac Mini:
curl -fsSL https://raw.githubusercontent.com/Lordsisodia/claude-brain-config/main/setup-new-device.sh | bash
```

### **Manual Setup Steps**
If you prefer manual setup:

```bash
# 1. Clone the repository
cd ~/DEV  # or wherever you want to install
git clone https://github.com/Lordsisodia/claude-brain-config.git

# 2. Run setup script
cd claude-brain-config
./setup-new-device.sh

# 3. Setup global Claude integration
./scripts/claude-global-sync.sh

# 4. Test the setup
./scripts/brain-sync-monitor.sh --dashboard
```

## 🧠 Automatic Claude Global Config

### **How It Works**
The system automatically:
1. **Links** `~/.claude/CLAUDE.md` to your brain config
2. **Syncs** settings.json with advanced hooks
3. **Updates** configurations every 15 minutes
4. **Monitors** file changes in real-time
5. **Resolves** conflicts intelligently

### **Global Integration Commands**
```bash
# Check integration status
./scripts/claude-global-sync.sh --status

# Force update global config
./scripts/claude-global-sync.sh --force

# Test integration
./scripts/claude-global-sync.sh --test
```

## 📱 Device-Specific Setup

### **Mac Mini Setup**
```bash
# SSH into your Mac Mini
ssh username@mac-mini-ip

# Run the setup script
curl -fsSL https://raw.githubusercontent.com/Lordsisodia/claude-brain-config/main/setup-new-device.sh | bash

# Verify setup
brain-dashboard  # New alias available after setup
```

### **Multiple Macs Setup**
For each additional Mac:

1. **Install Prerequisites**
   ```bash
   # Install Homebrew if needed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install GitHub CLI
   brew install gh
   
   # Login to GitHub
   gh auth login
   ```

2. **Run Setup Script**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Lordsisodia/claude-brain-config/main/setup-new-device.sh | bash
   ```

3. **Verify Cross-Device Sync**
   ```bash
   brain-dashboard
   ```

## 🔄 Sync Behavior Across Devices

### **How Sync Works**
- **GitHub Actions**: Cloud sync every 30 minutes
- **Local Cron**: Device sync every 15 minutes  
- **Real-time**: File change detection
- **Conflict Resolution**: Automatic with backup branches

### **Sync Status Dashboard**
```bash
# View sync status on any device
brain-dashboard

# Manual sync trigger
brain-sync

# Real-time monitoring
brain-monitor
```

## 📁 File Structure After Setup

```
Device 1 (Main Mac):
~/DEV/claude-brain-config/        # Main repository
~/.claude/CLAUDE.md               # Symlink to brain config
~/.claude/settings.json           # Symlink to hooks

Device 2 (Mac Mini):
~/DEV/claude-brain-config/        # Synced repository
~/.claude/CLAUDE.md               # Symlink to brain config
~/.claude/settings.json           # Synlink to hooks

GitHub Repository:
https://github.com/Lordsisodia/claude-brain-config
├── Auto-sync every 30 minutes
├── Conflict resolution
└── Change tracking
```

## 🎯 Shell Aliases (Available on All Devices)

After setup, these aliases are available:

```bash
brain-sync              # Manual sync trigger
brain-dashboard         # View sync status dashboard
brain-monitor           # Real-time file monitoring
brain-config            # Navigate to config directory
claude-brain            # Full sync monitor
```

## 🛠 Troubleshooting

### **Common Issues & Solutions**

**Issue: Cron job not running**
```bash
# Check cron status
crontab -l

# Manually add if missing
echo "*/15 * * * * cd '$HOME/DEV/claude-brain-config' && '$HOME/DEV/claude-brain-config/scripts/auto-sync-local.sh' >> '$HOME/DEV/claude-brain-config/logs/auto-sync.log' 2>&1" | crontab -
```

**Issue: GitHub authentication failed**
```bash
# Re-authenticate GitHub CLI
gh auth login
gh auth refresh
```

**Issue: Symlinks broken**
```bash
# Fix Claude global config links
./scripts/claude-global-sync.sh --force
```

**Issue: Sync conflicts**
```bash
# View conflict resolution
./scripts/brain-sync-monitor.sh --check

# Manual conflict resolution
cd ~/DEV/claude-brain-config
git status
git pull origin main
```

## 📊 Monitoring & Logs

### **Log Locations**
```bash
# Auto-sync logs
tail -f ~/DEV/claude-brain-config/logs/auto-sync.log

# Global sync logs  
tail -f ~/DEV/claude-brain-config/logs/global-sync.log

# Monitoring logs
tail -f ~/DEV/claude-brain-config/logs/sync-monitor.log
```

### **Health Check Commands**
```bash
# Check all systems
./scripts/brain-sync-monitor.sh --check

# Test GitHub connectivity
curl -s https://api.github.com/repos/Lordsisodia/claude-brain-config

# Verify cron jobs
crontab -l | grep auto-sync
```

## 🔧 Customization Options

### **Custom Sync Intervals**
Edit sync intervals by modifying cron job:
```bash
# Edit cron for different interval (e.g., every 5 minutes)
crontab -e
# Change: */15 * * * * to */5 * * * *
```

### **Custom Install Directory**
```bash
# Install to custom location
./setup-new-device.sh ~/Projects/claude-brain-config
```

### **Selective Syncing**
Edit `.gitignore` to exclude certain files:
```bash
echo "logs/*.log" >> .gitignore
echo "cache/*" >> .gitignore
```

## 🌟 Advanced Features

### **Cross-Device Commands**
Run commands that sync across all devices:

```bash
# Add a new intelligence module (syncs everywhere)
echo "# New module" >> shared/custom-intelligence.yml
brain-sync  # Pushes to all devices

# Update global Claude config (affects all devices)
./scripts/claude-global-sync.sh --force
```

### **Device-Specific Configurations**
Create device-specific settings:

```bash
# Create device-specific config
hostname > device-configs/$(hostname).yml
git add device-configs/$(hostname).yml
brain-sync
```

## 🎉 Success Verification

### **Test Complete Setup**
Run this verification on each device:

```bash
# 1. Check repository sync
cd ~/DEV/claude-brain-config
git status
git log -1

# 2. Check global Claude integration
ls -la ~/.claude/CLAUDE.md
head -5 ~/.claude/CLAUDE.md

# 3. Check auto-sync
brain-dashboard

# 4. Test aliases
brain-sync
```

### **Expected Output**
- ✅ Repository cloned and up-to-date
- ✅ Claude global config linked
- ✅ Auto-sync running every 15 minutes
- ✅ Shell aliases working
- ✅ Dashboard showing sync status

## 📞 Support

### **Getting Help**
- **Dashboard**: Run `brain-dashboard` for status
- **Logs**: Check `logs/` directory for detailed info
- **GitHub Issues**: [Report problems](https://github.com/Lordsisodia/claude-brain-config/issues)
- **Re-run Setup**: `./setup-new-device.sh` is safe to run multiple times

---

**🧠 Your Claude Brain Config is now synchronized across all devices!**

*Changes made on any device automatically propagate to all others within 15-30 minutes.*