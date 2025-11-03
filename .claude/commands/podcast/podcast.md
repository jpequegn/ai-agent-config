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
import os
from pathlib import Path

P3_PATH = Path(os.path.expanduser("~/Code/parakeet-podcast-processor"))
P3_VENV = P3_PATH / "venv" / "bin" / "activate"
P3_DB = P3_PATH / "data" / "p3.duckdb"
```

### Database Schema Reference

**CRITICAL**: The P³ system uses DuckDB, not SQLite. Always use the correct database path and schema.

**Database Path**: `~/Code/parakeet-podcast-processor/data/p3.duckdb`

**Table Schemas**:

**episodes table**:
- `id` (INTEGER) - Primary key
- `podcast_id` (INTEGER) - Foreign key to podcasts table
- `title` (VARCHAR) - Episode title
- `date` (TIMESTAMP) - Episode publication date
- `url` (VARCHAR) - Episode URL
- `file_path` (VARCHAR) - Path to downloaded audio file
- `duration_seconds` (INTEGER) - Episode duration
- `status` (VARCHAR) - Processing status (downloaded, transcribed, processed)
- `created_at` (TIMESTAMP) - When episode was added to database
- `s3_url` (VARCHAR) - S3 storage URL if applicable

**podcasts table**:
- `id` (INTEGER) - Primary key
- `title` (VARCHAR) - Podcast name (NOT "name")
- `rss_url` (VARCHAR) - RSS feed URL
- `category` (VARCHAR) - Podcast category
- `created_at` (TIMESTAMP) - When podcast was added

**transcripts table**:
- `id` (INTEGER) - Primary key
- `episode_id` (INTEGER) - Foreign key to episodes table
- `text` (VARCHAR) - Transcript segment text
- `created_at` (TIMESTAMP) - When transcript was created

**IMPORTANT**: Transcripts are stored as **multiple segments per episode**, not as a single record. To get a complete transcript:
```python
# Get all segments for an episode and concatenate
result = conn.execute('''
    SELECT text
    FROM transcripts
    WHERE episode_id = ?
    ORDER BY id ASC
''', [episode_id]).fetchall()

full_transcript = ' '.join([row[0] for row in result])
```

**summaries table**:
- `id` (INTEGER) - Primary key
- `episode_id` (INTEGER) - Foreign key to episodes table
- `key_topics` (JSON) - Array of key topics
- `themes` (JSON) - Array of themes
- `quotes` (JSON) - Array of notable quotes
- `startups` (JSON) - Array of mentioned startups/companies
- `digest_date` (DATE) - Date of digest generation
- `full_summary` (VARCHAR) - Complete episode summary text
- `created_at` (TIMESTAMP) - When summary was created
- `key_takeaways` (JSON) - Array of key takeaways

**Important Notes**:
- Use `created_at` field to filter by download date (NOT `downloaded_at`)
- Podcast name is `podcasts.title` (NOT `podcasts.name`)
- Episode publication date is `episodes.date`
- Join episodes to podcasts using `episodes.podcast_id = podcasts.id`

### Primary Task: Show Status

When invoked without arguments, execute `p3 status` to show the current pipeline state:

```bash
cd ~/Code/parakeet-podcast-processor
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

### Secondary Task: Interactive Analysis & Queries

For natural language queries about podcasts, use **direct DuckDB queries** instead of shell commands for better performance and reliability.

**Query Categories & Examples**:

#### 1. Time-Based Queries
**"What episodes were downloaded today/this week?"**
```python
cd ~/Code/parakeet-podcast-processor && source venv/bin/activate && python3 -c "
import duckdb
from datetime import date

conn = duckdb.connect('data/p3.duckdb')
today = date.today()  # or use date range for weeks

result = conn.execute('''
    SELECT
        e.title,
        p.title as podcast_name,
        e.created_at,
        e.status,
        e.date as episode_date
    FROM episodes e
    JOIN podcasts p ON e.podcast_id = p.id
    WHERE DATE(e.created_at) = ?
    ORDER BY e.created_at DESC
''', [today]).fetchall()

# Format and display results
conn.close()
"
```

#### 2. Content Search Queries
**"Find episodes about [topic]"**
- Query episode titles and summaries tables
- Use LIKE or full-text search on title field
- Join with podcasts for complete context

**"Search transcript for specific content"**
```python
# Search transcripts (remember: multiple segments per episode)
cd ~/Code/parakeet-podcast-processor && source venv/bin/activate && python3 -c "
import duckdb

conn = duckdb.connect('data/p3.duckdb')

# Find episodes with keyword in transcript
result = conn.execute('''
    SELECT DISTINCT
        e.id,
        e.title,
        p.title as podcast_name,
        e.date
    FROM episodes e
    JOIN podcasts p ON e.podcast_id = p.id
    JOIN transcripts t ON t.episode_id = e.id
    WHERE LOWER(t.text) LIKE ?
    ORDER BY e.date DESC
''', ['%keyword%']).fetchall()

# To get full context around a match:
# 1. Get all transcript segments for the episode
# 2. Concatenate them: full_transcript = ' '.join([row[0] for row in segments])
# 3. Search for keyword position: pos = full_transcript.lower().find('keyword')
# 4. Extract context: section = full_transcript[pos-500:pos+2000]

conn.close()
"
```

#### 3. Podcast-Specific Queries
**"Latest episodes from [podcast name]"**
```python
# Filter by podcasts.title and order by episodes.date DESC
```

#### 4. Status Queries
**"What's pending transcription?"**
```python
# Filter by status field: WHERE status = 'downloaded'
```

**Key Query Patterns**:
- Always join episodes to podcasts: `JOIN podcasts p ON e.podcast_id = p.id`
- Use `p.title` for podcast name (never `p.name`)
- Use `e.created_at` for download date filtering
- Use `e.date` for episode publication date
- Format timestamps with `.strftime()` for readability
- Handle empty results gracefully with fallback queries

**Working with Segmented Transcripts**:
- Transcripts are stored as multiple rows per episode (typically 100-1000+ segments)
- Always use `ORDER BY id ASC` when concatenating segments to preserve order
- For search queries, use `DISTINCT` on episode info when joining transcripts
- For content extraction:
  1. Find episode ID with keyword match
  2. Retrieve ALL segments for that episode
  3. Concatenate segments: `' '.join([row[0] for row in segments])`
  4. Search and extract context from full transcript
- A single transcript segment is typically 80-100 characters
- Full episode transcripts range from 50,000-100,000+ characters

**Analysis Output Format**:
- 📻 Use emoji indicators for visual clarity
- Include episode title, podcast name, dates, and status
- Provide counts and summaries
- Suggest related queries or actions

### Error Handling

**Database Schema Errors:**
If you encounter "no such column" or "table does not have column" errors:
1. ✅ CHECK: Use `podcasts.title` NOT `podcasts.name`
2. ✅ CHECK: Use `episodes.created_at` for download date, NOT `downloaded_at`
3. ✅ CHECK: Database is DuckDB at `data/p3.duckdb`, NOT SQLite
4. ✅ VERIFY: Run schema check first if uncertain:
   ```python
   python3 -c "import duckdb; conn = duckdb.connect('data/p3.duckdb'); print(conn.execute('DESCRIBE episodes').fetchall())"
   ```

**P³ Not Found:**
```
❌ Error: Parakeet Podcast Processor not found at expected location.

Expected: ~/Code/parakeet-podcast-processor

Please ensure P³ is installed and the path is correct.
```

**Virtual Environment Issues:**
```
⚠️  Warning: Virtual environment not activated properly.

Try manually activating:
  cd ~/Code/parakeet-podcast-processor
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
- DuckDB queries: <1 second (much faster than shell commands)
- Analysis queries: 2-5 seconds depending on database size
- All operations timeout after 60 seconds

### Best Practices for Query Execution

**DO**:
✅ Use direct DuckDB Python queries for data access
✅ Reference the schema documentation above before writing queries
✅ Test join syntax: `episodes.podcast_id = podcasts.id`
✅ Use parameterized queries with `?` placeholders for safety
✅ Format output with emoji indicators and clear structure

**DON'T**:
❌ Assume SQLite syntax or column names
❌ Use non-existent columns like `podcasts.name` or `episodes.downloaded_at`
❌ Try shell commands when direct database access is better
❌ Skip error handling for empty results

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
