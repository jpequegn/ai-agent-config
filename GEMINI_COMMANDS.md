# GEMINI_COMMANDS.md - Custom Commands for Gemini AI

Custom command framework for Gemini AI, adapted from Claude Code SuperClaude system.

## Core Development Commands

### `/build [target] [flags]`
**Purpose**: Project builder with framework detection  
**Usage**: `/build frontend`, `/build api --optimize`  
**Flags**:
- `--optimize`: Enable production optimizations
- `--watch`: Enable file watching for development
- `--framework [name]`: Specify framework (react, vue, angular, node, python)

### `/implement [feature] [flags]`
**Purpose**: Feature and code implementation  
**Usage**: `/implement user-authentication`, `/implement payment-integration --type api`  
**Flags**:
- `--type [component|api|service|feature]`: Specify implementation type
- `--framework [name]`: Target framework
- `--test`: Include test implementation

## Analysis Commands

### `/analyze [target] [flags]`
**Purpose**: Multi-dimensional code and system analysis  
**Usage**: `/analyze security`, `/analyze performance --deep`  
**Flags**:
- `--deep`: Comprehensive analysis with detailed recommendations
- `--focus [area]`: Focus on specific area (security, performance, quality, architecture)
- `--metrics`: Include quantitative metrics

### `/troubleshoot [symptoms] [flags]`
**Purpose**: Problem investigation and debugging  
**Usage**: `/troubleshoot "app crashes on login"`, `/troubleshoot memory-leak`  
**Flags**:
- `--verbose`: Detailed diagnostic output
- `--test`: Include test scenarios for reproduction

### `/explain [topic] [flags]`
**Purpose**: Educational explanations of code or concepts  
**Usage**: `/explain authentication-flow`, `/explain "this function"`  
**Flags**:
- `--level [beginner|intermediate|advanced]`: Explanation depth
- `--examples`: Include code examples

## Quality & Optimization Commands

### `/improve [target] [flags]`
**Purpose**: Evidence-based code enhancement  
**Usage**: `/improve performance`, `/improve code-quality`  
**Flags**:
- `--focus [performance|security|quality|accessibility]`: Improvement focus
- `--metrics`: Show before/after metrics
- `--safe`: Conservative improvements only

### `/cleanup [target] [flags]`
**Purpose**: Project cleanup and technical debt reduction  
**Usage**: `/cleanup unused-dependencies`, `/cleanup code-style`  
**Flags**:
- `--aggressive`: More extensive cleanup
- `--dry-run`: Preview changes without applying

### `/refactor [target] [flags]`
**Purpose**: Code restructuring and modernization  
**Usage**: `/refactor legacy-module`, `/refactor to-typescript`  
**Flags**:
- `--pattern [name]`: Apply specific design pattern
- `--preserve-behavior`: Ensure functional equivalence

## Documentation Commands

### `/document [target] [flags]`
**Purpose**: Documentation generation  
**Usage**: `/document api`, `/document component-library`  
**Flags**:
- `--format [markdown|jsdoc|sphinx]`: Output format
- `--lang [en|es|fr|de|ja|zh]`: Language for documentation
- `--examples`: Include usage examples

## Testing Commands

### `/test [type] [flags]`
**Purpose**: Testing workflows  
**Usage**: `/test unit`, `/test e2e --browser chrome`  
**Flags**:
- `--coverage`: Include coverage report
- `--watch`: Run in watch mode
- `--browser [chrome|firefox|safari]`: For E2E tests

## Version Control Commands

### `/git [operation] [flags]`
**Purpose**: Git workflow assistant  
**Usage**: `/git commit`, `/git pr`  
**Flags**:
- `--message [text]`: Commit message
- `--branch [name]`: Target branch
- `--squash`: Squash commits

## Project Management Commands

### `/estimate [task] [flags]`
**Purpose**: Evidence-based estimation  
**Usage**: `/estimate "add payment feature"`, `/estimate refactoring`  
**Flags**:
- `--breakdown`: Show task breakdown
- `--risks`: Include risk assessment

### `/task [operation] [flags]`
**Purpose**: Task management  
**Usage**: `/task create "implement login"`, `/task list`  
**Flags**:
- `--priority [low|medium|high|critical]`: Task priority
- `--assign [user]`: Assign to team member

## Design Commands

### `/design [domain] [flags]`
**Purpose**: Design and architecture  
**Usage**: `/design database-schema`, `/design component-hierarchy`  
**Flags**:
- `--pattern [mvc|mvvm|microservices]`: Architecture pattern
- `--visualize`: Generate diagrams

## Meta Commands

### `/workflow [name] [flags]`
**Purpose**: Workflow automation  
**Usage**: `/workflow ci-cd`, `/workflow deployment`  
**Flags**:
- `--steps`: Show detailed steps
- `--automate`: Generate automation scripts

### `/index [query] [flags]`
**Purpose**: Search and navigate codebase  
**Usage**: `/index "authentication"`, `/index functions`  
**Flags**:
- `--type [function|class|component|file]`: Filter by type
- `--include-tests`: Include test files

## Advanced Flags (Can be used with most commands)

### Analysis Depth Flags
- `--quick`: Fast, surface-level analysis
- `--standard`: Normal depth (default)
- `--deep`: Comprehensive analysis
- `--exhaustive`: Maximum depth analysis

### Output Control Flags
- `--verbose`: Detailed output
- `--quiet`: Minimal output
- `--json`: JSON formatted output
- `--markdown`: Markdown formatted output

### Performance Flags
- `--fast`: Optimize for speed over thoroughness
- `--parallel`: Use parallel processing where possible
- `--cache`: Use cached results when available

### Safety Flags
- `--dry-run`: Preview without making changes
- `--backup`: Create backups before changes
- `--validate`: Validate changes before applying
- `--safe-mode`: Maximum safety checks

### Scope Flags
- `--file [path]`: Single file scope
- `--dir [path]`: Directory scope
- `--project`: Entire project scope
- `--global`: System-wide scope

## Command Chaining

Commands can be chained using `&&` or `;`:
```
/analyze security && /improve --focus security
/build --optimize ; /test unit ; /git commit --message "Production build"
```

## Custom Aliases

You can create aliases for frequently used command combinations:
```
/alias deploy = /build --optimize && /test all && /git push
/alias review = /analyze quality && /test unit && /document changes
```

## Interactive Mode

Add `--interactive` or `-i` to any command for step-by-step execution with confirmations:
```
/refactor legacy-code --interactive
/improve performance -i
```

## Help System

- `/help`: Show all available commands
- `/help [command]`: Show detailed help for specific command
- `/examples [command]`: Show usage examples

## Configuration

Commands respect a `.gemini.config.json` file in the project root:
```json
{
  "defaultFlags": {
    "verbose": false,
    "validate": true,
    "backup": true
  },
  "aliases": {
    "qa": "test all && analyze quality",
    "ship": "build --optimize && test all && git push"
  },
  "preferences": {
    "language": "en",
    "outputFormat": "markdown",
    "safeMode": false
  }
}
```

## Quick Start Examples

### Starting a new feature:
```
/task create "Add user dashboard"
/design component-hierarchy
/implement dashboard --type component --framework react
/test unit
/document dashboard
/git commit --message "Add user dashboard feature"
```

### Improving existing code:
```
/analyze quality --focus performance
/improve performance --metrics
/refactor --pattern observer
/test all --coverage
/git pr --message "Performance improvements"
```

### Debugging an issue:
```
/troubleshoot "login fails intermittently"
/analyze security --deep
/test e2e --browser chrome
/improve --focus security --safe
```

## Notes

- Commands are case-insensitive
- Partial command matching is supported (e.g., `/ana` matches `/analyze`)
- Use quotes for multi-word arguments
- Commands maintain context between invocations in the same session
- All commands support `--help` flag for inline documentation