**Purpose**: SISO Agency Component Development and Testing Workflow

---

@include shared/universal-constants.yml#Universal_Legend

## Command Execution
Execute: immediate. --plan→show plan first
Legend: Generated based on symbols used in command
Purpose: "[Component Development] in $ARGUMENTS"

Streamlined component development workflow optimized for the SISO Agency Platform's 400+ React component architecture.

@include shared/flag-inheritance.yml#Universal_Always

Examples:
- `/component-build --create ClientCard` - Create new client management component
- `/component-build --enhance TaskBoard --perf` - Optimize existing component
- `/component-build --test --coverage` - Run comprehensive component testing
- `/component-build --audit --security` - Security audit for components

## Component Development Modes

**--create:** New component creation workflow
- Generate component with TypeScript interfaces
- Create associated test files with Jest/React Testing Library
- Generate Storybook stories for documentation
- Apply SISO brand styling and theme consistency
- Integrate with existing design system patterns

**--enhance:** Existing component optimization
- Performance analysis and optimization
- Accessibility compliance enhancement
- Responsive design improvements
- Type safety strengthening
- Code quality improvements

**--test:** Component testing and validation
- Unit test generation and execution
- Integration test creation
- Visual regression testing
- Accessibility testing
- Performance benchmarking

**--audit:** Component security and quality audit
- Security vulnerability scanning
- Performance bottleneck identification
- Code quality assessment
- Best practice compliance checking
- Technical debt analysis

## SISO Platform Component Categories

**Client Management Components:**
- Client onboarding flow components
- Document management interfaces
- Progress tracking dashboards
- Communication management tools
- Service delivery tracking

**Instagram Lead Components:**
- Lead generation interfaces
- Outreach campaign management
- Lead scoring and filtering
- Analytics and reporting dashboards
- Campaign automation controls

**Agency Dashboard Components:**
- Performance metrics widgets
- Financial tracking components
- Project portfolio displays
- Team collaboration tools
- Reporting and analytics

**Task Management Components:**
- Kanban board implementations
- Calendar view components
- Priority management interfaces
- Progress tracking widgets
- Notification systems

## MCP Integration for Component Development

**Magic MCP for UI Generation:**
- Intelligent component scaffolding
- Design system integration
- Responsive layout generation
- Accessibility compliance automation
- Brand consistency enforcement

**Playwright MCP for Testing:**
- Automated visual regression testing
- Cross-browser compatibility validation
- Performance testing under load
- User interaction flow testing
- Accessibility compliance verification

**Supabase MCP for Data Integration:**
- Type-safe database integration
- Real-time data synchronization
- Query optimization for components
- Data validation and sanitization
- Performance monitoring integration

**Sequential MCP for Complex Logic:**
- Component architecture analysis
- Performance optimization strategies
- Security vulnerability assessment
- Integration pattern recommendations
- Technical debt reduction planning

## Intelligent Component Workflows

**New Component Creation:**
`/component-build --create [ComponentName] --magic --supabase --pup`
- Magic: Generate component structure and styling
- Supabase: Set up type-safe data integration
- Playwright: Create automated test suite

**Performance Optimization:**
`/component-build --enhance [ComponentName] --perf --seq --pup`
- Sequential: Analyze performance bottlenecks
- Playwright: Validate performance improvements
- Generate optimization recommendations

**Security and Quality Audit:**
`/component-build --audit [ComponentName] --security --seq --magic`
- Sequential: Complex security analysis
- Magic: UI security best practice validation
- Comprehensive security reporting

**Comprehensive Testing:**
`/component-build --test [ComponentName] --coverage --pup --magic`
- Playwright: Full browser testing suite
- Magic: Visual component validation
- Coverage reporting and analysis

## SISO-Specific Component Patterns

**Client Onboarding Components:**
- Multi-step form validation
- Document upload and verification
- Progress tracking and status updates
- Communication logging and history
- Integration with client management system

**Instagram Lead Components:**
- Lead import and validation
- Campaign creation and management
- Analytics and performance tracking
- Automated outreach workflows
- Lead scoring and prioritization

**Financial Management Components:**
- Invoice generation and tracking
- Payment processing integration
- Expense management and categorization
- Financial reporting and analytics
- Budget planning and monitoring

**Project Portfolio Components:**
- Project showcase and galleries
- Feature documentation and specs
- Progress tracking and milestones
- Client collaboration interfaces
- Portfolio management tools

## Quality Gates and Validation

**Performance Standards:**
- Component rendering time < 16ms
- Bundle size impact analysis
- Memory usage optimization
- API call efficiency validation
- User interaction responsiveness

**Security Requirements:**
- Input validation and sanitization
- XSS prevention measures
- Data encryption in transit
- Access control implementation
- Privacy compliance validation

**Accessibility Compliance:**
- WCAG 2.1 AA compliance
- Screen reader compatibility
- Keyboard navigation support
- Color contrast validation
- Focus management implementation

**Brand Consistency:**
- SISO brand color palette adherence
- Typography and spacing standards
- Component design system compliance
- Responsive design implementation
- Cross-browser compatibility

## Automated Development Workflows

**Component Lifecycle Management:**
- Automated component creation with templates
- Dependency management and optimization
- Test generation and validation
- Documentation generation and updates
- Performance monitoring and alerting

**Quality Assurance Automation:**
- Pre-commit component validation
- Automated testing pipeline integration
- Performance regression detection
- Security vulnerability scanning
- Code quality assessment

**Integration Testing:**
- Component integration validation
- API integration testing
- Data flow verification
- User journey testing
- Cross-component communication

## Development Environment Optimization

**Hot Reload and Development:**
- Fast refresh implementation
- Component isolation testing
- Real-time performance monitoring
- Error boundary implementation
- Development tool integration

**Build Optimization:**
- Component tree shaking
- Bundle splitting strategies
- Asset optimization
- Caching strategies
- Progressive loading implementation

**Team Collaboration:**
- Component library documentation
- Design system integration
- Code review automation
- Knowledge sharing workflows
- Best practice enforcement

@include shared/execution-patterns.yml#Component_Development

@include shared/hybrid-mcp-patterns.yml#UI_Development

@include shared/universal-constants.yml#Standard_Messages_Templates