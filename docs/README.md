# Project Documentation

## Overview
This directory contains comprehensive documentation for the project, organized by type and purpose.

## Directory Structure

### `features/`
Contains both development stories and user-facing feature documentation.

**Structure**: 
- `features/[feature-name]/` - One directory per feature
  - `story-[no].md` - Individual development stories with acceptance criteria  
  - `implementation-[no].md` - Implementation plans with tasks and progress
  - `feature-overview.md` - User-facing feature documentation and workflows

### `architecture/`
System architecture documentation and technical decisions.

**Files**:
- `system-overview.md` - High-level system architecture
- `business-overview.md` - Project purpose, goals, and business context
- `decisions/` - Architectural Decision Records (ADRs)
- `diagrams/` - Architecture diagrams and visual representations

### `api/`
API documentation and reference materials.

**Files**:
- `endpoints.md` - API endpoint documentation
- `changelog.md` - API version history and changes
- `authentication.md` - Authentication and security guidelines

## Documentation Standards

### Writing Guidelines
- **Clarity**: Write for your intended audience
- **Conciseness**: Be comprehensive but not verbose
- **Currency**: Keep documentation up-to-date with code changes
- **Consistency**: Follow established formats and patterns

### Maintenance
- Update documentation with every relevant code change
- Review and update quarterly for accuracy
- Remove or archive outdated information
- Use automated tools where possible

### Formatting
- Use Markdown for all documentation
- Follow consistent heading structure
- Include code examples and diagrams where helpful
- Use proper linking between related documents

## Getting Started
1. Review the main README.md for project setup
2. Check `architecture/system-overview.md` for system understanding
3. Browse `features/` for user-facing functionality
4. Reference `api/` for technical integration details

## Contributing
When making changes:
1. Follow the documentation update process in `prompts/update-documentation.prompt.md`
2. Update relevant sections during development, not after
3. Ensure examples and code snippets are tested and accurate
4. Review related documents for consistency
