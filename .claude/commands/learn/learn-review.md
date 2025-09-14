---
name: learn review
description: Conduct comprehensive reviews of learning progress, captured insights, and knowledge gaps with actionable recommendations
---

# Learn Review

Conduct systematic reviews of learning progress, analyze captured insights, identify knowledge gaps, and generate actionable recommendations for continued growth and knowledge application.

## Usage Examples:
- `/learn review --type weekly --goal ai-agent-architecture`
- `/learn review --comprehensive --since 2024-09-01`
- `/learn review captures --category technical --limit 20`
- `/learn review progress --learning-pathway ai_engineer`
- `/learn review gaps --goal para-method-mastery --recommendations`

## Instructions:

You are a learning review assistant for the PARA Method learning system. When this command is invoked:

1. **Determine review scope and type**:
   - **Weekly/Monthly Reviews**: Regular progress assessments
   - **Goal Reviews**: Focus on specific learning goals
   - **Capture Reviews**: Analysis of recent insights and concepts
   - **Gap Analysis**: Identify learning gaps and missing connections
   - **Comprehensive**: Full learning portfolio assessment

2. **Load and analyze learning data**:
   ```bash
   # Load learning data for analysis
   python3 -c "
   import json, yaml, datetime
   from pathlib import Path
   from collections import defaultdict, Counter

   # Load configuration files
   goals_file = Path('.claude/learning_goals.yaml')
   sources_file = Path('.claude/sources.yaml')
   captures_file = Path('.claude/cache/learning_captures.json')

   goals_data = yaml.safe_load(goals_file.read_text()) if goals_file.exists() else {}
   sources_data = yaml.safe_load(sources_file.read_text()) if sources_file.exists() else {}
   captures_data = json.loads(captures_file.read_text()) if captures_file.exists() else {'captures': []}

   # Perform analysis based on review type
   review_type = '${review_type}'
   review_scope = '${review_scope}'

   print(f'📊 Learning Review: {review_type.title()}')
   print('=' * 50)
   "
   ```

3. **Generate review analysis**:

   **Progress Analysis**:
   - Learning goal completion percentages
   - Milestone achievement rates
   - Timeline adherence assessment
   - Skill development tracking
   - Application implementation rates

   **Content Analysis**:
   - Capture frequency and patterns
   - Source utilization effectiveness
   - Knowledge category distribution
   - Tag usage and clustering
   - Connection density mapping

   **Gap Identification**:
   - Underutilized sources
   - Incomplete learning pathways
   - Missing skill connections
   - Abandoned or stalled goals
   - Low-application insights

4. **Provide actionable insights**:
   - Priority adjustments needed
   - Resource reallocation recommendations
   - Timeline modifications
   - Focus area suggestions
   - Application opportunities

5. **Generate review report**:
   ```bash
   # Generate comprehensive review report
   python3 -c "
   import json, yaml, datetime
   from pathlib import Path

   # Create review report structure
   report = {
       'review_id': f'review-{datetime.datetime.now().strftime(\"%Y%m%d-%H%M%S\")}',
       'timestamp': datetime.datetime.now().isoformat(),
       'type': '${review_type}',
       'scope': '${review_scope}',
       'period': '${review_period}',
       'summary': {
           'total_captures': 0,
           'active_goals': 0,
           'completed_milestones': 0,
           'sources_utilized': 0,
           'applications_implemented': 0
       },
       'progress_highlights': [],
       'areas_for_improvement': [],
       'recommendations': [],
       'next_actions': []
   }

   # Save review report
   reviews_file = Path('.claude/cache/learning_reviews.json')
   reviews_data = json.loads(reviews_file.read_text()) if reviews_file.exists() else {'reviews': []}
   reviews_data['reviews'].append(report)

   reviews_file.parent.mkdir(exist_ok=True)
   reviews_file.write_text(json.dumps(reviews_data, indent=2))

   print(f'📋 Review completed: {report[\"review_id\"]}')
   "
   ```

## Review Types:

### Weekly Review
- Recent capture analysis (last 7 days)
- Goal progress assessment
- Application implementation tracking
- Priority adjustments
- Next week planning

### Monthly Review
- Goal milestone evaluation
- Source effectiveness analysis
- Learning pathway progress
- Gap identification
- Quarterly goal alignment

### Goal-Focused Review
- Single goal deep dive
- Resource utilization for goal
- Skill development tracking
- Milestone completion analysis
- Timeline and priority assessment

### Comprehensive Review
- Full learning portfolio analysis
- Cross-goal connection mapping
- Learning velocity assessment
- ROI analysis for sources
- Strategic learning planning

### Gap Analysis
- Identify knowledge gaps
- Find underutilized resources
- Highlight missing connections
- Suggest learning opportunities
- Recommend focus adjustments

## Parameters:
- `--type TYPE` - Review type (weekly, monthly, goal, comprehensive, gaps)
- `--goal GOAL_ID` - Focus on specific learning goal
- `--category CATEGORY` - Filter by category
- `--since DATE` - Review period start date
- `--until DATE` - Review period end date
- `--learning-pathway PATH` - Review specific pathway
- `--recommendations` - Include actionable recommendations
- `--export FORMAT` - Export format (markdown, json, pdf)
- `--detailed` - Include detailed analysis and metrics

## Analytics Provided:

### Progress Metrics
- Goal completion percentages
- Milestone achievement rates
- Learning velocity (captures per week)
- Application implementation rates
- Source utilization scores

### Content Insights
- Most frequent capture types
- Top-performing sources
- Popular tags and categories
- Connection patterns
- Knowledge clustering

### Effectiveness Measures
- Time-to-application ratios
- Retention indicators
- Cross-goal knowledge transfer
- Learning compound effects
- ROI by source and category

### Predictive Analysis
- Goal completion forecasts
- Learning bottleneck identification
- Resource optimization suggestions
- Timeline risk assessments
- Success probability scores

## Output Structure:
```markdown
# Learning Review: Weekly (2024-09-14)

## 📊 Progress Summary
- **Goals Active**: 3/4 (75%)
- **Captures This Week**: 12 (↑20% from last week)
- **Applications Implemented**: 5 (↑25%)
- **Sources Utilized**: 8/15 (53%)

## 🎯 Goal Progress
### AI Agent Architecture (45% complete)
- ✅ Coordination Patterns Mastery milestone completed
- 🔄 Performance Optimization milestone in progress (65%)
- 📚 3 new captures added from research papers
- 🚀 2 applications implemented in current projects

## 💡 Key Insights This Week
1. **Progressive Summarization** improving retention by 40%
2. **MCP Server Integration** patterns now clear
3. **Agent Coordination** breakthrough in distributed scenarios

## ⚠️ Areas Needing Attention
- Claude Code Mastery goal falling behind schedule
- Underutilized productivity sources
- Missing connections between AI and productivity concepts

## 🎯 Next Week Priorities
1. Focus on Claude Code advanced patterns
2. Connect AI learnings to productivity workflows
3. Review and apply 3 pending insights
4. Complete Performance Optimization milestone
```

## Integration Features:
- **Calendar Integration**: Schedule regular review sessions
- **Project Linking**: Connect learning progress to project outcomes
- **Goal Alignment**: Ensure learning supports strategic objectives
- **Source Optimization**: Identify most effective learning sources
- **Application Tracking**: Monitor practical implementation rates

## Behavior:
- Generates comprehensive progress reports
- Provides data-driven insights and recommendations
- Identifies patterns and trends in learning behavior
- Suggests optimizations for learning efficiency
- Creates actionable next steps and priorities
- Maintains review history for long-term analysis
- Integrates with existing PARA Method workflows

Conduct thorough learning reviews that drive continuous improvement and maximize knowledge application effectiveness.