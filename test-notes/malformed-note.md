---
title: "Malformed Note
date: 2024-09-13
category: [this, is, malformed, yaml
tags: no closing bracket
---

# This is a note with malformed frontmatter

The YAML above is invalid, but the engine should handle it gracefully.

- [ ] This should still be parsed as an action item
- [x] This one is completed
- [ ] Another item without assignee

**Attendees:** Jane Doe, john@example.com

Some content with #hashtags and dates like 2024-12-25.

This note should demonstrate graceful error handling.