---
name: podcast-fetch
description: Download new podcast episodes from configured RSS feeds
---

# Podcast Fetch - Download Episodes

Download new podcast episodes from configured RSS feeds using the Parakeet Podcast Processor (P³).

## Usage
- `/podcast fetch` - Download up to 10 new episodes (default)
- `/podcast fetch --max-episodes 5` - Download up to 5 episodes
- `/podcast fetch --max-episodes 20` - Download up to 20 episodes

## Instructions

You are responsible for downloading podcast episodes through the P³ system.

### Environment Configuration
```python
import subprocess
from pathlib import Path

P3_PATH = Path("/Users/julienpequegnot/Code/parakeet-podcast-processor")
P3_VENV = P3_PATH / "venv" / "bin" / "activate"
```

### Command Execution

**Parse Arguments:**
- Extract `--max-episodes N` from user input (default: 10)
- Validate N is a positive integer (1-50 range recommended)

**Execute Fetch:**
```bash
cd /Users/julienpequegnot/Code/parakeet-podcast-processor
source venv/bin/activate
p3 fetch --max-episodes [N]
```

**Execution Details:**
- Operation timeout: 300 seconds (5 minutes)
- Expected time: ~30 seconds per episode
- Audio normalization: Automatic (16kHz mono)

### Output Format

**Success Response:**
```
📥 Fetching Podcast Episodes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Downloading up to [N] episodes...

✅ Downloaded Episodes:
1. All-In Podcast - E147: AI Revolution in Enterprise
   📅 2025-10-01 | ⏱️  82 min | 📦 125 MB

2. My First Million - E423: Building in Public
   📅 2025-09-30 | ⏱️  67 min | 📦 98 MB

3. Lex Fridman Podcast - #394: Sam Altman Returns
   📅 2025-09-29 | ⏱️  156 min | 📦 228 MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
• Downloaded: [count] episodes
• Total size: [size] MB
• Total duration: [duration] hours

Next Steps:
💡 Transcribe episodes: /podcast transcribe
💡 Check status: /podcast
```

**Partial Success:**
```
📥 Fetching Podcast Episodes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Downloaded: [count] episodes
⚠️  Skipped: [count] episodes (already downloaded)
❌ Failed: [count] episodes

Failed Downloads:
• [Episode title] - [Error reason]

Successfully downloaded [count] new episodes.
```

**Error Response:**
```
❌ Download Failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Error: [error message]

Possible causes:
• Network connectivity issues
• RSS feed unavailable
• Invalid feed configuration
• Disk space insufficient

Troubleshooting:
1. Check internet connection
2. Verify RSS feeds in config/feeds.yaml
3. Check available disk space
4. Try with fewer episodes: /podcast fetch --max-episodes 5
```

### Error Handling

**P³ Not Found:**
```
❌ Error: P³ system not found

Expected location: /Users/julienpequegnot/Code/parakeet-podcast-processor

Please verify P³ is installed correctly.
```

**Invalid Arguments:**
```
⚠️  Invalid argument: --max-episodes must be a positive integer (1-50)

Usage: /podcast fetch --max-episodes [N]
Example: /podcast fetch --max-episodes 10
```

**Timeout:**
```
⏱️  Operation timed out after 5 minutes

This may happen with slow network connections or many episodes.

Suggestions:
• Try with fewer episodes: /podcast fetch --max-episodes 5
• Check network connection
• Retry the operation
```

**Disk Space:**
```
💾 Insufficient disk space

Required: ~[size] MB per episode
Available: [available] MB

Free up disk space and try again.
```

### Implementation Details

```python
def fetch_episodes(max_episodes: int = 10) -> dict:
    """
    Fetch podcast episodes using P³ CLI

    Args:
        max_episodes: Maximum number of episodes to download (1-50)

    Returns:
        dict with download results and metadata

    Raises:
        ValueError: If max_episodes out of range
        TimeoutError: If operation exceeds 5 minutes
        RuntimeError: If P³ command fails
    """
    # Validate arguments
    if not 1 <= max_episodes <= 50:
        raise ValueError("max_episodes must be between 1 and 50")

    # Build command
    cmd = f"p3 fetch --max-episodes {max_episodes}"

    # Execute with timeout
    result = run_p3_command(
        cmd.split(),
        timeout=300  # 5 minutes
    )

    # Parse and return results
    return parse_fetch_output(result)
```

### Performance Expectations

- **Audio Download**: ~30 seconds per episode
- **Audio Normalization**: ~5 seconds per episode
- **Total Time**: ~35 seconds × number of episodes
- **Network Bandwidth**: ~150 MB per hour of audio

### Configuration

Episodes are downloaded based on RSS feeds configured in:
```
/Users/julienpequegnot/Code/parakeet-podcast-processor/config/feeds.yaml
```

### Related Commands
- `/podcast` - Check download status
- `/podcast transcribe` - Transcribe downloaded episodes
- `/podcast digest` - Generate episode summaries

### Tips
- Start with fewer episodes (5-10) to test
- Check available disk space before large downloads
- Downloaded episodes persist across sessions
- Already downloaded episodes are automatically skipped
