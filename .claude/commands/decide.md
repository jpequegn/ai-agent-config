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