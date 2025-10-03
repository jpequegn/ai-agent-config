---
name: podcast-transcribe
description: Transcribe downloaded podcast audio using Parakeet MLX (Apple Silicon optimized)
---

# Podcast Transcribe - Generate Transcripts

Transcribe podcast audio using Parakeet MLX with Apple Silicon optimization for ultra-fast transcription.

## Usage
- `/podcast transcribe` - Transcribe all pending episodes
- `/podcast transcribe --episode-id ID` - Transcribe specific episode
- `/podcast transcribe --model small` - Use specific Whisper model
- `/podcast transcribe --skip-errors` - Skip episodes with previous errors

## Instructions

You are responsible for transcribing podcast audio through the P³ system with Parakeet MLX.

### Environment Configuration
```python
import subprocess
import os
from pathlib import Path

P3_PATH = Path(os.path.expanduser("~/Code/parakeet-podcast-processor"))
P3_VENV = P3_PATH / "venv" / "bin" / "activate"
```

### Command Execution

**Parse Arguments:**
- `--episode-id ID` (optional): Specific episode to transcribe
- `--model MODEL` (optional): Whisper model (base, small, medium, large)
  - Default: `base` (fastest, good quality)
  - Recommended: `small` (balance of speed/accuracy)
- `--skip-errors` (optional): Skip episodes that previously failed

**Execute Transcription:**
```bash
cd ~/Code/parakeet-podcast-processor
source venv/bin/activate
p3 transcribe --skip-errors --model base
```

**Execution Details:**
- Operation timeout: 600 seconds (10 minutes)
- Performance: 60 min audio → ~1-2 seconds (30x faster than real-time)
- Uses: Apple Silicon MLX optimization
- Output: Full transcript with timestamps

### Output Format

**Success Response:**
```
🎙️  Transcribing Podcast Episodes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using model: base (Apple Silicon MLX)

✅ Transcription Progress:

1. All-In Podcast - E147: AI Revolution in Enterprise
   ⏱️  Duration: 82 min | Processing: 2.4s
   📝 Words: 14,523 | Accuracy: 94.2%
   ✅ Complete

2. My First Million - E423: Building in Public
   ⏱️  Duration: 67 min | Processing: 1.9s
   📝 Words: 11,847 | Accuracy: 92.8%
   ✅ Complete

3. Lex Fridman Podcast - #394: Sam Altman Returns
   ⏱️  Duration: 156 min | Processing: 4.1s
   📝 Words: 27,659 | Accuracy: 95.1%
   ✅ Complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
• Transcribed: 3 episodes
• Total duration: 5.1 hours
• Total words: 54,029
• Processing time: 8.4 seconds
• Speed: ~2,181x faster than real-time 🚀

Next Steps:
💡 Generate summaries: /podcast digest
💡 Analyze content: /podcast [query]
```

**Partial Success:**
```
🎙️  Transcribing Podcast Episodes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Transcribed: 5 episodes
⚠️  Skipped: 2 episodes (already transcribed)
❌ Failed: 1 episode

Failed Episodes:
• All-In E148 - Audio file corrupted
  Fix: Re-download with /podcast fetch

Successfully transcribed 5 new episodes.
```

**Progress Indicator (for long operations):**
```
🎙️  Transcribing...

[████████████████░░░░] 80% (4/5 episodes)

Current: Lex Fridman Podcast - #394
Elapsed: 45s | Remaining: ~12s
```

### Model Selection Guide

**base** (Default - Fastest)
- Speed: ~30x faster than real-time
- Accuracy: ~92-94%
- Best for: Quick processing, casual listening
- Size: 74 MB

**small** (Recommended - Balanced)
- Speed: ~20x faster than real-time
- Accuracy: ~94-96%
- Best for: Most use cases, good balance
- Size: 244 MB

**medium** (High Accuracy)
- Speed: ~10x faster than real-time
- Accuracy: ~96-97%
- Best for: Important content, detailed analysis
- Size: 769 MB

**large** (Maximum Accuracy)
- Speed: ~5x faster than real-time
- Accuracy: ~97-98%
- Best for: Critical transcriptions, publication
- Size: 1550 MB

### Error Handling

**P³ Not Found:**
```
❌ Error: P³ system not found

Expected location: ~/Code/parakeet-podcast-processor

Please verify P³ is installed correctly.
```

**No Episodes to Transcribe:**
```
📭 No episodes available for transcription

Status:
• Downloaded: 0 episodes
• Already transcribed: [count] episodes

Get started:
  /podcast fetch --max-episodes 10
```

**Audio File Error:**
```
❌ Transcription Failed

Episode: [Episode title]
Error: Audio file corrupted or invalid format

Solutions:
1. Re-download: /podcast fetch
2. Check audio file integrity
3. Skip with --skip-errors flag
```

**Model Download Required:**
```
📥 Downloading Whisper Model...

Model: small (244 MB)
This is a one-time download.

[████████░░░░░░░░░░░░] 40% (98 MB / 244 MB)

Please wait...
```

**Timeout:**
```
⏱️  Transcription timed out after 10 minutes

This is unusual with Parakeet MLX optimization.

Possible causes:
• Very long episode (>3 hours)
• System resource constraints
• Model loading issues

Try:
• Transcribe specific episode: /podcast transcribe --episode-id [ID]
• Use faster model: /podcast transcribe --model base
• Check system resources
```

### Implementation Details

```python
def transcribe_episodes(
    episode_id: str = None,
    model: str = "base",
    skip_errors: bool = False
) -> dict:
    """
    Transcribe podcast episodes using Parakeet MLX

    Args:
        episode_id: Specific episode ID (optional)
        model: Whisper model (base, small, medium, large)
        skip_errors: Skip episodes with previous errors

    Returns:
        dict with transcription results and statistics

    Raises:
        ValueError: If model invalid
        TimeoutError: If operation exceeds 10 minutes
        RuntimeError: If P³ command fails
    """
    # Validate model
    valid_models = ['base', 'small', 'medium', 'large']
    if model not in valid_models:
        raise ValueError(f"Model must be one of: {valid_models}")

    # Build command
    cmd = ["p3", "transcribe", "--model", model]

    if episode_id:
        cmd.extend(["--episode-id", episode_id])

    if skip_errors:
        cmd.append("--skip-errors")

    # Execute with timeout
    result = run_p3_command(cmd, timeout=600)  # 10 minutes

    return parse_transcription_output(result)
```

### Performance Expectations

**With Parakeet MLX (Apple Silicon):**
- 60 min audio → 1-2 seconds (30-50x faster than real-time)
- 120 min audio → 3-4 seconds
- Batch of 10 episodes (~10 hours) → ~30 seconds

**Comparison:**
- Traditional Whisper: 60 min → 60 min (real-time)
- Whisper.cpp: 60 min → 5-10 min (6-12x)
- Parakeet MLX: 60 min → 1-2 sec (30-50x) ⚡

### Technical Details

**Parakeet MLX Features:**
- Apple Silicon GPU acceleration
- Optimized for M1/M2/M3 chips
- Batched processing for efficiency
- Automatic audio normalization
- Timestamp generation
- Speaker diarization (when available)

### Related Commands
- `/podcast fetch` - Download episodes for transcription
- `/podcast digest` - Generate summaries from transcripts
- `/podcast` - Check transcription status

### Tips
- Use `base` model for quick processing of many episodes
- Use `small` for best balance of speed and accuracy
- Use `--skip-errors` to avoid re-processing failed episodes
- Transcription quality depends on audio quality
- Very long episodes (>3 hours) may take longer
