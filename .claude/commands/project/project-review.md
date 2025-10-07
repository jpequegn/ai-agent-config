---
name: project-review
description: Weekly and monthly project review generation with stakeholder communication
---

# /project review - Intelligence Project Reviews

Generate comprehensive project reviews with actionable business insights, stakeholder communications, and predictive analytics.

## Usage Examples:
- `/project review` - Generate current week review for all active projects
- `/project review --weekly` - Detailed weekly review with recommendations
- `/project review --monthly` - Strategic monthly review with trends
- `/project review mobile-app-v2 --format executive` - Project-specific review
- `/project review --format email` - Stakeholder communication ready

## Instructions:

You are an intelligent project review system. When this command is invoked, you will:

### Core Functionality

Execute the ProjectReviewGenerator tool to create comprehensive project reviews:

```python
from tools import ProjectReviewGenerator

generator = ProjectReviewGenerator()

# Generate review based on parameters
review = generator.generate_review(
    period="weekly" or "monthly",  # Based on flags
    project_id=None or "specific-project",  # If specific project requested
    format="executive" or "detailed" or "email",  # Based on --format flag
    output_format="markdown"  # Default
)

# Display formatted output
print(review.formatted_output)
```

### Command Actions

**Weekly Review** `/project review` or `/project review --weekly`:
```python
review = generator.generate_review(period="weekly", format="executive")
print(review.formatted_output)
```

**Monthly Strategic Review** `/project review --monthly`:
```python
review = generator.generate_review(period="monthly", format="executive")
print(review.formatted_output)
```

**Project-Specific Review** `/project review <project-id>`:
```python
review = generator.generate_review(
    period="weekly",
    project_id="mobile-app-v2",
    format="executive"
)
print(review.formatted_output)
```

**Email Format** `/project review --format email`:
```python
review = generator.generate_review(period="weekly", format="email")
print(review.formatted_output)
```

**Detailed Format** `/project review --format detailed`:
```python
review = generator.generate_review(period="weekly", format="detailed")
print(review.formatted_output)
```

### What ProjectReviewGenerator Does

The tool automatically:

1. **Collects Multi-Source Data**
   - Project configurations from `.claude/projects.yaml`
   - GitHub activity and metrics
   - Notes and action items
   - Calendar events and timeline data
   - Team performance data

2. **Calculates Health Metrics**
   - Individual project health scores
   - Portfolio-wide health trends
   - Component-level breakdowns
   - Period-over-period comparisons

3. **Analyzes Trends**
   - 30-day trends for weekly reviews
   - 90-day trends for monthly reviews
   - Direction detection (improving/stable/declining)
   - Confidence scoring and predictions

4. **Identifies Critical Decisions**
   - Projects with declining health
   - Critical or multiple high risks
   - At-risk completion predictions
   - Priority-sorted decision list

5. **Generates Recommendations**
   - Immediate action items
   - Strategic planning suggestions
   - Team performance insights
   - Success pattern replication

6. **Formats Output**
   - Uses professional templates
   - Audience-appropriate language
   - Executive summaries
   - Detailed technical reports
   - Stakeholder-ready emails

### Output Formats

**Executive Format** (Default):
- High-level highlights and key decisions
- Portfolio health metrics and trends
- Completion predictions with confidence
- Strategic recommendations
- Stakeholder communications

**Detailed Format**:
- Everything in executive format
- Component-level health breakdowns
- Detailed activity metrics
- Individual milestone progress
- Comprehensive team metrics

**Email Format**:
- Concise stakeholder communication
- Key wins and decisions needed
- Portfolio status summary
- Clear next steps
- Professional email structure

### Advanced Features

**Velocity Analysis**:
```python
velocity_trends = generator.analyze_velocity_trends(
    project_data=review.project_statuses,
    period="weekly"
)
```

**Predictive Insights**:
```python
insights = generator.generate_predictive_insights(
    project_data=review.project_statuses
)
```

### Error Handling

ProjectReviewGenerator includes:
- **Automatic Caching**: 5-minute cache for performance (DataCollector)
- **Retry Logic**: 3 attempts with exponential backoff
- **Graceful Degradation**: Continues with partial data if sources unavailable
- **Type Safety**: Pydantic models ensure data consistency

### Benefits of Tool-Based Approach

✅ **Simplified Command**: 15-20 lines vs 600+ lines
- All analytics logic centralized in tool
- Templates handle all formatting
- Consistent methodology across reviews

✅ **Predictive Intelligence**: HealthCalculator integration
- Completion predictions with confidence intervals
- Trend analysis with direction detection
- Risk identification before issues materialize

✅ **Performance**: Optimized data collection
- ~4s → <1s for cached reviews
- Reduced API calls by ~75%
- <50ms health calculations per project

✅ **Testable & Maintainable**:
- Unit tests for all analytics logic
- Reusable across other commands
- Easy to add new review formats via templates

✅ **Type-Safe & Reliable**:
- Pydantic models for all data structures
- Automatic validation and error handling
- Graceful degradation when data unavailable

### Integration

The tool integrates with:
- **ConfigManager**: Type-safe project configuration access
- **DataCollector**: Multi-source data aggregation with caching
- **HealthCalculator**: Algorithmic health scoring and predictions
- **NoteProcessor**: Project notes and action items
- **OutputFormatter**: Professional template-based formatting

All data is automatically collected, analyzed, and formatted - the command simply needs to call the tool and display the output.

### Example: Full Weekly Review

```python
from tools import ProjectReviewGenerator

# Initialize generator
generator = ProjectReviewGenerator()

# Generate weekly executive review
review = generator.generate_review(
    period="weekly",
    format="executive"
)

# Display review
print(review.formatted_output)

# Optional: Show performance metrics
print(f"\nGenerated in {review.processing_time_ms:.0f}ms")
print(f"Analyzed {len(review.projects)} projects")
print(f"Portfolio health: {review.portfolio_health:.2%}")
```

That's it! The tool handles all the complexity of data collection, health calculation, trend analysis, decision identification, and formatting.
