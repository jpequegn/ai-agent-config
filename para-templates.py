#!/usr/bin/env python3
"""
PARA Method Note Template System

A flexible template system for creating notes with variable substitution.
Supports built-in templates and custom template creation.
"""

import os
import sys
import yaml
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader, Template

class ParaTemplateEngine:
    """Template engine for PARA Method notes"""

    def __init__(self, config_path: str = ".para-config.yaml"):
        self.config_path = Path(config_path)
        self.templates_dir = Path("templates")
        self.builtin_dir = self.templates_dir / "built-in"
        self.custom_dir = self.templates_dir / "custom"

        # Ensure directories exist
        self.builtin_dir.mkdir(parents=True, exist_ok=True)
        self.custom_dir.mkdir(parents=True, exist_ok=True)

        # Load configuration
        self.config = self._load_config()

        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader([str(self.builtin_dir), str(self.custom_dir)]),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Add custom filters
        self.jinja_env.filters['slugify'] = self._slugify

    def _load_config(self) -> Dict[str, Any]:
        """Load PARA configuration"""
        if not self.config_path.exists():
            return self._default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            'user': {
                'name': 'User',
                'email': 'user@example.com'
            },
            'directories': {
                'projects': '1-projects',
                'areas': '2-areas',
                'resources': '3-resources',
                'archive': '4-archive',
                'inbox': 'inbox'
            }
        }

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text

    def get_default_variables(self) -> Dict[str, str]:
        """Get default template variables"""
        now = datetime.datetime.now()

        return {
            'date': now.strftime('%Y-%m-%d'),
            'datetime': now.strftime('%Y-%m-%d %H:%M'),
            'time': now.strftime('%H:%M'),
            'timestamp': now.strftime('%Y-%m-%d-%H%M'),
            'year': str(now.year),
            'month': now.strftime('%m'),
            'day': now.strftime('%d'),
            'weekday': now.strftime('%A'),
            'user_name': self.config.get('user', {}).get('name', 'User'),
            'user_email': self.config.get('user', {}).get('email', 'user@example.com'),
        }

    def list_templates(self) -> Dict[str, List[str]]:
        """List available templates"""
        templates = {
            'built-in': [],
            'custom': []
        }

        # Built-in templates
        if self.builtin_dir.exists():
            for template_file in self.builtin_dir.glob('*.md'):
                templates['built-in'].append(template_file.stem)

        # Custom templates
        if self.custom_dir.exists():
            for template_file in self.custom_dir.glob('*.md'):
                templates['custom'].append(template_file.stem)

        return templates

    def get_template_info(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get template metadata"""
        template_file = None

        # Check built-in first
        builtin_path = self.builtin_dir / f"{template_name}.md"
        if builtin_path.exists():
            template_file = builtin_path
        else:
            # Check custom
            custom_path = self.custom_dir / f"{template_name}.md"
            if custom_path.exists():
                template_file = custom_path

        if not template_file:
            return None

        # Parse frontmatter
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    return frontmatter or {}

            return {}
        except Exception:
            return {}

    def create_note(self, template_name: str, variables: Dict[str, str] = None,
                   output_path: str = None) -> str:
        """Create a note from template"""
        # Merge default variables with provided ones
        template_vars = self.get_default_variables()
        if variables:
            template_vars.update(variables)

        # Load template file directly to handle frontmatter
        template_file = None
        builtin_path = self.builtin_dir / f"{template_name}.md"
        if builtin_path.exists():
            template_file = builtin_path
        else:
            custom_path = self.custom_dir / f"{template_name}.md"
            if custom_path.exists():
                template_file = custom_path

        if not template_file:
            raise ValueError(f"Template '{template_name}' not found")

        # Read and process template
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove frontmatter if present
            template_content = content
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    template_content = parts[2].strip()

            # Render template
            template = self.jinja_env.from_string(template_content)
            rendered_content = template.render(**template_vars)
        except Exception as e:
            raise ValueError(f"Error rendering template '{template_name}': {e}")

        # Determine output path
        if not output_path:
            # Auto-generate filename based on template and variables
            base_name = f"{template_vars['timestamp']}_{template_name}"
            if 'title' in template_vars:
                title_slug = self._slugify(template_vars['title'])
                base_name = f"{template_vars['timestamp']}_{title_slug}"

            output_path = f"inbox/{base_name}.md"

        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write note
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

        return str(output_file)

    def create_custom_template(self, name: str, content: str, metadata: Dict[str, Any] = None):
        """Create a custom template"""
        template_file = self.custom_dir / f"{name}.md"

        # Prepare content with frontmatter
        if metadata:
            frontmatter = yaml.dump(metadata, default_flow_style=False)
            full_content = f"---\n{frontmatter}---\n\n{content}"
        else:
            full_content = content

        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(full_content)

        return str(template_file)


def main():
    """CLI interface for template system"""
    parser = argparse.ArgumentParser(description="PARA Method Note Template System")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # List templates
    list_parser = subparsers.add_parser('list', help='List available templates')

    # Create note
    create_parser = subparsers.add_parser('create', help='Create note from template')
    create_parser.add_argument('template', help='Template name')
    create_parser.add_argument('--title', help='Note title')
    create_parser.add_argument('--project', help='Project name')
    create_parser.add_argument('--attendees', help='Meeting attendees (comma-separated)')
    create_parser.add_argument('--output', '-o', help='Output file path')
    create_parser.add_argument('--var', action='append', help='Custom variable (key=value)')

    # Template info
    info_parser = subparsers.add_parser('info', help='Show template information')
    info_parser.add_argument('template', help='Template name')

    # Create custom template
    custom_parser = subparsers.add_parser('new-template', help='Create custom template')
    custom_parser.add_argument('name', help='Template name')
    custom_parser.add_argument('--file', help='Template file to copy from')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    engine = ParaTemplateEngine()

    if args.command == 'list':
        templates = engine.list_templates()
        print("Available Templates:")
        print("\nBuilt-in:")
        for template in sorted(templates['built-in']):
            info = engine.get_template_info(template)
            description = info.get('description', 'No description') if info else 'No description'
            print(f"  {template:<20} - {description}")

        print("\nCustom:")
        if templates['custom']:
            for template in sorted(templates['custom']):
                info = engine.get_template_info(template)
                description = info.get('description', 'No description') if info else 'No description'
                print(f"  {template:<20} - {description}")
        else:
            print("  (none)")

    elif args.command == 'create':
        variables = {}

        # Add common variables
        if args.title:
            variables['title'] = args.title
        if args.project:
            variables['project'] = args.project
        if args.attendees:
            variables['attendees'] = args.attendees

        # Parse custom variables
        if args.var:
            for var in args.var:
                if '=' in var:
                    key, value = var.split('=', 1)
                    variables[key] = value

        try:
            output_file = engine.create_note(args.template, variables, args.output)
            print(f"Created note: {output_file}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'info':
        info = engine.get_template_info(args.template)
        if info:
            print(f"Template: {args.template}")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print(f"Template '{args.template}' not found or has no metadata")

    elif args.command == 'new-template':
        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            content = "# {{ title or 'New Note' }}\n\nDate: {{ date }}\n\n## Notes\n\n"

        metadata = {
            'description': f'Custom template: {args.name}',
            'category': 'custom',
            'para_suggestion': 'inbox'
        }

        try:
            template_file = engine.create_custom_template(args.name, content, metadata)
            print(f"Created custom template: {template_file}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()