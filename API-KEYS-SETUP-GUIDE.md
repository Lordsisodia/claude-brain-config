# 🔑 Complete API Keys Setup Guide - Make Your MCPs Fully Functional

## 🚨 **Required API Keys by Template:**

### **🎯 Most Important (Get These First):**
1. **GitHub Personal Access Token** - Used in almost every template
2. **Brave Search API Key** - For web search capabilities  
3. **Supabase URL + Anon Key** - For database operations

---

## 📋 **Complete API Key List:**

### **🔧 Development & Code Management:**
| Service | Where to Get | Environment Variable | Used In Templates |
|---------|--------------|---------------------|-------------------|
| **GitHub** | [GitHub Settings → Developer → Personal Access Tokens](https://github.com/settings/tokens) | `GITHUB_PERSONAL_ACCESS_TOKEN` | All development templates |
| **Supabase** | Supabase Dashboard → Settings → API | `SUPABASE_URL`<br>`SUPABASE_ANON_KEY` | All database templates |

### **🔍 Search & Research:**
| Service | Where to Get | Environment Variable | Used In Templates |
|---------|--------------|---------------------|-------------------|
| **Brave Search** | [Brave Search API](https://api.search.brave.com/register) | `BRAVE_SEARCH_API_KEY` | AI intelligence templates |
| **Exa Search** | [Exa.ai API](https://exa.ai/api) | `EXA_API_KEY` | Ultimate development |

### **🎨 Design & UI:**
| Service | Where to Get | Environment Variable | Used In Templates |
|---------|--------------|---------------------|-------------------|
| **Figma** | [Figma Settings → Personal Access Tokens](https://www.figma.com/developers/api#access-tokens) | `FIGMA_ACCESS_TOKEN` | UI frontend templates |
| **Canva** | [Canva Developers](https://www.canva.com/developers/) | `CANVA_API_KEY` | UI frontend templates |
| **Miro** | [Miro Developer Platform](https://developers.miro.com/) | `MIRO_ACCESS_TOKEN` | UI/Planning templates |

### **💬 Communication & Collaboration:**
| Service | Where to Get | Environment Variable | Used In Templates |
|---------|--------------|---------------------|-------------------|
| **Slack** | [Slack API → Your Apps](https://api.slack.com/apps) | `SLACK_BOT_TOKEN`<br>`SLACK_USER_TOKEN` | Communication templates |
| **Discord** | [Discord Developer Portal](https://discord.com/developers/applications) | `DISCORD_BOT_TOKEN` | Communication templates |
| **Microsoft Teams** | [Azure App Registration](https://portal.azure.com/) | `TEAMS_WEBHOOK_URL` | Enterprise templates |

### **📊 Project Management:**
| Service | Where to Get | Environment Variable | Used In Templates |
|---------|--------------|---------------------|-------------------|
| **Notion** | [Notion Integrations](https://www.notion.so/my-integrations) | `NOTION_API_KEY` | Enterprise/Planning templates |
| **Jira** | [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) | `JIRA_API_TOKEN`<br>`JIRA_SITE_URL` | Enterprise/Planning templates |
| **Linear** | [Linear Settings → API](https://linear.app/settings/api) | `LINEAR_API_KEY` | Planning templates |
| **Asana** | [Asana Developer Console](https://app.asana.com/0/my-apps) | `ASANA_ACCESS_TOKEN` | Planning templates |
| **ClickUp** | [ClickUp Apps](https://app.clickup.com/apps) | `CLICKUP_API_TOKEN` | Planning templates |
| **Todoist** | [Todoist App Console](https://todoist.com/app_console) | `TODOIST_API_TOKEN` | Planning templates |
| **Airtable** | [Airtable Account → API](https://airtable.com/create/tokens) | `AIRTABLE_API_KEY` | Enterprise templates |

### **☁️ Cloud & Infrastructure:**
| Service | Where to Get | Environment Variable | Used In Templates |
|---------|--------------|---------------------|-------------------|
| **AWS** | [AWS IAM Console](https://console.aws.amazon.com/iam/) | `AWS_ACCESS_KEY_ID`<br>`AWS_SECRET_ACCESS_KEY`<br>`AWS_REGION` | Backend/Enterprise templates |
| **Google Cloud** | [Google Cloud Console](https://console.cloud.google.com/) | `GOOGLE_SHEETS_API_KEY` | Enterprise templates |

### **🗄️ Databases:**
| Service | Where to Get | Environment Variable | Used In Templates |
|---------|--------------|---------------------|-------------------|
| **PostgreSQL** | Your database provider | `POSTGRES_CONNECTION_STRING` | Backend templates |
| **MongoDB** | [MongoDB Atlas](https://cloud.mongodb.com/) | `MONGODB_CONNECTION_STRING` | Backend templates |
| **Redis** | Your Redis provider | `REDIS_URL` | Backend templates |

---

## 🚀 **Quick Setup Process:**

### **1. Choose Your Template:**
```bash
setup-mcp enterprise-poweruser  # Most comprehensive
setup-mcp project-planning-powerhouse  # For PDR planning
setup-mcp ui-frontend-powerhouse  # For UI development
setup-mcp backend-developer-stack  # For backend work
```

### **2. Get Essential API Keys First:**
```bash
# Must-haves for any template:
1. GitHub Personal Access Token
2. Brave Search API Key  
3. Supabase URL + Anon Key

# Then add others based on your template
```

### **3. Edit Configuration:**
```bash
nano .claude.json
# Replace "your-api-key" with actual values
```

### **4. Test Setup:**
```bash
claude
/mcp  # Should show all connected tools
```

---

## 💡 **Pro Tips:**

### **Free Tiers Available:**
- ✅ **GitHub**: Free personal access tokens
- ✅ **Brave Search**: Free tier with 2000 queries/month
- ✅ **Supabase**: Free tier with 500MB database
- ✅ **Notion**: Free personal plan
- ✅ **Linear**: Free for small teams
- ✅ **Figma**: Free for 3 files

### **Priority Setup Order:**
1. **GitHub** (Essential for all development)
2. **Brave Search** (Essential for AI research)
3. **Supabase** (Essential for database work)
4. **Notion** (Essential for documentation)
5. **Slack** (Essential for team work)
6. **Project Management** (Jira/Linear/Asana - pick your primary)
7. **Design Tools** (Figma/Miro - if you do UI work)
8. **Cloud Services** (AWS/GCP - for deployment)

### **Security Best Practices:**
- 🔒 Use environment variables, never hardcode keys
- 🔄 Rotate tokens regularly
- 🎯 Use minimal permissions (read-only when possible)
- 📝 Document which keys are used where

---

## 🎯 **Template-Specific Minimums:**

### **For PDR Planning:**
- ✅ GitHub, Notion, Jira/Linear (choose one)
- ⏩ **Result**: AI can create PRDs, manage tasks, track progress

### **For UI Development:**
- ✅ GitHub, Figma, Brave Search
- ⏩ **Result**: AI can generate components, convert designs to code

### **For Backend Development:**
- ✅ GitHub, Supabase/PostgreSQL, AWS (optional)
- ⏩ **Result**: AI can manage databases, create APIs, deploy services

### **For Enterprise Teams:**
- ✅ GitHub, Slack, Notion, Jira, Figma
- ⏩ **Result**: Complete workflow from planning to deployment

**Start with your essential 3-5 keys and add more as needed!** 🚀