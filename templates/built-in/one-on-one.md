---
description: "One-on-one meeting template"
category: "meeting"
para_suggestion: "2-areas"
variables:
  - name: "person"
    description: "Person you're meeting with"
    required: true
  - name: "title"
    description: "Meeting focus/title"
    required: false
---

# 1:1 with {{ person }} - {{ date }}

**Date:** {{ datetime }}
**Participants:** {{ user_name }}, {{ person }}
{% if title %}**Focus:** {{ title }}{% endif %}

## Check-in
- **How are things going overall?**
- **Any blockers or challenges?**
- **What's going well?**

## Work & Projects

### Current Focus
- [Current project/priority 1]
- [Current project/priority 2]
- [Current project/priority 3]

### Progress Updates
- **Wins/Accomplishments:**
  - [Achievement 1]
  - [Achievement 2]

- **Challenges:**
  - [Challenge 1]
  - [Challenge 2]

### Upcoming Work
- [Next priority 1]
- [Next priority 2]

## Development & Growth

### Skills & Learning
- **What would you like to learn/improve?**
- **Any training or resources needed?**
- **Career goals discussion**

### Feedback Exchange
- **Feedback for {{ person }}:**
  - [Positive feedback]
  - [Areas for growth]

- **Feedback from {{ person }}:**
  - [Feedback received]

## Team & Process

### Team Dynamics
- **How is collaboration going?**
- **Any team concerns?**
- **Process improvements?**

### Support Needed
- **What can I help with?**
- **Resources or support needed?**
- **Blockers to remove?**

## Action Items
- [ ] [Action for {{ user_name }}] - Due: [date]
- [ ] [Action for {{ person }}] - Due: [date]
- [ ] [Shared action] - Due: [date]

## Notes for Next Time
- **Topics to revisit:**
- **Goals to check on:**
- **Follow-ups needed:**

---
**Next 1:1:** [Date]
**Tags:** one-on-one, {{ person | slugify }}, team-management
**PARA Location:** 2-areas/team-management/one-on-ones/