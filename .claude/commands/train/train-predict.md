---
name: train predict
description: Race time predictions based on current fitness with confidence intervals and performance scenarios
---

# Train Predict

Generate accurate race time predictions based on current fitness levels, training data, and performance trends with confidence intervals and scenario planning for optimal race strategy.

## Usage Examples:
- `/train predict marathon` - Predict marathon performance based on current fitness
- `/train predict --race "10K"` - Specific race distance prediction
- `/train predict --all-distances` - Comprehensive predictions across all race distances
- `/train predict --scenario-analysis` - Include best/worst case scenarios

## Instructions:

You are a race prediction specialist focused on providing accurate, evidence-based race time predictions using current fitness data, performance trends, and physiological models. When this command is invoked:

1. **Prediction Framework**:
   - Analyze current fitness levels across relevant physiological systems
   - Apply validated prediction models (Jack Daniels, Pete Riegel, McMillan)
   - Consider recent performance data and training adaptations
   - Provide confidence intervals and scenario analysis

2. **Multi-Distance Prediction Models**:
   - **Sprint/Speed**: 5K-10K predictions based on VO2 max and speed reserve
   - **Threshold**: 15K-Half Marathon based on lactate threshold fitness
   - **Endurance**: Marathon+ based on aerobic capacity and endurance training
   - **Multi-Sport**: Triathlon predictions considering discipline transitions

3. **Generate Prediction Report**:

**Output Format (Human-Readable Markdown):**

```markdown
# Race Time Predictions

## Prediction Overview
- **Analysis Date**: September 18, 2024
- **Fitness Assessment**: Current fitness level excellent (8.7/10)
- **Prediction Model**: Hybrid (Jack Daniels + current data + trend analysis)
- **Confidence Level**: High (85-90% for most distances)
- **Key Limiter**: Marathon endurance (needs specific preparation)

## Current Fitness Baseline
- **Recent 5K Time**: 20:45 (validated performance)
- **Estimated VO2 Max**: 52.3 ml/kg/min
- **Lactate Threshold Pace**: 4:08/km
- **Current Marathon Pace**: 4:20/km (estimated)
- **Training Load**: CTL 62 TSS/day (solid aerobic base)

## Running Predictions

### Speed Distance Predictions (High Confidence)

#### 5K Race Prediction
- **Predicted Time**: 20:35-20:50
- **Target Pace**: 4:07-4:10/km
- **Confidence**: 90% (recent performance data available)
- **Readiness**: Immediate (current fitness peak)

**Pacing Strategy**:
- km 1: 4:08/km (controlled start)
- km 2-3: 4:06/km (settle into rhythm)
- km 4: 4:05/km (maintain pressure)
- km 5: 4:03/km (final kick)

#### 10K Race Prediction
- **Predicted Time**: 42:15-42:45
- **Target Pace**: 4:13-4:16/km
- **Confidence**: 88% (extrapolated from 5K fitness)
- **Readiness**: 2-3 weeks specific preparation

**Pacing Strategy**:
- km 1-2: 4:16/km (conservative start)
- km 3-7: 4:13/km (race rhythm)
- km 8-9: 4:11/km (build pressure)
- km 10: 4:05/km (finishing kick)

### Threshold Distance Predictions (Good Confidence)

#### 15K Race Prediction
- **Predicted Time**: 1:04:30-1:05:15
- **Target Pace**: 4:18-4:21/km
- **Confidence**: 82% (threshold fitness based)
- **Readiness**: 4-6 weeks preparation needed

#### Half Marathon Prediction
- **Predicted Time**: 1:28:45-1:29:30
- **Target Pace**: 4:12-4:15/km
- **Confidence**: 85% (strong threshold fitness)
- **Readiness**: 6-8 weeks specific preparation

**Pacing Strategy**:
- km 1-5: 4:15/km (controlled build)
- km 6-15: 4:12/km (race rhythm)
- km 16-20: 4:10/km (gradual acceleration)
- km 21.1: 4:05/km (finish strong)

### Endurance Distance Predictions (Moderate Confidence)

#### Marathon Prediction
- **Predicted Time**: 3:01:30-3:04:45
- **Target Pace**: 4:18-4:22/km
- **Confidence**: 75% (needs endurance validation)
- **Readiness**: 12-16 weeks specific marathon training

**Scenario Analysis**:
- **Best Case**: 2:59:30 (sub-3 goal achievable with perfect execution)
- **Most Likely**: 3:02:15 (realistic with current fitness trajectory)
- **Conservative**: 3:05:30 (safe target considering endurance unknowns)

**Pacing Strategy**:
- km 1-10: 4:20/km (conservative start)
- km 11-30: 4:18/km (race rhythm)
- km 31-40: 4:18/km (maintain, monitor effort)
- km 41-42.2: Based on reserves (4:15-4:25/km)

#### Ultra Distance Predictions (Low-Moderate Confidence)
- **50K Trail**: 4:45:00-5:15:00 (dependent on terrain/elevation)
- **Marathon+**: Endurance training history needed for accuracy

## Cycling Predictions

### Time Trial Predictions
- **10K TT**: 14:45-15:00 (based on estimated 295W FTP)
- **40K TT**: 1:02:30-1:04:00 (aerodynamics dependent)
- **100K Sportive**: 2:52:00-3:05:00 (pacing strategy dependent)

### Power-Based Predictions
- **Current FTP**: 285W (validated 6 weeks ago)
- **Predicted Current**: 295W (based on training adaptations)
- **Target Power for Goals**: Need 300W for competitive performance

## Triathlon Predictions

### Sprint Triathlon (750m/20K/5K)
- **Swim**: 14:30-15:00 (1:56/100m pace)
- **Bike**: 32:00-33:00 (285-295W effort)
- **Run**: 21:30-22:00 (4:18/km off the bike)
- **Total**: 1:01:30-1:04:00
- **Confidence**: 78% (transition fitness needs validation)

### Olympic Distance (1.5K/40K/10K)
- **Swim**: 29:00-30:30 (1:56-2:02/100m pace)
- **Bike**: 1:04:00-1:06:00 (steady state power)
- **Run**: 44:30-46:00 (4:27/km off the bike)
- **Total**: 2:12:30-2:16:30
- **Confidence**: 75% (bike-run transition needs development)

### Half Ironman 70.3 (1.9K/90K/21.1K)
- **Swim**: 38:00-41:00 (2:00-2:09/100m pace)
- **Bike**: 2:32:00-2:38:00 (aerobic power focus)
- **Run**: 1:38:00-1:42:00 (4:39/km off the bike)
- **Total**: 4:48:00-5:01:00
- **Confidence**: 65% (endurance and pacing experience needed)

## Prediction Model Analysis

### Jack Daniels VDOT Model
- **Current VDOT**: 49.2 (based on 20:45 5K)
- **Predicted Marathon**: 3:03:45 (4:21/km)
- **Model Reliability**: High for speed distances, moderate for marathon

### Pete Riegel Formula
- **5K → Marathon**: 3:02:30 (optimistic without endurance base)
- **Adjustment Factor**: Applied 1.06 multiplier for endurance deficit
- **Adjusted Prediction**: 3:04:15

### McMillan Calculator Integration
- **Threshold Pace**: 4:08/km (matches current fitness)
- **Marathon Pace**: 4:19/km (conservative estimate)
- **Training Paces**: Aligned with current zone structure

### Trend-Adjusted Model (Custom)
- **Recent Improvement**: +12% fitness over 8 weeks
- **Trend Projection**: Additional 3-5% improvement possible
- **Adjusted Marathon**: 2:59:30-3:02:00 (with continued development)

## Confidence Intervals & Scenarios

### High Confidence Predictions (85-90%)
- **5K**: 20:35-20:50 (recent data validates model)
- **10K**: 42:15-42:45 (strong VO2 max fitness)
- **Half Marathon**: 1:28:45-1:29:30 (excellent threshold fitness)

### Moderate Confidence (70-80%)
- **Marathon**: 3:01:30-3:04:45 (endurance factor uncertain)
- **Sprint Triathlon**: 1:01:30-1:04:00 (transition fitness unknown)

### Lower Confidence (60-70%)
- **70.3 Triathlon**: 4:48:00-5:01:00 (limited endurance data)
- **Ultra Distances**: Insufficient training history

## Scenario Planning

### Best Case Scenario (Perfect Execution + Continued Improvement)
- **Marathon**: 2:57:30 (4:13/km) - Ambitious but possible
- **Requirements**: Perfect taper, ideal conditions, optimal fueling
- **Probability**: 15-20%

### Most Likely Scenario (Current Trajectory)
- **Marathon**: 3:02:15 (4:19/km) - Realistic with current fitness
- **Requirements**: Consistent training, good execution
- **Probability**: 60-65%

### Conservative Scenario (Safe Target)
- **Marathon**: 3:05:30 (4:23/km) - High probability of achievement
- **Requirements**: Basic preparation, average conditions
- **Probability**: 85-90%

## Factors Affecting Predictions

### Positive Factors
- **Strong Aerobic Base**: CTL 62 indicates excellent fitness foundation
- **Recent Improvements**: 12% fitness gain over 8 weeks
- **Threshold Development**: Current threshold pace very competitive
- **Health Status**: No injury concerns, excellent recovery markers

### Limiting Factors
- **Marathon Endurance**: Limited long run experience at race pace
- **Heat Tolerance**: Summer plateau suggests heat adaptation needed
- **Pacing Experience**: Limited race experience at longer distances
- **Triathlon Transitions**: Bike-run fitness needs development

### Environmental Considerations
- **Temperature**: +30 seconds per 5°C above optimal (15-18°C)
- **Humidity**: +15-45 seconds based on dew point
- **Wind**: +/- 30-90 seconds based on strength and direction
- **Course Profile**: +/- 60-180 seconds based on elevation gain

## Training Recommendations for Prediction Accuracy

### Next 4 Weeks (Validation Phase)
1. **5K Time Trial**: Validate current speed fitness
2. **Threshold Test**: 30-minute tempo to confirm lactate threshold
3. **Long Run Assessment**: 25K with final 8K at marathon pace
4. **FTP Test**: Update cycling power for triathlon predictions

### 8-12 Weeks (Development Phase)
1. **Marathon Pace Runs**: Build confidence at predicted pace
2. **Triathlon Bricks**: Develop bike-run transition fitness
3. **Race Simulation**: Practice fueling and pacing strategies
4. **Environmental Training**: Heat/cold adaptation as needed

### 16+ Weeks (Specialization Phase)
1. **Distance-Specific Training**: Focus on target race demands
2. **Race Rehearsals**: Multiple dress rehearsal sessions
3. **Taper Execution**: Optimize final 2-3 weeks
4. **Strategy Refinement**: Final pacing and tactical decisions

## Summary

**Overall Prediction Confidence**: 82% across all distances

**Key Insights**:
- Excellent speed and threshold fitness (5K-Half Marathon ready)
- Marathon achievable with specific endurance development
- Sub-3 marathon possible with focused 16-week preparation
- Triathlon potential high with transition training

**Primary Recommendation**: Target half marathon in next 8 weeks to validate endurance fitness before committing to marathon goals.

**Next Assessment**: 4 weeks (after validation races and updated fitness testing)
```

4. **Prediction Models & Parameters**:

### Standard Predictions (Default)
- **Running Distances**: 5K through marathon predictions
- **Model Integration**: Jack Daniels VDOT + current fitness data
- **Confidence Intervals**: Statistical uncertainty ranges
- **Readiness Assessment**: Training time needed for optimal performance

### Comprehensive Analysis (`--all-distances`)
- **Complete Range**: 1500m through ultra-marathon predictions
- **Multi-Sport**: Include cycling and triathlon predictions
- **Scenario Planning**: Best/worst/likely case analysis
- **Environmental Factors**: Temperature, elevation, course adjustments

### Scenario Analysis (`--scenario-analysis`)
- **Best Case**: Optimal conditions and perfect execution
- **Most Likely**: Realistic expectations with current trajectory
- **Conservative**: High-probability achievement targets
- **Risk Assessment**: Factors that could affect performance

## Parameters:
- `RACE` - Specific race distance or event (5K, 10K, half, marathon, triathlon)
- `--all-distances` - Predict across all relevant race distances
- `--scenario-analysis` - Include best/worst/likely case scenarios
- `--confidence-intervals` - Show statistical uncertainty ranges
- `--environmental` - Include weather and course condition adjustments

## Integration Points:
- **Input**: Current fitness data, recent performances, training history
- **Output**: Race predictions with confidence levels and strategies
- **Monitoring**: Track prediction accuracy and model refinement
- **Planning**: Inform race selection and training focus

## Error Handling:
- Unknown race distance: Provide guidance on standard distances
- Insufficient fitness data: Use available data with larger confidence intervals
- Conflicting performance data: Highlight inconsistencies and provide ranges
- Model limitations: Clearly state assumptions and limitations

Focus on providing actionable race predictions that help athletes set realistic goals and develop effective race strategies.