# ADR-001: Multi-Agent File-Based Communication Architecture

## Status
**Accepted** - November 2025

## Context
The project requires demonstrating multi-agent orchestration capabilities while maintaining clear separation of concerns between language processing (Claude) and mathematical computation (Python). We need to design a system where autonomous agents can coordinate complex workflows without direct coupling.

## Decision
We will implement a **file-based multi-agent communication architecture** where:
- Agents communicate exclusively through standardized file formats
- Each agent has a single, well-defined responsibility
- The file system acts as the message bus between agents
- Python handles only mathematical operations (embeddings, statistics)
- Claude handles all language operations (translation, text generation, analysis)

## Architecture Components

### Agent Responsibilities
```
Main Orchestrator:
- Workflow coordination
- User input processing  
- Result aggregation
- Report generation

Translator Agents (3):
- translator_1: English → French
- translator_2: French → Italian  
- translator_3: Italian → English
- Each operates autonomously

Python Scripts:
- calculate_distance.py: Semantic analysis only
- No translation or language processing
```

### Communication Protocol
```
File Locations:
/tmp/original_sentence.txt      # Input
/tmp/first_hop_translation.md   # EN→FR result
/tmp/second_hop_translation.md  # FR→IT result
/tmp/third_hop_translation.md   # IT→EN result

File Format:
Markdown with YAML headers containing:
- Source/target languages
- Timestamps
- Quality metrics
- Processing metadata
```

## Rationale

### Advantages
1. **True Agent Autonomy**: Each agent can operate independently without knowledge of others
2. **Clear Separation of Concerns**: Language vs. mathematical operations are cleanly separated
3. **Debugging Transparency**: All inter-agent communication is visible in files
4. **Scalability**: Easy to add new translation hops or analysis agents
5. **Academic Demonstration**: Clearly shows multi-agent coordination principles

### Compared Alternatives

**Alternative 1: Direct Function Calls**
- Pros: Faster execution, simpler code
- Cons: Tight coupling, no autonomy demonstration, poor academic value
- Rejected: Doesn't demonstrate multi-agent principles

**Alternative 2: Message Queue System**
- Pros: Industry standard, async messaging
- Cons: Additional infrastructure, overkill for academic project
- Rejected: Complexity doesn't match project scope

**Alternative 3: API-Based Communication**
- Pros: RESTful, industry standard
- Cons: Requires web server, network complexity
- Rejected: Adds unnecessary complexity for local academic project

## Implementation Details

### File Naming Convention
- Predictable paths enable agent discovery
- Atomic operations prevent race conditions
- Markdown format ensures human readability
- Temporary files cleaned up automatically

### Error Handling
- Each agent validates input files
- Retry logic for temporary failures
- Fallback strategies for translation errors
- State recovery from interruptions

### Quality Assurance
- File format validation
- Language detection verification
- Translation quality scoring
- Processing time tracking

## Consequences

### Positive
- **Academic Excellence**: Clear demonstration of multi-agent coordination
- **Maintainability**: Easy to modify individual agents without affecting others
- **Extensibility**: Simple to add new languages or analysis methods
- **Transparency**: Complete audit trail of all operations

### Negative
- **Performance Overhead**: File I/O slower than direct function calls
- **Storage Requirements**: Temporary files consume disk space
- **Synchronization Complexity**: Agents must coordinate through file presence

### Mitigation Strategies
- Use SSD storage for better I/O performance
- Implement automatic cleanup of temporary files
- Add file locking to prevent race conditions
- Monitor disk space usage during batch experiments

## Monitoring and Success Metrics
- **Agent Coordination Success Rate**: 100% for valid inputs
- **File Operation Reliability**: No data corruption
- **Processing Time**: <30 seconds for manual mode, <10 minutes for automated
- **Error Recovery**: Graceful handling of all failure scenarios

## References
- Software submission guidelines requirement for multi-agent demonstration
- Academic best practices for distributed systems
- File-based communication patterns in agent architectures

---
*This ADR establishes the foundational architecture enabling true multi-agent coordination while meeting academic requirements for autonomous system demonstration.*
