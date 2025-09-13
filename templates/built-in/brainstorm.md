---
description: "Brainstorming session template"
category: "creative"
para_suggestion: "1-projects"
variables:
  - name: "topic"
    description: "Brainstorming topic or challenge"
    required: true
  - name: "participants"
    description: "Session participants"
    required: false
  - name: "duration"
    description: "Session duration"
    required: false
---

# Brainstorm: {{ topic }} - {{ date }}

**Date:** {{ datetime }}
**Topic:** {{ topic }}
{% if participants %}**Participants:** {{ participants }}{% endif %}
{% if duration %}**Duration:** {{ duration }}{% else %}**Duration:** [Duration]{% endif %}

## Challenge/Opportunity
**Problem Statement:**
{{ topic }}

**Context:**
- [Background information]
- [Current situation]
- [Constraints or requirements]

**Success Criteria:**
- [What does success look like?]
- [Key metrics or outcomes]

## Ground Rules
- [ ] No judgment during idea generation
- [ ] Build on others' ideas
- [ ] Quantity over quality initially
- [ ] Stay focused on the topic
- [ ] Capture everything

## Ideas Generated

### Round 1: Initial Ideas
1. [Idea 1]
2. [Idea 2]
3. [Idea 3]
4. [Idea 4]
5. [Idea 5]

### Round 2: Building & Combining
- **Idea combinations:**
  - [Combination 1]
  - [Combination 2]

- **Variations:**
  - [Variation 1]
  - [Variation 2]

### Round 3: Wild Ideas
- [Crazy idea 1]
- [Crazy idea 2]
- [What if...?]

## Idea Evaluation

### Top Ideas (Initial Filter)
1. **[Idea Name]**
   - Pros: [Benefits]
   - Cons: [Challenges]
   - Effort: [High/Medium/Low]
   - Impact: [High/Medium/Low]

2. **[Idea Name]**
   - Pros: [Benefits]
   - Cons: [Challenges]
   - Effort: [High/Medium/Low]
   - Impact: [High/Medium/Low]

3. **[Idea Name]**
   - Pros: [Benefits]
   - Cons: [Challenges]
   - Effort: [High/Medium/Low]
   - Impact: [High/Medium/Low]

### Priority Matrix
| Idea | Impact | Effort | Priority |
|------|--------|--------|----------|
| [Idea 1] | High/Med/Low | High/Med/Low | 1/2/3 |
| [Idea 2] | High/Med/Low | High/Med/Low | 1/2/3 |

## Next Steps
- [ ] Research top 3 ideas further
- [ ] Create prototypes/mockups
- [ ] Get stakeholder feedback
- [ ] Define implementation plan
- [ ] Schedule follow-up session

## Follow-up Actions
- [ ] [Action 1] - @[person] - Due: [date]
- [ ] [Action 2] - @[person] - Due: [date]
- [ ] [Action 3] - @[person] - Due: [date]

## Parking Lot
*Ideas to revisit later:*
- [Future idea 1]
- [Future idea 2]

---
**Tags:** brainstorm, {{ topic | slugify }}, creative
**PARA Location:** {% if project %}1-projects/{{ project | slugify }}/{% else %}3-resources/ideas/{% endif %}