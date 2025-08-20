#!/bin/bash

# Claude Brain Config - New Device Setup Script
# Automatically sets up claude-brain-config on any new Mac/Linux device

set -e

# Configuration
REPO_URL="https://github.com/Lordsisodia/claude-brain-config.git"
DEFAULT_INSTALL_DIR="$HOME/DEV/claude-brain-config"
CLAUDE_CONFIG_DIR="$HOME/.claude"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}🧠 Claude Brain Config - New Device Setup${NC}"
    echo -e "${BLUE}===========================================${NC}"
    echo ""
}

# Function to check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install git first."
        exit 1
    fi
    print_status "Git found: $(git --version)"
    
    # Check if gh CLI is installed
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI not found. Installing..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            if command -v brew &> /dev/null; then
                brew install gh
            else
                print_error "Homebrew not found. Please install GitHub CLI manually: https://cli.github.com/"
                exit 1
            fi
        else
            print_error "Please install GitHub CLI: https://cli.github.com/"
            exit 1
        fi
    fi
    print_status "GitHub CLI found: $(gh --version | head -1)"
    
    # Check if logged into GitHub
    if ! gh auth status &> /dev/null; then
        print_warning "Not logged into GitHub CLI. Please login..."
        gh auth login
    fi
    print_status "GitHub CLI authenticated"
}

# Function to setup directory structure
setup_directories() {
    print_info "Setting up directory structure..."
    
    # Create DEV directory if it doesn't exist
    local dev_dir="$(dirname "$DEFAULT_INSTALL_DIR")"
    if [[ ! -d "$dev_dir" ]]; then
        mkdir -p "$dev_dir"
        print_status "Created DEV directory: $dev_dir"
    fi
    
    # Create Claude config directory
    if [[ ! -d "$CLAUDE_CONFIG_DIR" ]]; then
        mkdir -p "$CLAUDE_CONFIG_DIR"
        print_status "Created Claude config directory: $CLAUDE_CONFIG_DIR"
    fi
}

# Function to clone repository
clone_repository() {
    print_info "Cloning Claude Brain Config repository..."
    
    if [[ -d "$DEFAULT_INSTALL_DIR" ]]; then
        print_warning "Directory already exists. Updating..."
        cd "$DEFAULT_INSTALL_DIR"
        git pull origin main
    else
        git clone "$REPO_URL" "$DEFAULT_INSTALL_DIR"
        print_status "Repository cloned to: $DEFAULT_INSTALL_DIR"
    fi
    
    cd "$DEFAULT_INSTALL_DIR"
}

# Function to setup Claude global config integration
setup_claude_integration() {
    print_info "Setting up Claude global config integration..."
    
    # Create symlink for CLAUDE.md
    local claude_md_source="$DEFAULT_INSTALL_DIR/templates/claude-code-guide.md"
    local claude_md_target="$CLAUDE_CONFIG_DIR/CLAUDE.md"
    
    # Check if templates exist, create if not
    if [[ ! -f "$claude_md_source" ]]; then
        print_info "Creating Claude Code guide template..."
        mkdir -p "$(dirname "$claude_md_source")"
        cat > "$claude_md_source" << 'EOF'
# Claude Brain Config - Global Configuration

This file is automatically synchronized with your Claude Brain Config system.

## Auto-Include Core Intelligence
@include ../shared/superclaude-core.yml#Core_Philosophy
@include ../shared/musk-algorithm-core.yml#Musk_Algorithm_Core_Thinking
@include ../shared/task-intelligence-system.yml#Intelligent_Task_Analysis
@include ../shared/mcp-intelligence-system.yml#MCP_Intelligence_Core

## Enhanced Capabilities
- Multi-agent orchestration
- Advanced reasoning patterns
- Intelligent task decomposition
- Real-time sync with GitHub

## Sync Status
Last updated: $(date)
Repository: https://github.com/Lordsisodia/claude-brain-config
EOF
    fi
    
    # Create symlink or copy file
    if [[ -L "$claude_md_target" ]]; then
        print_warning "CLAUDE.md symlink already exists"
    elif [[ -f "$claude_md_target" ]]; then
        print_warning "CLAUDE.md file exists. Creating backup..."
        cp "$claude_md_target" "$claude_md_target.backup.$(date +%Y%m%d-%H%M%S)"
        ln -sf "$claude_md_source" "$claude_md_target"
        print_status "Created symlink: $claude_md_target -> $claude_md_source"
    else
        ln -sf "$claude_md_source" "$claude_md_target"
        print_status "Created symlink: $claude_md_target -> $claude_md_source"
    fi
    
    # Setup settings.json integration
    local settings_source="$DEFAULT_INSTALL_DIR/settings.hooks.json"
    local settings_target="$CLAUDE_CONFIG_DIR/settings.json"
    
    if [[ -f "$settings_source" ]]; then
        if [[ -f "$settings_target" ]]; then
            print_warning "settings.json exists. Creating backup..."
            cp "$settings_target" "$settings_target.backup.$(date +%Y%m%d-%H%M%S)"
        fi
        ln -sf "$settings_source" "$settings_target"
        print_status "Created symlink: $settings_target -> $settings_source"
    fi
}

# Function to setup auto-sync
setup_auto_sync() {
    print_info "Setting up auto-sync system..."
    
    # Make scripts executable
    chmod +x "$DEFAULT_INSTALL_DIR/scripts/"*.sh
    print_status "Made scripts executable"
    
    # Setup cron job
    local cron_command="*/15 * * * * cd '$DEFAULT_INSTALL_DIR' && '$DEFAULT_INSTALL_DIR/scripts/auto-sync-local.sh' >> '$DEFAULT_INSTALL_DIR/logs/auto-sync.log' 2>&1"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "auto-sync-local.sh"; then
        print_warning "Auto-sync cron job already exists"
    else
        print_info "Adding auto-sync cron job (every 15 minutes)..."
        (crontab -l 2>/dev/null || echo "") | grep -v "auto-sync-local.sh" | { cat; echo "$cron_command"; } | crontab -
        print_status "Auto-sync cron job added"
    fi
    
    # Create logs directory
    mkdir -p "$DEFAULT_INSTALL_DIR/logs"
    
    # Test auto-sync
    print_info "Testing auto-sync functionality..."
    "$DEFAULT_INSTALL_DIR/scripts/auto-sync-local.sh"
    print_status "Auto-sync test completed"
}

# Function to setup shell aliases
setup_shell_aliases() {
    print_info "Setting up shell aliases..."
    
    local shell_rc=""
    if [[ "$SHELL" == *"zsh"* ]]; then
        shell_rc="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        shell_rc="$HOME/.bashrc"
    fi
    
    if [[ -n "$shell_rc" ]]; then
        local alias_block="# Claude Brain Config Aliases
alias brain-sync='$DEFAULT_INSTALL_DIR/scripts/auto-sync-local.sh'
alias brain-dashboard='$DEFAULT_INSTALL_DIR/scripts/brain-sync-monitor.sh --dashboard'
alias brain-monitor='$DEFAULT_INSTALL_DIR/scripts/brain-sync-monitor.sh --monitor'
alias brain-config='cd $DEFAULT_INSTALL_DIR'
alias claude-brain='$DEFAULT_INSTALL_DIR/scripts/brain-sync-monitor.sh'"
        
        if ! grep -q "Claude Brain Config Aliases" "$shell_rc" 2>/dev/null; then
            echo "" >> "$shell_rc"
            echo "$alias_block" >> "$shell_rc"
            print_status "Added shell aliases to $shell_rc"
        else
            print_warning "Shell aliases already exist in $shell_rc"
        fi
    fi
}

# Function to create desktop shortcuts (macOS)
create_desktop_shortcuts() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "Creating desktop shortcuts..."
        
        local desktop_dir="$HOME/Desktop"
        
        # Claude Brain Dashboard shortcut
        cat > "$desktop_dir/Claude Brain Dashboard.command" << EOF
#!/bin/bash
cd "$DEFAULT_INSTALL_DIR"
./scripts/brain-sync-monitor.sh --dashboard
read -p "Press Enter to close..."
EOF
        chmod +x "$desktop_dir/Claude Brain Dashboard.command"
        
        # Claude Brain Sync shortcut  
        cat > "$desktop_dir/Claude Brain Sync.command" << EOF
#!/bin/bash
cd "$DEFAULT_INSTALL_DIR"
./scripts/auto-sync-local.sh
read -p "Press Enter to close..."
EOF
        chmod +x "$desktop_dir/Claude Brain Sync.command"
        
        print_status "Created desktop shortcuts"
    fi
}

# Function to display completion summary
show_completion_summary() {
    print_header
    echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}📁 Installation Directory:${NC} $DEFAULT_INSTALL_DIR"
    echo -e "${BLUE}🔗 Repository:${NC} $REPO_URL"
    echo -e "${BLUE}⚙️ Claude Config:${NC} $CLAUDE_CONFIG_DIR"
    echo ""
    echo -e "${YELLOW}🚀 Quick Commands:${NC}"
    echo "  brain-sync              # Run manual sync"
    echo "  brain-dashboard         # View sync dashboard" 
    echo "  brain-monitor           # Start real-time monitoring"
    echo "  brain-config            # Go to config directory"
    echo ""
    echo -e "${YELLOW}🔄 Auto-Sync Status:${NC}"
    echo "  • Runs every 15 minutes automatically"
    echo "  • GitHub Actions sync every 30 minutes"
    echo "  • Real-time file monitoring available"
    echo ""
    echo -e "${YELLOW}📋 Next Steps:${NC}"
    echo "  1. Restart your terminal to load aliases"
    echo "  2. Run 'brain-dashboard' to check sync status"
    echo "  3. Your Claude configurations are now globally linked"
    echo "  4. All changes sync automatically across devices"
    echo ""
    echo -e "${GREEN}✨ Claude Brain Config is now active on this device!${NC}"
    echo ""
}

# Main setup function
main() {
    print_header
    
    # Get custom install directory if provided
    if [[ -n "$1" ]]; then
        DEFAULT_INSTALL_DIR="$1"
    fi
    
    print_info "Installing to: $DEFAULT_INSTALL_DIR"
    
    # Run setup steps
    check_prerequisites
    setup_directories
    clone_repository
    setup_claude_integration
    setup_auto_sync
    setup_shell_aliases
    create_desktop_shortcuts
    
    show_completion_summary
}

# Handle script arguments
case "$1" in
    --help)
        echo "Claude Brain Config - New Device Setup"
        echo ""
        echo "Usage: $0 [INSTALL_DIRECTORY]"
        echo ""
        echo "Arguments:"
        echo "  INSTALL_DIRECTORY    Custom installation directory (default: ~/DEV/claude-brain-config)"
        echo ""
        echo "Options:"
        echo "  --help              Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                                    # Install to default location"
        echo "  $0 ~/Projects/claude-brain-config    # Install to custom location"
        echo ""
        echo "What this script does:"
        echo "  1. Clones the Claude Brain Config repository"
        echo "  2. Sets up automatic GitHub syncing (every 15 minutes)"
        echo "  3. Links Claude global configuration files"
        echo "  4. Creates shell aliases and desktop shortcuts"
        echo "  5. Configures real-time monitoring"
        ;;
    *)
        main "$@"
        ;;
esac