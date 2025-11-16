# Claude Folder Structure Guide

This document explains the organization of the `.claude` folder and how it's designed for scalability and maintainability.

## Overview

The `.claude` folder contains all multi-agent orchestration configuration, organized for maximum clarity and extensibility.

```
.claude/
├── main.md                              # Main orchestrator (entry point)
├── settings.local.json                  # Local configuration
├── FOLDER_STRUCTURE.md                  # This file
│
├── agents/                              # All agent definitions
│   ├── translators/                     # Category: Translation agents
│   │   ├── translator-1-en-fr.md
│   │   ├── translator-2-fr-it.md
│   │   └── translator-3-it-en.md
│   │
│   ├── orchestrators/                   # Category: Orchestration agents
│   │   ├── translation-experiment-orchestrator.md
│   │   ├── batch-experiment-orchestrator.md
│   │   └── embedding-analyzer.md
│   │
│   ├── code-reviewer/                   # Category: Code quality agents
│   │   └── code-reviewer.md
│   │
│   └── qa-expert/                       # Category: QA agents
│       └── qa-expert.md
│
├── commands/                            # Runnable commands
│   └── run-translation-experiment.md    # Main experiment command
│
└── skills/                              # Reusable skills (only .md files)
    ├── translate/
    │   └── SKILL.md
    ├── typo-injector/
    │   └── SKILL.md
    ├── embeddings/
    │   └── SKILL.md
    └── chart-generator/
        └── SKILL.md
```

## Key Principles

### 1. **File Format Consistency**
- **Only `.md` files** in `.claude/` folder
- All agent definitions are `.md` files
- All skill definitions are `.md` files
- No `.py`, `.js`, or other code files (kept in root `/scripts/`)
- No mixed file types

### 2. **Logical Organization by Type**
Agents are organized in subdirectories by their function:
- `/agents/translators/` - Language translation agents
- `/agents/orchestrators/` - Workflow coordination agents
- `/agents/code-reviewer/` - Code quality agents
- `/agents/qa-expert/` - Testing/quality agents

### 3. **Naming Convention**
- **Kebab-case**: All folder and file names use `kebab-case`
- **Descriptive names**: File names clearly indicate purpose
  - `translator-1-en-fr.md` (source-target pair)
  - `code-reviewer.md` (clear purpose)
  - `embedding-analyzer.md` (action + object)

### 4. **Scalability Ready**
Easy to add new agent categories in the future:
```
agents/
├── translators/          # Existing
├── orchestrators/        # Existing
├── code-reviewer/        # Existing
├── qa-expert/           # Existing
├── security-auditor/    # Future: Add when needed
├── performance-engineer/# Future: Add when needed
├── api-designer/        # Future: Add when needed
├── data-scientist/      # Future: Add when needed
└── devops-engineer/     # Future: Add when needed
```

## How Claude Uses This Structure

### Agent Discovery
Claude finds agents by:
- Scanning `/agents/` directory and subdirectories
- Looking for `.md` files
- Using file names to identify agent types
- Reading YAML frontmatter (if present) for metadata

### File References
Claude can work with this structure through:
- **File paths**: Can launch agents using relative paths
  - `agents/translators/translator-1-en-fr.md`
  - `agents/orchestrators/embedding-analyzer.md`
- **Pattern matching**: Can find agents by glob patterns
  - `agents/**/translator-*.md` (all translators)
  - `agents/orchestrators/*.md` (all orchestrators)

### Communication
- Agents communicate via files in `/tmp/` directory
- Outputs are saved to `/results/` directory
- Settings are read from `settings.local.json`

## Adding New Agents

### Step 1: Choose a Category
Identify the agent's primary function:
- Code quality → `code-reviewer/`
- Testing → `qa-expert/`
- Orchestration → `orchestrators/`
- New category? → Create new folder in `agents/`

### Step 2: Create Subfolder
```bash
mkdir -p agents/your-category/
```

### Step 3: Create Agent File
Create `agents/your-category/agent-name.md` with:
- Clear description in frontmatter (optional)
- Purpose section
- Responsibilities section
- Tools available section
- Workflow/instructions

### Example: Adding a Security Auditor
```bash
# Create folder
mkdir agents/security-auditor

# Create file
touch agents/security-auditor/security-auditor.md

# Add content following existing agent format
```

### Step 4: Update Documentation
- Update README.md with new agent description
- Update this file with new folder structure
- Update FOLDER_STRUCTURE.md with examples

## File Naming Conventions

### Agents
- **Format**: `{agent-name}.md` or `{type}-{number}-{detail}.md`
- **Examples**:
  - `translator-1-en-fr.md` (numbered with language pair)
  - `code-reviewer.md` (simple, self-explanatory)
  - `embedding-analyzer.md` (action + object)
  - `batch-experiment-orchestrator.md` (descriptive compound)

### Folders
- **Format**: `{category-name}/`
- **Examples**:
  - `translators/` (plural for collections)
  - `orchestrators/` (plural for collections)
  - `code-reviewer/` (singular for single agent)
  - `qa-expert/` (singular for single agent)

### Skills
- **Format**: `{skill-name}/SKILL.md`
- **Examples**:
  - `translate/SKILL.md`
  - `typo-injector/SKILL.md`
  - `embeddings/SKILL.md`
  - `chart-generator/SKILL.md`

## Benefits of This Structure

### 1. **Clarity**
- Clear folder organization makes it easy to find agents
- Descriptive names indicate purpose at a glance
- No confusion between agent types

### 2. **Maintainability**
- Each agent has its own file
- Related agents grouped together
- Easy to locate and modify specific agents

### 3. **Scalability**
- Easy to add new agent categories
- No file conflicts or naming collisions
- Can grow to support dozens of agents

### 4. **Claude Compatibility**
- Claude can discover agents through folder structure
- File pattern matching works reliably
- Minimal configuration needed

### 5. **Version Control**
- Clean git history
- Easy to track changes by agent
- Simple diff viewing

## Implementation Notes

### For New Projects
When starting a new project with similar structure:
1. Create base structure with main categories
2. Add agents incrementally
3. Keep related agents together
4. Use consistent naming conventions
5. Document additions

### File Format
All files should be standard Markdown (`.md`) with optional YAML frontmatter:

```markdown
---
name: agent-name
description: Brief description
tools: Tool1, Tool2, Tool3
model: sonnet
---

# Agent Name

Content here...
```

## Testing the Structure

Verify the structure is working:

```bash
# List all agents
find .claude/agents -type f -name "*.md"

# List agents by type
find .claude/agents/translators -type f -name "*.md"
find .claude/agents/orchestrators -type f -name "*.md"

# Count agents by category
echo "Translators:" && ls -1 .claude/agents/translators | wc -l
echo "Orchestrators:" && ls -1 .claude/agents/orchestrators | wc -l
echo "Code Reviewers:" && ls -1 .claude/agents/code-reviewer | wc -l
echo "QA Experts:" && ls -1 .claude/agents/qa-expert | wc -l
```

## Future Enhancements

Potential improvements:
- [ ] Create index/manifest file listing all agents
- [ ] Add version information for agents
- [ ] Create agent templates for quick creation
- [ ] Add capabilities matrix showing agent skills
- [ ] Create performance benchmarks
- [ ] Add cost analysis per agent
- [ ] Create automated testing for agents
- [ ] Add usage examples and tutorials
