**Purpose**: Supabase Database Health Check and Optimization

---

@include shared/universal-constants.yml#Universal_Legend

## Command Execution
Execute: immediate. --plan→show plan first
Legend: Generated based on symbols used in command
Purpose: "[Database Health Analysis] in $ARGUMENTS"

Comprehensive database health monitoring and optimization specifically designed for the SISO Agency Platform's 70+ table Supabase architecture.

@include shared/flag-inheritance.yml#Universal_Always

Examples:
- `/db-health --check` - Basic health assessment
- `/db-health --rls` - RLS policy analysis
- `/db-health --optimize` - Performance optimization
- `/db-health --security` - Security audit

## Database Health Analysis Modes

**--check:** Complete database health assessment
- Table relationship analysis across 70+ tables
- Index performance evaluation
- Query execution plan analysis
- Connection pool health monitoring
- Migration status verification

**--rls:** Row Level Security policy optimization
- RLS policy effectiveness analysis
- Security gap identification
- Performance impact assessment
- Policy recommendation generation
- Access pattern optimization

**--optimize:** Performance optimization analysis
- Slow query identification and optimization
- Index usage analysis and recommendations
- Table size and growth pattern analysis
- Connection optimization suggestions
- Caching strategy recommendations

**--security:** Database security audit
- Authentication and authorization review
- Data encryption validation
- Access control verification
- Sensitive data exposure analysis
- Compliance requirement checking

**--migration:** Migration analysis and planning
- Pending migration impact assessment
- Data integrity validation
- Rollback strategy verification
- Performance impact prediction
- Dependency analysis

## SISO Platform Specific Database Features

**Agency Data Architecture:**
- Client onboarding data flow analysis
- Instagram lead data integrity validation
- Financial transaction security review
- Project portfolio data optimization
- User engagement metrics analysis

**Critical Table Monitoring:**
- `client_onboarding` - Multi-step progress validation
- `instagram_leads` - Lead generation performance
- `financial_transactions` - Payment security audit
- `portfolio_items` - Project showcase optimization
- `tasks` - Task management efficiency

**Performance Critical Queries:**
- Client dashboard data aggregation
- Instagram lead filtering and sorting
- Financial reporting query optimization
- Task assignment and tracking
- User authentication and session management

## MCP Integration for Database Operations

**Supabase MCP Integration:**
- Real-time database metrics monitoring
- Automated RLS policy analysis
- Query performance profiling
- Migration impact assessment
- Type safety validation

**Sequential MCP for Complex Analysis:**
- Multi-table relationship analysis
- Complex performance bottleneck identification
- Security threat modeling
- Architectural improvement recommendations
- Migration strategy planning

**Desktop Commander for Database Files:**
- Migration file organization
- SQL script validation
- Backup file management
- Database documentation generation
- Schema change tracking

## Automated Health Check Workflows

**Daily Health Check:**
`/db-health --check --supabase --seq`
- Automated health metrics collection
- Performance baseline comparison
- Security posture assessment
- Issue prioritization and alerting

**RLS Policy Audit:**
`/db-health --rls --security --supabase --seq`
- Comprehensive RLS policy analysis
- Security gap identification
- Performance impact evaluation
- Optimization recommendations

**Performance Optimization:**
`/db-health --optimize --supabase --seq --desktop`
- Query performance analysis
- Index optimization recommendations
- Table structure improvements
- Caching strategy validation

**Pre-Migration Validation:**
`/db-health --migration --supabase --seq --comprehensive`
- Migration impact analysis
- Data integrity verification
- Performance regression prediction
- Rollback strategy validation

## Critical Monitoring Areas

**Data Integrity Validation:**
- Foreign key constraint verification
- Data consistency across related tables
- Orphaned record identification
- Referential integrity maintenance

**Performance Bottlenecks:**
- Slow query identification
- Index usage optimization
- Connection pool utilization
- Query execution plan analysis

**Security Vulnerabilities:**
- RLS policy gap analysis
- Unauthorized access pattern detection
- Data exposure risk assessment
- Compliance requirement validation

**Scalability Assessment:**
- Table growth pattern analysis
- Query performance under load
- Connection scaling recommendations
- Resource utilization optimization

## Intelligent Alerting and Reporting

**Health Score Calculation:**
- Composite health metrics generation
- Trend analysis and forecasting
- Threshold-based alerting
- Performance degradation detection

**Automated Recommendations:**
- Index creation suggestions
- Query optimization proposals
- RLS policy improvements
- Migration planning guidance

**Compliance Reporting:**
- Security audit trail generation
- Performance benchmark tracking
- Data governance compliance
- Regulatory requirement validation

## Integration with Development Workflow

**Pre-Commit Hooks:**
- Migration validation before deployment
- RLS policy testing automation
- Performance regression detection
- Security vulnerability scanning

**CI/CD Pipeline Integration:**
- Automated health checks in deployment pipeline
- Performance baseline validation
- Security compliance verification
- Migration success confirmation

**Development Environment Sync:**
- Local database health monitoring
- Development data integrity validation
- Test environment performance parity
- Schema synchronization verification

@include shared/security-patterns.yml#Database_Security

@include shared/hybrid-mcp-patterns.yml#Database_Operations

@include shared/universal-constants.yml#Standard_Messages_Templates