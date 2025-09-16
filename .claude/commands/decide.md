# /decide - Decision Framework & Analysis Engine

## Purpose
Multi-criteria decision analysis (MCDA) system with structured frameworks, stakeholder integration, and outcome tracking for evidence-based decision making.

## Usage
```
/decide [command] [arguments] [--options]
```

## Decision Commands

### Framework Analysis
- `/decide framework "Mobile app tech stack"` - Apply structured framework analysis
- `/decide framework --type technical "Database migration"` - Use specific framework type
- `/decide framework --stakeholders john@company.com,sarah@company.com "API redesign"` - Include stakeholders
- `/decide framework --id custom-decision-2024 "Strategic planning"` - Set decision tracking ID

### Option Comparison
- `/decide compare "React Native" "Native Development"` - Side-by-side comparison
- `/decide compare --criteria performance,cost,speed "Option A" "Option B"` - Focus on specific criteria
- `/decide compare --stakeholder-view john@company.com "Solution 1" "Solution 2"` - Stakeholder perspective

### Custom Criteria Definition
- `/decide criteria --create` - Define new decision criteria set
- `/decide criteria --template business` - Use predefined criteria template
- `/decide criteria --weight performance=0.3,cost=0.4,speed=0.3` - Set custom weights
- `/decide criteria --validate` - Validate current criteria configuration

### Option Scoring
- `/decide score --options "React,Vue,Angular"` - Score multiple options against active criteria
- `/decide score --option "Current Solution" --baseline` - Score against baseline
- `/decide score --rationale --detailed` - Include detailed scoring rationale
- `/decide score --stakeholder-scores` - Include stakeholder-specific scoring

### Stakeholder Analysis & Alignment
- `/decide stakeholders "Mobile app architecture"` - Identify and analyze decision stakeholders
- `/decide influence --decision "API redesign"` - Map stakeholder influence and interest levels
- `/decide alignment "Database migration"` - Assess stakeholder alignment and identify conflicts
- `/decide communication --template executive "Budget planning"` - Generate stakeholder-specific communication plans

## Intelligence Layers

### Framework Integration
- **Automatic Framework Selection**: Analyzes decision context to recommend optimal framework
- **Multi-Framework Support**: Business, technical, product, hiring, process frameworks
- **Custom Framework Creation**: Define domain-specific frameworks with weighted criteria
- **Integration with existing** `decision_frameworks.yaml` and `stakeholder_contexts.yaml`

### Stakeholder Intelligence
- **Automatic Stakeholder Mapping**: Identifies relevant stakeholders based on decision scope
- **Communication Optimization**: Tailors analysis to stakeholder preferences and roles
- **Consensus Building**: Provides strategies for building stakeholder alignment
- **Resistance Management**: Identifies and addresses potential sources of resistance

### Multi-Criteria Decision Analysis (MCDA)
- **Weighted Scoring**: Applies framework-specific criteria weighting
- **Risk-Adjusted Analysis**: Incorporates risk assessment into scoring
- **Confidence Intervals**: Provides confidence levels for recommendations
- **Sensitivity Analysis**: Shows how changes in weights affect outcomes

### Decision Intelligence
- **Historical Pattern Matching**: Leverages past decisions for improved accuracy
- **Success Probability Estimation**: Predicts likelihood of successful outcomes
- **Implementation Roadmaps**: Provides detailed execution plans
- **Outcome Tracking**: Monitors actual vs. predicted results

## Command Implementations

### `/decide framework` - Framework Analysis Engine

**Purpose**: Apply structured decision frameworks to complex decisions with stakeholder analysis and outcome tracking.

**Core Functionality**:
1. **Intelligent Framework Selection**
   - Analyze decision context and classify decision type
   - Recommend optimal framework (business, technical, product, hiring, process)
   - Load framework criteria, weights, and evaluation methods
   - Integrate with `decision_frameworks.yaml` configuration

2. **Comprehensive Option Analysis**
   - Generate complete option set including alternatives and status quo
   - Apply systematic scoring across all framework criteria
   - Calculate weighted scores with risk adjustment
   - Perform comparative analysis with pros/cons breakdown

3. **Stakeholder Integration**
   - Map stakeholders based on decision scope and organizational impact
   - Load stakeholder profiles from `stakeholder_contexts.yaml`
   - Apply stakeholder preferences and communication styles
   - Generate consensus-building strategies

4. **Evidence-Based Recommendations**
   - Synthesize analysis into clear, actionable recommendation
   - Provide confidence scoring with supporting rationale
   - Include implementation roadmap with success metrics
   - Generate stakeholder-specific communication plans

**Output Format**: Comprehensive decision analysis with scoring matrix, stakeholder impact assessment, risk analysis, and implementation roadmap.

### `/decide compare` - Option Comparison Engine

**Purpose**: Focused side-by-side comparison of specific options with detailed analysis.

**Core Functionality**:
1. **Structured Comparison Framework**
   - Load active decision criteria or use framework defaults
   - Apply consistent scoring methodology across options
   - Generate side-by-side comparison matrix
   - Highlight key differentiators and trade-offs

2. **Multi-Dimensional Analysis**
   - Score options across all relevant criteria
   - Calculate weighted totals and rankings
   - Identify winner and runner-up with confidence levels
   - Analyze sensitivity to criteria weight changes

3. **Contextual Insights**
   - Consider stakeholder preferences and constraints
   - Factor in organizational context and current state
   - Assess implementation feasibility and resource requirements
   - Evaluate strategic alignment and long-term implications

**Usage Examples**:
```markdown
# Option Comparison: React Native vs Native Development

## Comparison Matrix
| Criteria | Weight | React Native | Native Dev | Winner |
|----------|--------|--------------|------------|--------|
| Development Speed | 30% | 9/10 | 5/10 | React Native |
| Performance | 25% | 7/10 | 10/10 | Native |
| Cost | 20% | 8/10 | 4/10 | React Native |
| Team Skills | 15% | 9/10 | 6/10 | React Native |
| Maintenance | 10% | 7/10 | 8/10 | Native |

## Weighted Score
- **React Native**: 7.65/10 ⭐ **WINNER**
- **Native Development**: 6.35/10

## Key Insights
- React Native wins on speed, cost, and team alignment
- Native development superior for performance-critical features
- Consider hybrid approach for performance-sensitive components
```

### `/decide criteria` - Criteria Definition Engine

**Purpose**: Define, customize, and manage decision criteria sets for consistent evaluation.

**Core Functionality**:
1. **Criteria Set Management**
   - Create new criteria sets from scratch or templates
   - Load predefined criteria from framework templates
   - Customize criteria names, descriptions, and scales
   - Set and adjust criteria weights with validation

2. **Template System**
   - Business criteria: Financial impact, strategic alignment, risk, resources
   - Technical criteria: Scalability, maintainability, security, performance
   - Product criteria: User value, market demand, feasibility, resources
   - Custom criteria: Define domain-specific evaluation dimensions

3. **Weight Validation**
   - Ensure weights sum to 1.0 (100%)
   - Provide weight distribution analysis
   - Suggest optimal weight ranges based on decision type
   - Validate criteria relevance for decision context

4. **Criteria Analytics**
   - Show criteria usage patterns across past decisions
   - Analyze criteria effectiveness and predictive power
   - Suggest criteria modifications based on outcomes
   - Generate criteria performance reports

**Interactive Criteria Builder**:
```markdown
# Custom Criteria Definition

## Criteria Set: Technical Architecture Decision
1. **Scalability** (25%)
   - Scale: 1-10 | Type: Quantitative
   - Description: Ability to handle growth in users and data

2. **Maintainability** (25%)
   - Scale: 1-10 | Type: Qualitative
   - Description: Code quality and ease of maintenance

3. **Security** (20%)
   - Scale: 1-10 | Type: Quantitative
   - Description: Security posture and compliance

4. **Development Speed** (15%)
   - Scale: 1-10 | Type: Quantitative
   - Description: Impact on development velocity

5. **Cost** (15%)
   - Scale: 1-10 | Type: Quantitative
   - Description: Total cost of ownership

**Weight Distribution**: ✅ Valid (100%)
**Criteria Relevance**: ✅ High for technical decisions
**Template Base**: Technical Decision Framework
```

### `/decide score` - Scoring Engine

**Purpose**: Score individual options against active criteria with detailed rationale.

**Core Functionality**:
1. **Systematic Scoring**
   - Apply active criteria set to specified options
   - Use consistent 1-10 scoring scale with anchored definitions
   - Generate detailed rationale for each score
   - Calculate weighted total scores and rankings

2. **Stakeholder Perspectives**
   - Score options from different stakeholder viewpoints
   - Weight scores by stakeholder influence levels
   - Identify areas of stakeholder agreement and conflict
   - Generate stakeholder-specific recommendations

3. **Confidence Assessment**
   - Evaluate confidence level for each score (1-100%)
   - Identify areas requiring additional information
   - Flag high-uncertainty scores for further analysis
   - Provide confidence-adjusted scoring

4. **Comparative Analysis**
   - Compare scores against baseline or status quo
   - Show score distributions and ranges
   - Identify sensitivity to score variations
   - Generate "what-if" scenarios for score changes

**Detailed Scoring Output**:
```markdown
# Option Scoring: React Native

## Framework Criteria Scores

### Scalability: 7/10 (Confidence: 85%)
**Rationale**: React Native handles moderate to high scale well with proper architecture. Some limitations with very high user volumes may require native performance optimization. Based on similar implementations at Airbnb and Facebook scale.

**Supporting Evidence**:
- Handles 10M+ daily active users in production apps
- Memory usage ~15% higher than native but manageable
- CPU performance ~10-20% overhead vs native

### Maintainability: 8/10 (Confidence: 90%)
**Rationale**: Strong maintainability due to single codebase, extensive ecosystem, and team's existing React expertise. Hot reloading and debugging tools excellent.

**Supporting Evidence**:
- 70% code reuse between platforms reduces maintenance burden
- Team's React experience directly applicable
- Active community support and regular updates

### Security: 7/10 (Confidence: 75%)
**Rationale**: Generally secure with regular security updates. Some third-party native module risks. Requires careful package vetting.

**Supporting Evidence**:
- Regular security patches from Meta
- Known vulnerabilities typically patched quickly
- Need additional auditing for native modules

## Weighted Total: 7.3/10
**Confidence Level**: 83%
**Recommendation**: Strong candidate for current requirements
```

### `/decide stakeholders` - Stakeholder Identification Engine

**Purpose**: Identify and analyze all relevant stakeholders for a specific decision with influence mapping and engagement strategies.

**Core Functionality**:
1. **Automatic Stakeholder Discovery**
   - Load stakeholder profiles from `stakeholder_contexts.yaml`
   - Identify stakeholders based on decision scope and organizational impact
   - Map direct and indirect stakeholder relationships
   - Include external stakeholders and decision groups

2. **Stakeholder Categorization**
   - Classify stakeholders by influence level and decision authority
   - Group by department, role, and decision involvement type
   - Identify decision makers, implementers, and affected parties
   - Flag key champions and potential resistors

3. **Impact and Interest Analysis**
   - Assess decision impact on each stakeholder group
   - Evaluate stakeholder interest levels and priorities
   - Map stakeholder concerns and typical decision patterns
   - Generate stakeholder engagement priority matrix

4. **Integration with Team Data**
   - Pull from team roster for current organizational structure
   - Consider current project assignments and workloads
   - Include historical decision participation data
   - Factor in recent 1:1 notes and team feedback

**Example Usage**:
```markdown
# 👥 Stakeholder Analysis: Mobile App Architecture Decision

## Identified Stakeholders (8 total)

### Primary Decision Makers
- **John Smith** (Engineering Manager) - Final decision authority
  - **Authority Level**: Final decision maker
  - **Key Concerns**: Resource allocation, team capacity, timeline
  - **Communication Style**: Executive summary preferred

### Technical Implementation Team
- **Sarah Johnson** (Senior Developer) - High technical influence
  - **Authority Level**: Technical implementation lead
  - **Expertise**: React Native, mobile development, system architecture
  - **Key Concerns**: Technical debt, maintainability, team skills

### Affected Stakeholders
- **Product Manager** - User experience requirements
- **Design Team Lead** - UI/UX implementation complexity
- **QA Lead** - Testing strategy requirements
- **DevOps Team** - Deployment and infrastructure impact

### External Stakeholders
- **CTO** - Strategic oversight and budget approval
- **Customer Support** - Post-launch maintenance burden

## Engagement Priority Matrix
**High Priority**: John, Sarah, Product Manager
**Medium Priority**: Design Lead, QA Lead, CTO
**Low Priority**: DevOps Team, Customer Support
```

### `/decide influence` - Influence Mapping Engine

**Purpose**: Map stakeholder influence levels, decision-making power, and interest in specific decisions.

**Core Functionality**:
1. **Power-Interest Grid Analysis**
   - Plot stakeholders on power vs. interest matrix
   - Identify high-power, high-interest key players
   - Flag low-power, high-interest supporters
   - Analyze high-power, low-interest stakeholders requiring attention

2. **Decision Authority Mapping**
   - Map formal decision-making authority chains
   - Identify informal influence networks and relationships
   - Assess veto power and approval requirements
   - Track coalition formation opportunities

3. **Influence Effectiveness Tracking**
   - Analyze historical influence patterns from stakeholder data
   - Track success rates of different influence approaches
   - Measure stakeholder engagement effectiveness over time
   - Identify optimal influence timing and methods

4. **Dynamic Influence Assessment**
   - Consider context-specific influence variations
   - Factor in current organizational dynamics
   - Account for recent stakeholder relationship changes
   - Assess influence evolution throughout decision process

**Example Output**:
```markdown
# 🎯 Influence Mapping: API Redesign Decision

## Power-Interest Grid

### High Power, High Interest (Key Players)
- **John Smith** (Engineering Manager)
  - **Power Score**: 9/10 - Budget authority, team leadership
  - **Interest Score**: 8/10 - Affects team productivity directly
  - **Strategy**: Collaborate and involve in decision-making

- **Sarah Johnson** (Senior Developer)
  - **Power Score**: 7/10 - Technical expertise, implementation lead
  - **Interest Score**: 9/10 - Direct impact on daily work
  - **Strategy**: Technical partnership and detailed consultation

### High Power, Low Interest (Context Setters)
- **CTO**
  - **Power Score**: 10/10 - Ultimate technical authority
  - **Interest Score**: 4/10 - Focused on higher-level strategy
  - **Strategy**: Keep informed with executive summaries

### Low Power, High Interest (Supporters)
- **Junior Developers**
  - **Power Score**: 3/10 - Limited formal authority
  - **Interest Score**: 8/10 - Daily usage impact
  - **Strategy**: Keep informed, gather feedback

## Coalition Opportunities
**Technical Alliance**: Sarah + DevOps + QA Lead
**Leadership Support**: John + CTO for resource approval
**User Perspective**: Product Manager + Junior Developers
```

### `/decide alignment` - Alignment Assessment Engine

**Purpose**: Assess stakeholder alignment with potential decisions and identify areas of conflict or resistance.

**Core Functionality**:
1. **Position Assessment**
   - Analyze likely stakeholder positions based on historical patterns
   - Consider stakeholder priorities and influence factors
   - Factor in current organizational context and pressures
   - Predict stakeholder support levels for different options

2. **Conflict Identification**
   - Identify areas of stakeholder disagreement
   - Map competing priorities and interests
   - Analyze resource allocation conflicts
   - Assess timeline and implementation preference conflicts

3. **Resistance Analysis**
   - Predict sources and intensity of potential resistance
   - Analyze root causes of stakeholder concerns
   - Assess resistance impact on decision implementation
   - Identify resistance mitigation strategies

4. **Consensus Opportunity Mapping**
   - Identify areas of natural stakeholder alignment
   - Map win-win opportunity scenarios
   - Assess compromise and trade-off possibilities
   - Generate consensus-building strategies

**Example Output**:
```markdown
# ⚖️ Alignment Assessment: Database Migration Strategy

## Stakeholder Position Analysis

### Aligned Stakeholders (Supporting)
- **DevOps Team** - Supports cloud-native solution
  - **Position**: Strongly favors modern infrastructure
  - **Rationale**: Aligns with automation and scalability goals
  - **Confidence**: 90% support likelihood

- **Engineering Manager** - Supports gradual migration
  - **Position**: Favors phased approach to minimize risk
  - **Rationale**: Reduces team disruption and timeline pressure
  - **Confidence**: 80% support likelihood

### Neutral Stakeholders (Undecided)
- **Product Manager** - Focused on minimal user impact
  - **Key Concern**: Feature delivery timeline disruption
  - **Decision Factor**: Migration timeline and rollback plan
  - **Influence Strategy**: Demonstrate minimal user-facing impact

### Potential Resistance
- **Senior Developer (Database Specialist)** - May resist new technology
  - **Concern**: Learning curve and expertise transfer
  - **Resistance Level**: Medium (6/10)
  - **Mitigation**: Training plan and knowledge transfer sessions

## Conflict Analysis
**Primary Conflict**: Speed vs. Stability
- **Speed Advocates**: Product Manager, CTO (market pressure)
- **Stability Advocates**: DevOps, Database Specialist (risk aversion)
- **Resolution Approach**: Phased migration with early wins

**Resource Conflict**: Training vs. Delivery
- **Training Needs**: Database Specialist, Junior Developers
- **Delivery Pressure**: Product Manager, Engineering Manager
- **Resolution Approach**: Parallel training during low-impact phases

## Consensus Building Opportunities
**Shared Priority**: System reliability and performance
**Common Ground**: Everyone values minimal business disruption
**Win-Win Scenario**: Phased approach with performance improvements at each stage
```

### `/decide communication` - Communication Strategy Engine

**Purpose**: Generate stakeholder-specific communication plans tailored to preferences, roles, and decision involvement.

**Core Functionality**:
1. **Stakeholder Communication Profiling**
   - Load communication preferences from stakeholder contexts
   - Adapt message content to stakeholder roles and expertise
   - Consider decision authority levels and information needs
   - Factor in preferred communication channels and timing

2. **Message Customization**
   - Generate stakeholder-specific message content and framing
   - Adapt technical depth and business focus by audience
   - Include relevant concerns and value propositions
   - Provide clear action items and next steps

3. **Communication Template Generation**
   - Create executive summaries for leadership stakeholders
   - Generate technical analyses for implementation teams
   - Develop user impact communications for affected parties
   - Provide scripts and talking points for conversations

4. **Multi-Channel Strategy**
   - Recommend optimal communication channels per stakeholder
   - Sequence communications for maximum effectiveness
   - Plan feedback collection and response strategies
   - Schedule follow-up communications and checkpoints

**Example Output**:
```markdown
# 💬 Communication Strategy: Budget Planning Decision

## Stakeholder Communication Plan

### Executive Leadership (CTO, Engineering Manager)
**Communication Template**: Executive Summary
**Channel**: Email + brief meeting
**Timing**: Before team communications
**Key Messages**:
- **Financial Impact**: $200K investment, 15% efficiency gain
- **Strategic Value**: Positions team for 2024 growth targets
- **Risk Assessment**: Low risk, proven technology adoption
- **Decision Timeline**: Approval needed by Friday for Q4 implementation

**Sample Message**:
"Subject: Q4 Budget Allocation: Engineering Infrastructure Investment

Executive Summary:
- Requesting $200K for infrastructure modernization
- Expected 15% productivity improvement and $300K annual savings
- Low-risk implementation using proven technologies
- Decision needed by Oct 15 for Q4 execution

Business Case: [Detailed financial analysis attached]
Implementation Plan: [Phased approach with milestones]
Your Action: Review attached analysis, approve budget allocation"

### Technical Team (Developers, DevOps)
**Communication Template**: Technical Analysis
**Channel**: Team meeting + technical documentation
**Timing**: After leadership approval
**Key Messages**:
- **Technical Benefits**: Improved CI/CD, automated deployment
- **Implementation Plan**: 3-phase rollout with training
- **Resource Requirements**: 2 weeks team time, external consulting
- **Skills Development**: New tools training and certification opportunities

**Sample Message**:
"Team Infrastructure Modernization: Technical Overview

Technical Scope:
- Migration to containerized deployment (Docker + Kubernetes)
- CI/CD pipeline automation (GitHub Actions)
- Infrastructure as Code (Terraform)
- Monitoring and observability (Datadog integration)

Implementation Phases:
Phase 1: CI/CD pipeline setup (Weeks 1-2)
Phase 2: Containerization (Weeks 3-4)
Phase 3: Production deployment (Weeks 5-6)

Training Plan: [Detailed skill development roadmap]
Your Role: Active participation in planning sessions, skills development"

### Affected Users (Product, Support, QA)
**Communication Template**: Impact Assessment
**Channel**: All-hands meeting + FAQ document
**Timing**: During implementation phases
**Key Messages**:
- **Benefit Summary**: Faster releases, more reliable deployments
- **Timeline Impact**: No disruption to feature delivery schedule
- **Support Changes**: New deployment notification system
- **Feedback Channels**: Weekly check-ins, dedicated Slack channel

## Communication Schedule
**Week 1**: Executive approvals and leadership alignment
**Week 2**: Technical team planning and skills assessment
**Week 3**: All-hands announcement and Q&A session
**Week 4**: Implementation kickoff with regular updates
**Weekly**: Progress updates and feedback collection
```

## Integration Points

### System Integration
- **Decision Frameworks**: Loads frameworks from `decision_frameworks.yaml`
- **Stakeholder Context**: Integrates with `stakeholder_contexts.yaml`
- **Team Integration**: Uses team roster for stakeholder identification
- **Project Integration**: Considers current projects and resource constraints
- **Decision Tracking**: Stores decisions in `decision_frameworks.yaml` for outcome tracking

### Data Flow
```
User Request → Command Router → Framework Selection → Stakeholder Mapping →
Option Analysis → Scoring Engine → Risk Assessment → Recommendation →
Communication Strategy → Implementation Planning → Decision Tracking
```

### Quality Assurance
- **Framework Validation**: Ensures proper framework application
- **Score Consistency**: Validates scoring logic and rationale
- **Stakeholder Coverage**: Confirms all relevant stakeholders included
- **Implementation Feasibility**: Assesses practical implementation considerations

## Best Practices

### Framework Selection
- Choose appropriate framework based on decision type and complexity
- Ensure criteria relevance and proper weighting for context
- Include quantitative and qualitative assessment methods
- Validate framework fit before proceeding with analysis

### Stakeholder Management
- Map all directly and indirectly affected stakeholders early
- Adapt communication style to stakeholder preferences and roles
- Build consensus through structured consultation process
- Address resistance proactively with targeted strategies

### Decision Quality
- Generate comprehensive option sets including status quo and alternatives
- Apply systematic evaluation with evidence-based scoring methodology
- Include implementation feasibility and resource requirements in analysis
- Provide confidence levels and uncertainty analysis for transparency

### Outcome Optimization
- Track decision outcomes against predictions for continuous improvement
- Capture lessons learned and update frameworks based on experience
- Monitor stakeholder satisfaction and decision effectiveness over time
- Use outcome data to refine framework accuracy and relevance

Always ensure decisions are evidence-based, stakeholder-inclusive, and optimized for successful implementation and measurable outcomes.