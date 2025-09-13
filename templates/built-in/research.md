---
description: "Research notes and learning template"
category: "research"
para_suggestion: "3-resources"
variables:
  - name: "topic"
    description: "Research topic or subject"
    required: true
  - name: "source"
    description: "Primary source or starting point"
    required: false
  - name: "purpose"
    description: "Why researching this topic"
    required: false
---

# Research: {{ topic }} - {{ date }}

**Date:** {{ datetime }}
**Topic:** {{ topic }}
{% if source %}**Primary Source:** {{ source }}{% endif %}
{% if purpose %}**Purpose:** {{ purpose }}{% endif %}

## Research Question(s)
- [Primary question you want to answer]
- [Secondary question]
- [What specific aspect interests you?]

## Background
**What I already know:**
- [Current knowledge point 1]
- [Current knowledge point 2]

**What I need to learn:**
- [Knowledge gap 1]
- [Knowledge gap 2]

## Sources & References

### Primary Sources
1. **[Source Title/Name]**
   - Type: [Book/Article/Website/Video]
   - Author: [Author name]
   - URL/Reference: [Link or citation]
   - Key insights: [What did you learn?]

2. **[Source Title/Name]**
   - Type: [Book/Article/Website/Video]
   - Author: [Author name]
   - URL/Reference: [Link or citation]
   - Key insights: [What did you learn?]

### Supporting Sources
- [Additional source 1] - [Key point]
- [Additional source 2] - [Key point]
- [Additional source 3] - [Key point]

## Key Findings

### Main Insights
1. **[Insight 1]**
   - Details: [Explanation]
   - Source: [Where this came from]
   - Importance: [Why this matters]

2. **[Insight 2]**
   - Details: [Explanation]
   - Source: [Where this came from]
   - Importance: [Why this matters]

### Surprising Discoveries
- [Something unexpected you learned]
- [Assumption that was challenged]

### Questions Raised
- [New questions that emerged]
- [Areas needing deeper exploration]

## Patterns & Connections
- **Connects to:** [Related topics/projects]
- **Patterns noticed:** [Recurring themes]
- **Contradictions:** [Conflicting information]

## Practical Applications
- **How can I use this?**
  - [Application 1]
  - [Application 2]

- **Next experiments/actions:**
  - [ ] [Try/test something]
  - [ ] [Apply learning to project]
  - [ ] [Share with team/others]

## Further Research Needed
- [ ] [Specific area to explore deeper]
- [ ] [Expert to contact]
- [ ] [Additional source to find]
- [ ] [Experiment to conduct]

## Summary
**Key Takeaways:**
- [Main takeaway 1]
- [Main takeaway 2]
- [Main takeaway 3]

**Changed my thinking about:**
[How this research shifted your perspective]

---
**Tags:** research, {{ topic | slugify }}, learning
**PARA Location:** 3-resources/{{ topic | slugify }}/