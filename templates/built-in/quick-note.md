---
description: "Quick capture template for ideas and thoughts"
category: "capture"
para_suggestion: "inbox"
variables:
  - name: "title"
    description: "Brief title or topic"
    required: false
  - name: "source"
    description: "Where this came from"
    required: false
---

# {{ title | default('Quick Note') }} - {{ date }}

**Created:** {{ datetime }}
{% if source %}**Source:** {{ source }}{% endif %}

## Main Idea
[Capture the key thought, idea, or information here]

## Details
- [Supporting detail 1]
- [Supporting detail 2]
- [Supporting detail 3]

## Context
{% if source %}**Where:** {{ source }}{% endif %}
**Why important:** [Why did this catch your attention?]

## Potential Actions
- [ ] [Potential action 1]
- [ ] [Potential action 2]
- [ ] [Research needed]

## Related Topics
- [Related project/area 1]
- [Related project/area 2]

## Processing Notes
*To be filled during inbox review:*
- **PARA Category:** [Projects/Areas/Resources/Archive]
- **Move to:** [Specific folder path]
- **Priority:** [High/Medium/Low]
- **Next action:** [What to do with this]

---
**Tags:** quick-note, inbox{% if source %}, {{ source | slugify }}{% endif %}
**PARA Location:** inbox/ (process during review)