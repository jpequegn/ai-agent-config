#!/usr/bin/env python3
"""
PARA Method Note Processing Engine

A comprehensive engine for parsing, processing, and manipulating markdown note files
with frontmatter, extracting action items, attendees, dates, tags, and providing
auto-categorization suggestions.
"""

import os
import re
import sys
import yaml
import shutil
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum

class ParaCategory(Enum):
    """PARA Method categories"""
    PROJECTS = "1-projects"
    AREAS = "2-areas"
    RESOURCES = "3-resources"
    ARCHIVE = "4-archive"
    INBOX = "inbox"

@dataclass
class ActionItem:
    """Represents an action item extracted from a note"""
    text: str
    completed: bool
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    line_number: Optional[int] = None
    priority: Optional[str] = None

@dataclass
class ParsedNote:
    """Represents a fully parsed note with all extracted information"""
    file_path: str
    frontmatter: Dict[str, Any]
    content: str
    raw_content: str
    action_items: List[ActionItem]
    attendees: List[str]
    dates: List[str]
    tags: List[str]
    suggested_category: Optional[ParaCategory] = None
    word_count: int = 0
    estimated_read_time: int = 0  # in minutes

class NoteParsingError(Exception):
    """Exception raised when note parsing fails"""
    pass

class NoteSafetyError(Exception):
    """Exception raised when file operations are unsafe"""
    pass

class ParaNoteProcessor:
    """Core note processing engine for PARA Method notes"""

    def __init__(self, config_path: str = ".para-config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

        # Backup directory for safe operations
        self.backup_dir = Path('.para-backups')
        self.backup_dir.mkdir(exist_ok=True)

        # Regex patterns for extraction
        self.action_item_pattern = re.compile(
            r'^(\s*)-\s*\[([x\s])\]\s*(.+?)(?:\s*-\s*@(\w+))?(?:\s*-\s*(?:due|Due):?\s*([^\n]+?))?(?:\s*\[([^\]]+)\])?\s*$',
            re.MULTILINE
        )

        self.attendee_pattern = re.compile(
            r'(?:attendees?|participants?):?\s*([^\n]+)',
            re.IGNORECASE | re.MULTILINE
        )

        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )

        self.date_pattern = re.compile(
            r'\b\d{4}-\d{2}-\d{2}(?:\s+\d{1,2}:\d{2}(?::\d{2})?)?\b'
        )

        self.tag_pattern = re.compile(
            r'(?:^|\s)#([a-zA-Z0-9_-]+)'
        )

        # Keywords for PARA categorization
        self.categorization_keywords = {
            ParaCategory.PROJECTS: {
                'high': ['project', 'deadline', 'deliverable', 'milestone', 'launch', 'complete', 'finish'],
                'medium': ['task', 'goal', 'objective', 'outcome', 'result'],
                'low': ['plan', 'strategy', 'roadmap']
            },
            ParaCategory.AREAS: {
                'high': ['responsibility', 'maintain', 'ongoing', 'continuous', 'regular'],
                'medium': ['team', 'process', 'standard', 'policy', 'procedure'],
                'low': ['management', 'oversight', 'monitoring']
            },
            ParaCategory.RESOURCES: {
                'high': ['reference', 'documentation', 'guide', 'tutorial', 'research'],
                'medium': ['knowledge', 'learning', 'study', 'article', 'book'],
                'low': ['information', 'data', 'facts', 'resource']
            }
        }

    def _load_config(self) -> Dict[str, Any]:
        """Load PARA configuration"""
        if not self.config_path.exists():
            return {}

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            return {}

    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of the file before modification"""
        if not file_path.exists():
            raise NoteSafetyError(f"File does not exist: {file_path}")

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{file_path.name}_{timestamp}.bak"
        backup_path = self.backup_dir / backup_name

        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            raise NoteSafetyError(f"Failed to create backup: {e}")

    def parse_frontmatter(self, content: str) -> Tuple[Dict[str, Any], str]:
        """Parse YAML frontmatter from markdown content"""
        if not content.strip():
            return {}, content

        if not content.startswith('---'):
            return {}, content

        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}, content

            frontmatter_str = parts[1].strip()
            markdown_content = parts[2].lstrip('\n')

            if not frontmatter_str:
                return {}, markdown_content

            frontmatter = yaml.safe_load(frontmatter_str)
            return frontmatter or {}, markdown_content

        except yaml.YAMLError as e:
            raise NoteParsingError(f"Invalid YAML frontmatter: {e}")
        except Exception as e:
            raise NoteParsingError(f"Error parsing frontmatter: {e}")

    def extract_action_items(self, content: str) -> List[ActionItem]:
        """Extract action items from markdown content"""
        action_items = []

        for match in self.action_item_pattern.finditer(content):
            indent = match.group(1) or ""
            completed = match.group(2).lower() == 'x'
            text = match.group(3).strip()
            assignee = match.group(4)
            due_date = match.group(5)
            priority = match.group(6)

            # Find line number
            line_number = content[:match.start()].count('\n') + 1

            action_items.append(ActionItem(
                text=text,
                completed=completed,
                assignee=assignee,
                due_date=due_date.strip() if due_date else None,
                line_number=line_number,
                priority=priority
            ))

        return action_items

    def extract_attendees(self, content: str) -> List[str]:
        """Extract attendees from note content"""
        attendees = []

        # Look for attendee patterns
        for match in self.attendee_pattern.finditer(content):
            attendee_text = match.group(1).strip()

            # Split by common delimiters and clean up
            parts = re.split(r'[,;\n\r]+', attendee_text)
            for part in parts:
                part = part.strip()
                if part and part != 'TBD' and part != 'N/A':
                    # Remove email addresses for cleaner names
                    clean_part = re.sub(self.email_pattern, '', part).strip()
                    if clean_part:
                        attendees.append(clean_part)

        # Also extract email addresses separately
        emails = self.email_pattern.findall(content)
        attendees.extend(emails)

        return list(set(attendees))  # Remove duplicates

    def extract_dates(self, content: str) -> List[str]:
        """Extract dates from content"""
        dates = self.date_pattern.findall(content)
        return list(set(dates))  # Remove duplicates

    def extract_tags(self, content: str, frontmatter: Dict[str, Any] = None) -> List[str]:
        """Extract tags from content and frontmatter"""
        tags = set()

        # Extract hashtags from content
        hashtags = self.tag_pattern.findall(content)
        tags.update(hashtags)

        # Extract from frontmatter
        if frontmatter:
            fm_tags = frontmatter.get('tags', [])
            if isinstance(fm_tags, str):
                # Handle comma-separated tags
                fm_tags = [tag.strip() for tag in fm_tags.split(',')]
            elif isinstance(fm_tags, list):
                fm_tags = [str(tag) for tag in fm_tags]
            tags.update(fm_tags)

        return list(tags)

    def analyze_content_category(self, content: str, frontmatter: Dict[str, Any] = None) -> Optional[ParaCategory]:
        """Analyze content to suggest PARA category"""
        content_lower = content.lower()

        # Check frontmatter for explicit suggestion
        if frontmatter:
            para_suggestion = frontmatter.get('para_suggestion')
            if para_suggestion:
                try:
                    return ParaCategory(para_suggestion)
                except ValueError:
                    pass

        # Score each category based on keyword presence
        scores = {}

        for category, keywords in self.categorization_keywords.items():
            score = 0
            for weight_level, word_list in keywords.items():
                weight = {'high': 3, 'medium': 2, 'low': 1}[weight_level]
                for keyword in word_list:
                    occurrences = content_lower.count(keyword)
                    score += occurrences * weight
            scores[category] = score

        # Return category with highest score, if significant
        if scores:
            max_category = max(scores, key=scores.get)
            max_score = scores[max_category]

            # Only suggest if score is meaningful
            if max_score >= 2:
                return max_category

        return ParaCategory.INBOX  # Default fallback

    def calculate_read_time(self, content: str) -> Tuple[int, int]:
        """Calculate word count and estimated read time"""
        # Remove markdown formatting for accurate word count
        clean_content = re.sub(r'[#*`_\[\](){}]', '', content)
        clean_content = re.sub(r'\n+', ' ', clean_content)

        words = len(clean_content.split())

        # Average reading speed: 200 words per minute
        read_time = max(1, round(words / 200))

        return words, read_time

    def parse_note(self, file_path: str, validate: bool = True) -> ParsedNote:
        """Parse a markdown note file and extract all information"""
        file_path = Path(file_path)

        if not file_path.exists():
            raise NoteParsingError(f"File does not exist: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
        except Exception as e:
            raise NoteParsingError(f"Could not read file {file_path}: {e}")

        if not raw_content.strip():
            raise NoteParsingError(f"File is empty: {file_path}")

        try:
            # Parse frontmatter and content
            frontmatter, content = self.parse_frontmatter(raw_content)

            # Extract all information
            action_items = self.extract_action_items(content)
            attendees = self.extract_attendees(content)
            dates = self.extract_dates(content)
            tags = self.extract_tags(content, frontmatter)
            suggested_category = self.analyze_content_category(content, frontmatter)
            word_count, read_time = self.calculate_read_time(content)

            return ParsedNote(
                file_path=str(file_path),
                frontmatter=frontmatter,
                content=content,
                raw_content=raw_content,
                action_items=action_items,
                attendees=attendees,
                dates=dates,
                tags=tags,
                suggested_category=suggested_category,
                word_count=word_count,
                estimated_read_time=read_time
            )

        except Exception as e:
            if validate:
                raise NoteParsingError(f"Error parsing note {file_path}: {e}")
            else:
                # Return partial data for malformed notes - try to extract what we can
                try:
                    # Try to extract content even if frontmatter is malformed
                    content = raw_content
                    if raw_content.startswith('---'):
                        parts = raw_content.split('---', 2)
                        if len(parts) >= 3:
                            content = parts[2].lstrip('\n')

                    # Extract what we can from the content
                    action_items = self.extract_action_items(content)
                    attendees = self.extract_attendees(content)
                    dates = self.extract_dates(content)
                    tags = self.extract_tags(content)
                    suggested_category = self.analyze_content_category(content)
                    word_count, read_time = self.calculate_read_time(content)

                    return ParsedNote(
                        file_path=str(file_path),
                        frontmatter={},
                        content=content,
                        raw_content=raw_content,
                        action_items=action_items,
                        attendees=attendees,
                        dates=dates,
                        tags=tags,
                        suggested_category=suggested_category or ParaCategory.INBOX,
                        word_count=word_count,
                        estimated_read_time=read_time
                    )
                except:
                    # If even graceful parsing fails, return minimal data
                    return ParsedNote(
                        file_path=str(file_path),
                        frontmatter={},
                        content=raw_content,
                        raw_content=raw_content,
                        action_items=[],
                        attendees=[],
                        dates=[],
                        tags=[],
                        suggested_category=ParaCategory.INBOX,
                        word_count=0,
                        estimated_read_time=1
                    )

    def update_note_frontmatter(self, file_path: str, updates: Dict[str, Any], create_backup: bool = True) -> bool:
        """Safely update note frontmatter"""
        file_path = Path(file_path)

        if create_backup:
            self.create_backup(file_path)

        try:
            parsed_note = self.parse_note(file_path)

            # Merge updates
            new_frontmatter = {**parsed_note.frontmatter, **updates}

            # Rebuild content
            if new_frontmatter:
                fm_yaml = yaml.dump(new_frontmatter, default_flow_style=False, sort_keys=False)
                new_content = f"---\n{fm_yaml}---\n\n{parsed_note.content}"
            else:
                new_content = parsed_note.content

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return True

        except Exception as e:
            raise NoteSafetyError(f"Failed to update frontmatter: {e}")

    def batch_process_notes(self, directory: str, pattern: str = "*.md") -> List[ParsedNote]:
        """Process multiple notes in a directory"""
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            raise NoteParsingError(f"Directory does not exist: {directory}")

        notes = []
        failed_files = []

        for file_path in directory.glob(pattern):
            try:
                parsed_note = self.parse_note(file_path, validate=False)
                notes.append(parsed_note)
            except Exception as e:
                failed_files.append((str(file_path), str(e)))
                print(f"Warning: Failed to process {file_path}: {e}")

        if failed_files:
            print(f"Successfully processed {len(notes)} files, {len(failed_files)} failed")

        return notes

    def find_orphaned_action_items(self, directory: str = ".") -> List[Tuple[str, ActionItem]]:
        """Find action items that may be orphaned or forgotten"""
        notes = self.batch_process_notes(directory)
        orphaned_items = []

        for note in notes:
            for action_item in note.action_items:
                # Check if action item might be orphaned
                is_orphaned = (
                    not action_item.completed and
                    (not action_item.due_date or self._is_overdue(action_item.due_date)) and
                    not action_item.assignee
                )

                if is_orphaned:
                    orphaned_items.append((note.file_path, action_item))

        return orphaned_items

    def _is_overdue(self, due_date_str: str) -> bool:
        """Check if a due date string represents an overdue item"""
        try:
            # Try to parse common date formats
            for date_format in ['%Y-%m-%d', '%Y-%m-%d %H:%M', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    due_date = datetime.datetime.strptime(due_date_str, date_format)
                    return due_date < datetime.datetime.now()
                except ValueError:
                    continue
            return False
        except:
            return False

def main():
    """CLI interface for note processing engine"""
    parser = argparse.ArgumentParser(description="PARA Method Note Processing Engine")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse a single note file')
    parse_parser.add_argument('file', help='Note file to parse')
    parse_parser.add_argument('--json', action='store_true', help='Output as JSON')
    parse_parser.add_argument('--graceful', action='store_true', help='Handle malformed notes gracefully')

    # Batch process command
    batch_parser = subparsers.add_parser('batch', help='Process multiple notes')
    batch_parser.add_argument('directory', help='Directory containing notes')
    batch_parser.add_argument('--pattern', default='*.md', help='File pattern to match')
    batch_parser.add_argument('--summary', action='store_true', help='Show summary only')

    # Action items command
    action_parser = subparsers.add_parser('actions', help='Find action items')
    action_parser.add_argument('--directory', default='.', help='Directory to search')
    action_parser.add_argument('--orphaned', action='store_true', help='Show only orphaned items')

    # Update frontmatter command
    update_parser = subparsers.add_parser('update', help='Update note frontmatter')
    update_parser.add_argument('file', help='Note file to update')
    update_parser.add_argument('--key', action='append', help='Key to update (key=value format)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    processor = ParaNoteProcessor()

    try:
        if args.command == 'parse':
            validate = not args.graceful
            note = processor.parse_note(args.file, validate=validate)

            if args.json:
                import json
                print(json.dumps(asdict(note), indent=2, default=str))
            else:
                print(f"📄 Note: {note.file_path}")
                print(f"📊 Words: {note.word_count} (~{note.estimated_read_time} min read)")
                print(f"📂 Suggested category: {note.suggested_category.value}")

                if note.frontmatter:
                    print(f"📋 Frontmatter: {len(note.frontmatter)} fields")

                if note.action_items:
                    print(f"✅ Action items: {len(note.action_items)} total")
                    for item in note.action_items[:3]:  # Show first 3
                        status = "✓" if item.completed else "○"
                        print(f"   {status} {item.text[:50]}{'...' if len(item.text) > 50 else ''}")

                if note.attendees:
                    print(f"👥 Attendees: {', '.join(note.attendees[:3])}{'...' if len(note.attendees) > 3 else ''}")

                if note.tags:
                    print(f"🏷️  Tags: {', '.join(note.tags)}")

        elif args.command == 'batch':
            notes = processor.batch_process_notes(args.directory, args.pattern)

            if args.summary:
                total_actions = sum(len(note.action_items) for note in notes)
                completed_actions = sum(sum(1 for item in note.action_items if item.completed) for note in notes)
                total_words = sum(note.word_count for note in notes)

                print(f"📊 Processed {len(notes)} notes")
                print(f"📝 Total words: {total_words:,}")
                print(f"✅ Action items: {completed_actions}/{total_actions} completed")

                # Category distribution
                categories = {}
                for note in notes:
                    cat = note.suggested_category.value
                    categories[cat] = categories.get(cat, 0) + 1

                print("📂 Category suggestions:")
                for cat, count in sorted(categories.items()):
                    print(f"   {cat}: {count} notes")
            else:
                for note in notes:
                    print(f"{note.file_path}: {note.word_count} words, {len(note.action_items)} actions")

        elif args.command == 'actions':
            if args.orphaned:
                orphaned = processor.find_orphaned_action_items(args.directory)
                print(f"🔍 Found {len(orphaned)} potentially orphaned action items:")
                for file_path, action_item in orphaned[:10]:  # Show first 10
                    print(f"   {Path(file_path).name}: {action_item.text[:60]}{'...' if len(action_item.text) > 60 else ''}")
            else:
                notes = processor.batch_process_notes(args.directory)
                all_actions = []
                for note in notes:
                    for action in note.action_items:
                        all_actions.append((note.file_path, action))

                print(f"✅ Found {len(all_actions)} action items across {len(notes)} notes")
                incomplete = [action for _, action in all_actions if not action.completed]
                print(f"⏳ {len(incomplete)} incomplete action items")

        elif args.command == 'update':
            if not args.key:
                print("Error: No keys specified. Use --key key=value format.")
                return

            updates = {}
            for key_value in args.key:
                if '=' not in key_value:
                    print(f"Error: Invalid key format: {key_value}")
                    continue
                key, value = key_value.split('=', 1)
                updates[key] = value

            success = processor.update_note_frontmatter(args.file, updates)
            if success:
                print(f"✅ Updated frontmatter in {args.file}")
            else:
                print(f"❌ Failed to update {args.file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()