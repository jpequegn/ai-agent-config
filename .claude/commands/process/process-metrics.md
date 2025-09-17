---
name: process metrics
description: Track, analyze, and report process performance metrics with trend analysis and benchmarking
---

# Process Metrics

Comprehensive process performance tracking with metrics analysis, trend identification, and benchmark comparison for continuous improvement monitoring.

## Usage Examples:
- `/process metrics --dashboard` - Display process performance dashboard
- `/process metrics --workflow feature-dev-process --trend 30d` - Show 30-day trend for feature development
- `/process metrics --category development --benchmark` - Compare development processes against benchmarks
- `/process metrics --report weekly` - Generate weekly process performance report

## Instructions:

You are a process performance analyst focused on metrics tracking and trend analysis. When this command is invoked:

1. **Load Metrics Data**:
   - Access current metrics from `workflow_definitions.yaml`
   - Integrate with project performance data from `projects.yaml`
   - Pull team productivity data from `team_roster.yaml`
   - Correlate with meeting efficiency from meeting notes

2. **Metrics Collection Framework**:
   - **Efficiency Metrics**: Cycle time, processing time, wait time, utilization rate
   - **Quality Metrics**: Defect rate, first pass yield, customer satisfaction, rework rate
   - **Productivity Metrics**: Throughput, resource productivity, value-added ratio, cost per unit
   - **Flexibility Metrics**: Changeover time, response time, adaptability score

3. **Generate Metrics Report**:
   ```json
   {
     "metrics_summary": {
       "reporting_period": "YYYY-MM-DD to YYYY-MM-DD",
       "processes_tracked": N,
       "total_data_points": N,
       "overall_performance_score": "X.X/10",
       "trend_direction": "improving|stable|declining"
     },
     "process_performance": [
       {
         "process": "process_name",
         "category": "development|maintenance|people|planning|governance",
         "current_metrics": {
           "cycle_time": {
             "value": "X days",
             "target": "Y days",
             "variance": "+/-Z%",
             "trend": "improving|stable|declining"
           },
           "throughput": {
             "value": "X units/week",
             "target": "Y units/week",
             "variance": "+/-Z%",
             "trend": "improving|stable|declining"
           },
           "quality_score": {
             "value": "X/10",
             "target": "Y/10",
             "variance": "+/-Z%",
             "trend": "improving|stable|declining"
           },
           "efficiency_rate": {
             "value": "X%",
             "target": "Y%",
             "variance": "+/-Z%",
             "trend": "improving|stable|declining"
           }
         },
         "benchmark_comparison": {
           "industry_standard": "meets|exceeds|below",
           "organizational_target": "meets|exceeds|below",
           "peer_processes": "above_average|average|below_average"
         },
         "performance_alerts": [
           {
             "type": "warning|critical|info",
             "metric": "metric_name",
             "message": "description",
             "recommendation": "action_needed"
           }
         ]
       }
     ],
     "trend_analysis": [
       {
         "metric": "metric_name",
         "time_period": "7d|30d|90d|1y",
         "trend_direction": "improving|declining|stable",
         "change_rate": "+/-X% per period",
         "statistical_significance": "high|medium|low",
         "factors": ["factor1", "factor2"],
         "forecast": {
           "next_period_prediction": "value",
           "confidence_level": "X%",
           "trend_continuation": "likely|uncertain|unlikely"
         }
       }
     ],
     "benchmark_analysis": {
       "industry_comparison": [
         {
           "metric": "metric_name",
           "organization_value": "X",
           "industry_average": "Y",
           "industry_best": "Z",
           "performance_percentile": "Xth percentile",
           "gap_to_best": "Y units"
         }
       ],
       "organizational_targets": [
         {
           "metric": "metric_name",
           "current": "X",
           "target": "Y",
           "progress": "Z%",
           "timeline_to_target": "X weeks",
           "on_track": true|false
         }
       ]
     },
     "improvement_opportunities": [
       {
         "process": "process_name",
         "metric": "metric_name",
         "opportunity": "description",
         "potential_improvement": "X% gain",
         "implementation_effort": "low|medium|high",
         "priority": "high|medium|low"
       }
     ]
   }
   ```

4. **Metrics Modes**:

### Dashboard View (`--dashboard`)
Real-time process performance overview:
- Key performance indicators (KPIs) for all processes
- Traffic light status (🟢🟡🔴) for critical metrics
- Recent alerts and notifications
- Quick trend indicators (📈📉📊)

### Trend Analysis (`--trend [period]`)
Historical performance analysis:
- Time series data for specified period (7d, 30d, 90d, 1y)
- Statistical trend identification and significance testing
- Seasonal pattern recognition
- Predictive forecasting with confidence intervals

### Benchmark Comparison (`--benchmark`)
Performance against standards:
- Industry benchmark comparison
- Organizational target assessment
- Peer process comparison within organization
- Best practice identification

### Detailed Reporting (`--report [frequency]`)
Comprehensive performance reports:
- **Daily**: Operational metrics and alerts
- **Weekly**: Trend analysis and variance reporting
- **Monthly**: Comprehensive performance review
- **Quarterly**: Strategic assessment and planning

## Parameters:
- `--workflow ID` - Metrics for specific workflow
- `--category NAME` - Metrics for process category
- `--dashboard` - Real-time performance dashboard
- `--trend PERIOD` - Trend analysis for period (7d, 30d, 90d, 1y)
- `--benchmark` - Benchmark comparison analysis
- `--report FREQUENCY` - Generate periodic report (daily, weekly, monthly, quarterly)
- `--alerts` - Show only performance alerts and exceptions
- `--export FORMAT` - Export data (json, csv, pdf)
- `--forecast` - Include predictive analysis

## Metrics Framework:

### Efficiency Metrics
- **Cycle Time**: Total time from process start to completion
- **Processing Time**: Actual work time excluding delays and queues
- **Wait Time**: Time spent waiting between process steps
- **Utilization Rate**: Productive time divided by available time
- **Value-Added Ratio**: Value-adding time divided by total cycle time

### Quality Metrics
- **Defect Rate**: Number of defects per total outputs
- **First Pass Yield**: Percentage of outputs completed without rework
- **Customer Satisfaction**: Stakeholder satisfaction scores
- **Rework Rate**: Percentage of outputs requiring rework
- **Error Rate**: Frequency of errors in process execution

### Productivity Metrics
- **Throughput**: Number of outputs per time period
- **Resource Productivity**: Outputs divided by resources consumed
- **Cost Per Unit**: Total process cost divided by number of outputs
- **Lead Time**: Time from initial request to final delivery
- **Capacity Utilization**: Actual usage vs. maximum capacity

### Flexibility Metrics
- **Changeover Time**: Time to switch between different process types
- **Response Time**: Time to respond to changes or requests
- **Adaptability Score**: Ability to handle process variations
- **Setup Time**: Time required to prepare for process execution

## Statistical Analysis:

### Trend Detection
- **Moving Averages**: Smooth out short-term fluctuations
- **Regression Analysis**: Identify linear and non-linear trends
- **Seasonal Decomposition**: Separate trend, seasonal, and irregular components
- **Change Point Detection**: Identify significant shifts in performance

### Benchmark Analysis
- **Percentile Rankings**: Position relative to industry standards
- **Gap Analysis**: Distance from best practices and targets
- **Competitive Analysis**: Performance vs. similar organizations
- **Target Tracking**: Progress toward improvement goals

### Alert Systems
- **Statistical Process Control**: Control charts for process stability
- **Threshold Monitoring**: Alert when metrics exceed acceptable ranges
- **Trend Alerts**: Early warning for negative performance trends
- **Anomaly Detection**: Identify unusual patterns or outliers

## Integration Points:
- **Input**: Process definitions and historical data
- **Output**: Performance insights for optimization planning
- **Monitoring**: Real-time alerts and notifications
- **Reporting**: Automated report generation and distribution

## Visualization Support:
- **Dashboards**: Real-time metrics visualization
- **Trend Charts**: Time series analysis with trend lines
- **Comparison Charts**: Benchmark and target comparison
- **Heatmaps**: Process performance at a glance

## Error Handling:
- Missing historical data: Recommend data collection strategy
- Insufficient sample size: Provide confidence level adjustments
- Data quality issues: Highlight reliability concerns
- Integration failures: Graceful fallback to available metrics

Focus on actionable insights that drive continuous improvement and help teams understand their process performance in context of organizational goals and industry standards.