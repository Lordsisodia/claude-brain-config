# Admin Dashboard Flow Documentation

## Table of Contents
1. [Authentication Flow](#authentication-flow)
2. [Admin Pages Structure](#admin-pages-structure)
3. [Component Dependencies](#component-dependencies)
4. [Database Schema](#database-schema)
5. [Automation Systems](#automation-systems)
6. [Critical vs Optional Features](#critical-vs-optional-features)

---

## Authentication Flow

### 1. Login Process
```
/auth → Supabase Auth → Check user_roles → Redirect to /admin
```

**Components:**
- `AuthGuard` - Protects admin routes with `adminOnly={true}`
- `useAdminCheck` hook - Validates admin status via RPC
- Auto-redirect from `/home` to `/admin` for admin users

**Database:**
- `user_roles` table with enum: 'admin' | 'client'
- RPC function: `is_admin` for role verification

---

## Admin Pages Structure

### Core Navigation (/admin)
```
Admin Dashboard
├── Overview (Main Dashboard)
├── Clients
├── Teams  
├── Projects
├── Automation
├── Business Tools
└── Partnership
```

### 1. Main Dashboard (`/admin`)
**Purpose:** Central command center with metrics and quick actions

**Components:**
- `AdminDashboard.tsx` - Main container
- Three tabs: Overview, Project Tasks, Reports
- Real-time metrics from `agency_metrics` table

**Features:**
- Client statistics
- Task analytics
- Revenue tracking
- Team performance

### 2. Client Management (`/admin/clients`)
**Purpose:** Complete client lifecycle management

**Pages:**
- `/admin/clients` - Client list with table/card views
- `/admin/clients/:id` - Individual client details
- `/admin/outreach` - Instagram lead management

**Components:**
- `components/admin/clients/ClientsView.tsx`
- `components/admin/clients/ClientDetail.tsx`
- Table with sorting, filtering, bulk actions

**Database:**
- `client_onboarding` - Main client data
- `projects` - Client projects
- `instagram_leads` - Lead tracking

### 3. Team Operations
**Purpose:** Team and task management

**Pages:**
- `/admin/teams` - Team overview
- `/admin/teams/:id` - Team member tasks
- `/admin/tasks` - Global task management

**Features:**
- Task assignment
- Progress tracking
- Time entries
- Performance metrics

**Database:**
- `tasks` table with categories
- `subtasks` for detailed tracking
- `time_entries` for time tracking

### 4. Project Management
**Purpose:** Project planning and design tools

**Pages:**
- `/admin/plans` - Plan templates
- `/admin/wireframes` - Design tools
- `/admin/user-flow` - User flow builder

**Components:**
- Plan builder with drag-drop
- Wireframe editor
- Flow diagram tools

### 5. Automation Hub (`/admin/automation`)
**Purpose:** AI-powered automation center

**Features:**
- Task automation dashboard
- Rate limit monitoring
- Queue management
- Token usage tracking

**Components:**
- `AutomationDashboard.tsx`
- `TaskQueue.tsx`
- `RateLimitStatus.tsx`

**Services:**
- `TaskManagementAgent.ts`
- `ProjectBasedTaskAgent.ts`
- `aiTaskAgent.ts`

### 6. Business Tools
**Pages:**
- `/admin/daily-planner` - AI-powered daily planning
- `/admin/lifelock` - Time tracking system
- `/admin/payments` - Financial management

**Database:**
- `daily_tracker_tasks`
- `lifelock_tasks`
- `financial_transactions`

### 7. Partnership Management (`/admin/partnership`)
**Purpose:** Complete partner program administration

**Features:**
- Partner dashboard
- Commission tracking
- Training materials
- Performance analytics

---

## Component Dependencies

### Critical Component Tree
```
App.tsx
└── Router
    └── AuthGuard (adminOnly={true})
        └── AdminLayout
            ├── AdminSidebar
            ├── AdminHeader
            └── [Admin Pages]
```

### Shared Admin Components
- `components/admin/shared/AdminLayout.tsx`
- `components/admin/shared/AdminSidebar.tsx`
- `components/admin/shared/MetricCard.tsx`
- `components/admin/shared/DataTable.tsx`

---

## Database Schema

### Core Admin Tables
```sql
-- Essential for admin functionality
user_roles (user_id, role)
profiles (id, full_name, role)
client_onboarding (id, company_name, status)
projects (id, client_id, name)
tasks (id, project_id, title, category)

-- Automation & metrics
automation_tasks (id, type, status)
agency_metrics (id, metric_type, value)
automation_rate_limits (service, limit)

-- Business operations
daily_tracker_tasks (id, task, date)
lifelock_tasks (id, title, time_entries)
financial_transactions (id, type, amount)
```

---

## Automation Systems

### 1. Claude Code Automation Engine
**Location:** `services/claude-workflow-engine.ts`
**Purpose:** Orchestrates AI-powered workflows

### 2. Task Management Agents
**Files:**
- `TaskManagementAgent.ts` - Main task automation
- `ProjectBasedTaskAgent.ts` - Project organization
- `aiTaskAgent.ts` - AI task generation

### 3. Daily Planning AI
**File:** `dailyTrackerAI.ts`
**Purpose:** Automated daily planning and prioritization

### 4. Multi-Stage Prompt System
**File:** `multiStagePromptSystem.ts`
**Purpose:** Complex AI task processing

---

## Critical vs Optional Features

### 🔴 Critical (Must Have)
1. **Authentication System**
   - Supabase auth
   - Role-based access
   - Admin route protection

2. **Core Admin Pages**
   - Main dashboard
   - Client management
   - Team/task management
   - Basic project tracking

3. **Database Essentials**
   - User roles
   - Client data
   - Projects
   - Tasks

### 🟡 Optional (Nice to Have)
1. **Advanced Features**
   - AI automation
   - Daily planner
   - Life Lock system
   - Financial tracking

2. **Design Tools**
   - Wireframe builder
   - User flow designer
   - Plan templates

3. **Partnership System**
   - Partner management
   - Commission tracking
   - Training hub

### 🟢 Progressive Enhancement
Start with critical features and add:
1. Basic automation
2. Advanced analytics
3. AI features
4. Business tools
5. Full partnership system

---

## Usage Patterns

### Minimal Admin Setup
```typescript
// Just need these routes active:
/auth
/admin (dashboard)
/admin/clients
/admin/teams
/admin/tasks
```

### Full Feature Setup
```typescript
// All routes including:
/admin/automation
/admin/daily-planner
/admin/partnership/*
/admin/wireframes
// etc.
```

---

## Notes for Future Development

1. **Modularity**: Each admin section is self-contained and can be disabled by removing routes
2. **Database**: Most features have dedicated tables that can be ignored if not used
3. **Components**: Unused components are tree-shaken in production builds
4. **Services**: AI services only initialize when features are accessed
5. **Scalability**: Start minimal and add features as needed

---

*Generated: October 2024*
*Purpose: Reference for understanding admin dashboard architecture*