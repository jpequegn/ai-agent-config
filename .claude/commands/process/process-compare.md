---
name: process compare
description: Compare process efficiency across teams, time periods, and configurations to identify best practices
---

# Process Compare

Compare process efficiency across teams, time periods, and different process configurations to identify best practices, performance gaps, and optimization opportunities.

## Usage Examples:
- `/process compare --teams frontend backend` - Compare process efficiency between teams
- `/process compare --periods Q1 Q2 Q3` - Compare quarterly performance trends
- `/process compare --workflows feature-dev-v1 feature-dev-v2` - Compare process versions
- `/process compare --benchmark industry` - Compare against industry standards

## Instructions:

You are a process comparison analyst focused on identifying performance patterns and best practices. When this command is invoked:

1. **Load Comparison Data**:
   - Access `.claude/workflow_definitions.yaml` for process definitions
   - Load historical performance data from `projects.yaml`
   - Pull team-specific data from `team_roster.yaml`
   - Integrate benchmark data and industry standards

2. **Comparison Analysis**:
   - **Performance Metrics**: Cycle time, throughput, quality, efficiency
   - **Resource Utilization**: Team capacity, tool usage, cost efficiency
   - **Quality Indicators**: Defect rates, rework, customer satisfaction
   - **Trend Analysis**: Improvement trajectories and performance consistency

3. **Generate Comparison Report**:

**Output Format (Human-Readable Markdown):**

```markdown
# Process Efficiency Comparison Analysis

## Team Performance Comparison

### Feature Development Process: Frontend vs Backend Teams

| Metric | Frontend Team | Backend Team | Variance | Best Practice |
|--------|---------------|--------------|----------|---------------|
| **Cycle Time** | 6.2 days 🟢 | 8.7 days 🟡 | +40% | Frontend process |
| **Throughput** | 4.8 features/week 🟢 | 3.1 features/week 🔴 | -35% | Frontend capacity |
| **Defect Rate** | 0.12 🟡 | 0.06 🟢 | -50% | Backend quality |
| **First Pass Yield** | 78% 🟡 | 92% 🟢 | +18% | Backend process |

### Key Insights:
**Frontend Team Advantages:**
- ⚡ **Faster Delivery**: 2.5 days shorter cycle time
- 🔄 **Higher Throughput**: 55% more features delivered
- 🛠️ **Better Tooling**: Automated testing pipeline reduces manual overhead

**Backend Team Advantages:**
- 🎯 **Higher Quality**: 50% fewer defects, better first-pass yield
- 📋 **Thorough Planning**: More comprehensive requirements analysis
- 🔍 **Code Review Process**: More rigorous review standards

## Time Period Comparison

### Quarterly Performance Trends (Feature Development)

| Quarter | Cycle Time | Throughput | Quality Score | Team Satisfaction |
|---------|------------|------------|---------------|-------------------|
| **Q1 2024** | 9.2 days | 2.8 features/week | 7.2/10 | 6.8/10 |
| **Q2 2024** | 7.5 days 📈 | 3.4 features/week 📈 | 8.1/10 📈 | 7.5/10 📈 |
| **Q3 2024** | 6.8 days 📈 | 4.1 features/week 📈 | 8.3/10 📈 | 8.2/10 📈 |

### Improvement Trajectory:
- **Cycle Time**: 26% improvement over 3 quarters
- **Throughput**: 46% increase in delivery capacity
- **Quality**: 15% improvement in quality scores
- **Satisfaction**: 21% increase in team satisfaction

### Contributing Factors:
1. **Q2 Improvements**: Implemented automated testing, reduced review bottlenecks
2. **Q3 Improvements**: Added self-service environments, streamlined requirements

## Process Version Comparison

### Feature Development: V1 vs V2 Process

| Stage | V1 Duration | V2 Duration | Improvement | Change Made |
|-------|-------------|-------------|-------------|-------------|
| **Requirements** | 2.5 days | 1.8 days | -28% 🟢 | Template + async review |
| **Design** | 2.0 days | 1.5 days | -25% 🟢 | Design system + automation |
| **Development** | 6.0 days | 5.2 days | -13% 🟡 | Better tooling + training |
| **Testing** | 3.0 days | 1.8 days | -40% 🟢 | Automated testing pipeline |
| **Deployment** | 1.5 days | 0.7 days | -53% 🟢 | CI/CD automation |

### V2 Process Wins:
- **Total Cycle Time**: 15 → 11 days (27% improvement)
- **Automation Coverage**: 30% → 75% of manual tasks
- **Error Reduction**: 45% fewer deployment issues
- **Team Efficiency**: 60% less time on repetitive tasks

## Benchmark Comparison

### Industry Standards vs Current Performance

| Metric | Our Performance | Industry Average | Industry Best | Gap Analysis |
|--------|-----------------|------------------|---------------|--------------|
| **Feature Cycle Time** | 7.5 days 🟢 | 10.2 days | 5.8 days | Above average, 23% from best |
| **Defect Rate** | 0.08 🟢 | 0.15 | 0.03 | Above average, 62% from best |
| **Team Velocity** | 3.8 features/week 🟡 | 3.2 features/week | 5.2 features/week | Above average, 27% from best |
| **Customer Satisfaction** | 8.1/10 🟢 | 7.3/10 | 9.2/10 | Above average, 12% from best |

### Strategic Positioning:
- 🎯 **Strengths**: Quality and cycle time exceed industry averages
- 🚀 **Opportunities**: Velocity and satisfaction have room for improvement
- 📊 **Competitive Advantage**: 26% faster than industry average cycle time
```

4. **Comparison Modes**:

### Team Comparison (`--teams [team1] [team2]`)
- Compare process performance across different teams
- Identify best practices and knowledge transfer opportunities
- Resource allocation and capacity optimization
- Cross-team learning and standardization

### Time Period Comparison (`--periods [p1] [p2] [p3]`)
- Track performance trends over time
- Measure improvement trajectory and sustainability
- Identify seasonal patterns and external factors
- Validate process changes and optimization efforts

### Process Version Comparison (`--workflows [v1] [v2]`)
- Compare different versions of the same process
- Measure impact of process changes and improvements
- A/B testing results for process modifications
- Change management effectiveness assessment

### Benchmark Comparison (`--benchmark [type]`)
- Compare against industry standards and best practices
- Competitive positioning and gap analysis
- Strategic planning and target setting
- Performance calibration and goal alignment

## Parameters:
- `--teams TEAM1 TEAM2 ...` - Compare specific teams
- `--periods PERIOD1 PERIOD2 ...` - Compare time periods (Q1, Q2, 2023, 2024)
- `--workflows WORKFLOW1 WORKFLOW2 ...` - Compare process versions
- `--benchmark TYPE` - Compare against benchmarks (industry, competitor, internal)
- `--metrics METRIC1 METRIC2 ...` - Focus on specific metrics
- `--format markdown|json|csv` - Output format (default: markdown)
- `--statistical` - Include statistical significance testing

## Comparison Framework:

### Performance Dimensions
- **Speed**: Cycle time, lead time, processing time
- **Quality**: Defect rates, customer satisfaction, rework
- **Efficiency**: Resource utilization, cost per unit, automation
- **Predictability**: Variance, consistency, reliability

### Statistical Analysis
- **Variance Analysis**: Statistical significance of differences
- **Trend Analysis**: Performance trajectory and sustainability
- **Correlation Analysis**: Relationship between different metrics
- **Confidence Intervals**: Reliability of performance differences

### Best Practice Identification
- **Performance Leaders**: Teams/periods with best metrics
- **Success Factors**: Common elements in high-performing processes
- **Transferable Practices**: Improvements that can be replicated
- **Change Effectiveness**: Impact of specific process modifications

## Insight Generation:

### Performance Gaps
- Quantified differences between comparison subjects
- Root cause analysis for performance variations
- Opportunity sizing for improvement initiatives
- Priority ranking based on impact and effort

### Success Patterns
- Common characteristics of high-performing processes
- Environmental factors contributing to success
- Resource allocation patterns in top performers
- Cultural and organizational enablers

### Improvement Opportunities
- Specific areas where underperformers can improve
- Best practices for knowledge transfer
- Resource reallocation recommendations
- Process standardization opportunities

## Integration Points:
- **Input**: Historical data, team metrics, benchmark databases
- **Output**: Improvement roadmaps and best practice guides
- **Monitoring**: Track implementation of identified improvements
- **Learning**: Feed insights back to process optimization

## Error Handling:
- Missing comparison data: Use available data with confidence indicators
- Statistical insignificance: Highlight when differences aren't meaningful
- Incomplete time periods: Pro-rate metrics and flag limitations
- Team structure changes: Account for organizational changes in analysis

Provide objective, data-driven comparisons that enable evidence-based process improvement decisions and facilitate organizational learning from best practices.