**Purpose**: SISO Agency Platform Daily Development Workflow

---

@include shared/universal-constants.yml#Universal_Legend

## Command Execution
Execute: immediate. --plan→show plan first
Legend: Generated based on symbols used in command
Purpose: "[Daily SISO Development Workflow] in $ARGUMENTS"

Daily development workflow automation for the SISO Agency Onboarding Platform, optimized for agency-specific needs.

@include shared/flag-inheritance.yml#Universal_Always

Examples:
- `/siso-daily --health` - Daily health check
- `/siso-daily --dev` - Development session setup
- `/siso-daily --security` - Security audit routine

## SISO-Specific Workflow Modes

**--health:** Daily platform health check
- Database architecture review (70+ tables)
- RLS policy validation and optimization
- Supabase connection and performance check
- Component dependency analysis
- Build configuration validation

**--dev:** Development session preparation
- Clean build artifacts and temp files
- Update dependencies and security patches
- Generate fresh TypeScript types from Supabase
- Component architecture validation
- Development environment setup

**--security:** Agency security compliance check
- Client data protection audit
- Financial transaction security review
- Instagram lead data privacy validation
- Authentication flow security testing
- OWASP compliance verification

**--deploy:** Pre-deployment validation
- Full test suite execution
- Performance benchmarking
- Security vulnerability scan
- Database migration validation
- Production readiness check

## MCP Integration for SISO Platform

**Supabase MCP Integration:**
- Real-time database health monitoring
- RLS policy optimization recommendations
- Query performance analysis
- Migration impact assessment
- Type generation and validation

**Magic MCP for UI Development:**
- Agency-specific component generation
- Client onboarding UI optimization
- Instagram lead management interfaces
- Dashboard component creation
- Responsive design validation

**Desktop Commander for Project Management:**
- Large codebase organization (7,965 files)
- Dependency cleanup and optimization
- File structure analysis and recommendations
- Build artifact management
- Performance monitoring

## Intelligent Automation Workflows

**Morning Routine:**
`/siso-daily --health --supabase --desktop`
- Database health check with Supabase MCP
- File organization analysis
- Dependency vulnerability scan
- Performance baseline establishment

**Development Session:**
`/siso-daily --dev --magic --supabase --seq`
- Fresh environment setup
- Component development ready
- Database types synchronized
- AI-assisted architecture review

**Security Audit:**
`/siso-daily --security --comprehensive --seq --supabase --pup`
- Multi-layer security analysis
- Client data protection verification
- Automated penetration testing
- Compliance reporting

**Pre-Deployment:**
`/siso-daily --deploy --all-mcp --comprehensive`
- Complete system validation
- Performance optimization
- Security clearance
- Production readiness

## SISO Platform Specific Features

**Client Onboarding Optimization:**
- Multi-step onboarding component analysis
- Document management security review
- User experience flow validation
- Performance optimization recommendations

**Instagram Lead Management:**
- Lead generation code security audit
- Data privacy compliance checking
- API integration performance analysis
- Automation workflow optimization

**Agency Dashboard Enhancement:**
- Performance metrics analysis
- Component rendering optimization
- Data visualization improvements
- User engagement tracking

**Financial Transaction Security:**
- Payment processing security audit
- Invoice management validation
- Financial data encryption verification
- Compliance reporting automation

## Auto-Detection and Smart Workflows

**Project Context Awareness:**
- Detect current working area (Admin, Client, Partner portals)
- Automatically select relevant MCP combinations
- Adapt security focus based on data sensitivity
- Optimize performance checks for current component

**Git Hook Integration:**
- Pre-commit security scanning
- Automated component testing
- Database migration validation
- Performance regression detection

**Intelligent Reporting:**
- Daily health summary generation
- Performance trend analysis
- Security compliance tracking
- Development velocity metrics

## Quality Gates and Validation

**Critical Path Validation:**
- Client onboarding flow integrity
- Payment processing security
- Instagram lead data protection
- User authentication robustness

**Performance Benchmarks:**
- Component rendering performance
- Database query optimization
- API response time validation
- Bundle size monitoring

**Security Compliance:**
- GDPR compliance for client data
- Financial data protection standards
- Instagram API usage compliance
- User privacy protection validation

@include shared/research-patterns.yml#Mandatory_Research_Flows

@include shared/hybrid-mcp-patterns.yml#Full_Stack_Development

@include shared/universal-constants.yml#Standard_Messages_Templates