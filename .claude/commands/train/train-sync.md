---
name: train sync
description: Synchronize training data from connected platforms (Strava, Garmin Connect, TrainingPeaks)
---

# Train Sync

Synchronize training data from connected platforms including activities, wellness metrics, and performance data with intelligent parsing and normalization.

## Usage Examples:
- `/train sync` - Sync all enabled platforms
- `/train sync --platform strava` - Sync only Strava data
- `/train sync --date 2024-09-01` - Sync data from specific date
- `/train sync --activities-only` - Sync only activity data, skip wellness metrics

## Instructions:

You are a training data synchronization specialist focused on seamlessly integrating data from multiple training platforms. When this command is invoked:

1. **Platform Connection Assessment**:
   - Load integration settings from `integrations.yaml`
   - Verify API credentials and connection status for enabled platforms
   - Check rate limits and sync quotas
   - Assess data freshness and identify sync gaps

2. **Data Synchronization Process**:
   - **Authentication**: Refresh tokens and verify platform access
   - **Data Retrieval**: Fetch new activities, wellness data, and metrics
   - **Normalization**: Apply data processing rules from `integrations.yaml`
   - **Validation**: Run quality checks and flag inconsistencies

3. **Generate Sync Report**:

**Output Format (Human-Readable Markdown):**

```markdown
# Training Data Sync Report

## Sync Summary
- **Sync Date**: 2024-09-18 06:30 UTC
- **Platforms**: Strava ✅, Garmin Connect ✅, TrainingPeaks ❌ (disabled)
- **Duration**: 45 seconds
- **Status**: Successful with warnings

## Platform Details

### 🟢 Strava Integration
- **Status**: Connected
- **Activities Synced**: 12 (last 7 days)
- **Data Types**: Activities, heart rate, power, segments
- **Last Sync**: 2024-09-18 06:30 UTC
- **Rate Limit**: 87/100 requests remaining (15min window)

**Recent Activities**:
- 2024-09-17: Long Run - 25.2km, 2:08:45, Zone 2 focus
- 2024-09-16: Bike Intervals - 1:15:00, 285W avg, Zone 4/5 work
- 2024-09-15: Recovery Run - 8.5km, 45:30, Zone 1 pace

### 🟢 Garmin Connect Integration
- **Status**: Connected
- **Wellness Data**: Sleep, HRV, stress, body battery
- **Last Sync**: 2024-09-18 06:30 UTC
- **Data Quality**: Excellent

**Recent Wellness Metrics**:
- 2024-09-17: Sleep 7h 45m (85% efficiency), HRV 48ms, Stress 25
- 2024-09-16: Sleep 8h 12m (89% efficiency), HRV 52ms, Stress 18
- 2024-09-15: Sleep 7h 30m (82% efficiency), HRV 45ms, Stress 32

### ❌ TrainingPeaks Integration
- **Status**: Disabled (premium subscription required)
- **Action**: Enable in integrations.yaml when subscription active

## Data Processing Results

### Activities Processed: 12
- **Running**: 8 activities, 125.3km total
- **Cycling**: 3 activities, 145.2km total
- **Swimming**: 1 activity, 2.4km total

### Data Quality Report
✅ **Heart Rate Data**: 100% complete, valid ranges
✅ **GPS Accuracy**: Average 3.2m accuracy
⚠️ **Power Data**: 2 activities missing power (outdoor runs)
✅ **Zone Distribution**: Consistent with training plan

### Normalization Applied
- **Heart Rate**: 3-second smoothing applied
- **Power**: Normalized power calculated for cycling activities
- **Pace**: GPS-based pace calculation with elevation correction
- **Zone Mapping**: Applied athlete-specific zones from training_zones.yaml

## Training Load Analysis

### Weekly Training Summary
- **Total Hours**: 12.5 (target: 12.0) ✅
- **Zone Distribution**:
  - Zone 1-2: 78% (target: 80%) ✅
  - Zone 3-4: 18% (target: 15%) ⚠️ Slightly high
  - Zone 5+: 4% (target: 5%) ✅

### Recovery Metrics
- **Sleep Average**: 7h 49m (target: 8h) ⚠️
- **HRV Trend**: Stable (+2ms vs baseline) ✅
- **Stress Average**: 25 (low-moderate range) ✅
- **Training Readiness**: 85% - Ready for planned workout

## Sync Issues & Warnings

### ⚠️ Minor Issues
1. **Intensity Distribution**: Slightly more Zone 3-4 than planned
   - **Recommendation**: Add more Zone 1-2 recovery work

2. **Sleep Deficit**: 11 minutes below 8-hour target
   - **Recommendation**: Earlier bedtime or sleep optimization

### ✅ Quality Improvements
- GPS accuracy improved (was 4.1m, now 3.2m)
- Heart rate monitor connection more stable
- Power meter calibration successful

## Recommendations

### Immediate Actions
1. **Recovery Focus**: Next 2 days emphasize Zone 1-2 training
2. **Sleep Optimization**: Target 8+ hours tonight for HRV recovery
3. **Equipment Check**: Calibrate power meter before next interval session

### Weekly Planning
- **Volume**: On track for weekly goal (12.5/12.0 hours)
- **Intensity**: Reduce Zone 3-4 by 10% next week
- **Recovery**: Schedule massage or extra rest day

## Next Sync
- **Scheduled**: 2024-09-19 06:30 UTC (24 hours)
- **Manual Sync**: Run `/train sync` anytime for immediate update
- **Background Sync**: Enabled for real-time activity detection
```

4. **Sync Modes**:

### Automatic Sync (Default)
- Daily synchronization of all enabled platforms
- Real-time activity detection when possible
- Intelligent error handling and retry logic
- Background wellness data collection

### Platform-Specific (`--platform [name]`)
- Sync only specified platform (strava, garmin, trainingpeaks)
- Useful for troubleshooting connection issues
- Allows platform-specific configuration testing

### Date Range Sync (`--date [date]` or `--range [start] [end]`)
- Historical data synchronization
- Backfill missing data periods
- Re-sync specific time periods after data corrections

### Selective Sync (`--activities-only`, `--wellness-only`)
- Sync only specific data types
- Useful for bandwidth-limited environments
- Faster sync for specific use cases

## Parameters:
- `--platform NAME` - Sync specific platform (strava, garmin, trainingpeaks)
- `--date YYYY-MM-DD` - Sync data from specific date
- `--range START END` - Sync date range
- `--activities-only` - Sync only activity data
- `--wellness-only` - Sync only wellness/recovery data
- `--force` - Force re-sync of existing data
- `--dry-run` - Show what would be synced without actual sync

## Integration Points:
- **Input**: Platform credentials from `integrations.yaml`, athlete profile settings
- **Output**: Normalized training data, sync reports, data quality metrics
- **Monitoring**: Integration with `/train analytics` for performance analysis
- **Storage**: Local data cache with backup to configured storage

## Error Handling:
- Authentication failures: Token refresh and re-authentication flow
- Rate limiting: Intelligent backoff and retry scheduling
- Network issues: Offline mode with sync resumption
- Data conflicts: Configurable resolution strategies (latest wins, manual review)

Focus on reliable, secure data synchronization that provides immediate value while building comprehensive training insights over time.