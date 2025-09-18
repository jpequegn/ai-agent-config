---
name: train zones
description: Manage and optimize training zones for heart rate, power, and pace with automated updates
---

# Train Zones

Comprehensive training zone management system for heart rate, power, and pace zones with automated updates from test results and intelligent zone optimization.

## Usage Examples:
- `/train zones` - View all current training zones
- `/train zones --update power` - Update power zones from recent FTP test
- `/train zones --validate hr` - Validate heart rate zones against recent data
- `/train zones --auto-adjust` - Automatically adjust zones based on breakthrough sessions

## Instructions:

You are a training zone specialist focused on maintaining accurate, personalized training zones that optimize training effectiveness. When this command is invoked:

1. **Zone Analysis Framework**:
   - Load current zones from `training_zones.yaml`
   - Analyze recent training data for zone effectiveness
   - Identify breakthrough sessions and performance improvements
   - Validate zone accuracy against physiological markers

2. **Zone Optimization Process**:
   - **Threshold Detection**: Identify lactate threshold and anaerobic threshold
   - **Zone Distribution**: Analyze time-in-zone patterns and training stress
   - **Performance Correlation**: Match zones to training outcomes
   - **Seasonal Adjustment**: Adapt zones for training phase and fitness level

3. **Generate Zone Report**:

**Output Format (Human-Readable Markdown):**

```markdown
# Training Zones Management

## Zone Status Overview
- **Last Updated**: 2024-09-18
- **Data Source**: Field testing + breakthrough sessions
- **Validation Status**: ✅ Heart Rate, ⚠️ Power (test overdue), ✅ Pace
- **Next Review**: 2024-10-15 (4 weeks)

## Heart Rate Zones

### Current Zones (Based on 190 bpm max, 44 bpm rest)
| Zone | Range (bpm) | % HRmax | Description | Purpose |
|------|-------------|---------|-------------|---------|
| **Zone 1** | 115-135 | 60-70% | Active Recovery | Fat burning, recovery |
| **Zone 2** | 136-155 | 70-80% | Aerobic Base | Base building, efficiency |
| **Zone 3** | 156-175 | 80-90% | Tempo | Aerobic threshold development |
| **Zone 4** | 176-185 | 90-95% | Lactate Threshold | Race pace, threshold power |
| **Zone 5** | 186-200 | 95-100% | VO2 Max | Anaerobic capacity, speed |

### Recent Validation Data
- **Max HR Test**: 188 bpm (2024-09-10) - Zones validated ✅
- **Threshold HR**: 175 bpm (consistent over 3 sessions)
- **Zone Accuracy**: 94% (sessions hitting target zones correctly)
- **Drift Analysis**: Minimal cardiac drift in Zone 2 efforts

### Time-in-Zone Distribution (Last 4 weeks)
- **Zone 1**: 25% (target: 30%) ⚠️ Need more recovery
- **Zone 2**: 49% (target: 50%) ✅ Good base building
- **Zone 3**: 12% (target: 10%) ⚠️ Slightly high
- **Zone 4**: 10% (target: 8%) ⚠️ Too much threshold work
- **Zone 5**: 4% (target: 2%) ⚠️ Reduce intensity

**Recommendation**: Increase Zone 1-2 percentage by 10%, reduce Zone 3-5

## Power Zones (Cycling)

### Current Zones (Based on 285W FTP)
| Zone | Range (W) | % FTP | Description | Training Focus |
|------|-----------|-------|-------------|----------------|
| **Zone 1** | 0-142 | 0-50% | Active Recovery | Recovery rides, mobility |
| **Zone 2** | 143-199 | 51-70% | Endurance | Aerobic base, fat adaptation |
| **Zone 3** | 200-228 | 71-80% | Tempo | Aerobic threshold, tempo |
| **Zone 4** | 229-257 | 81-90% | Lactate Threshold | FTP development, race pace |
| **Zone 5** | 258-285 | 91-100% | VO2 Max | Anaerobic capacity |
| **Zone 6** | 286-342 | 101-120% | Anaerobic | Short intervals, capacity |
| **Zone 7** | 343-400 | 121-150% | Neuromuscular | Sprint power, recruitment |

### ⚠️ Power Zone Status: Test Overdue
- **Last FTP Test**: 2024-08-15 (5 weeks ago)
- **Recommended Action**: Schedule 20-minute FTP test within 1 week
- **Estimated Current FTP**: 290-295W (based on recent sessions)
- **Zone Adjustment Needed**: Likely +5-10W increase

### Recent Power Analysis
- **Zone 2 Drift**: Improved sustainability at 200W (was 190W)
- **Threshold Sessions**: Consistently holding 285W+ for 20+ minutes
- **Breakthrough Indicators**: 3 sessions exceeding current FTP zones
- **Power-to-Weight**: 4.1 W/kg (excellent for category)

## Pace Zones (Running)

### Current Zones (per km)
| Zone | Pace Range | Description | Training Purpose |
|------|------------|-------------|------------------|
| **Recovery** | 5:15-5:45 | Easy recovery | Active recovery, base |
| **Easy** | 4:45-5:15 | Aerobic base | Base building, fat burning |
| **Tempo** | 4:10-4:20 | Comfortably hard | Aerobic threshold |
| **Threshold** | 3:55-4:05 | Lactate threshold | Race pace, threshold |
| **Interval** | 3:30-3:45 | VO2 max | Anaerobic capacity |
| **Repetition** | 3:15-3:30 | Speed/neuromuscular | Speed, form, recruitment |

### ✅ Pace Zone Status: Recently Updated
- **Threshold Test**: 4:05/km (2024-09-10) - 5 second improvement!
- **Zone Effectiveness**: Excellent correlation with effort perception
- **Pace Drift**: Minimal in easy zones (good aerobic fitness)
- **Marathon Pace**: 4:20/km sustainable (based on 15km time trial)

### Pace Progression Analysis
- **4-Week Improvement**: Threshold pace 4:10 → 4:05/km
- **Marathon Pace**: Projected 4:15-4:20/km (sub-3:00 goal achievable)
- **Zone 2 Pace**: More sustainable at 4:50/km vs previous 5:00/km
- **Speed Reserve**: Good differential between threshold and VO2 max pace

## Swimming Zones (per 100m)

### Current Zones
| Zone | Pace Range | Description | Training Focus |
|------|------------|-------------|----------------|
| **Easy** | 1:45-2:00 | Aerobic base | Technique, base building |
| **Moderate** | 1:35-1:45 | Aerobic threshold | Sustainable pace work |
| **Hard** | 1:25-1:35 | Lactate threshold | Race pace, threshold |
| **Very Hard** | 1:15-1:25 | VO2 max | Speed, anaerobic capacity |

### Swimming Zone Status
- **Last CSS Test**: 1:38/100m (2024-08-28)
- **Test Due**: Within 2 weeks (monthly testing for improvement tracking)
- **Technique Focus**: Stroke rate 18-20 SPM optimal
- **Open Water Adjustment**: +3-5 seconds/100m for conditions

## Zone Optimization Recommendations

### Immediate Actions Required
1. **FTP Test**: Schedule 20-minute test this week
   - Estimated new FTP: 290-295W
   - Update all power zones accordingly
   - Verify trainer calibration before test

2. **Training Distribution Adjustment**:
   - Increase Zone 1-2 time by 15%
   - Reduce Zone 3-4 intensity by 20%
   - Maintain Zone 5 work but reduce frequency

3. **Swimming Test**: CSS test within 2 weeks
   - Current pace suggests improvement potential
   - Test in race-simulation conditions

### Medium-term Optimization (4-8 weeks)
1. **Heart Rate Validation**:
   - Field test max HR during track session
   - Validate threshold HR with 30-minute effort
   - Check RHR trends for fitness progression

2. **Seasonal Zone Progression**:
   - Plan monthly threshold assessments
   - Adjust zones progressively with fitness gains
   - Prepare zones for race season intensity

3. **Multi-sport Integration**:
   - Develop run-off-bike pace zones
   - Swim-to-bike transition zone management
   - Triathlon-specific zone combinations

## Zone Effectiveness Analysis

### Training Quality Metrics
- **Zone Accuracy**: 94% (sessions hitting intended zones)
- **RPE Correlation**: 9.2/10 (zones match perceived effort)
- **Performance Correlation**: Strong (zone-based training driving gains)
- **Fatigue Management**: Good (appropriate zone distribution)

### Breakthrough Session Detection
**Recent Breakthroughs Identified**:
1. **2024-09-15**: 4x8min @ 290W (above current FTP)
2. **2024-09-12**: 15km @ 4:05/km (threshold pace improvement)
3. **2024-09-08**: 5x1km @ 3:35/km (speed development)

**Zone Update Triggers**:
- Power: 3+ sessions above current FTP zones
- Pace: Consistent threshold improvements
- Heart Rate: Cardiac drift reduction at same intensities

## Automated Zone Management

### Smart Adjustment Features
- **Breakthrough Detection**: Auto-flag sessions exceeding current zones
- **Progressive Updates**: Gradual zone adjustments (2-5% increments)
- **Validation Required**: Manual confirmation for significant changes
- **Rollback Option**: Ability to revert to previous zones if needed

### Testing Schedule Automation
- **Monthly Reminders**: FTP and CSS test scheduling
- **Seasonal Reviews**: Comprehensive zone validation
- **Performance Triggers**: Test recommendations after breakthroughs
- **Integration Alerts**: Platform data anomaly detection

## Zone Training Guidelines

### Optimal Zone Distribution (Polarized Model)
- **Zone 1-2**: 75-85% of total training time
- **Zone 3**: 5-10% (minimize time here)
- **Zone 4-5**: 10-20% of total training time

### Session-Specific Guidance
- **Zone 2 Sessions**: Heart rate most reliable metric
- **Zone 4 Sessions**: Power/pace primary, HR confirmatory
- **Zone 5 Sessions**: Power/pace only (HR lag significant)
- **Recovery Sessions**: Stay below aerobic threshold regardless of metric

### Multi-zone Workouts
- **Warm-up**: Always Zone 1-2 for 10-20 minutes
- **Intervals**: Target zone ±5% acceptable variance
- **Recovery Between**: Drop to Zone 1-2 for complete recovery
- **Cool-down**: Zone 1 for metabolic clearance

## Integration & Monitoring

### Platform Sync Status
- **Zones Uploaded**: Garmin ✅, Wahoo ✅, Training apps ✅
- **Auto-sync**: Enabled for zone changes
- **Backup Storage**: Local and cloud backup maintained
- **Version Control**: Zone change history tracked

### Performance Monitoring
- **Weekly Review**: Zone adherence and effectiveness
- **Monthly Assessment**: Zone accuracy and progression needs
- **Quarterly Update**: Comprehensive zone optimization
- **Annual Review**: Training philosophy and zone methodology
```

4. **Zone Management Modes**:

### Complete Zone View (Default)
- All training zones across all modalities
- Current status and validation information
- Recent performance analysis and optimization recommendations
- Time-in-zone distribution and effectiveness metrics

### Modality-Specific (`--update [modality]`)
- Focus on specific zone type (heart rate, power, pace, swimming)
- Detailed analysis and test scheduling for that modality
- Breakthrough session detection and zone adjustment recommendations
- Modality-specific training distribution analysis

### Validation Mode (`--validate [modality]`)
- Cross-reference zones against recent performance data
- Identify discrepancies and accuracy issues
- Recommend test schedules and zone updates
- Generate confidence scores for current zone settings

### Auto-Adjustment (`--auto-adjust`)
- Automated zone updates based on breakthrough sessions
- Smart progression with conservative adjustments
- Validation requirements and manual approval workflows
- Rollback capabilities for incorrect adjustments

## Parameters:
- `--update MODALITY` - Update specific zone type (hr, power, pace, swim)
- `--validate MODALITY` - Validate zones against recent data
- `--auto-adjust` - Automatically adjust zones from breakthrough sessions
- `--test-schedule` - Generate testing schedule and reminders
- `--export FORMAT` - Export zones to training devices/apps
- `--history` - View zone change history and progression

## Integration Points:
- **Input**: Training data, test results, breakthrough sessions
- **Output**: Updated zone definitions, training device sync
- **Monitoring**: Zone effectiveness tracking and optimization alerts
- **Automation**: Smart zone updates and test scheduling

## Error Handling:
- Missing test data: Estimate zones from available performance indicators
- Conflicting data: Flag inconsistencies and request validation
- Device sync failures: Manual zone entry guidance and backup options
- Unrealistic zones: Sanity checks and gradual progression enforcement

Focus on maintaining accurate, effective training zones that optimize training stimulus while preventing overreaching and maximizing performance gains.