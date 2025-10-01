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
class CategorizationResult:
    """Represents a PARA categorization result with confidence and reasoning"""
    category: ParaCategory
    confidence: float  # 0.0 to 1.0
    reasoning: List[str]  # List of reasons for this categorization
    alternative_categories: List[Tuple[ParaCategory, float]]  # Other possibilities with scores
    manual_override: bool = False  # Whether this was manually set

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
    categorization_result: Optional[CategorizationResult] = None
    suggested_category: Optional[ParaCategory] = None  # Maintained for backward compatibility
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

        # Enhanced keywords and patterns for PARA categorization
        self.categorization_keywords = {
            ParaCategory.PROJECTS: {
                'high': ['project', 'deadline', 'deliverable', 'milestone', 'launch', 'complete', 'finish',
                        'campaign', 'initiative', 'sprint', 'release', 'build', 'implementation'],
                'medium': ['task', 'goal', 'objective', 'outcome', 'result', 'target', 'achievement',
                          'timeline', 'schedule', 'feature', 'development'],
                'low': ['plan', 'strategy', 'roadmap', 'proposal', 'design', 'prototype']
            },
            ParaCategory.AREAS: {
                'high': ['responsibility', 'maintain', 'ongoing', 'continuous', 'regular', 'routine',
                        'standard', 'process', 'procedure', 'policy', 'operational'],
                'medium': ['team', 'department', 'role', 'function', 'service', 'support',
                          'administration', 'management', 'oversight'],
                'low': ['monitoring', 'review', 'assessment', 'evaluation', 'governance']
            },
            ParaCategory.RESOURCES: {
                'high': ['reference', 'documentation', 'guide', 'tutorial', 'research', 'study',
                        'article', 'paper', 'report', 'analysis', 'knowledge base'],
                'medium': ['knowledge', 'learning', 'education', 'training', 'information',
                          'insights', 'best practices', 'lessons learned'],
                'low': ['data', 'facts', 'resource', 'material', 'content', 'archive']
            }
        }

        # Temporal indicators for enhanced categorization
        self.temporal_patterns = {
            'deadline_indicators': re.compile(r'\b(?:due|deadline|by|until|before)\s+(?:(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(?:\d{4}-\d{2}-\d{2})|(?:today|tomorrow|next week|next month))', re.IGNORECASE),
            'project_timeframes': re.compile(r'\b(?:this week|next week|this month|next month|this quarter|Q[1-4]|sprint|iteration|phase \d+)', re.IGNORECASE),
            'ongoing_indicators': re.compile(r'\b(?:always|regularly|daily|weekly|monthly|quarterly|annually|ongoing|continuous|perpetual)', re.IGNORECASE),
            'completion_indicators': re.compile(r'\b(?:completed|finished|done|shipped|launched|delivered|closed)', re.IGNORECASE),
            'research_indicators': re.compile(r'\b(?:investigate|research|study|analyze|explore|learn about|understand)', re.IGNORECASE)
        }

        # Content structure patterns
        self.structure_patterns = {
            'meeting_structure': re.compile(r'(?:agenda|attendees|action items|decisions|next steps)', re.IGNORECASE),
            'project_structure': re.compile(r'(?:objectives|deliverables|timeline|milestones|risks|dependencies)', re.IGNORECASE),
            'resource_structure': re.compile(r'(?:summary|key points|references|links|further reading)', re.IGNORECASE)
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

    def analyze_content_category(self, content: str, frontmatter: Dict[str, Any] = None) -> CategorizationResult:
        """Analyze content to suggest PARA category with confidence and reasoning"""
        content_lower = content.lower()
        reasoning = []

        # Check for manual override first
        if frontmatter:
            manual_category = frontmatter.get('para_category') or frontmatter.get('para_suggestion')
            if manual_category:
                try:
                    category = ParaCategory(manual_category)
                    return CategorizationResult(
                        category=category,
                        confidence=1.0,
                        reasoning=['Manual override in frontmatter'],
                        alternative_categories=[],
                        manual_override=True
                    )
                except ValueError:
                    reasoning.append(f"Invalid manual category '{manual_category}' ignored")

        # Initialize scoring system
        scores = {
            ParaCategory.PROJECTS: {'score': 0, 'factors': []},
            ParaCategory.AREAS: {'score': 0, 'factors': []},
            ParaCategory.RESOURCES: {'score': 0, 'factors': []},
            ParaCategory.ARCHIVE: {'score': 0, 'factors': []}
        }

        # 1. Keyword-based scoring (40% weight)
        for category, keywords in self.categorization_keywords.items():
            keyword_score = 0
            matched_keywords = []

            for weight_level, word_list in keywords.items():
                weight = {'high': 3, 'medium': 2, 'low': 1}[weight_level]
                for keyword in word_list:
                    occurrences = content_lower.count(keyword)
                    if occurrences > 0:
                        keyword_score += occurrences * weight
                        matched_keywords.append(f"{keyword}({occurrences})")

            if matched_keywords:
                scores[category]['score'] += keyword_score * 0.4
                scores[category]['factors'].append(f"Keywords: {', '.join(matched_keywords[:3])}")

        # 2. Temporal pattern analysis (30% weight)
        temporal_score = self._analyze_temporal_patterns(content, scores)

        # 3. Content structure analysis (20% weight)
        structure_score = self._analyze_content_structure(content, scores)

        # 4. Action item analysis (10% weight)
        action_items = self.extract_action_items(content)
        self._analyze_action_items(action_items, content, scores)

        # 5. Archive detection for completed projects
        self._detect_archive_candidates(content, frontmatter, scores)

        # Calculate final scores and confidence
        final_scores = [(cat, data['score']) for cat, data in scores.items()]
        final_scores.sort(key=lambda x: x[1], reverse=True)

        if final_scores[0][1] <= 0:
            # No clear categorization found
            return CategorizationResult(
                category=ParaCategory.INBOX,
                confidence=0.1,
                reasoning=['No clear categorization signals found'],
                alternative_categories=[]
            )

        best_category, best_score = final_scores[0]

        # Calculate confidence based on score separation and absolute score
        max_possible_score = 10.0  # Theoretical maximum
        confidence = min(0.95, best_score / max_possible_score)

        # Boost confidence if there's clear separation from alternatives
        if len(final_scores) > 1:
            second_score = final_scores[1][1]
            if best_score > second_score * 1.5:  # 50% higher than second best
                confidence = min(0.95, confidence * 1.2)

        # Reduce confidence if multiple categories are close
        if len(final_scores) > 1 and final_scores[1][1] > best_score * 0.8:
            confidence *= 0.8

        # Minimum confidence threshold
        confidence = max(0.1, confidence)

        # Build alternative categories (excluding the best one)
        alternatives = []
        for cat, score in final_scores[1:4]:  # Top 3 alternatives
            if score > 0:
                alt_confidence = min(0.9, score / max_possible_score)
                alternatives.append((cat, alt_confidence))

        # Compile reasoning from all factors
        reasoning = scores[best_category]['factors']
        if not reasoning:
            reasoning = ['Based on content analysis']

        return CategorizationResult(
            category=best_category,
            confidence=confidence,
            reasoning=reasoning,
            alternative_categories=alternatives,
            manual_override=False
        )

    def _analyze_temporal_patterns(self, content: str, scores: Dict) -> None:
        """Analyze temporal patterns in content to inform categorization"""

        # Deadline indicators suggest projects
        deadline_matches = self.temporal_patterns['deadline_indicators'].findall(content)
        if deadline_matches:
            scores[ParaCategory.PROJECTS]['score'] += len(deadline_matches) * 0.8
            scores[ParaCategory.PROJECTS]['factors'].append(f"Deadlines detected: {len(deadline_matches)}")

        # Project timeframe indicators
        timeframe_matches = self.temporal_patterns['project_timeframes'].findall(content)
        if timeframe_matches:
            scores[ParaCategory.PROJECTS]['score'] += len(timeframe_matches) * 0.6
            scores[ParaCategory.PROJECTS]['factors'].append(f"Project timeframes: {len(timeframe_matches)}")

        # Ongoing indicators suggest areas
        ongoing_matches = self.temporal_patterns['ongoing_indicators'].findall(content)
        if ongoing_matches:
            scores[ParaCategory.AREAS]['score'] += len(ongoing_matches) * 0.7
            scores[ParaCategory.AREAS]['factors'].append(f"Ongoing activities: {len(ongoing_matches)}")

        # Completion indicators might suggest archive
        completion_matches = self.temporal_patterns['completion_indicators'].findall(content)
        if completion_matches:
            scores[ParaCategory.ARCHIVE]['score'] += len(completion_matches) * 0.5
            scores[ParaCategory.ARCHIVE]['factors'].append(f"Completion indicators: {len(completion_matches)}")

        # Research indicators suggest resources
        research_matches = self.temporal_patterns['research_indicators'].findall(content)
        if research_matches:
            scores[ParaCategory.RESOURCES]['score'] += len(research_matches) * 0.6
            scores[ParaCategory.RESOURCES]['factors'].append(f"Research activities: {len(research_matches)}")

    def _analyze_content_structure(self, content: str, scores: Dict) -> None:
        """Analyze content structure patterns"""

        # Meeting structure suggests areas (ongoing responsibilities)
        if self.structure_patterns['meeting_structure'].search(content):
            scores[ParaCategory.AREAS]['score'] += 0.4
            scores[ParaCategory.AREAS]['factors'].append("Meeting structure detected")

        # Project structure suggests projects
        if self.structure_patterns['project_structure'].search(content):
            scores[ParaCategory.PROJECTS]['score'] += 0.5
            scores[ParaCategory.PROJECTS]['factors'].append("Project structure detected")

        # Resource structure suggests resources
        if self.structure_patterns['resource_structure'].search(content):
            scores[ParaCategory.RESOURCES]['score'] += 0.4
            scores[ParaCategory.RESOURCES]['factors'].append("Resource structure detected")

    def _analyze_action_items(self, action_items: List[ActionItem], content: str, scores: Dict) -> None:
        """Analyze action items to inform categorization"""
        if not action_items:
            return

        incomplete_items = [item for item in action_items if not item.completed]
        completed_items = [item for item in action_items if item.completed]

        # Many incomplete action items with deadlines suggest projects
        deadline_items = [item for item in incomplete_items if item.due_date]
        if deadline_items:
            scores[ParaCategory.PROJECTS]['score'] += len(deadline_items) * 0.1
            scores[ParaCategory.PROJECTS]['factors'].append(f"Action items with deadlines: {len(deadline_items)}")

        # High ratio of completed items might suggest archive
        if action_items:
            completion_ratio = len(completed_items) / len(action_items)
            if completion_ratio > 0.8:
                scores[ParaCategory.ARCHIVE]['score'] += 0.3
                scores[ParaCategory.ARCHIVE]['factors'].append(f"High completion ratio: {completion_ratio:.1%}")

    def _detect_archive_candidates(self, content: str, frontmatter: Dict[str, Any], scores: Dict) -> None:
        """Detect if content should be archived"""

        # Check for explicit completion status
        if frontmatter:
            status = frontmatter.get('status', '').lower()
            if status in ['completed', 'done', 'finished', 'shipped', 'cancelled']:
                scores[ParaCategory.ARCHIVE]['score'] += 1.0
                scores[ParaCategory.ARCHIVE]['factors'].append(f"Status: {status}")

        # Check for age-based archiving (if we have creation date)
        if frontmatter:
            created = frontmatter.get('created') or frontmatter.get('date')
            if created:
                try:
                    # Try to parse date
                    from dateutil.parser import parse
                    created_date = parse(str(created)).date()
                    age_days = (datetime.date.today() - created_date).days

                    # Suggest archiving for old completed projects (6+ months)
                    if age_days > 180 and any(word in content.lower() for word in ['completed', 'finished', 'done']):
                        scores[ParaCategory.ARCHIVE]['score'] += 0.4
                        scores[ParaCategory.ARCHIVE]['factors'].append(f"Old completed content: {age_days} days")

                except:
                    pass  # Ignore date parsing errors

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
            categorization_result = self.analyze_content_category(content, frontmatter)
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
                categorization_result=categorization_result,
                suggested_category=categorization_result.category,  # Backward compatibility
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
                    categorization_result = self.analyze_content_category(content)
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
                        categorization_result=categorization_result,
                        suggested_category=categorization_result.category if categorization_result else ParaCategory.INBOX,
                        word_count=word_count,
                        estimated_read_time=read_time
                    )
                except:
                    # If even graceful parsing fails, return minimal data
                    fallback_categorization = CategorizationResult(
                        category=ParaCategory.INBOX,
                        confidence=0.0,
                        reasoning=['Failed to parse content - defaulted to inbox'],
                        alternative_categories=[]
                    )
                    return ParsedNote(
                        file_path=str(file_path),
                        frontmatter={},
                        content=raw_content,
                        raw_content=raw_content,
                        action_items=[],
                        attendees=[],
                        dates=[],
                        tags=[],
                        categorization_result=fallback_categorization,
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

    def analyze_project_lifecycle(self, note: ParsedNote) -> Dict[str, Any]:
        """Analyze project lifecycle stage and recommend actions"""
        lifecycle_analysis = {
            'current_stage': 'unknown',
            'completion_percentage': 0.0,
            'recommended_action': 'review',
            'archive_candidate': False,
            'reasons': []
        }

        content_lower = note.content.lower()
        frontmatter = note.frontmatter

        # Check explicit project status in frontmatter
        status = frontmatter.get('status', '').lower()
        if status:
            if status in ['completed', 'done', 'finished', 'shipped', 'delivered']:
                lifecycle_analysis['current_stage'] = 'completed'
                lifecycle_analysis['completion_percentage'] = 1.0
                lifecycle_analysis['archive_candidate'] = True
                lifecycle_analysis['recommended_action'] = 'archive'
                lifecycle_analysis['reasons'].append(f'Status marked as: {status}')
            elif status in ['cancelled', 'abandoned', 'on-hold', 'paused']:
                lifecycle_analysis['current_stage'] = 'stalled'
                lifecycle_analysis['archive_candidate'] = True
                lifecycle_analysis['recommended_action'] = 'archive_or_revive'
                lifecycle_analysis['reasons'].append(f'Status marked as: {status}')
            elif status in ['active', 'in-progress', 'ongoing']:
                lifecycle_analysis['current_stage'] = 'active'
                lifecycle_analysis['recommended_action'] = 'monitor'
                lifecycle_analysis['reasons'].append(f'Status marked as: {status}')

        # Analyze action items completion rate
        if note.action_items:
            completed_count = sum(1 for item in note.action_items if item.completed)
            completion_rate = completed_count / len(note.action_items)
            lifecycle_analysis['completion_percentage'] = completion_rate

            if completion_rate >= 0.9:
                lifecycle_analysis['current_stage'] = 'nearly_complete'
                lifecycle_analysis['archive_candidate'] = True
                lifecycle_analysis['recommended_action'] = 'review_for_archive'
                lifecycle_analysis['reasons'].append(f'High completion rate: {completion_rate:.1%}')
            elif completion_rate >= 0.7:
                lifecycle_analysis['current_stage'] = 'active'
                lifecycle_analysis['recommended_action'] = 'push_to_complete'
                lifecycle_analysis['reasons'].append(f'Good progress: {completion_rate:.1%}')
            elif completion_rate <= 0.2 and len(note.action_items) > 3:
                lifecycle_analysis['current_stage'] = 'stalled'
                lifecycle_analysis['recommended_action'] = 'review_viability'
                lifecycle_analysis['reasons'].append(f'Low progress: {completion_rate:.1%}')

        # Analyze temporal indicators
        if 'completed' in content_lower or 'finished' in content_lower or 'shipped' in content_lower:
            lifecycle_analysis['archive_candidate'] = True
            lifecycle_analysis['reasons'].append('Completion indicators found in content')

        # Check for age-based lifecycle decisions
        created_date = frontmatter.get('created') or frontmatter.get('date')
        if created_date:
            try:
                from dateutil.parser import parse
                created_date = parse(str(created_date)).date()
                age_days = (datetime.date.today() - created_date).days

                if age_days > 365:  # More than a year old
                    if lifecycle_analysis['completion_percentage'] < 0.3:
                        lifecycle_analysis['archive_candidate'] = True
                        lifecycle_analysis['recommended_action'] = 'review_viability'
                        lifecycle_analysis['reasons'].append(f'Stale project: {age_days} days old with minimal progress')
                elif age_days > 180:  # More than 6 months
                    if lifecycle_analysis['completion_percentage'] < 0.1:
                        lifecycle_analysis['recommended_action'] = 'review_viability'
                        lifecycle_analysis['reasons'].append(f'Aging project: {age_days} days with little progress')
            except:
                pass  # Ignore date parsing errors

        # Check for overdue items that might indicate stalled project
        overdue_items = 0
        for item in note.action_items:
            if item.due_date and self._is_overdue(item.due_date) and not item.completed:
                overdue_items += 1

        if overdue_items > 2:
            lifecycle_analysis['current_stage'] = 'at_risk'
            lifecycle_analysis['recommended_action'] = 'urgent_review'
            lifecycle_analysis['reasons'].append(f'{overdue_items} overdue action items')

        return lifecycle_analysis

    def find_cross_references(self, note: ParsedNote, all_notes: List[ParsedNote]) -> Dict[str, List[str]]:
        """Find cross-references between notes for better organization"""
        cross_refs = {
            'related_projects': [],
            'related_areas': [],
            'related_resources': [],
            'shared_tags': [],
            'shared_people': [],
            'similar_content': []
        }

        note_tags = set(note.tags)
        note_attendees = set(note.attendees)
        note_content_words = set(note.content.lower().split())

        # Remove common words for better content matching
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        note_content_words -= common_words

        for other_note in all_notes:
            if other_note.file_path == note.file_path:
                continue

            # Find notes with shared tags
            other_tags = set(other_note.tags)
            shared_tags = note_tags & other_tags
            if shared_tags and len(shared_tags) >= 2:  # At least 2 shared tags
                category_key = f'related_{other_note.categorization_result.category.value.split("-")[1] if other_note.categorization_result else "notes"}'
                if category_key in cross_refs:
                    cross_refs[category_key].append({
                        'file': other_note.file_path,
                        'reason': f'Shared tags: {", ".join(shared_tags)}',
                        'confidence': min(0.9, len(shared_tags) * 0.3)
                    })

            # Find notes with shared people
            other_attendees = set(other_note.attendees)
            shared_people = note_attendees & other_attendees
            if shared_people and len(shared_people) >= 1:
                cross_refs['shared_people'].append({
                    'file': other_note.file_path,
                    'reason': f'Shared people: {", ".join(shared_people)}',
                    'confidence': min(0.8, len(shared_people) * 0.4)
                })

            # Find notes with similar content (basic word overlap)
            other_content_words = set(other_note.content.lower().split()) - common_words
            if len(note_content_words) > 10 and len(other_content_words) > 10:  # Only for substantial notes
                word_overlap = note_content_words & other_content_words
                if len(word_overlap) > 5:  # At least 5 shared meaningful words
                    similarity_score = len(word_overlap) / min(len(note_content_words), len(other_content_words))
                    if similarity_score > 0.15:  # At least 15% word overlap
                        cross_refs['similar_content'].append({
                            'file': other_note.file_path,
                            'reason': f'Content similarity: {similarity_score:.1%}',
                            'confidence': min(0.7, similarity_score * 2)
                        })

        # Sort each category by confidence
        for category in cross_refs:
            if isinstance(cross_refs[category], list) and cross_refs[category]:
                cross_refs[category].sort(key=lambda x: x.get('confidence', 0), reverse=True)
                # Keep only top 5 in each category
                cross_refs[category] = cross_refs[category][:5]

        return cross_refs

    def suggest_reorganization(self, directory: str = ".") -> Dict[str, Any]:
        """Analyze notes and suggest PARA reorganization"""
        notes = self.batch_process_notes(directory)

        reorganization_plan = {
            'total_notes': len(notes),
            'category_distribution': {},
            'archive_candidates': [],
            'cross_reference_opportunities': [],
            'lifecycle_actions': [],
            'confidence_issues': []
        }

        # Analyze category distribution
        for note in notes:
            if note.categorization_result:
                category = note.categorization_result.category.value
                if category not in reorganization_plan['category_distribution']:
                    reorganization_plan['category_distribution'][category] = {
                        'count': 0,
                        'avg_confidence': 0,
                        'low_confidence_count': 0
                    }

                cat_data = reorganization_plan['category_distribution'][category]
                cat_data['count'] += 1
                cat_data['avg_confidence'] += note.categorization_result.confidence

                if note.categorization_result.confidence < 0.6:
                    cat_data['low_confidence_count'] += 1
                    reorganization_plan['confidence_issues'].append({
                        'file': note.file_path,
                        'category': category,
                        'confidence': note.categorization_result.confidence,
                        'alternatives': [(alt[0].value, alt[1]) for alt in note.categorization_result.alternative_categories[:2]]
                    })

        # Calculate average confidence per category
        for category in reorganization_plan['category_distribution']:
            cat_data = reorganization_plan['category_distribution'][category]
            if cat_data['count'] > 0:
                cat_data['avg_confidence'] /= cat_data['count']

        # Find archive candidates and lifecycle actions
        for note in notes:
            if note.categorization_result and note.categorization_result.category != ParaCategory.ARCHIVE:
                lifecycle = self.analyze_project_lifecycle(note)
                if lifecycle['archive_candidate']:
                    reorganization_plan['archive_candidates'].append({
                        'file': note.file_path,
                        'current_category': note.categorization_result.category.value,
                        'completion_rate': lifecycle['completion_percentage'],
                        'reasons': lifecycle['reasons']
                    })

                if lifecycle['recommended_action'] in ['urgent_review', 'review_viability']:
                    reorganization_plan['lifecycle_actions'].append({
                        'file': note.file_path,
                        'action': lifecycle['recommended_action'],
                        'stage': lifecycle['current_stage'],
                        'reasons': lifecycle['reasons']
                    })

        # Find cross-reference opportunities (sample a few notes to avoid performance issues)
        sample_notes = notes[:10] if len(notes) > 10 else notes
        for note in sample_notes:
            cross_refs = self.find_cross_references(note, notes)
            for category, refs in cross_refs.items():
                if refs:  # If there are cross-references
                    reorganization_plan['cross_reference_opportunities'].append({
                        'file': note.file_path,
                        'category': category,
                        'references': refs[:3]  # Top 3 references
                    })

        return reorganization_plan

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

    # Project lifecycle command
    lifecycle_parser = subparsers.add_parser('lifecycle', help='Analyze project lifecycle')
    lifecycle_parser.add_argument('file', help='Note file to analyze')
    lifecycle_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Cross-references command
    crossref_parser = subparsers.add_parser('crossref', help='Find cross-references for a note')
    crossref_parser.add_argument('file', help='Note file to analyze')
    crossref_parser.add_argument('--directory', default='.', help='Directory to search for references')
    crossref_parser.add_argument('--json', action='store_true', help='Output as JSON')

    # Reorganization analysis command
    reorg_parser = subparsers.add_parser('reorganize', help='Suggest PARA reorganization')
    reorg_parser.add_argument('--directory', default='.', help='Directory to analyze')
    reorg_parser.add_argument('--json', action='store_true', help='Output as JSON')

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

        elif args.command == 'lifecycle':
            note = processor.parse_note(args.file)
            lifecycle = processor.analyze_project_lifecycle(note)

            if args.json:
                import json
                print(json.dumps(lifecycle, indent=2, default=str))
            else:
                print(f"🔄 Project Lifecycle Analysis: {Path(args.file).name}")
                print(f"📊 Stage: {lifecycle['current_stage']}")
                print(f"✅ Completion: {lifecycle['completion_percentage']:.1%}")
                print(f"🎯 Recommended action: {lifecycle['recommended_action']}")
                if lifecycle['archive_candidate']:
                    print("📦 Archive candidate: Yes")
                if lifecycle['reasons']:
                    print("💡 Reasons:")
                    for reason in lifecycle['reasons']:
                        print(f"   • {reason}")

        elif args.command == 'crossref':
            note = processor.parse_note(args.file)
            all_notes = processor.batch_process_notes(args.directory)
            cross_refs = processor.find_cross_references(note, all_notes)

            if args.json:
                import json
                print(json.dumps(cross_refs, indent=2, default=str))
            else:
                print(f"🔗 Cross-references for: {Path(args.file).name}")
                total_refs = sum(len(refs) for refs in cross_refs.values() if isinstance(refs, list))
                if total_refs == 0:
                    print("   No cross-references found")
                else:
                    for category, refs in cross_refs.items():
                        if refs:
                            print(f"\n📂 {category.replace('_', ' ').title()}: ({len(refs)} found)")
                            for ref in refs[:3]:  # Show top 3
                                print(f"   • {Path(ref['file']).name} - {ref['reason']} (confidence: {ref['confidence']:.1%})")

        elif args.command == 'reorganize':
            reorg_plan = processor.suggest_reorganization(args.directory)

            if args.json:
                import json
                print(json.dumps(reorg_plan, indent=2, default=str))
            else:
                print(f"📊 PARA Reorganization Analysis ({reorg_plan['total_notes']} notes)")

                print("\n📂 Category Distribution:")
                for category, data in reorg_plan['category_distribution'].items():
                    print(f"   {category}: {data['count']} notes (avg confidence: {data['avg_confidence']:.1%})")
                    if data['low_confidence_count'] > 0:
                        print(f"      ⚠️  {data['low_confidence_count']} with low confidence")

                if reorg_plan['archive_candidates']:
                    print(f"\n📦 Archive Candidates ({len(reorg_plan['archive_candidates'])} found):")
                    for candidate in reorg_plan['archive_candidates'][:5]:  # Show first 5
                        print(f"   • {Path(candidate['file']).name} ({candidate['completion_rate']:.1%} complete)")

                if reorg_plan['lifecycle_actions']:
                    print(f"\n🔄 Lifecycle Actions ({len(reorg_plan['lifecycle_actions'])} needed):")
                    for action in reorg_plan['lifecycle_actions'][:5]:  # Show first 5
                        print(f"   • {Path(action['file']).name}: {action['action']} ({action['stage']})")

                if reorg_plan['confidence_issues']:
                    print(f"\n⚠️  Low Confidence Issues ({len(reorg_plan['confidence_issues'])} found):")
                    for issue in reorg_plan['confidence_issues'][:5]:  # Show first 5
                        print(f"   • {Path(issue['file']).name}: {issue['confidence']:.1%} confidence")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()