---
name: podcast-digest
description: Generate AI-powered summaries and insights from podcast transcripts
---

# Podcast Digest - Generate Episode Summaries

Generate comprehensive AI-powered summaries from podcast transcripts using local LLMs (Ollama) or cloud providers.

## Usage
- `/podcast digest` - Generate digests for all transcribed episodes
- `/podcast digest --episode-id ID` - Generate digest for specific episode
- `/podcast digest --provider ollama --model llama3.2` - Use specific LLM
- `/podcast digest --provider anthropic` - Use Claude for analysis

## Instructions

You are responsible for generating intelligent podcast summaries through the P³ digest system.

### Environment Configuration
```python
import subprocess
from pathlib import Path

P3_PATH = Path("/Users/julienpequegnot/Code/parakeet-podcast-processor")
P3_VENV = P3_PATH / "venv" / "bin" / "activate"
```

### Command Execution

**Parse Arguments:**
- `--episode-id ID` (optional): Specific episode to process
- `--provider PROVIDER` (optional): LLM provider
  - `ollama` (default): Local Ollama instance
  - `openai`: OpenAI API
  - `anthropic`: Claude API
- `--model MODEL` (optional): Specific model
  - Ollama: `llama3.2` (default), `mistral`, `mixtral`
  - OpenAI: `gpt-4`, `gpt-3.5-turbo`
  - Anthropic: `claude-3-opus`, `claude-3-sonnet`

**Execute Digest:**
```bash
cd /Users/julienpequegnot/Code/parakeet-podcast-processor
source venv/bin/activate
p3 digest --provider ollama --model llama3.2 --skip-errors
```

**Execution Details:**
- Operation timeout: 600 seconds (10 minutes)
- Expected time: ~10 seconds per transcript (local Ollama)
- Cloud APIs: ~5-15 seconds depending on episode length
- Output: Structured markdown with key insights

### Output Format

**Success Response:**
```
📝 Generating Podcast Digests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Provider: Ollama (llama3.2)

✅ Digest Generation:

1. All-In Podcast - E147: AI Revolution in Enterprise
   ⏱️  Processing: 8.2s | 📝 14,523 words
   ✅ Digest generated

2. My First Million - E423: Building in Public
   ⏱️  Processing: 6.7s | 📝 11,847 words
   ✅ Digest generated

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
• Processed: 2 episodes
• Total time: 14.9s
• Average: 7.5s per episode

Next Steps:
💡 View digests: Check digest files in P³ directory
💡 Analyze content: /podcast [query about the content]
💡 Export: /podcast export --date today
```

**Detailed Digest Display:**

When generating a digest, display the formatted output:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# All-In Podcast E147: AI Revolution in Enterprise

**📅 Date**: 2025-10-01 | **⏱️ Duration**: 82 min | **🎙️ Podcast**: All-In

## 📌 Key Takeaways

• Enterprise AI adoption is accelerating faster than expected, with companies moving from experimentation to production in record time

• OpenAI's enterprise tier is seeing 40% month-over-month growth, indicating strong demand for productized AI solutions

• Regulatory landscape is shifting toward AI safety frameworks, with both EU and US preparing comprehensive legislation

• The gap between AI capabilities and practical implementation is narrowing, driven by improved tooling and infrastructure

• Venture capital is flowing heavily into AI infrastructure and enterprise applications, with valuations reaching historic highs

## 🎯 Main Themes

### 1. Enterprise AI Transformation
The conversation focused heavily on how enterprises are adopting AI technologies. The hosts discussed the rapid shift from pilot projects to full-scale deployments, with particular emphasis on:
- Integration with existing enterprise systems
- ROI measurement and business case development
- Change management and organizational readiness

### 2. Investment Landscape Changes
The podcast explored shifting investment patterns in AI:
- Infrastructure investments (compute, data platforms)
- Application layer opportunities
- Consolidation predictions in the AI tooling space

### 3. Regulatory Considerations
Discussion of emerging regulatory frameworks:
- EU AI Act implications for global companies
- US approach to AI governance
- Balance between innovation and safety

## 💬 Notable Quotes

> "We're seeing AI move from experimentation to production faster than any technology in history. What took cloud computing 10 years is happening with AI in 18 months." - Chamath Palihapitiya

> "The question isn't whether AI will transform your business, it's whether you'll still have a business if you don't transform with AI." - Jason Calacanis

> "Enterprise AI adoption follows a pattern: skepticism, pilot projects, executive buy-in, then rapid scaling. We're seeing companies skip straight to step four." - David Friedberg

## 🎓 Key Insights

**Technical Evolution**
- Foundation models are becoming commoditized
- Focus shifting to fine-tuning and domain-specific applications
- Infrastructure layer seeing significant investment

**Business Impact**
- Productivity gains of 20-40% in early adopters
- New business models emerging around AI capabilities
- Traditional software companies under pressure to integrate AI

**Market Dynamics**
- Consolidation expected in crowded tooling space
- Winners will have distribution and integration advantages
- Open source playing significant role in democratization

## ✅ Action Items & Recommendations

**For Businesses:**
- Evaluate current AI readiness and identify pilot opportunities
- Invest in data infrastructure and quality
- Develop AI governance frameworks before regulatory mandates

**For Investors:**
- Monitor regulatory developments closely
- Focus on application layer with clear ROI
- Consider infrastructure plays for long-term positioning

**For Individuals:**
- Develop AI literacy and practical skills
- Understand how AI impacts your industry
- Experiment with AI tools in daily workflows

## 🔗 Related Topics

- Previous episodes on AI regulation (E142, E145)
- OpenAI's enterprise strategy
- EU AI Act implementation timeline
- Venture capital trends in AI sector

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Error Handling

**No Transcripts Available:**
```
📭 No transcripts available for digest generation

Status:
• Downloaded: [count] episodes
• Transcribed: 0 episodes
• Digests: [count] episodes

Generate transcripts first:
  /podcast transcribe
```

**LLM Provider Error:**
```
❌ Digest Generation Failed

Provider: Ollama
Error: Connection refused - Ollama not running

Solutions:
1. Start Ollama: ollama serve
2. Verify Ollama is installed
3. Use alternative provider: /podcast digest --provider openai

Check Ollama status:
  ollama list
```

**API Key Missing:**
```
⚠️  API Key Required

Provider: OpenAI
Error: OPENAI_API_KEY environment variable not set

Set your API key:
  export OPENAI_API_KEY="sk-..."

Or use local Ollama:
  /podcast digest --provider ollama
```

**Timeout:**
```
⏱️  Digest generation timed out after 10 minutes

Episode: [Episode title] (very long transcript)

Solutions:
• Process shorter episodes first
• Use faster model
• Increase chunk processing

Try specific episode:
  /podcast digest --episode-id [shorter-episode-id]
```

### Provider Recommendations

**Ollama (Default - Free & Local)**
- ✅ No API costs
- ✅ Privacy (runs locally)
- ✅ Fast for most episodes
- ⚠️ Requires local installation
- Model: llama3.2 (7B) recommended

**OpenAI (Cloud - High Quality)**
- ✅ Excellent quality
- ✅ Fast processing
- ✅ Reliable
- ❌ API costs (~$0.01-0.05 per episode)
- Model: gpt-4-turbo recommended

**Anthropic (Cloud - Best Quality)**
- ✅ Superior analysis
- ✅ Great for complex content
- ✅ 100K+ token context
- ❌ Higher API costs (~$0.05-0.15 per episode)
- Model: claude-3-sonnet recommended

### Implementation Details

```python
def generate_digest(
    episode_id: str = None,
    provider: str = "ollama",
    model: str = None,
    skip_errors: bool = False
) -> dict:
    """
    Generate podcast digest using AI

    Args:
        episode_id: Specific episode ID (optional)
        provider: LLM provider (ollama, openai, anthropic)
        model: Specific model name (provider-dependent)
        skip_errors: Skip episodes with previous errors

    Returns:
        dict with digest content and metadata

    Raises:
        ValueError: If provider/model invalid
        TimeoutError: If operation exceeds 10 minutes
        RuntimeError: If P³ command fails
    """
    # Validate provider
    valid_providers = ['ollama', 'openai', 'anthropic']
    if provider not in valid_providers:
        raise ValueError(f"Provider must be one of: {valid_providers}")

    # Set default models
    if model is None:
        defaults = {
            'ollama': 'llama3.2',
            'openai': 'gpt-4-turbo',
            'anthropic': 'claude-3-sonnet'
        }
        model = defaults[provider]

    # Build command
    cmd = [
        "p3", "digest",
        "--provider", provider,
        "--model", model
    ]

    if episode_id:
        cmd.extend(["--episode-id", episode_id])

    if skip_errors:
        cmd.append("--skip-errors")

    # Execute with timeout
    result = run_p3_command(cmd, timeout=600)  # 10 minutes

    return parse_digest_output(result)
```

### Performance Expectations

**Processing Time by Provider:**
- Ollama (local): ~8-12 seconds per episode
- OpenAI API: ~5-8 seconds per episode
- Anthropic API: ~6-10 seconds per episode

**Cost Estimates (per episode):**
- Ollama: Free (local compute)
- OpenAI GPT-4: $0.01-0.05
- Anthropic Claude-3: $0.05-0.15

### Digest Content Structure

Each generated digest includes:

1. **Metadata**: Title, date, duration, podcast name
2. **Key Takeaways**: 3-5 bullet points of main insights
3. **Main Themes**: Detailed sections on core topics
4. **Notable Quotes**: Memorable quotes with attribution
5. **Key Insights**: Deep analysis and connections
6. **Action Items**: Practical recommendations
7. **Related Topics**: Links to related content

### Related Commands
- `/podcast transcribe` - Generate transcripts for digest
- `/podcast` - Query digest content
- `/podcast fetch` - Download new episodes

### Tips
- Use Ollama for routine digests (free, fast, good quality)
- Use Claude-3 for in-depth analysis of important content
- Process digests in batches overnight for efficiency
- Digests are saved and can be queried later
- Export digests to markdown for sharing
