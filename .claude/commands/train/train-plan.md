---
name: train plan
description: Generate scientifically periodized training plans for specific goals with adaptive progression
---

# Train Plan

Generate comprehensive, periodized training plans tailored to specific goals, current fitness level, and individual constraints with intelligent progression and adaptation capabilities.

## Usage Examples:
- `/train plan sub-3-marathon` - Generate sub-3 hour marathon training plan
- `/train plan sub-3-marathon --race-date 2025-04-20` - Plan with specific race date
- `/train plan 70.3-improvement --weeks 28` - 28-week triathlon improvement plan
- `/train plan --goal "Break 40min 10K" --current-fitness analyze` - Custom goal with fitness analysis

## Instructions:

You are a training plan specialist focused on creating scientifically periodized, goal-specific training plans that adapt to individual circumstances. When this command is invoked:

1. **Goal and Fitness Analysis**:
   - Load athlete profile from `athlete_profile.yaml`
   - Load goal templates from `training_plans.yaml`
   - Analyze current fitness level against goal requirements
   - Calculate realistic timeline and progression requirements

2. **Plan Generation Framework**:
   - **Periodization**: Apply scientific periodization principles
   - **Individualization**: Adapt to athlete constraints and preferences
   - **Progression**: Build systematic volume and intensity progression
   - **Risk Management**: Include injury prevention and load management

3. **Generate Training Plan**:

**Output Format (Human-Readable Markdown):**

```markdown
# Sub-3 Hour Marathon Training Plan

## Goal Analysis
- **Target Time**: 2:59:59 (4:15/km pace)
- **Current Fitness**: Marathon pace ~4:25/km (based on recent 10k PR)
- **Fitness Gap**: Need 10 sec/km improvement (~4% faster)
- **Timeline**: 28 weeks available (optimal for this goal)
- **Achievability**: 85% confidence (realistic with consistent training)

## Periodization Structure

### Phase 1: Base Building (Weeks 1-12)
**Focus**: Aerobic development, injury prevention, base fitness
- **Weekly Volume**: 65-85km, building gradually
- **Intensity Distribution**: 85% easy, 10% moderate, 5% hard
- **Key Adaptations**: Mitochondrial density, fat oxidation, aerobic capacity

**Key Sessions**:
- Long run progression: 25km → 32km
- 2 tempo runs per week (gradually increasing)
- Easy running at 5:00-5:30/km
- Weekly volume increase: 5-7km per week

**Volume Progression**:
- Week 1-3: 65-70km
- Week 4: Recovery week (55km)
- Week 5-7: 72-78km
- Week 8: Recovery week (60km)
- Week 9-11: 80-85km
- Week 12: Recovery week (65km)

### Phase 2: Build (Weeks 13-20)
**Focus**: Marathon-specific fitness, lactate threshold development
- **Weekly Volume**: 85-95km peak
- **Intensity Distribution**: 75% easy, 15% moderate, 10% hard
- **Key Adaptations**: Lactate clearance, race pace efficiency, glycogen utilization

**Key Sessions**:
- Marathon pace runs: 15km → 25km at 4:15/km
- Threshold intervals: 5x8min → 3x15min
- Long runs with marathon pace segments
- Weekly track session for leg speed

**Specific Workouts**:
- Tuesday: Marathon pace progression (15k, 18k, 21k, 25k)
- Thursday: Threshold work (8x8min, 6x10min, 4x12min, 3x15min)
- Sunday: Long run with pace work (25k easy + 5k at race pace)

### Phase 3: Peak & Taper (Weeks 21-28)
**Focus**: Race sharpening, recovery, race preparation
- **Weekly Volume**: 95km → 50km (taper)
- **Intensity Distribution**: 80% easy, 15% moderate, 5% hard
- **Key Adaptations**: Neuromuscular readiness, glycogen supercompensation

**Key Sessions**:
- Race pace simulation: 30km at goal pace
- Sharpening intervals: 8x400m at 3:50/km
- 3-week structured taper
- Mental preparation and race strategy

**Taper Schedule**:
- Week 21-22: Peak weeks (90-95km)
- Week 23-24: Early taper (75-80km)
- Week 25-26: Mid taper (60-65km)
- Week 27: Final taper (50km)
- Week 28: Race week (35km + race)

## Weekly Schedule Template

### Base/Build Phase Schedule
- **Monday**: Rest or easy 6km recovery
- **Tuesday**: Tempo/Threshold session + easy 6km
- **Wednesday**: Easy 8-10km aerobic base
- **Thursday**: Intervals/Marathon pace + easy 6km
- **Friday**: Rest or easy 6km recovery
- **Saturday**: Easy 10-12km moderate effort
- **Sunday**: Long run (progressive distance and intensity)

### Sample Week 16 (Build Phase)
- **Monday**: Rest day (complete recovery)
- **Tuesday**: 18km marathon pace run (3k warmup, 15k at 4:15/km, 3k cooldown)
- **Wednesday**: 8km easy (5:15-5:30/km conversational pace)
- **Thursday**: Threshold intervals (3k warmup, 6x10min at 4:05/km with 90s recovery, 3k cooldown)
- **Friday**: 6km easy recovery (5:30+/km very relaxed)
- **Saturday**: 12km easy (5:00-5:15/km comfortable)
- **Sunday**: 28km long run (23km easy + 5km at marathon pace)
- **Total**: 91km for the week

## Success Metrics & Testing

### Phase 1 Targets (Week 8)
- **10K Time Trial**: 42:30 (4:15/km for 10k)
- **Long Run**: 30km at 5:00/km without excessive fatigue
- **Resting HR**: Stable or decreasing trend
- **Weekly Volume**: Comfortable completion of 80km weeks

### Phase 2 Targets (Week 16)
- **Half Marathon**: 1:28:00 (4:10/km average)
- **Marathon Pace**: 20km at 4:15/km feeling controlled
- **Threshold**: 30min continuous at 4:05/km
- **Recovery**: Good adaptation to 90km weeks

### Phase 3 Targets (Week 20)
- **30K Time Trial**: 2:07:30 at marathon pace (confidence test)
- **Speed**: 5x1km at 3:55/km (speed reserve validation)
- **Readiness**: Feeling fresh and eager to race

## Risk Mitigation Strategies

### Injury Prevention Protocol
- **Volume Increases**: Maximum 7km per week (10% rule)
- **Recovery Weeks**: Every 4th week with 25-30% volume reduction
- **Surface Variation**: 70% road, 20% trail, 10% track
- **Shoe Rotation**: Minimum 2 pairs, replace every 600km

### Load Management
- **Heart Rate Monitoring**: Stay in prescribed zones
- **RPE Guidance**: Easy should feel conversational (6-7/10)
- **Sleep Target**: 8+ hours per night during heavy training
- **Stress Monitoring**: Reduce intensity during high life stress

### Contingency Planning
- **Missed Sessions**: Easy runs can be skipped, reschedule hard sessions
- **Illness**: Complete rest if fever, easy movement if minor cold
- **Injury**: Immediate assessment, cross-training alternatives
- **Travel**: Maintain easy running, adapt to available facilities

## Nutrition & Recovery Integration

### Fueling Strategy
- **Daily**: 6-8g carbs/kg bodyweight during base, 8-10g during build
- **Long Runs**: Practice race fueling (30-60g carbs/hour after 90min)
- **Recovery**: Protein + carb within 30min post-workout
- **Hydration**: Monitor urine color, increase during high volume

### Recovery Protocols
- **Sleep**: Consistent 8+ hours, track with wearable device
- **Massage**: Weekly during build phase, bi-weekly during base
- **Mobility**: 15min daily routine focusing on hips, calves, glutes
- **Strength**: 2x/week focusing on running-specific movements

## Progress Tracking & Adaptations

### Weekly Monitoring
- **Completion Rate**: Target 95% of planned sessions
- **RPE Trends**: Easy sessions should feel easier over time
- **Sleep Quality**: 7+ hours with good efficiency
- **Motivation**: High enthusiasm for training

### Monthly Assessments
- **Time Trials**: Validate training pace improvements
- **Zone Updates**: Recalculate based on fitness improvements
- **Plan Adjustments**: Modify based on adaptation and life factors
- **Equipment Review**: Check shoe mileage, gear condition

### Adaptation Triggers
- **Ahead of Schedule**: Consider more aggressive goals or longer taper
- **Behind Schedule**: Extend phases, reduce volume, maintain fitness
- **Injury Issues**: Implement prevention protocols, consider physio
- **Life Stress**: Prioritize recovery, reduce intensity

## JSON Response Schema

```json
{
  "status": "success",
  "command": "/train plan",
  "data": {
    "plan_id": "sub-3-marathon-2025-04",
    "goal": "sub-3-marathon",
    "race_date": "2025-04-20",
    "total_weeks": 28,
    "current_phase": {
      "name": "Base Building",
      "week": 1,
      "focus": "aerobic_development"
    },
    "weekly_structure": {
      "total_volume": "65km",
      "hard_sessions": 2,
      "long_run": "25km",
      "recovery_days": 2
    },
    "key_workouts": [
      {
        "day": "Tuesday",
        "type": "tempo",
        "description": "6x1km at 4:30/km, 90s recovery"
      },
      {
        "day": "Thursday",
        "type": "intervals",
        "description": "8x400m at 4:00/km, 400m jog recovery"
      },
      {
        "day": "Sunday",
        "type": "long_run",
        "description": "25km easy pace (5:00-5:15/km)"
      }
    ],
    "adaptations": [
      "Volume increase: 5km/week for 4 weeks",
      "Long run progression: +2km every 2 weeks"
    ],
    "success_metrics": {
      "week_8_10k": "42:30",
      "week_16_half": "1:28:00",
      "week_20_30k": "2:07:30"
    }
  }
}
```

## Race Day Strategy

### Pre-Race Preparation (Final 10 Days)
- **Carb Loading**: 3 days of 10-12g/kg carbohydrate
- **Tapering**: Maintain intensity, reduce volume significantly
- **Sleep**: Prioritize 8+ hours, especially 2 nights before
- **Mental**: Visualize race segments, practice positive self-talk

### Race Execution
- **Pacing**: Start 5-10 seconds slower than target for first 10k
- **Fueling**: 250ml sports drink every 5k, gel at 25k and 35k
- **Split Strategy**: Even effort (not even pace) accounting for course
- **Mental**: Break race into 4x10.5k segments, focus on process

### Post-Race Recovery
- **Immediate**: Easy walking, hydration, gentle stretching
- **Week 1**: Easy jogging only, 30-40km total
- **Week 2-3**: Gradual return to normal training
- **Month 2**: Plan next goal and training cycle
```

4. **Plan Generation Modes**:

### Goal-Specific Planning (Default)
- Generate plans for predefined goals (sub-3-marathon, 70.3-improvement)
- Apply goal-specific periodization and progression
- Include realistic timeline and success probability
- Integrate race-specific training and strategy

### Custom Goal Planning (`--goal "description"`)
- Create plans for user-defined goals
- Analyze goal requirements and design custom periodization
- Provide achievability assessment and timeline recommendations
- Adapt existing templates to match custom objectives

### Fitness-Based Planning (`--current-fitness analyze`)
- Generate plans based on comprehensive fitness analysis
- Determine optimal goals based on current capabilities
- Create progressive challenges that match fitness trajectory
- Include detailed gap analysis and improvement pathways

### Timeline-Specific Planning (`--weeks N`, `--race-date DATE`)
- Adapt periodization to available time
- Optimize phase distribution for given timeline
- Adjust progression rates based on time constraints
- Include contingency planning for compressed timelines

## Parameters:
- `GOAL` - Target goal (sub-3-marathon, 70.3-improvement, custom description)
- `--race-date DATE` - Specific race date for timeline planning
- `--weeks N` - Total training weeks available
- `--current-fitness analyze` - Base plan on comprehensive fitness analysis
- `--experience LEVEL` - Athlete experience level (beginner, intermediate, advanced)
- `--volume PREFERENCE` - Volume preference (conservative, moderate, aggressive)
- `--save-plan` - Save generated plan for future adaptation

## Integration Points:
- **Input**: Athlete profile, training zones, current fitness data, goal specifications
- **Output**: Comprehensive periodized training plan with progression tracking
- **Monitoring**: Integration with `/train week` for detailed weekly planning
- **Adaptation**: Connection with `/train adapt` for plan modifications

## Error Handling:
- Unrealistic goals: Provide achievability assessment and alternative suggestions
- Insufficient time: Recommend minimum timeline or modified goals
- Missing fitness data: Request recent performance data or testing
- Conflicting constraints: Prioritize safety and provide compromise solutions

Focus on creating scientifically sound, individualized training plans that balance ambition with realism while maintaining athlete safety and long-term development.