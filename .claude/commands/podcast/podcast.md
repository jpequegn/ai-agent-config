---
name: podcast
description: Parakeet Podcast Processor (P³) interface - Interactive podcast analysis and status
---

# Podcast Processing Command (Default Mode)

Interface to the Parakeet Podcast Processor (P³) system for podcast downloading, transcription, and analysis.

## Usage
- `/podcast` - Show pipeline status and enable interactive analysis
- `/podcast [query]` - Analyze podcast content with natural language query

## Instructions

You are an intelligent podcast analysis assistant interfacing with the Parakeet Podcast Processor (P³) system.

### Environment Configuration
```python
import subprocess
from pathlib import Path

P3_PATH = Path("/Users/julienpequegnot/Code/parakeet-podcast-processor")
P3_VENV = P3_PATH / "venv" / "bin" / "activate"
```

### Primary Task: Show Status

When invoked without arguments, execute `p3 status` to show the current pipeline state:

```bash
cd /Users/julienpequegnot/Code/parakeet-podcast-processor
source venv/bin/activate
p3 status
```

Display results in this format:

```
📻 Podcast Pipeline Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Downloaded:    [count] episodes
Transcribed:   [count] episodes
Processed:     [count] episodes
Pending:       [count] episodes

Recent Activity:
• [Episode title] - [Podcast name] ([status])
• [Episode title] - [Podcast name] ([status])
...

💡 Use subcommands:
   /podcast fetch - Download new episodes
   /podcast transcribe - Transcribe audio
   /podcast digest - Generate summaries
```

### Secondary Task: Interactive Analysis

When invoked with a query (e.g., `/podcast What are the key themes?`), use the P³ analyze capabilities:

```bash
cd /Users/julienpequegnot/Code/parakeet-podcast-processor
source venv/bin/activate
p3 analyze --query "[user's query]" --format json
```

**Example Queries:**
- "What are the key themes from this week's podcasts?"
- "Find episodes discussing AI and venture capital"
- "Summarize the latest episode from All-In Podcast"
- "What topics were covered about regulatory frameworks?"

**Analysis Output:**
- Extract relevant information from podcast database
- Provide context-aware answers with episode references
- Include timestamps and quotes when relevant
- Suggest related episodes or topics

### Error Handling

**P³ Not Found:**
```
❌ Error: Parakeet Podcast Processor not found at expected location.

Expected: /Users/julienpequegnot/Code/parakeet-podcast-processor

Please ensure P³ is installed and the path is correct.
```

**Virtual Environment Issues:**
```
⚠️  Warning: Virtual environment not activated properly.

Try manually activating:
  cd /Users/julienpequegnot/Code/parakeet-podcast-processor
  source venv/bin/activate
  p3 status
```

**No Episodes Found:**
```
📭 No episodes in database.

Get started with:
  /podcast fetch --max-episodes 10
```

### Performance Notes
- Status check: <1 second
- Analysis queries: 2-5 seconds depending on database size
- All operations timeout after 60 seconds

### Related Commands
- `/podcast fetch` - Download new podcast episodes
- `/podcast transcribe` - Transcribe downloaded audio
- `/podcast digest` - Generate episode summaries

### Technical Details

**Implementation:**
```python
def run_p3_command(cmd: list[str], timeout: int = 60) -> str:
    """Execute P³ command in proper environment"""
    full_cmd = (
        f"cd {P3_PATH} && "
        f"source {P3_VENV} && "
        f"{' '.join(cmd)}"
    )

    result = subprocess.run(
        full_cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        raise Exception(f"P³ command failed: {result.stderr}")

    return result.stdout
```

**Command Execution:**
- Validate P³ installation exists
- Activate virtual environment
- Execute appropriate p3 command
- Parse and format output
- Handle errors gracefully

### Output Format

Always provide clear, formatted output with:
- Status indicators (✅ ❌ ⚠️ 📻 💡)
- Structured information with headers
- Actionable suggestions
- Links to related commands
