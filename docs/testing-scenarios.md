# Testing Scenarios Documentation

Comprehensive testing framework for the PARA Notes API system with Claude Code integration.

## Testing Strategy

### Testing Pyramid

```
         /\
        /  \      E2E Tests (10%)
       /____\     - Workflow validation
      /      \    - Claude Code integration
     /________\   Integration Tests (20%)
    /          \  - API response validation
   /____________\ - Cross-command workflows
  /              \
 /________________\ Unit Tests (70%)
                    - Individual command testing
                    - Parameter validation
                    - Error handling
```

### Test Categories

1. **Unit Tests**: Individual command functionality
2. **Integration Tests**: Cross-command workflows and API validation
3. **End-to-End Tests**: Complete Claude Code integration scenarios
4. **Performance Tests**: Load testing and response time validation
5. **Security Tests**: Input validation and sanitization
6. **Accessibility Tests**: Claude Code user experience validation

## Unit Test Scenarios

### Command: capture

#### Successful Creation Tests

**Test**: Basic note creation
```bash
./notes capture --template quick-note --topic "Test Note"
```
**Expected**:
- `success: true`
- `data.file_path` contains valid path
- `data.template: "quick-note"`
- File created in inbox directory

**Test**: Meeting note with attendees
```bash
./notes capture --template meeting --topic "Sprint Planning" --attendees "john,sarah,mike"
```
**Expected**:
- Meeting template applied
- Attendees properly parsed and stored
- Date defaults to today

**Test**: Custom date specification
```bash
./notes capture --template meeting --topic "Future Meeting" --date "2024-12-25"
```
**Expected**:
- Date properly parsed and applied
- File naming includes specified date

#### Natural Language Processing Tests

**Test**: Complex natural language input
```bash
./notes capture about "budget review" with cfo,manager using meeting template on 2024-10-15
```
**Expected**:
- Template: meeting
- Topic: "budget review"
- Attendees: "cfo,manager"
- Date: "2024-10-15"

**Test**: Natural language edge cases
```bash
./notes capture using brainstorm template about "AI strategy, machine learning, and automation" with "product team, engineering leads"
```
**Expected**:
- Complex topics with commas handled correctly
- Multi-word attendee groups preserved
- Template correctly identified

#### Error Handling Tests

**Test**: Invalid template
```bash
./notes capture --template invalid-template --topic "Test"
```
**Expected**:
- `success: false`
- `error_details: "TEMPLATE_NOT_FOUND: ..."`
- Suggestions include available templates

**Test**: Missing required parameter
```bash
./notes capture --template meeting
```
**Expected**:
- `success: false`
- `error_details: "MISSING_REQUIRED_PARAM: ..."`
- Suggestions include parameter format

### Command: process-inbox

#### Basic Processing Tests

**Test**: Empty inbox
```bash
./notes process-inbox
```
**Expected**:
- `success: true`
- `data.notes_processed: 0`
- `data.total_notes: 0`

**Test**: Batch processing limit
```bash
./notes process-inbox --batch 3
```
**Expected**:
- Process maximum 3 files
- Proper batch size respected

#### AI Suggestion Tests

**Test**: Category suggestions
```bash
./notes process-inbox --auto-suggest
```
**Expected**:
- `data.suggestions` contains file → category mappings
- Valid PARA categories suggested
- Confidence-based suggestions

### Command: research

#### Analysis Tests

**Test**: Note analysis
```bash
./notes research --file "test-note.md"
```
**Expected**:
- `data.analysis.word_count` accurate
- `data.analysis.action_items` counted
- `data.suggestions.category` provided

**Test**: Topic expansion
```bash
./notes research --file "ai-research.md" --expand-topics
```
**Expected**:
- `data.suggestions.related_topics` populated
- Topics relevant to content

#### Error Handling Tests

**Test**: File not found
```bash
./notes research --file "nonexistent.md"
```
**Expected**:
- `success: false`
- `error_details: "FILE_NOT_FOUND: ..."`

### Command: find

#### Search Tests

**Test**: Text query search
```bash
./notes find --query "meeting"
```
**Expected**:
- Results contain query term
- Relevance scores provided
- File paths valid

**Test**: Date range search
```bash
./notes find --date-range last-week
```
**Expected**:
- Only files from last week included
- Date filtering accurate

#### Edge Cases

**Test**: No results
```bash
./notes find --query "nonexistent-term-xyz123"
```
**Expected**:
- `data.total_results: 0`
- `data.results: []`
- Helpful suggestions provided

### Command: follow-up

#### Action Item Tests

**Test**: Overdue items
```bash
./notes follow-up --status overdue
```
**Expected**:
- Only overdue items returned
- Status accurately calculated
- Summary statistics correct

**Test**: Assignee filtering
```bash
./notes follow-up --assignee "john"
```
**Expected**:
- Only john's action items returned
- Case-insensitive matching

### Command: prep

#### Meeting Preparation Tests

**Test**: Basic meeting prep
```bash
./notes prep --topic "Sprint Review" --attendees "team,stakeholders"
```
**Expected**:
- Meeting template applied
- Preparation checklist included
- File created successfully

### Command: list-templates

#### Template Listing Tests

**Test**: Template enumeration
```bash
./notes list-templates
```
**Expected**:
- Built-in templates listed
- Custom templates included
- Descriptions provided

**Test**: JSON output format
```bash
./notes list-templates --json
```
**Expected**:
- Valid JSON response
- Template structure consistent

## Integration Test Scenarios

### Cross-Command Workflows

#### Workflow: Complete Note Lifecycle

```bash
# 1. Create note
./notes capture --template meeting --topic "Project Kickoff" --attendees "team"

# 2. Research and analyze
./notes research --file "inbox/2024-09-13-1025_project-kickoff.md" --expand-topics

# 3. Process and categorize
./notes process-inbox --auto-suggest

# 4. Find related notes
./notes find --query "project"

# 5. Track action items
./notes follow-up --status pending
```

**Expected**:
- Each step succeeds
- Data flows correctly between commands
- File paths remain consistent
- Cross-references work properly

#### Workflow: Weekly Review Process

```bash
# 1. Process all inbox notes
./notes process-inbox --auto-suggest --batch 10

# 2. Review action items
./notes follow-up --status all

# 3. Create summary note
./notes capture --template quick-note --topic "Weekly Review Summary"
```

**Expected**:
- Batch processing handles multiple files
- Action items properly tracked
- Summary creation succeeds

### API Response Validation

#### Schema Compliance Tests

**Test**: All commands return valid JSON
```javascript
const commands = [
  './notes capture --template quick-note --topic "Test"',
  './notes process-inbox',
  './notes research --file "test.md"',
  './notes find --query "test"',
  './notes follow-up',
  './notes prep --topic "Test"',
  './notes list-templates'
];

for (const command of commands) {
  const response = await execute(command);
  validateSchema(response, baseResponseSchema);
}
```

**Expected**:
- All responses match base schema
- Required fields present
- Data types correct

#### Error Response Validation

**Test**: Consistent error format
```javascript
const errorCommands = [
  './notes capture --template invalid',
  './notes research --file nonexistent.md',
  './notes find --invalid-flag',
];

for (const command of errorCommands) {
  const response = await execute(command);
  expect(response.success).toBe(false);
  expect(response.error_details).toBeTruthy();
  expect(response.suggestions).toBeArray();
}
```

## End-to-End Test Scenarios

### Claude Code Integration Tests

#### Scenario: Natural Language Note Creation

**User Input**: "Create a meeting note about sprint planning with john and sarah for tomorrow"

**Test Steps**:
1. Claude Code parses natural language
2. Extracts parameters: template=meeting, topic="sprint planning", attendees="john,sarah", date=tomorrow
3. Executes command with extracted parameters
4. Validates response format
5. Presents success message to user

**Expected**:
- Natural language properly parsed
- Command executed successfully
- User feedback appropriate
- File created as expected

#### Scenario: Error Recovery Workflow

**User Input**: "Create a note using invalid-template"

**Test Steps**:
1. Command fails with TEMPLATE_NOT_FOUND error
2. Claude Code presents error message
3. Suggests alternative templates
4. User selects valid template
5. Command re-executed successfully

**Expected**:
- Error handled gracefully
- User guided to resolution
- Recovery workflow completes

#### Scenario: Multi-Step Workflow

**User Input**: "Help me organize my notes and create action items"

**Test Steps**:
1. Execute `process-inbox --auto-suggest`
2. Present categorization suggestions
3. Execute `follow-up --status pending`
4. Present action items summary
5. Offer to create follow-up notes

**Expected**:
- Multi-command workflow executes
- Data properly correlated
- User experience seamless

### Browser/UI Integration Tests (if applicable)

#### Test: File System Integration

**Scenario**: Note file accessibility
```javascript
test('created notes are accessible via file system', async () => {
  const response = await execute('./notes capture --template quick-note --topic "Test"');
  const filePath = response.data.file_path;

  expect(fs.existsSync(filePath)).toBe(true);
  const content = fs.readFileSync(filePath, 'utf-8');
  expect(content).toContain('Test');
});
```

## Performance Test Scenarios

### Response Time Tests

**Test**: Command execution speed
```javascript
const performanceTests = [
  { command: './notes capture --template quick-note --topic "Test"', maxTime: 500 },
  { command: './notes list-templates', maxTime: 200 },
  { command: './notes find --query "test"', maxTime: 1000 },
  { command: './notes process-inbox --batch 5', maxTime: 2000 }
];

for (const test of performanceTests) {
  const startTime = Date.now();
  await execute(test.command);
  const duration = Date.now() - startTime;

  expect(duration).toBeLessThan(test.maxTime);
}
```

### Load Testing

**Test**: Concurrent command execution
```javascript
test('handles concurrent requests', async () => {
  const concurrentCommands = Array(10).fill('./notes list-templates');
  const promises = concurrentCommands.map(cmd => execute(cmd));

  const results = await Promise.all(promises);

  results.forEach(result => {
    expect(result.success).toBe(true);
  });
});
```

### Memory Usage Tests

**Test**: Large file processing
```javascript
test('processes large notes efficiently', async () => {
  // Create large test file (>1MB)
  const largeContent = 'test content '.repeat(100000);
  fs.writeFileSync('test-large.md', largeContent);

  const startMemory = process.memoryUsage();
  const response = await execute('./notes research --file test-large.md');
  const endMemory = process.memoryUsage();

  expect(response.success).toBe(true);
  expect(endMemory.heapUsed - startMemory.heapUsed).toBeLessThan(50 * 1024 * 1024); // 50MB limit
});
```

## Security Test Scenarios

### Input Validation Tests

**Test**: Command injection prevention
```bash
./notes capture --topic "test; rm -rf /" --template quick-note
```
**Expected**:
- Command injection prevented
- Topic properly escaped
- No system commands executed

**Test**: Path traversal prevention
```bash
./notes capture --output "../../../etc/passwd" --template quick-note --topic "test"
```
**Expected**:
- Path traversal blocked
- File created in appropriate directory
- Security boundaries maintained

### Data Sanitization Tests

**Test**: XSS prevention in output
```bash
./notes capture --topic "<script>alert('xss')</script>" --template quick-note
```
**Expected**:
- Script tags properly escaped
- JSON output safe for web display
- No code execution in responses

## Accessibility Test Scenarios

### Claude Code UX Tests

**Test**: Error message clarity
```javascript
test('error messages are user-friendly', async () => {
  const response = await execute('./notes capture --template invalid');

  expect(response.message).toBeAccessible(); // Human-readable
  expect(response.suggestions).toContainActionableItems();
  expect(response.error_details).toContainTechnicalDetails();
});
```

**Test**: Success message informativeness
```javascript
test('success messages provide useful information', async () => {
  const response = await execute('./notes capture --template quick-note --topic "Test"');

  expect(response.message).toContainFilePath();
  expect(response.suggestions).toContainNextActions();
});
```

## Test Automation

### Continuous Integration Tests

```yaml
# .github/workflows/test-para-notes.yml
name: PARA Notes API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          ./setup-para.sh

      - name: Run unit tests
        run: python -m pytest tests/unit/

      - name: Run integration tests
        run: python -m pytest tests/integration/

      - name: Run performance tests
        run: python -m pytest tests/performance/
```

### Test Data Management

```python
# tests/fixtures/test_data.py
import json
import tempfile
from pathlib import Path

class TestDataManager:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_notes = []

    def create_test_note(self, template, topic, **kwargs):
        """Create a test note for testing purposes"""
        note_data = {
            'template': template,
            'topic': topic,
            'created': '2024-09-13',
            **kwargs
        }

        file_path = Path(self.temp_dir) / f"test-{len(self.test_notes)}.md"
        with open(file_path, 'w') as f:
            json.dump(note_data, f)

        self.test_notes.append(str(file_path))
        return str(file_path)

    def cleanup(self):
        """Clean up test data"""
        import shutil
        shutil.rmtree(self.temp_dir)
```

## Test Documentation

### Test Case Template

```markdown
### Test Case: [Test Name]

**Objective**: [What this test validates]

**Prerequisites**:
- [Required setup]
- [Test data needed]

**Test Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Results**:
- [Expected outcome 1]
- [Expected outcome 2]

**Pass Criteria**:
- [Criteria for test success]

**Test Data**:
- [Required test data]

**Notes**:
- [Additional information]
```

### Test Coverage Requirements

**Minimum Coverage Targets**:
- Unit Tests: 90% code coverage
- Integration Tests: 80% workflow coverage
- End-to-End Tests: 100% critical path coverage
- Error Scenarios: 100% error code coverage

**Quality Gates**:
- All tests must pass before deployment
- Performance tests must meet SLA requirements
- Security tests must show no vulnerabilities
- Accessibility tests must meet WCAG standards

## Conclusion

This comprehensive testing framework ensures the PARA Notes API system maintains high quality, security, and reliability standards while providing excellent Claude Code integration experience. Regular execution of these test scenarios helps catch issues early and maintain system integrity.

For implementation details, see [API Reference](api-reference.md) and [Claude Code Integration Guide](claude-code-guide.md).