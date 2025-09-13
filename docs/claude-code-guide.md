# Claude Code Integration Guide

Complete integration guide for using the PARA Notes API within Claude Code workflows.

## Overview

The PARA Notes system is designed specifically for Claude Code integration, providing a unified JSON API that enables seamless note-taking, project management, and knowledge organization within AI-assisted development workflows.

## Getting Started

### Prerequisites

1. **PARA Notes System**: Installed and configured with `./setup-para.sh`
2. **Claude Code**: Access to Claude Code with command execution permissions
3. **Configuration**: Valid `.para-config.yaml` in project root

### Basic Integration

All PARA Notes commands return structured JSON responses optimized for Claude Code processing:

```json
{
  "success": true,
  "command": "capture",
  "message": "Human-readable status",
  "data": { ... },
  "suggestions": ["Next actions..."],
  "error_details": null
}
```

## Core Integration Patterns

### 1. Conversational Note Creation

**User Intent**: "I need to capture notes from my meeting with the design team about the new website"

**Claude Code Processing**:
```javascript
// Extract parameters from natural language
const intent = parseIntent("meeting with design team about new website");
// Results in: template=meeting, topic="new website", attendees="design team"

// Execute command
await executeCommand('./notes capture about "new website" with design team using meeting template');
```

**Response Handling**:
```javascript
if (response.success) {
  showSuccess(`Created meeting note: ${response.data.file_path}`);
  offerSuggestions(response.suggestions);
} else {
  showError(response.message);
  provideSolutions(response.suggestions);
}
```

### 2. Intelligent Project Context

**User Intent**: "Create a quick note about the API performance issue we discussed"

**Claude Code Workflow**:
1. **Context Analysis**: Determine if this relates to existing projects
2. **Template Selection**: Choose appropriate template based on content
3. **Parameter Extraction**: Extract key information from natural language
4. **Execution**: Run command with extracted parameters
5. **Follow-up**: Suggest related actions based on response

### 3. Batch Processing Integration

**User Intent**: "Process all the notes I've captured this week and organize them"

**Claude Code Implementation**:
```bash
# Process inbox with AI suggestions
./notes process-inbox --auto-suggest --batch 10

# Parse response for suggested categorizations
# Present categorization options to user
# Execute moves based on user approval
```

## Command-Specific Integrations

### capture Command

**Natural Language Patterns**:
- "Create a meeting note about sprint planning with john and sarah"
- "Quick note: need to follow up on budget discussion"
- "Research note about AI trends for next week"

**Claude Code Processing**:
```javascript
function processCaptureRequest(userInput) {
  const patterns = {
    template: /using\s+(\w+)\s+template/,
    topic: /about\s+"([^"]+)"/,
    attendees: /with\s+([^,\n]+(?:,\s*[^,\n]+)*)/,
    date: /on\s+(\d{4}-\d{2}-\d{2})/
  };

  // Extract parameters and build command
  const params = extractParameters(userInput, patterns);
  return buildCommand('capture', params);
}
```

### process-inbox Command

**Use Cases**:
- Weekly review and organization
- Bulk categorization with AI assistance
- Action item extraction and tracking

**Integration Example**:
```javascript
async function weeklyReview() {
  const result = await execute('./notes process-inbox --auto-suggest');

  if (result.success) {
    const { suggestions, action_items } = result.data;

    // Present categorization suggestions
    await presentCategorizations(suggestions);

    // Highlight pending action items
    await highlightActionItems(action_items);

    // Offer follow-up workflows
    await suggestFollowups(result.suggestions);
  }
}
```

### research Command

**Integration Patterns**:
- Automatic analysis after note creation
- Research workflow initiation
- Content enrichment and linking

**Example Workflow**:
```javascript
async function enhanceNote(filePath) {
  const analysis = await execute(`./notes research --file "${filePath}" --expand-topics`);

  if (analysis.success) {
    const { suggestions } = analysis.data;

    // Offer to create related notes
    if (suggestions.related_topics) {
      await suggestRelatedNotes(suggestions.related_topics);
    }

    // Propose PARA categorization
    if (suggestions.category) {
      await suggestCategorization(filePath, suggestions.category);
    }
  }
}
```

### find Command

**Search Integration**:
```javascript
async function intelligentSearch(query) {
  // Natural language to structured search
  const searchParams = parseSearchIntent(query);
  const results = await execute(`./notes find --query "${searchParams.query}" --date-range ${searchParams.dateRange}`);

  if (results.success) {
    // Present results with relevance scoring
    await presentSearchResults(results.data.results);

    // Suggest refinements
    if (results.data.total_results === 0) {
      await suggestSearchRefinements(query);
    }
  }
}
```

## Workflow Examples

### Daily Standup Workflow

```javascript
async function dailyStandup() {
  console.log("📋 Daily Standup Preparation");

  // 1. Review yesterday's notes
  const yesterday = formatDate(new Date(Date.now() - 86400000));
  const yesterdayNotes = await execute(`./notes find --date-range yesterday`);

  // 2. Check pending action items
  const actionItems = await execute('./notes follow-up --status pending');

  // 3. Create today's standup note
  const standupNote = await execute('./notes capture --template meeting --topic "Daily Standup" --attendees "team"');

  // 4. Present summary
  presentStandupSummary(yesterdayNotes, actionItems, standupNote);
}
```

### Project Kickoff Workflow

```javascript
async function projectKickoff(projectName, attendees) {
  console.log(`🚀 Starting project: ${projectName}`);

  // 1. Create project kickoff note
  const kickoffNote = await execute(`./notes capture --template project-kickoff --topic "${projectName} Kickoff" --attendees "${attendees.join(',')}"`);

  // 2. Set up project structure
  if (kickoffNote.success) {
    // 3. Create follow-up tasks
    await execute('./notes capture --template quick-note --topic "Define project requirements"');
    await execute('./notes capture --template quick-note --topic "Set up development environment"');

    // 4. Schedule check-ins
    await execute('./notes prep --topic "Weekly Project Check-in" --attendees "team"');
  }

  return kickoffNote;
}
```

### Knowledge Base Building

```javascript
async function buildKnowledgeBase(topic) {
  console.log(`📚 Building knowledge base for: ${topic}`);

  // 1. Create research note
  const researchNote = await execute(`./notes capture --template research --topic "${topic}"`);

  // 2. Analyze and expand
  if (researchNote.success) {
    const analysis = await execute(`./notes research --file "${researchNote.data.file_path}" --expand-topics`);

    // 3. Create related notes for suggested topics
    if (analysis.success && analysis.data.suggestions.related_topics) {
      for (const relatedTopic of analysis.data.suggestions.related_topics) {
        await execute(`./notes capture --template research --topic "${relatedTopic}"`);
      }
    }
  }

  return researchNote;
}
```

## Error Handling Best Practices

### Graceful Error Recovery

```javascript
async function executeWithRecovery(command, options = {}) {
  try {
    const result = await execute(command);

    if (!result.success) {
      // Parse error details
      const errorInfo = parseErrorDetails(result.error_details);

      // Attempt recovery based on error type
      switch (errorInfo.code) {
        case 'TEMPLATE_NOT_FOUND':
          return await suggestAlternativeTemplate(errorInfo);

        case 'MISSING_REQUIRED_PARAM':
          return await promptForMissingParameter(errorInfo);

        case 'FILE_NOT_FOUND':
          return await handleFileNotFound(errorInfo);

        default:
          return await handleGenericError(result);
      }
    }

    return result;
  } catch (error) {
    return await handleSystemError(error);
  }
}
```

### User-Friendly Error Messages

```javascript
function translateErrorMessage(errorDetails) {
  const errorMap = {
    'TEMPLATE_NOT_FOUND': 'The template you specified doesn\'t exist. Would you like to see available templates?',
    'MISSING_REQUIRED_PARAM': 'Some required information is missing. Let me help you complete it.',
    'INVALID_PARAMETER_VALUE': 'One of the values you provided isn\'t valid. Let me help you fix it.',
    'PARSE_ERROR': 'I couldn\'t understand that request. Would you like to try a different approach?'
  };

  const code = errorDetails.split(':')[0];
  return errorMap[code] || 'Something went wrong. Let me help you troubleshoot this.';
}
```

## Advanced Integration Patterns

### Context-Aware Suggestions

```javascript
async function provideContextualSuggestions(userInput, currentContext) {
  // Analyze current working context
  const context = await analyzeContext(currentContext);

  // Match user input against context patterns
  if (context.inMeeting && userInput.includes('note')) {
    return suggestMeetingNote(context.attendees, context.topic);
  }

  if (context.workingOnProject && userInput.includes('research')) {
    return suggestProjectResearch(context.projectName);
  }

  if (context.hasActionItems && userInput.includes('follow up')) {
    return suggestActionItemReview();
  }

  return suggestGenericWorkflow(userInput);
}
```

### Multi-Command Workflows

```javascript
async function executeWorkflow(workflowName, params) {
  const workflows = {
    'weekly-review': async () => {
      const processed = await execute('./notes process-inbox --auto-suggest');
      const actionItems = await execute('./notes follow-up --status pending');
      const summary = await execute('./notes capture --template quick-note --topic "Weekly Review Summary"');

      return { processed, actionItems, summary };
    },

    'project-setup': async (projectName) => {
      const kickoff = await execute(`./notes capture --template project-kickoff --topic "${projectName}"`);
      const requirements = await execute(`./notes capture --template research --topic "${projectName} Requirements"`);

      return { kickoff, requirements };
    }
  };

  return await workflows[workflowName](params);
}
```

## Performance Optimization

### Response Caching

```javascript
class NotesCache {
  constructor(ttl = 300000) { // 5-minute TTL
    this.cache = new Map();
    this.ttl = ttl;
  }

  async get(command) {
    const cached = this.cache.get(command);
    if (cached && Date.now() - cached.timestamp < this.ttl) {
      return cached.data;
    }

    const result = await execute(command);
    this.cache.set(command, {
      data: result,
      timestamp: Date.now()
    });

    return result;
  }
}
```

### Batch Operations

```javascript
async function batchProcess(operations) {
  const results = await Promise.allSettled(
    operations.map(op => execute(op.command))
  );

  return results.map((result, index) => ({
    operation: operations[index],
    success: result.status === 'fulfilled',
    data: result.status === 'fulfilled' ? result.value : null,
    error: result.status === 'rejected' ? result.reason : null
  }));
}
```

## Testing Integration

### Unit Testing with Mock Responses

```javascript
describe('PARA Notes Integration', () => {
  beforeEach(() => {
    mockExecute = jest.fn();
  });

  test('should create meeting note from natural language', async () => {
    mockExecute.mockResolvedValue({
      success: true,
      data: { file_path: 'inbox/meeting-note.md' },
      suggestions: ['Edit the note', 'Schedule follow-up']
    });

    const result = await processCaptureRequest('meeting about sprint planning with team');

    expect(mockExecute).toHaveBeenCalledWith(
      './notes capture about "sprint planning" with team using meeting template'
    );
    expect(result.success).toBe(true);
  });
});
```

### Integration Testing

```javascript
describe('End-to-End Workflows', () => {
  test('weekly review workflow', async () => {
    const workflow = await weeklyReview();

    expect(workflow.processed.success).toBe(true);
    expect(workflow.actionItems.success).toBe(true);
    expect(workflow.processed.data.notes_processed).toBeGreaterThan(0);
  });
});
```

## Troubleshooting

### Common Issues

**Issue**: Templates not found
**Solution**: Check template availability with `./notes list-templates` and verify spelling

**Issue**: Natural language parsing failures
**Solution**: Use structured parameters as fallback: `--template meeting --topic "Your Topic"`

**Issue**: Permission errors
**Solution**: Verify file system permissions and PARA directory structure

**Issue**: JSON parsing errors
**Solution**: Ensure Claude Code is using the correct JSON output mode

### Debug Mode

```javascript
const DEBUG = process.env.DEBUG_PARA_NOTES === 'true';

async function debugExecute(command) {
  if (DEBUG) {
    console.log(`[DEBUG] Executing: ${command}`);
  }

  const result = await execute(command);

  if (DEBUG) {
    console.log(`[DEBUG] Result:`, JSON.stringify(result, null, 2));
  }

  return result;
}
```

## Best Practices

### 1. User Experience
- Always provide feedback on command execution
- Offer suggestions for next actions
- Handle errors gracefully with helpful messages
- Use natural language processing when possible

### 2. Performance
- Cache frequently accessed data
- Batch operations when possible
- Use appropriate batch sizes for processing
- Monitor response times and optimize accordingly

### 3. Error Handling
- Implement comprehensive error handling
- Provide actionable error messages
- Offer recovery options
- Log errors for debugging

### 4. Integration Patterns
- Use the suggestion system to guide user workflows
- Leverage natural language processing for better UX
- Implement context-aware behavior
- Maintain consistency with Claude Code patterns

## Conclusion

The PARA Notes system provides a powerful foundation for knowledge management within Claude Code workflows. By following these integration patterns and best practices, you can create seamless, intelligent note-taking experiences that enhance productivity and project organization.

For detailed API specifications, see [API Reference](api-reference.md).
For error handling details, see [Error Codes Reference](error-codes.md).
For natural language processing, see [Natural Language Guide](natural-language-guide.md).