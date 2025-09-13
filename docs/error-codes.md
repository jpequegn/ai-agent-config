# Error Codes Reference

Comprehensive reference for all error codes returned by the PARA Notes API system.

## Error Response Format

All errors follow a standardized JSON response format:

```json
{
  "success": false,
  "command": "command-name",
  "message": "Human-readable error message",
  "data": null,
  "suggestions": [
    "Actionable suggestion 1",
    "Actionable suggestion 2"
  ],
  "error_details": "ERROR_CODE: Detailed technical description"
}
```

## Error Code Categories

### Parameter Errors (1000-1099)

**1001 - MISSING_REQUIRED_PARAM**
- **Description**: A required parameter was not provided
- **Common Causes**:
  - Missing --topic for meeting templates
  - Missing --file for research command
- **Example**:
  ```json
  {
    "error_details": "MISSING_REQUIRED_PARAM: Meeting template requires --topic parameter",
    "suggestions": [
      "Add --topic parameter: /notes capture --template meeting --topic 'Your Topic'",
      "Use quick-note template which doesn't require topic: --template quick-note"
    ]
  }
  ```

**1002 - INVALID_PARAMETER_VALUE**
- **Description**: Parameter value is invalid or malformed
- **Common Causes**:
  - Invalid date format
  - Unrecognized template name
  - Invalid PARA category
- **Example**:
  ```json
  {
    "error_details": "INVALID_PARAMETER_VALUE: Date '2024-13-45' is not a valid date format",
    "suggestions": [
      "Use YYYY-MM-DD format: --date 2024-09-15",
      "Use relative dates: --date tomorrow"
    ]
  }
  ```

**1003 - PARAMETER_CONFLICT**
- **Description**: Conflicting parameters were provided
- **Common Causes**:
  - Both --output and natural language output specification
  - Conflicting date specifications
- **Example**:
  ```json
  {
    "error_details": "PARAMETER_CONFLICT: Cannot specify both --output and natural language output path",
    "suggestions": [
      "Use only --output parameter for explicit file paths",
      "Use only natural language for automatic naming"
    ]
  }
  ```

### Template Errors (1100-1199)

**1101 - TEMPLATE_NOT_FOUND**
- **Description**: Specified template does not exist
- **Common Causes**:
  - Typo in template name
  - Requesting non-existent custom template
- **Example**:
  ```json
  {
    "error_details": "TEMPLATE_NOT_FOUND: Template 'meting' not found (did you mean 'meeting'?)",
    "suggestions": [
      "Use /notes list-templates to see available templates",
      "Check spelling: did you mean 'meeting'?"
    ]
  }
  ```

**1102 - TEMPLATE_MALFORMED**
- **Description**: Template file exists but has invalid structure
- **Common Causes**:
  - Corrupted template file
  - Invalid Jinja2 syntax in custom template
- **Example**:
  ```json
  {
    "error_details": "TEMPLATE_MALFORMED: Template 'custom-template' contains invalid Jinja2 syntax at line 15",
    "suggestions": [
      "Check template file for syntax errors",
      "Use built-in templates as examples for custom template creation"
    ]
  }
  ```

**1103 - TEMPLATE_VARIABLE_MISSING**
- **Description**: Required template variable not provided
- **Common Causes**:
  - Custom template requires specific variables
  - Missing context for template rendering
- **Example**:
  ```json
  {
    "error_details": "TEMPLATE_VARIABLE_MISSING: Template requires 'project_name' variable",
    "suggestions": [
      "Add variable: --var project_name='Your Project'",
      "Check template documentation for required variables"
    ]
  }
  ```

### File System Errors (1200-1299)

**1201 - FILE_NOT_FOUND**
- **Description**: Specified file does not exist
- **Common Causes**:
  - Wrong file path in research/find commands
  - File was moved or deleted
- **Example**:
  ```json
  {
    "error_details": "FILE_NOT_FOUND: Note file 'notes/missing.md' does not exist",
    "suggestions": [
      "Use /notes find to locate the file",
      "Check if file path is correct"
    ]
  }
  ```

**1202 - PERMISSION_DENIED**
- **Description**: Insufficient permissions to read/write file or directory
- **Common Causes**:
  - Read-only file system
  - Insufficient user permissions
  - Protected directory
- **Example**:
  ```json
  {
    "error_details": "PERMISSION_DENIED: Cannot write to directory '/protected/notes/'",
    "suggestions": [
      "Choose a different output directory",
      "Check file permissions: chmod 755 /path/to/directory"
    ]
  }
  ```

**1203 - DISK_SPACE_FULL**
- **Description**: Insufficient disk space to create file
- **Common Causes**:
  - Full disk
  - Quota exceeded
- **Example**:
  ```json
  {
    "error_details": "DISK_SPACE_FULL: Cannot create file, insufficient disk space",
    "suggestions": [
      "Free up disk space before creating notes",
      "Use a different output location with more space"
    ]
  }
  ```

**1204 - FILE_ALREADY_EXISTS**
- **Description**: File already exists and overwrite not permitted
- **Common Causes**:
  - Duplicate file creation attempt
  - Protection against accidental overwrites
- **Example**:
  ```json
  {
    "error_details": "FILE_ALREADY_EXISTS: File 'meeting-notes.md' already exists",
    "suggestions": [
      "Use a different filename or add timestamp",
      "Add --force flag to overwrite existing file"
    ]
  }
  ```

### Parsing Errors (1300-1399)

**1301 - MALFORMED_NOTE**
- **Description**: Note file has invalid markdown or frontmatter structure
- **Common Causes**:
  - Corrupted frontmatter YAML
  - Invalid markdown structure
  - Encoding issues
- **Example**:
  ```json
  {
    "error_details": "MALFORMED_NOTE: Invalid YAML frontmatter in line 3 of 'note.md'",
    "suggestions": [
      "Use --graceful flag to handle malformed notes",
      "Check YAML syntax in frontmatter section"
    ]
  }
  ```

**1302 - NATURAL_LANGUAGE_PARSE_ERROR**
- **Description**: Could not parse natural language input
- **Common Causes**:
  - Ambiguous or unclear input
  - No recognizable patterns
- **Example**:
  ```json
  {
    "error_details": "NATURAL_LANGUAGE_PARSE_ERROR: No recognizable patterns in 'xyz abc def'",
    "suggestions": [
      "Use structured parameters: --topic 'your topic'",
      "Try: /notes capture --template meeting --topic 'Sprint Planning'"
    ]
  }
  ```

**1303 - DATE_PARSE_ERROR**
- **Description**: Could not parse date string
- **Common Causes**:
  - Invalid date format
  - Ambiguous relative date
- **Example**:
  ```json
  {
    "error_details": "DATE_PARSE_ERROR: Cannot parse 'next next week' as date",
    "suggestions": [
      "Use YYYY-MM-DD format: 2024-09-20",
      "Use simple relative dates: tomorrow, next week"
    ]
  }
  ```

### Configuration Errors (1400-1499)

**1401 - CONFIG_ERROR**
- **Description**: Configuration file issue
- **Common Causes**:
  - Missing .para-config.yaml
  - Invalid configuration syntax
- **Example**:
  ```json
  {
    "error_details": "CONFIG_ERROR: .para-config.yaml not found or invalid",
    "suggestions": [
      "Run ./setup-para.sh to initialize configuration",
      "Check YAML syntax in configuration file"
    ]
  }
  ```

**1402 - INVALID_CATEGORY**
- **Description**: Invalid PARA category specified
- **Common Causes**:
  - Typo in category name
  - Custom category not configured
- **Example**:
  ```json
  {
    "error_details": "INVALID_CATEGORY: 'project' is not valid (did you mean 'projects'?)",
    "suggestions": [
      "Valid categories: projects, areas, resources, archive",
      "Check spelling: 'projects' not 'project'"
    ]
  }
  ```

### Network/External Errors (1500-1599)

**1501 - NETWORK_ERROR**
- **Description**: Network-related failure during external operations
- **Common Causes**:
  - No internet connection for web search
  - API timeout
  - DNS resolution failure
- **Example**:
  ```json
  {
    "error_details": "NETWORK_ERROR: Failed to connect to external research API",
    "suggestions": [
      "Check internet connection",
      "Try again later if service is temporarily unavailable"
    ]
  }
  ```

**1502 - API_RATE_LIMIT**
- **Description**: External API rate limit exceeded
- **Common Causes**:
  - Too many API calls in short period
  - Service quota exceeded
- **Example**:
  ```json
  {
    "error_details": "API_RATE_LIMIT: Research API rate limit exceeded, retry in 60 seconds",
    "suggestions": [
      "Wait 60 seconds before retrying",
      "Reduce frequency of research requests"
    ]
  }
  ```

### System Errors (1600-1699)

**1601 - INTERNAL_ERROR**
- **Description**: Unexpected internal system error
- **Common Causes**:
  - Software bugs
  - System resource exhaustion
  - Corrupted state
- **Example**:
  ```json
  {
    "error_details": "INTERNAL_ERROR: Unexpected error in note processing pipeline",
    "suggestions": [
      "Try the command again",
      "Report this error if it persists"
    ]
  }
  ```

**1602 - TIMEOUT_ERROR**
- **Description**: Operation timed out
- **Common Causes**:
  - Large file processing
  - Slow file system
  - Resource contention
- **Example**:
  ```json
  {
    "error_details": "TIMEOUT_ERROR: Note processing timed out after 30 seconds",
    "suggestions": [
      "Try processing smaller batches",
      "Check system performance and resources"
    ]
  }
  ```

## Error Handling Best Practices

### For Claude Code Integration

1. **Always Check Success Flag**
   ```javascript
   if (!response.success) {
     // Handle error appropriately
     showErrorMessage(response.message);
     showSuggestions(response.suggestions);
   }
   ```

2. **Use Suggestions for Recovery**
   - Present suggestions to user for self-service recovery
   - Provide clickable/actionable suggestions when possible
   - Show alternative approaches

3. **Progressive Error Handling**
   ```javascript
   // Try graceful handling first
   try {
     result = await notesApi.research(file, {graceful: true});
   } catch (error) {
     // Fallback to manual processing
     showManualOptions(error.suggestions);
   }
   ```

### Error Prevention

1. **Validate Input Early**
   - Check required parameters before API calls
   - Validate date formats client-side
   - Verify file existence for file-based operations

2. **Use Graceful Modes**
   - Add `--graceful` flag for operations that might encounter malformed data
   - Implement retry logic for network operations
   - Provide fallback options for failed operations

3. **Provide Clear Context**
   - Include relevant context in error messages
   - Show the exact command that failed
   - Provide specific rather than generic suggestions

## Error Code Quick Reference

| Code | Category | Description |
|------|----------|-------------|
| 1001 | Parameter | Missing required parameter |
| 1002 | Parameter | Invalid parameter value |
| 1003 | Parameter | Parameter conflict |
| 1101 | Template | Template not found |
| 1102 | Template | Template malformed |
| 1103 | Template | Missing template variable |
| 1201 | File System | File not found |
| 1202 | File System | Permission denied |
| 1203 | File System | Disk space full |
| 1204 | File System | File already exists |
| 1301 | Parsing | Malformed note |
| 1302 | Parsing | Natural language parse error |
| 1303 | Parsing | Date parse error |
| 1401 | Configuration | Configuration error |
| 1402 | Configuration | Invalid category |
| 1501 | Network | Network error |
| 1502 | Network | API rate limit |
| 1601 | System | Internal error |
| 1602 | System | Timeout error |

## Testing Error Scenarios

Each error code should be tested with:

1. **Unit Tests**: Verify error code generation
2. **Integration Tests**: Test error propagation through API
3. **User Experience Tests**: Validate error messages and suggestions are helpful
4. **Recovery Tests**: Ensure suggested recovery actions work