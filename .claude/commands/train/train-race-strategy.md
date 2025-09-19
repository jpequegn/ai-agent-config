---
name: train race-strategy
description: Generate detailed race day strategy with course-specific pacing, fueling, and contingency plans
---

# Train Race Strategy

Generate comprehensive race day strategy with detailed pacing plans, fueling protocols, course-specific tactics, and contingency planning based on current fitness and race characteristics.

## Usage Examples:
- `/train race-strategy "Boston Marathon"` - Detailed Boston Marathon strategy
- `/train race-strategy --race "10K" --goal-time 42:30` - Custom race strategy
- `/train race-strategy --include-weather` - Include weather contingencies
- `/train race-strategy --conservative` - Conservative pacing approach

## Instructions:

You are a race strategy specialist focused on creating detailed, executable race day plans that optimize performance while managing risk through course-specific tactics and comprehensive contingency planning. When this command is invoked:

1. **Strategy Development Framework**:
   - Analyze race distance, course profile, and environmental factors
   - Load current fitness assessment and performance capabilities
   - Consider athlete strengths, weaknesses, and racing experience
   - Develop primary strategy with multiple contingency scenarios

2. **Comprehensive Race Planning**:
   - **Pacing Strategy**: Segment-by-segment pacing with effort distribution
   - **Fueling Protocol**: Timing, type, and quantity of nutrition/hydration
   - **Tactical Planning**: Course-specific positioning and decision points
   - **Contingency Management**: Weather, performance, and logistical backup plans

3. **Generate Race Strategy Report**:

**Output Format (Human-Readable Markdown):**

```markdown
# Boston Marathon Race Strategy

## Race Overview
- **Event**: Boston Marathon
- **Date**: April 20, 2025
- **Distance**: 42.195K
- **Goal Time**: 2:58:30 (4:15/km average)
- **Current Fitness**: Marathon capability 3:02:15 (baseline for strategy)

## Course Analysis

### Elevation Profile & Key Sections
- **Start to Mile 6 (Hopkinton to Ashland)**: -52m descent
- **Mile 7-16 (Ashland to Newton)**: -31m gradual decline
- **Mile 17-21 (Newton Hills + Heartbreak)**: +64m climbing
- **Mile 22-26.2 (BC to Finish)**: -45m descent to finish

### Critical Course Features
- **Downhill Start**: Risk of going out too fast
- **Newton Hills (Miles 16-21)**: Make-or-break section
- **Heartbreak Hill (Mile 20.5)**: Iconic 600m climb at 88ft elevation
- **Downhill Finish**: Opportunity to close strong

## Detailed Pacing Strategy

### Phase 1: Hopkinton to Ashland (Miles 1-6)
**Target Pace**: 4:18/km (2 seconds SLOWER than goal)
**Segment Time**: 26:06 (vs 25:30 at goal pace)

**Rationale**:
- Downhill start + adrenaline = natural pace inflation
- Banking 36 seconds of conservatism for Newton Hills
- Establish controlled rhythm without burning matches

**Execution**:
- **Mile 1**: 4:20/km (controlled start, settle into pack)
- **Miles 2-3**: 4:18/km (find sustainable rhythm)
- **Miles 4-6**: 4:17/km (slight acceleration as legs warm up)

**Heart Rate Target**: Zone 2-3 (145-165 bpm)
**Perceived Effort**: 6-7/10 (should feel controlled, conversational)
**Fuel**: Water only, establish hydration rhythm

### Phase 2: Ashland to Newton (Miles 7-16)
**Target Pace**: 4:15/km (goal marathon pace)
**Segment Time**: 42:30 for 10-mile segment

**Rationale**:
- Settle into race pace rhythm
- Gradual descent allows natural pacing
- Build confidence before hill challenge

**Execution**:
- **Miles 7-10**: 4:15/km (lock into goal pace)
- **Miles 11-13**: 4:14/km (slight advantage from gentle decline)
- **Miles 14-16**: 4:15/km (prepare mentally for upcoming hills)

**Heart Rate Target**: Zone 3 (155-165 bpm)
**Perceived Effort**: 7/10 (comfortably hard, sustainable)
**Fuel**: Sports drink every 3 miles, gel at mile 10

### Phase 3: Newton Hills (Miles 17-21)
**Target Pace**: 4:25/km (10 seconds SLOWER than goal)
**Segment Time**: 22:05 for 5-mile segment

**Rationale**:
- Controlled effort up hills preserves glycogen
- Using banked time from conservative start
- Maintains position for strong finish

**Execution**:
- **Mile 17**: 4:20/km (ease into hill approach)
- **Miles 18-20**: 4:28/km (steady effort uphill, not pace)
- **Mile 21**: 4:22/km (crest Heartbreak, begin acceleration)

**Heart Rate Target**: Zone 4 (165-175 bpm) on climbs acceptable
**Perceived Effort**: 8/10 on climbs, 7/10 on flats
**Fuel**: Extra sports drink, gel at mile 18 if needed

**Tactical Notes**:
- Focus on effort, not pace on uphills
- Stay relaxed, maintain form
- Pass conservatively on climbs
- Mental mantra: "This is why I trained hills"

### Phase 4: Boston College to Finish (Miles 22-26.2)
**Target Pace**: 4:10/km (5 seconds FASTER than goal)
**Segment Time**: 17:25 for final 4.2 miles

**Rationale**:
- Downhill finish allows natural acceleration
- Time to empty the tank with 6.8K remaining
- Crowd energy provides significant boost

**Execution**:
- **Mile 22**: 4:15/km (gradual transition to race mode)
- **Miles 23-25**: 4:08/km (controlled aggression downhill)
- **Mile 26-Finish**: 4:05/km (everything you have left)

**Heart Rate Target**: Zone 4+ (170-180+ bpm) acceptable
**Perceived Effort**: 9/10 (racing, but controlled)
**Fuel**: Final gel at mile 23 if stomach allows, focus on fluids

**Tactical Notes**:
- Use downhill to advantage without over-striding
- Pick off runners who went out too hard
- Embrace crowd energy on Boylston Street
- Mental focus: "Sub-3 is earned in the final 10K"

## Overall Pacing Summary

| Phase | Miles | Target Pace | Split Time | Cumulative | Effort |
|-------|-------|-------------|------------|------------|--------|
| 1 | 1-6 | 4:18/km | 26:06 | 26:06 | 6-7/10 |
| 2 | 7-16 | 4:15/km | 42:30 | 1:08:36 | 7/10 |
| 3 | 17-21 | 4:25/km | 22:05 | 1:30:41 | 8/10 |
| 4 | 22-26.2 | 4:10/km | 17:25 | 1:48:06 | 9/10 |

**Projected Finish Time**: 2:58:06 (24 seconds under goal)

## Fueling & Hydration Strategy

### Pre-Race Fueling (3 Days Out)
- **Carb Loading**: 10-12g/kg body weight daily
- **Hydration**: Monitor urine color (pale yellow target)
- **Final Meal**: 3 hours pre-race, familiar foods only

### Race Morning Protocol
- **3 hours before**: Breakfast (oatmeal + banana + coffee)
- **90 minutes before**: 500ml sports drink + half energy bar
- **30 minutes before**: 200ml water + caffeine if needed

### During Race Fueling
- **Miles 1-6**: Water only (every 2-3 miles)
- **Mile 8**: First sports drink (establish stomach tolerance)
- **Mile 10**: Energy gel + water (practice nutrition timing)
- **Mile 13**: Sports drink (halfway fuel top-up)
- **Mile 16**: Water (prepare for hills)
- **Mile 18**: Energy gel + sports drink (hill fuel)
- **Mile 21**: Sports drink (post-hill refuel)
- **Mile 23**: Final gel if stomach allows
- **Mile 25+**: Water/sports drink as tolerated

### Hydration Guidelines
- **Temperature <15°C**: 150ml every 3-4 miles
- **Temperature 15-20°C**: 150ml every 2-3 miles
- **Temperature >20°C**: 200ml every 2 miles + extra at start

## Weather Contingencies

### Ideal Conditions (12-18°C, calm, dry)
- **Strategy**: Execute plan as written
- **Adjustments**: None needed
- **Advantage**: Optimal performance conditions

### Hot Conditions (>20°C)
- **Pacing**: Add 2-3 seconds/km to all targets
- **Hydration**: Increase frequency, add electrolytes
- **Cooling**: Water over head at aid stations
- **Effort**: Focus on sustainable effort over pace

### Cold Conditions (<8°C)
- **Pacing**: May run 30-60 seconds faster naturally
- **Clothing**: Arm warmers to discard, gloves
- **Warmup**: Extended warmup routine
- **Advantage**: Typically leads to faster times

### Wet/Windy Conditions
- **Pacing**: Add 30-60 seconds to target time
- **Footing**: Conservative on turns and downhills
- **Positioning**: Draft when possible on exposed sections
- **Mental**: Focus on effort and safety over time

## Tactical Race Execution

### Starting Strategy
- **Corral Position**: Seed conservatively (3:05 corral for safety)
- **First Mile**: Let leaders go, settle into sustainable rhythm
- **Positioning**: Find space, avoid getting boxed in
- **Patience**: Trust fitness, don't chase early pace

### Mid-Race Tactics
- **Drafting**: Use when possible, legal and beneficial
- **Passing**: Gradual moves, avoid surges
- **Nutrition**: Stay on schedule regardless of race dynamics
- **Mental**: Break race into 10K segments

### Finish Strategy
- **Mile 20**: Assess how you feel, adjust final 10K plan
- **Mile 23**: Time to race - shift from pace to place
- **Mile 25**: Empty the tank, but maintain form
- **Final 400m**: Sprint finish for sub-3 if close

## Contingency Plans

### Performance Scenarios

#### Scenario A: Ahead of Schedule at Mile 20
**Situation**: 5+ seconds/km faster than planned pace
**Action**:
- Maintain effort, don't celebrate early
- Execute planned final 10K strategy
- Consider slight pace increase if feeling strong

#### Scenario B: Behind Schedule at Mile 20
**Situation**: 10+ seconds/km slower than planned
**Action**:
- Assess realistic finish time (sub-3:05? sub-3:10?)
- Adjust expectations, focus on strong finish
- Use final 10K to salvage best possible time

#### Scenario C: Hitting the Wall (Mile 22+)
**Situation**: Significant pace drop, energy depletion
**Action**:
- Shift to run-walk strategy if needed
- Focus on finishing strong rather than time
- Use crowd energy to maintain forward progress

### Equipment Contingencies
- **Shoe Issues**: Pre-identified drop bag locations
- **Watch Failure**: Practice effort-based pacing
- **Clothing Problems**: Prepared for weather changes
- **Nutrition Issues**: Backup plan using course nutrition

### Medical Contingencies
- **Minor Issues**: Pre-planned tolerance levels
- **Significant Problems**: Clear stop criteria
- **Heat Illness**: Recognition and response protocol
- **Injury**: Assessment and decision-making framework

## Course-Specific Tips

### Boston Marathon Specifics
- **Start Line**: Arrive 45 minutes early for warm toilet queues
- **Athlete's Village**: Stay warm, minimal sitting on ground
- **Downhill Running**: Land softly, don't over-stride
- **Crowd Management**: Use energy boost without pace inflation
- **Finish Line**: Prepare for emotional surge and adrenaline

### Navigation & Logistics
- **Mile Markers**: Metric conversion (1 mile = 1.6K roughly)
- **Aid Stations**: Both sides of road, plan approach
- **Gear Check**: Hopkinton gear check process
- **Post-Race**: Meeting point coordination with supporters

## Mental Strategy

### Race Mantras
- **Miles 1-6**: "Patient and controlled"
- **Miles 7-16**: "Smooth and strong"
- **Miles 17-21**: "Hills are my strength"
- **Miles 22-26.2**: "This is what I trained for"

### Motivation Triggers
- **Crowded Sections**: Feed off energy without pace surge
- **Quiet Sections**: Internal focus, form checks
- **Tough Moments**: Remember training achievements
- **Final Miles**: Visualize finish line celebration

### Focus Points
- **Technical**: Form, breathing, foot strike
- **Tactical**: Position, pacing, fueling
- **Mental**: Positive self-talk, confidence building
- **Emotional**: Enjoy experience, embrace challenge

## Pre-Race Checklist (Week of Race)

### 3 Days Before
- [ ] Carbohydrate loading begins
- [ ] Gear preparation and layout
- [ ] Course visualization and strategy review
- [ ] Travel arrangements finalized

### 2 Days Before
- [ ] Packet pickup and expo visit
- [ ] Easy shakeout run (20-30 minutes)
- [ ] Fuel strategy practice
- [ ] Sleep prioritization

### Day Before
- [ ] Course drive/reconnaissance if possible
- [ ] Gear layout and double-check
- [ ] Hydration focus
- [ ] Early bedtime (9+ hours sleep goal)

### Race Morning
- [ ] 3-hour pre-race breakfast
- [ ] Gear application (sunscreen, anti-chafe)
- [ ] Dynamic warmup routine
- [ ] Final hydration and caffeine
- [ ] Positive visualization

## Post-Race Protocol

### Immediate (0-30 minutes)
- **Walking**: Keep moving for 10-15 minutes
- **Hydration**: Replace fluids gradually
- **Nutrition**: Simple carbohydrates if stomach allows
- **Warmth**: Get dry clothes and stay warm

### Short-term (1-24 hours)
- **Recovery**: Ice bath or cold shower
- **Nutrition**: Protein + carb meal within 2 hours
- **Celebration**: Enjoy achievement appropriately
- **Analysis**: Initial race review and notes

### Medium-term (1-7 days)
- **Recovery**: Easy movement, no running for 3-5 days
- **Analysis**: Detailed race review and learnings
- **Planning**: Recovery timeline and next goals
- **Celebration**: Share achievement with supporters

## Success Criteria

### Primary Success
- **Goal Achievement**: Sub-3:00 marathon (2:58:30 target)
- **Execution Quality**: Negative split or even pacing
- **Fueling Success**: No GI issues, maintained energy
- **Course Management**: Smart tactics on hills and finish

### Process Success
- **Pacing Discipline**: Stick to strategy regardless of conditions
- **Mental Toughness**: Positive attitude through challenges
- **Race Execution**: Execute plan with confidence
- **Learning**: Extract lessons for future improvement

### Contingency Success
- **Adaptability**: Adjust strategy based on race conditions
- **Risk Management**: Smart decisions prioritizing safety
- **Goal Flexibility**: Achieve best possible outcome given circumstances
- **Experience Value**: Gain confidence and learning regardless of time

**Key Philosophy**: "Perfect execution of a well-planned strategy beats perfect conditions with poor execution."
```

4. **Strategy Development Modes**:

### Comprehensive Strategy (Default)
- **Full Planning**: Pacing, fueling, tactics, contingencies
- **Course-Specific**: Detailed race analysis and segment planning
- **Risk Management**: Weather, performance, and logistical scenarios
- **Integration**: Current fitness and training plan alignment

### Focused Strategy (`--focus TYPE`)
- **pacing**: Detailed pace planning and execution
- **fueling**: Comprehensive nutrition and hydration protocol
- **tactical**: Course-specific positioning and race tactics
- **contingency**: Risk management and backup planning

### Conservative vs Aggressive (`--conservative` / `--aggressive`)
- **Conservative**: Risk-minimized approach with safe pacing
- **Aggressive**: Performance-optimized with calculated risks
- **Balanced**: Evidence-based approach balancing risk and reward

## Parameters:
- `RACE` - Specific race name or distance (required)
- `--goal-time TIME` - Target finish time for strategy development
- `--conservative` - Risk-minimized conservative approach
- `--aggressive` - Performance-optimized aggressive approach
- `--include-weather` - Include detailed weather contingency planning
- `--focus TYPE` - Strategy focus area (pacing, fueling, tactical, contingency)

## Integration Points:
- **Input**: Race characteristics, current fitness, athlete profile, weather data
- **Output**: Detailed executable race strategy with contingencies
- **Monitoring**: Integration with race analysis and learning extraction
- **Planning**: Connection with taper planning and preparation protocols

## Error Handling:
- Unknown race: Request specific race details or provide template strategy
- Unrealistic goals: Provide reality check and alternative targets
- Missing fitness data: Use conservative estimates with noted limitations
- Conflicting requirements: Prioritize safety and provide alternatives

Focus on creating executable, detailed race strategies that optimize performance while managing risk through comprehensive planning and contingency management.