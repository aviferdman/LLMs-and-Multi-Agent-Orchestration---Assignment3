# System Architecture Documentation
## Multi-Agent Translation Semantic Drift Experiment

### Document Information
- **Version**: 1.0
- **Date**: November 2025
- **Project**: LLMs and Multi-Agent Orchestration - Assignment 3
- **Architecture Type**: Multi-Agent File-Based Communication System

---

## 1. Architecture Overview

### 1.1 System Context (C4 Model - Level 1)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              System Context                             │
└─────────────────────────────────────────────────────────────────────────┘

    [Researcher/Student]
           │
           │ Natural language commands
           │ ("Analyze sentence X" / "Run batch experiment")
           ▼
    ┌──────────────────────────────────────────┐
    │                                          │
    │     Multi-Agent Translation              │
    │     Semantic Drift System                │
    │                                          │
    │ • Processes sentences with typos         │
    │ • Coordinates multi-hop translations     │
    │ • Measures semantic drift                │
    │ • Generates research reports             │
    │                                          │
    └──────────────────────────────────────────┘
           │                            │
           │ Embedding requests          │ Translation requests
           ▼                            ▼
    ┌─────────────────┐         ┌─────────────────┐
    │  Sentence       │         │  Claude LLM     │
    │  Transformers   │         │  Translation    │
    │  Library        │         │  Service        │
    │                 │         │                 │
    │ • 384-dim       │         │ • Multi-lang    │
    │   embeddings    │         │   translation   │
    │ • Cosine        │         │ • High quality  │
    │   distance      │         │   output        │
    └─────────────────┘         └─────────────────┘
```

### 1.2 Key Architectural Principles

**Separation of Concerns:**
- **Claude Agents**: Handle all language-related operations (translation, text generation)
- **Python Scripts**: Handle all mathematical operations (embeddings, distances, statistics)
- **File System**: Mediates communication between agents

**Autonomous Agents:**
- Each agent operates independently
- No direct inter-agent dependencies
- Communication through standardized file contracts

**Event-Driven Workflow:**
- Agents respond to file creation events
- Sequential processing through the translation chain
- Asynchronous execution with synchronization points

---

## 2. Container Architecture (C4 Model - Level 2)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Container Architecture                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            Claude Environment                          │
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
│  │                 │    │                 │    │                 │     │
│  │ Main            │    │ Translator      │    │ Translator      │     │
│  │ Orchestrator    │◄──►│ Agent 1         │◄──►│ Agent 2         │     │
│  │ (.claude)       │    │ (EN → FR)       │    │ (FR → IT)       │     │
│  │                 │    │                 │    │                 │     │
│  │ • Workflow      │    │ • Translation   │    │ • Translation   │     │
│  │   coordination  │    │   execution     │    │   execution     │     │
│  │ • User input    │    │ • Quality       │    │ • Quality       │     │
│  │ • Report gen    │    │   validation    │    │   validation    │     │
│  │                 │    │                 │    │                 │     │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘     │
│           │                       │                       │            │
│           │              ┌─────────────────┐              │            │
│           │              │                 │              │            │
│           │              │ Translator      │              │            │
│           │              │ Agent 3         │◄─────────────┘            │
│           │              │ (IT → EN)       │                           │
│           │              │                 │                           │
│           │              │ • Final         │                           │
│           │              │   translation   │                           │
│           │              │ • Result        │                           │
│           │              │   preparation   │                           │
│           │              │                 │                           │
│           │              └─────────────────┘                           │
│           │                       │                                    │
└───────────┼───────────────────────┼────────────────────────────────────┘
            │                       │
            │                       │
            ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Shared File System                              │
│                                                                         │
│  /tmp/                           results/                              │
│  ├── original_sentence.txt       ├── manual_report.md                  │
│  ├── input_sentence.txt          ├── automated_report.md               │
│  ├── first_hop_translation.md    ├── semantic_drift_chart.png          │
│  ├── second_hop_translation.md   └── experiment_results.csv            │
│  └── third_hop_translation.md                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
            │                       │
            │                       │
            ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Python Environment                              │
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
│  │                 │    │                 │    │                 │     │
│  │ calculate_      │    │ embedding_      │    │ visualization_  │     │
│  │ distance.py     │    │ utils.py        │    │ generator.py    │     │
│  │                 │    │                 │    │                 │     │
│  │ • Main entry    │    │ • sentence-     │    │ • matplotlib    │     │
│  │   point         │    │   transformers  │    │   charts        │     │
│  │ • CLI interface │    │ • Embedding     │    │ • Statistical   │     │
│  │ • Error         │    │   computation   │    │   analysis      │     │
│  │   handling      │    │ • Distance      │    │ • Result        │     │
│  │                 │    │   calculation   │    │   export        │     │
│  │                 │    │                 │    │                 │     │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Container Responsibilities

**Claude Environment:**
- All natural language processing
- Translation coordination and execution
- Workflow orchestration and state management
- Report generation and result interpretation

**Shared File System:**
- Inter-container communication medium
- State persistence between execution phases
- Result storage and history management
- Atomic operations for data consistency

**Python Environment:**
- Mathematical computations only
- Embedding vector generation
- Statistical analysis and visualization
- No language processing or translation

---

## 3. Component Architecture (C4 Model - Level 3)

### 3.1 Main Orchestrator Component

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Main Orchestrator                               │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Input Parser    │    │ Mode Detector   │    │ Workflow        │
│                 │    │                 │    │ Coordinator     │
│ • Sentence      │    │ • Manual vs     │    │                 │
│   validation    │    │   Automated     │    │ • Agent         │
│ • Length check  │    │ • Batch size    │    │   sequencing    │
│ • Typo          │    │   detection     │    │ • Error         │
│   detection     │    │ • Parameter     │    │   recovery      │
│                 │    │   extraction    │    │ • Result        │
│                 │    │                 │    │   aggregation   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ State Manager   │    │ File I/O        │    │ Report          │
│                 │    │ Handler         │    │ Generator       │
│ • Execution     │    │                 │    │                 │
│   tracking      │    │ • File creation │    │ • Markdown      │
│ • Progress      │    │ • Atomic writes │    │   formatting    │
│   monitoring    │    │ • Lock          │    │ • Statistical   │
│ • Error state   │    │   management    │    │   summary       │
│   management    │    │ • Cleanup       │    │ • Visualization │
│                 │    │   operations    │    │   integration   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 3.2 Translator Agent Component

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Translator Agent                               │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ File Listener   │    │ Translation     │    │ Quality         │
│                 │    │ Engine          │    │ Validator       │
│ • Input file    │    │                 │    │                 │
│   monitoring    │    │ • Claude LLM    │    │ • Length check  │
│ • Format        │    │   integration   │    │ • Language      │
│   validation    │    │ • Language      │    │   detection     │
│ • Trigger       │    │   pair config   │    │ • Semantic      │
│   detection     │    │ • Context       │    │   validation    │
│                 │    │   preservation  │    │ • Error         │
│                 │    │                 │    │   flagging      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Error Handler   │    │ Output          │    │ Metadata        │
│                 │    │ Formatter       │    │ Manager         │
│ • Retry logic   │    │                 │    │                 │
│ • Fallback      │    │ • Markdown      │    │ • Timestamp     │
│   strategies    │    │   structure     │    │   tracking      │
│ • Error         │    │ • Header        │    │ • Language      │
│   reporting     │    │   generation    │    │   pair info     │
│ • State         │    │ • Content       │    │ • Quality       │
│   recovery      │    │   validation    │    │   metrics       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 3.3 Python Analysis Component

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Python Analysis Engine                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Embedding       │    │ Distance        │    │ Statistics      │
│ Computer        │    │ Calculator      │    │ Engine          │
│                 │    │                 │    │                 │
│ • Model loader  │    │ • Cosine        │    │ • Descriptive   │
│ • Text          │    │   similarity    │    │   statistics    │
│   preprocessing │    │ • Vector        │    │ • Correlation   │
│ • Vector        │    │   operations    │    │   analysis      │
│   generation    │    │ • Precision     │    │ • Trend         │
│ • Normalization │    │   control       │    │   detection     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Model Manager   │    │ CLI Interface   │    │ Visualization   │
│                 │    │                 │    │ Generator       │
│ • Model         │    │ • Argument      │    │                 │
│   caching       │    │   parsing       │    │ • Matplotlib    │
│ • Version       │    │ • Error         │    │   integration   │
│   control       │    │   handling      │    │ • Chart types   │
│ • Memory        │    │ • Output        │    │ • Export        │
│   optimization  │    │   formatting    │    │   formats       │
│                 │    │                 │    │ • Styling       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 4. Operational Architecture

### 4.1 Manual Mode Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Manual Mode Workflow                           │
└─────────────────────────────────────────────────────────────────────────┘

User Input: "Analyze: 'The quik brown fox...'"
    │
    ▼
┌─────────────────┐
│ Main            │
│ Orchestrator    │ ──┐ Saves original to /tmp/original_sentence.txt
│                 │   │
└─────────────────┘   │
    │                 │
    │ Launches        │
    ▼                 │
┌─────────────────┐   │
│ Translator 1    │   │ Reads original, translates EN→FR
│ (EN → FR)       │ ──┘ Writes to /tmp/first_hop_translation.md
│                 │
└─────────────────┘
    │
    │ File trigger
    ▼
┌─────────────────┐
│ Translator 2    │ ──┐ Reads French, translates FR→IT  
│ (FR → IT)       │   │ Writes to /tmp/second_hop_translation.md
│                 │   │
└─────────────────┘   │
    │                 │
    │ File trigger    │
    ▼                 │
┌─────────────────┐   │
│ Translator 3    │   │ Reads Italian, translates IT→EN
│ (IT → EN)       │ ──┘ Writes to /tmp/third_hop_translation.md
│                 │
└─────────────────┘
    │
    │ Completion signal
    ▼
┌─────────────────┐
│ Main            │ ──┐ Calls: python calculate_distance.py
│ Orchestrator    │   │ Reads original + final translation
│                 │   │ Generates report
└─────────────────┘   │
    │                 │
    │ Results         │
    ▼                 │
┌─────────────────┐   │
│ User            │ ──┘ Displays semantic distance + analysis
│                 │
└─────────────────┘

Time: ~30 seconds total
Files created: 4 temporary files + 1 result file
```

### 4.2 Automated Mode Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Automated Mode Workflow                         │
└─────────────────────────────────────────────────────────────────────────┘

User Input: "Run automated experiment"
    │
    ▼
┌─────────────────┐
│ Batch           │ ──┐ Phase 1: Sentence Generation
│ Orchestrator    │   │ • Creates 21 unique sentences (>15 words)
│                 │   │ • Introduces typos at 20-50% rates
└─────────────────┘   │ • Documents all variations
    │                 │
    │ For each        │
    │ sentence        │
    ▼                 │
┌─────────────────┐   │
│ Translation     │   │ Phase 2: Translation Processing
│ Pipeline        │ ──┘ • Runs each through 3-agent chain
│ (21 cycles)     │     • Documents intermediate results
│                 │     • Tracks qualitative observations
└─────────────────┘
    │
    │ All translations complete
    ▼
┌─────────────────┐
│ Report          │ ──┐ Phase 3: Qualitative Analysis
│ Generator       │   │ • Comprehensive markdown report
│                 │   │ • Statistical summary tables
└─────────────────┘   │ • Trend analysis and insights
    │                 │
    │ Report ready    │
    ▼                 │
┌─────────────────┐   │
│ Python          │   │ Phase 4: Quantitative Analysis
│ Analyzer        │ ──┘ • 21 embedding distance calculations
│                 │     • Statistical graph generation
└─────────────────┘     • Data export (CSV)
    │
    │ Complete analysis
    ▼
┌─────────────────┐
│ User            │ ──┐ Final consolidated report with:
│                 │   │ • All 21 sentence analyses
└─────────────────┘   │ • Statistical visualizations
                      │ • Research-quality insights
                      │
Time: ~10 minutes total
Files created: 63 translation files + 1 comprehensive report + graph + CSV
```

### 4.3 Error Handling and Recovery

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Error Handling Strategy                         │
└─────────────────────────────────────────────────────────────────────────┘

Translation Failure:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Agent detects   │───►│ Retry with      │───►│ Fallback to     │
│ translation     │    │ exponential     │    │ alternate       │
│ error           │    │ backoff         │    │ approach        │
└─────────────────┘    └─────────────────┘    └─────────────────┘

File Access Failure:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Lock detected   │───►│ Wait with       │───►│ Report timeout  │
│ or permission   │    │ increasing      │    │ and continue    │
│ denied          │    │ intervals       │    │ with next       │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Python Analysis Failure:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Embedding or    │───►│ Check model     │───►│ Report error    │
│ calculation     │    │ availability    │    │ with specific   │
│ error           │    │ and retry       │    │ guidance        │
└─────────────────┘    └─────────────────┘    └─────────────────┘

State Recovery:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ System          │───►│ Resume from     │───►│ Complete        │
│ interruption    │    │ last completed  │    │ remaining       │
│                 │    │ stage           │    │ stages          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 5. Data Architecture

### 5.1 File Communication Protocol

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     File Communication Protocol                         │
└─────────────────────────────────────────────────────────────────────────┘

File Naming Convention:
/tmp/original_sentence.txt      # Original input (clean)
/tmp/input_sentence.txt         # Typo-injected version
/tmp/first_hop_translation.md   # EN → FR result
/tmp/second_hop_translation.md  # FR → IT result  
/tmp/third_hop_translation.md   # IT → EN result

File Format Standard:
---
# Translation Result
**Source Language**: [language_code]
**Target Language**: [language_code] 
**Timestamp**: [ISO_8601]
**Agent**: [agent_identifier]
**Quality Score**: [0.0-1.0]

## Original Text
[source_text]

## Translated Text
[translated_text]

## Metadata
- Word count: [number]
- Character count: [number]
- Processing time: [milliseconds]
---

Atomic Operations Protocol:
1. Write to temporary file (.tmp extension)
2. Validate content structure
3. Atomic rename to final filename
4. Signal completion via file presence
5. Cleanup temporary files on success
```

### 5.2 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Data Flow Diagram                             │
└─────────────────────────────────────────────────────────────────────────┘

Input Data:
┌─────────────────┐
│ User Sentence   │
│ (with typos)    │
│                 │
│ "The quik brn   │
│  fox jumps ovr  │
│  the lazi dog"  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Structured      │
│ Input File      │
│                 │
│ • Original      │
│ • Typo count    │
│ • Word count    │
└─────────────────┘

Processing Chain:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ EN: "The quik   │───►│ FR: "Le renard  │───►│ IT: "La volpe   │
│ brown fox..."   │    │ brun rapide..."│    │ marrone..."     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │ EN: "The quick  │
                                               │ brown fox..."   │
                                               └─────────────────┘

Analysis Data:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Original Vector │    │ Final Vector    │    │ Distance        │
│ [384 dims]      │───►│ [384 dims]      │───►│ 0.234567        │
│                 │    │                 │    │                 │
│ [0.123, -0.456, │    │ [0.134, -0.445, │    │ (Cosine Dist)   │
│  0.789, ...]    │    │  0.778, ...]    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Output Data:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Detailed Report │    │ Statistical     │    │ Visualization   │
│ (Markdown)      │───►│ Summary (CSV)   │───►│ Charts (PNG)    │
│                 │    │                 │    │                 │
│ • Full chain    │    │ • All distances │    │ • Typo vs Dist  │
│ • Analysis      │    │ • Averages      │    │ • Trend lines   │
│ • Insights      │    │ • Std dev       │    │ • Statistics    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 6. Technology Architecture

### 6.1 Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Technology Stack                             │
└─────────────────────────────────────────────────────────────────────────┘

Execution Environment:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Claude Code CLI │    │ Python 3.8+     │    │ Local File      │
│                 │    │ Runtime         │    │ System          │
│ • Agent exec    │    │                 │    │                 │
│ • File I/O      │    │ • Math libs     │    │ • Persistence   │
│ • Orchestration │    │ • ML models     │    │ • Inter-process │
│                 │    │ • Visualization │    │   communication │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Core Libraries:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ sentence-       │    │ torch >=2.0.0   │    │ matplotlib      │
│ transformers    │    │                 │    │ >=3.7.0         │
│ >=2.2.2         │    │ • PyTorch       │    │                 │
│                 │    │   framework     │    │ • Chart         │
│ • Pre-trained   │    │ • Neural net    │    │   generation    │
│   models        │    │   operations    │    │ • Export        │
│ • Embeddings    │    │ • GPU support   │    │   formats       │
│ • Similarity    │    │   (optional)    │    │ • Styling       │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Supporting Libraries:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ numpy >=1.24.0  │    │ scipy >=1.10.0  │    │ transformers    │
│                 │    │                 │    │ >=4.30.0        │
│ • Array ops     │    │ • Distance      │    │                 │
│ • Vector math   │    │   calculations  │    │ • NLP utilities │
│ • Statistics    │    │ • Statistical   │    │ • Model mgmt    │
│                 │    │   functions     │    │ • Tokenization  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 6.2 Model Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            Model Architecture                          │
└─────────────────────────────────────────────────────────────────────────┘

Embedding Model: all-MiniLM-L6-v2
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Input Text      │───►│ Transformer     │───►│ 384-D Vector    │
│                 │    │ Architecture    │    │                 │
│ "Hello world"   │    │                 │    │ [0.123, -0.456, │
│                 │    │ • 6 layers      │    │  0.789, ...]    │
│ (Any length)    │    │ • 384 hidden    │    │                 │
│                 │    │ • 12 attention  │    │ (Normalized)    │
│                 │    │   heads         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Model Characteristics:
• Size: ~90MB download
• Languages: 100+ supported
• Speed: ~1000 sentences/second
• Accuracy: State-of-the-art for semantic similarity
• Memory: ~500MB RAM during inference

Distance Calculation:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Vector A        │    │ Cosine          │    │ Distance        │
│ [a1,a2,a3...]   │───►│ Similarity      │───►│ 1 - similarity  │
│                 │    │                 │    │                 │
│ Vector B        │    │ dot(A,B) /      │    │ Range: [0, 2]   │
│ [b1,b2,b3...]   │───►│ (|A| * |B|)     │───►│ 0 = identical   │
│                 │    │                 │    │ 2 = opposite    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 7. Security Architecture

### 7.1 Security Considerations

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Security Architecture                         │
└─────────────────────────────────────────────────────────────────────────┘

File System Security:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Temporary Files │    │ Result Files    │    │ Process         │
│ (/tmp/)         │    │ (results/)      │    │ Isolation       │
│                 │    │                 │    │                 │
│ • Auto cleanup  │    │ • Persistent    │    │ • No external   │
│ • Local only    │    │ • User owned    │    │   network calls │
│ • Process       │    │ • Read/write    │    │ • Sandboxed     │
│   ownership     │    │   permissions   │    │   execution     │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Data Privacy:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Input Text      │    │ Translation     │    │ Embeddings      │
│                 │    │ Processing      │    │                 │
│ • Local only    │    │                 │    │ • Local model   │
│ • No external   │    │ • Claude native │    │ • No external   │
│   transmission │    │ • No API keys   │    │   transmission  │
│ • Automatic     │    │ • No logging    │    │ • Memory only   │
│   cleanup       │    │   of content    │    │   processing    │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Dependency Security:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Python Packages │    │ Model Downloads │    │ Execution       │
│                 │    │                 │    │ Environment     │
│ • Version       │    │ • Hugging Face  │    │                 │
│   pinning       │    │   official      │    │ • Controlled    │
│ • Known sources │    │   sources       │    │   environment   │
│ • Integrity     │    │ • Checksum      │    │ • Resource      │
│   verification │    │   validation    │    │   limits        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 7.2 Risk Mitigation

**File Access Risks:**
- Temporary files in isolated /tmp/ directory
- Automatic cleanup on completion
- Process-level ownership controls

**Data Exposure Risks:**
- All processing happens locally
- No external API calls for translation
- No persistent storage of sensitive input

**Model Security Risks:**
- Official model sources only
- Checksum verification on download
- Sandboxed model execution

---

## 8. Performance Architecture

### 8.1 Performance Characteristics

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Performance Architecture                        │
└─────────────────────────────────────────────────────────────────────────┘

Translation Performance:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Single          │    │ Batch (21)      │    │ Optimization    │
│ Translation     │    │ Translations    │    │ Strategies      │
│                 │    │                 │    │                 │
│ ~30 seconds     │    │ ~10 minutes     │    │ • Parallel      │
│ • 3 hops        │    │ • 63 total ops  │    │   translation   │
│ • File I/O      │    │ • File batching │    │ • Model caching │
│ • Analysis      │    │ • Bulk analysis │    │ • Async I/O     │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Embedding Performance:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Single          │    │ Batch           │    │ Memory Usage    │
│ Calculation     │    │ Calculation     │    │                 │
│                 │    │                 │    │                 │
│ ~100ms          │    │ ~2 seconds      │    │ • Model: 500MB  │
│ • Load model    │    │ • 42 vectors    │    │ • Working: 100MB│
│ • Compute       │    │ • 21 distances  │    │ • Peak: 600MB   │
│ • Distance      │    │ • Statistics    │    │ • Cleanup: 50MB │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Scalability Metrics:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Memory Scaling  │    │ CPU Scaling     │    │ I/O Scaling     │
│                 │    │                 │    │                 │
│ O(1) per        │    │ O(n) parallel   │    │ O(n) sequential │
│ sentence        │    │ translation     │    │ file operations │
│ • Constant      │    │ • Linear batch  │    │ • Atomic writes │
│   embedding     │    │ • Multi-core    │    │ • Sequential    │
│   size          │    │   embedding     │    │   reading       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 8.2 Resource Requirements

**Minimum System Requirements:**
- CPU: 2 cores, 2.5 GHz
- RAM: 2 GB available
- Storage: 1 GB free space
- Network: For initial model download only

**Recommended System Requirements:**
- CPU: 4 cores, 3.0 GHz  
- RAM: 4 GB available
- Storage: 2 GB free space
- SSD for faster file I/O

**Resource Utilization:**
- Peak memory: 600 MB (model + processing)
- Average CPU: 30% during translation
- Peak CPU: 80% during embedding calculation
- Disk I/O: Minimal, mostly sequential

---

## 9. Deployment Architecture

### 9.1 Deployment Model

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Deployment Architecture                        │
└─────────────────────────────────────────────────────────────────────────┘

Local Development Environment:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Source Code     │    │ Dependencies    │    │ Execution       │
│                 │    │                 │    │                 │
│ • Git           │    │ • pip install   │    │ • Claude CLI    │
│   repository    │    │   -r require-   │    │ • Python        │
│ • Documentation │    │   ments.txt     │    │   interpreter   │
│ • Test data     │    │ • Model         │    │ • File system   │
│                 │    │   download      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Directory Structure (Deployed):
project-root/
├── .claude/                    # Agent definitions
│   ├── main.claude            
│   ├── agents/                
│   │   ├── translator_1.claude
│   │   ├── translator_2.claude
│   │   └── translator_3.claude
│   └── skills/                # Reusable components
├── docs/                      # Documentation
├── results/                   # Output directory  
├── tmp/                       # Temporary files
├── calculate_distance.py      # Analysis script
├── requirements.txt           # Dependencies
├── README.md                  # User guide
└── .gitignore                # Version control

Runtime Dependencies:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Python          │    │ Claude CLI      │    │ System          │
│ Environment     │    │                 │    │ Requirements    │
│                 │    │ • Agent engine  │    │                 │
│ • 3.8+          │    │ • File I/O      │    │ • Read/write    │
│ • pip packages  │    │ • Orchestration │    │   permissions   │
│ • ML libraries  │    │ • Error         │    │ • Temp space    │
│                 │    │   handling      │    │ • Network       │
│                 │    │                 │    │   (initial)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 9.2 Installation Process

```
Installation Workflow:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Prerequisites   │───►│ Dependency      │───►│ Verification    │
│ Check           │    │ Installation    │    │ & Testing       │
│                 │    │                 │    │                 │
│ • Python 3.8+   │    │ • pip install   │    │ • Import test   │
│ • pip available │    │ • Model         │    │ • CLI test      │
│ • Disk space    │    │   download      │    │ • Sample run    │
│ • Permissions   │    │ • Directory     │    │ • Cleanup       │
│                 │    │   creation      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘

Configuration:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Default         │    │ User            │    │ Environment     │
│ Settings        │    │ Customization   │    │ Variables       │
│                 │    │                 │    │                 │
│ • File paths    │    │ • Language      │    │ • TEMP_DIR      │
│ • Model names   │    │   preferences   │    │ • MODEL_CACHE   │
│ • Output format │    │ • Output dir    │    │ • LOG_LEVEL     │
│                 │    │ • Batch sizes   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

*This architecture documentation provides the technical foundation for understanding, implementing, and maintaining the Multi-Agent Translation Semantic Drift Experiment system. Each component is designed for modularity, reliability, and academic excellence.*
