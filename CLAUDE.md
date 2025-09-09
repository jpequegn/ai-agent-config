# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an AI agent metrics and configuration tracking repository. It's designed to maintain a history of metrics and performance data from AI agent interactions.

## Repository Structure

```
ai-agent-config/
├── metrics/
│   └── metrics-history.md    # Weekly metrics tracking file
└── README.md                  # Basic repository documentation
```

## Key Files

- **metrics/metrics-history.md**: Automatically updated by weekly check-ins to track agent performance metrics over time

## Development Workflow

### Updating Metrics
The metrics history file is designed to be automatically updated. When adding new metrics:
1. Append new entries to `metrics/metrics-history.md`
2. Follow the existing format (if established)
3. Include timestamp and relevant performance data

### Git Workflow
- Repository URL: `https://github.com/jpequegn/ai-agent-config.git`
- Main branch: `main`
- Commit messages should be descriptive of metrics updates or configuration changes

## Notes

This repository is in its initial state. As it grows, this file should be updated to include:
- Specific metrics format and structure once established
- Any automation scripts or tools for metrics collection
- Configuration file formats and schemas as they are added