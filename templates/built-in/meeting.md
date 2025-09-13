---
description: "General meeting notes template"
category: "meeting"
para_suggestion: "1-projects"
variables:
  - name: "title"
    description: "Meeting title/subject"
    required: true
  - name: "attendees"
    description: "Meeting attendees (comma-separated)"
    required: false
  - name: "project"
    description: "Related project name"
    required: false
---

# Meeting: {{ title }} - {{ date }}

**Date:** {{ datetime }}
**Attendees:** {{ attendees | default('TBD') }}
{% if project %}**Project:** {{ project }}
{% endif %}**Duration:** [Duration]

## Pre-Meeting
- [ ] Agenda prepared
- [ ] Materials shared
- [ ] Participants notified

## Agenda
1. [Agenda item 1]
2. [Agenda item 2]
3. [Agenda item 3]

## Discussion

### [Topic 1]
- Discussion points
- Key decisions
- Concerns raised

### [Topic 2]
- Discussion points
- Key decisions
- Concerns raised

## Decisions Made
- [ ] Decision 1 - [Decision details]
- [ ] Decision 2 - [Decision details]

## Action Items
- [ ] [Action item 1] - @[person] - Due: [date]
- [ ] [Action item 2] - @[person] - Due: [date]
- [ ] [Action item 3] - @[person] - Due: [date]

## Next Steps
- [ ] Schedule follow-up meeting
- [ ] Send meeting summary
- [ ] Update project documentation

## Follow-up
**Next Meeting:** [Date/Time]
**Agenda Preview:** [Items for next meeting]

---
**Tags:** meeting{% if project %}, {{ project | slugify }}{% endif %}
**PARA Location:** {% if project %}1-projects/{{ project | slugify }}/{% else %}2-areas/meetings/{% endif %}