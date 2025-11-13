# Multi-Agent Translation Semantic Drift Experiment

## Table of Contents
- [Overview](#overview)
- [What is This Project?](#what-is-this-project)
- [Multi-Agent Architecture](#multi-agent-architecture)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Experiment Types](#experiment-types)
  - [User Input Experiments](#user-input-experiments)
  - [Automated Experiments](#automated-experiments)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Agent and Skill Descriptions](#agent-and-skill-descriptions)
- [Experiment Configuration](#experiment-configuration)
- [Understanding Results](#understanding-results)
- [Example Runs](#example-runs)

---

## Overview

This project demonstrates **multi-agent orchestration** with semantic drift measurement caused by spelling errors across multiple language translations. It showcases how autonomous agents can communicate through files and coordinate complex workflows.

**Key Concept**: When text with spelling errors is translated through multiple languages and back to English (English → French → Italian → English), how much does the semantic meaning change compared to the original?

---

## What is This Project?

Imagine you have a sentence in English, but some words are misspelled. You translate it to French, then to Italian, then back to English. When you compare the final English translation to the original English (using semantic embeddings), how different is the meaning?

This project **automates that entire process** using:
- **Multiple Claude agents** that handle translations autonomously
- **File-based communication** between agents
- **Python scripts** ONLY for mathematical computations (embeddings, distances)
- **Claude translation skills** for language conversion (NOT Python)

The result is a measurement of **semantic drift** - how far the meaning has drifted from the original.

---

## Multi-Agent Architecture

### Conceptual Flow

```
User provides sentence with typos
        ↓
┌─────────────────────────────────────────┐
│   MAIN ORCHESTRATOR AGENT               │
│   - Saves original sentence             │
│   - Coordinates the workflow            │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│   TRANSLATOR 1 AGENT                    │
│   - Translates: English → French        │
│   - Writes: /tmp/first_hop_translation.md│
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│   TRANSLATOR 2 AGENT                    │
│   - Reads: /tmp/first_hop_translation.md │
│   - Translates: French → Italian        │
│   - Writes: /tmp/second_hop_translation.md│
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│   TRANSLATOR 3 AGENT                    │
│   - Reads: /tmp/second_hop_translation.md│
│   - Translates: Italian → English       │
│   - Writes: /tmp/third_hop_translation.md│
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│   ORCHESTRATOR (calls Python)           │
│   - Reads: original + final translation │
│   - Calls: python calculate_distance.py│
│   - Python computes embeddings & distance│
│   - Reports semantic distance           │
└─────────────────────────────────────────┘
        ↓
   Result displayed to user
```

### Key Design Principles

1. **Agent Autonomy**: Each agent operates independently
2. **File-Based Communication**: Agents write/read from standardized file locations
3. **Separation of Concerns**: Translation logic in agents/skills, math computations in Python
4. **Sequential Workflow**: Each step completes before the next begins
5. **Clear Handoffs**: Output of one agent is input to the next

---

## How It Works

### Step-by-Step Process

1. **User Input**: Provide an English sentence (may contain spelling errors)
   - Example: "The quik brown fox jumps ovr the lazi dog"

2. **Main Orchestrator**:
   - Saves the original sentence to `/tmp/original_sentence.txt`
   - Invokes translator_1 agent

3. **Translation Chain**:
   - **Translator 1**: Reads English, translates to French, saves to `/tmp/first_hop_translation.md`
   - **Translator 2**: Reads French file, translates to Italian, saves to `/tmp/second_hop_translation.md`
   - **Translator 3**: Reads Italian file, translates back to English, saves to `/tmp/third_hop_translation.md`

4. **Semantic Analysis**:
   - **Orchestrator** reads both original and final translation files
   - Calls `python calculate_distance.py "original" "final"`
   - Python computes embeddings (text → 384-dim vectors)
   - Python calculates cosine distance between vectors
   - Orchestrator reports the semantic drift

5. **Result**: User sees a distance value (0 = identical, 2 = opposite meaning)

### Why This Architecture?

- **Modularity**: Each agent has a single responsibility
- **Scalability**: Easy to add more translation hops or change languages
- **Transparency**: File-based communication makes debugging easy
- **Reusability**: Agents and skills can be reused in other projects

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Claude Code CLI (for user input experiments)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `sentence-transformers` - Semantic embedding models
- `torch` - Deep learning framework (required by sentence-transformers)
- `numpy` - Numerical computations
- `scipy` - Distance calculations
- `matplotlib` - Visualization (for graphs)
- `transformers` - NLP utilities

### Step 2: Verify Installation

Test the embeddings library:
```bash
python -c "from sentence_transformers import SentenceTransformer; print('Embeddings: OK')"
```

On first run, the embedding model (~90MB) will be downloaded automatically.

---

## Experiment Types

This project supports two distinct experiment types: **User Input Experiments** and **Automated Experiments**.

### User Input Experiments

**Purpose**: Interactive testing with custom sentences containing spelling errors

**How it works**:
- User provides a sentence with typos directly to Claude Code
- Multi-agent system processes the sentence through translation chain
- Agents communicate via file-based messaging
- Results are analyzed and reported in real-time

**Best for**:
- Testing specific sentences
- Understanding how particular typos affect translation
- Interactive exploration of semantic drift
- Demonstrating multi-agent coordination

**Example**:
```
User: "Please analyze this sentence: 'The quik brown fox jumps ovr the lazi dog'"
Claude: [Activates multi-agent system, reports semantic distance]
```

**Translation Chain**: English → French → Italian → English

---

### Automated Experiments

**Purpose**: Systematic batch testing across multiple typo rates using Claude orchestration

**How it works**:
- Claude's `batch_experiment_orchestrator` agent runs autonomously
- Generates typos at different rates (25%, 30%, 35%, 40%, 45%, 50%)
- Runs complete translation chain for each typo rate (3 iterations per rate = 18 total)
- Produces statistical analysis and comprehensive reports
- All orchestration handled by Claude agents, not Python scripts

**Best for**:
- Scientific analysis of typo rate vs semantic drift
- Multi-agent system demonstration
- Systematic experimental methodology
- Comprehensive statistical reporting

**Example**:
```
User: "Run the batch experiment"
Claude: [Executes 18 translation chains, produces summary report]
```

**Translation Chain**: English → French → Italian → English

**Output Files**:
- `results/batch_experiment_summary.md` - Comprehensive analysis report
- Statistical tables, trends, and individual run details
- All generated by Claude agents using file-based communication

---

## Usage

### Method 1: User Input Experiments (Interactive)

**Using Claude Code CLI:**

```
Please run the translation drift experiment with this sentence:
"The quik brown fox jumps ovr the lazi dog"
```

Claude will automatically:
1. Activate the main orchestrator
2. Run the translation chain through multiple agents
3. Compute semantic distance
4. Report results

**Example sentences to try**:
- `"The quik brown fox jumps ovr the lazi dog"` (25% typos)
- `"Th qk brwn fx jmps vr th lz dg"` (50% typos)
- `"Hello wrld, hw ar yu tday?"` (Different sentence structure)

### Method 2: Automated Experiments (Claude-Orchestrated Batch)

**Run the complete batch experiment:**
```
User: "Run the batch experiment"
```
or
```
User: "Run automated experiment with multiple typo rates"
```

This will:
- Test typo rates from 25% to 50% (6 data points)
- Generate 3 iterations per typo rate (18 total translation chains)
- Calculate comprehensive statistics (average, min, max, std dev per rate)
- Generate detailed markdown report
- All orchestration handled by Claude agents

**Customizing the automated experiment:**
To modify the experiment parameters, edit the batch_experiment_orchestrator agent file:
```
- Typo rates: Change from 25%-50% to your desired range
- Iterations: Modify number of sentences per rate
- Base sentence: Use different test sentences
- Translation languages: Modify the language chain
```

### Method 3: Direct Testing (Component Level)

Test individual components through Claude skills:

```
# Test typo injection skill
User: "Use the typo injector skill to add 25% typos to 'Hello world'"

# Test translation agents individually
User: "Translate 'Hello world' from English to French using translator_1"

# Test embedding analysis
User: "Calculate semantic distance between 'Hello world' and 'Bonjour le monde'"
```

**Note**: All component testing is done through Claude's skill system rather than direct Python calls.

---

## Project Structure

```
.
├── README.md                                     # This file
├── USAGE.md                                      # Quick start guide
├── requirements.txt                              # Python dependencies
├── calculate_distance.py                         # Semantic distance calculator (Python)
│
├── .claude/                                      # Multi-agent system (for user input)
│   ├── main.claude                               # Main orchestrator agent
│   │
│   ├── agents/
│   │   ├── translator_1.claude                   # English → French
│   │   ├── translator_2.claude                   # French → Italian
│   │   ├── translator_3.claude                   # Italian → Spanish
│   │   └── embedding_analyzer.claude             # Semantic distance analyzer
│   │
│   ├── skills/
│   │   ├── translate_language/
│   │   │   └── SKILL.md                          # Translation skill documentation
│   │   │
│   │   ├── typo-injector/
│   │   │   ├── typo_utils.py                     # Typo injection utilities
│   │   │   └── SKILL.md                          # Typo injection documentation
│   │   │
│   │   ├── embeddings/
│   │   │   ├── embedding_utils.py                # Embedding computation
│   │   │   └── SKILL.md                          # Embedding documentation
│   │   │
│   │   └── chart-generator/
│   │       ├── chart_utils.py                    # Visualization utilities
│   │       └── SKILL.md                          # Chart generation documentation
│   │
│   └── settings.local.json                       # Local settings
│
├── results/                                      # Experiment outputs
│   ├── experiment_summary.txt                    # Latest user input experiment
│   ├── semantic_analysis.md                      # Detailed analysis
│   ├── translation_flow.txt                      # Translation chain log
│   ├── semantic_drift_chart.png                  # Automated experiment chart
│   └── experiment_results.csv                    # Automated experiment data
│
└── tmp/                                          # Temporary files (created during execution)
    ├── original_sentence.txt                     # Saved by main orchestrator
    ├── first_hop_translation.md                  # Output of translator_1
    ├── second_hop_translation.md                 # Output of translator_2
    └── third_hop_translation.md                  # Output of translator_3
```

---

## Agent and Skill Descriptions

### Agents (For User Input Experiments)

#### 1. Main Orchestrator (`main.claude`)
**Purpose**: Coordinates the entire workflow

**Responsibilities**:
- Receives user input (English sentence with possible typos)
- Saves original sentence to file
- Invokes translator agents in sequence
- Calls embedding analyzer
- Reports final results

**Tools**: Task (to launch sub-agents), Write (to save files), Read

---

#### 2. Translator 1 (`agents/translator_1.claude`)
**Purpose**: First hop in translation chain

**Responsibilities**:
- Receives English text
- Translates English → French using translate skill
- Writes French translation to `/tmp/first_hop_translation.md`

**Input**: English text (direct from orchestrator)
**Output**: `/tmp/first_hop_translation.md`

**Tools**: Skill (translate), Write

---

#### 3. Translator 2 (`agents/translator_2.claude`)
**Purpose**: Second hop in translation chain

**Responsibilities**:
- Reads French text from `/tmp/first_hop_translation.md`
- Translates French → Italian using translate skill
- Writes Italian translation to `/tmp/second_hop_translation.md`

**Input**: `/tmp/first_hop_translation.md`
**Output**: `/tmp/second_hop_translation.md`

**Tools**: Read, Skill (translate), Write

---

#### 4. Translator 3 (`agents/translator_3.claude`)
**Purpose**: Third and final hop in translation chain - back to English

**Responsibilities**:
- Reads Italian text from `/tmp/second_hop_translation.md`
- Translates Italian → English using translate skill
- Writes English translation to `/tmp/third_hop_translation.md`

**Input**: `/tmp/second_hop_translation.md`
**Output**: `/tmp/third_hop_translation.md`

**Tools**: Read, Skill (translate), Write

---

#### 5. Python Distance Calculator (`calculate_distance.py`)
**Purpose**: Compute semantic distance between two sentences

**Responsibilities**:
- Receives two sentences as command-line arguments
- Computes 384-dimensional embeddings using sentence-transformers
- Calculates cosine distance between the embedding vectors
- Returns distance as a float (0-2 range)

**Input**: Two sentences via command line
**Output**: Float distance value (printed to stdout)

**Usage**: `python calculate_distance.py "sentence1" "sentence2"`

**Note**: This is a Python script, NOT a Claude agent. It's called by the orchestrator.

---

### Skills & Utilities

#### 1. Translation (`skills/translate/SKILL.md`)
**Purpose**: Translate text between languages

**Technology**: Uses Claude's native multilingual capabilities

**Capabilities**:
- Supports multiple languages
- Handles text with spelling errors gracefully
- Works with UTF-8 encoding (Hebrew, Arabic, Chinese, etc.)
- No external API calls required

**Usage**: Invoked by translator agents

---

#### 2. Typo Injection (`typo_utils.py`)
**Purpose**: Introduce spelling errors at specified rates

**Technology**: Random character substitution, deletion, insertion

**Input**: Clean text string, typo rate (0.0-1.0)
**Output**: Text with introduced spelling errors

**CLI Usage**:
```python
from typo_utils import introduce_typos
corrupted = introduce_typos("Hello world", typo_rate=0.25)
```

**Used by**: Automated experiments

---

#### 3. Embedding Computation (`embedding_utils.py`)
**Purpose**: Convert text to semantic vector representation

**Technology**: Uses `sentence-transformers` library with `all-MiniLM-L6-v2` model

**Input**: Text string (any language)
**Output**: 384-dimensional vector (normalized)

**Functions**:
- `compute_embedding(text)` - Single text to vector
- `cosine_distance(emb1, emb2)` - Distance between vectors

**What it does**:
- Converts text into a mathematical vector
- Captures semantic meaning (not just words)
- Normalized vectors enable distance comparison

---

#### 4. Visualization (`chart_utils.py`)
**Purpose**: Generate charts and save experimental results

**Technology**: Uses `matplotlib` for plotting

**Functions**:
- `plot_typo_vs_distance()` - Scatter plot with trend line
- `save_results_table()` - Export to CSV format

**Output**: PNG charts and CSV files

**Used by**: Automated experiments

---

## Experiment Configuration

### User Input Experiments Configuration

- **Original Language**: English
- **Translation Chain**: English → French → Italian → English
- **Input Method**: Direct user input to Claude Code
- **Typo Handling**: User provides pre-existing typos
- **Communication**: File-based agent messaging

### Automated Experiments Configuration

- **Original Language**: English
- **Translation Chain**: English → French → Italian → English
- **Typo Rates Tested**: 25%, 30%, 35%, 40%, 45%, 50% (6 data points)
- **Iterations per Rate**: 3 sentences (18 total translation chains)
- **Typo Generation**: Claude's typo-injector skill
- **Orchestration**: Claude batch_experiment_orchestrator agent
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Distance Metric**: Cosine distance

### Customization Options

#### Change Translation Languages

**For User Input Experiments**: Edit the agent files to use different language codes

**For Automated Experiments**: Edit the batch_experiment_orchestrator agent configuration:
```
# Modify the agent file to change:
- Translation chain languages
- Typo rates tested
- Number of iterations per rate
- Base sentence used for testing
```

#### Language Codes
- `en` = English, `fr` = French, `es` = Spanish, `he` = Hebrew
- `de` = German, `ja` = Japanese, `zh` = Chinese, `ar` = Arabic
- `ru` = Russian, `it` = Italian, `pt` = Portuguese

#### Change Number of Translation Hops

**For User Input**: Create additional translator agents
**For Automated**: Extend the `translation_chain` list

#### Modify Typo Rates (Automated Only)

Edit the batch_experiment_orchestrator agent:
```
Change: "Typo rates": 25%, 30%, 35%, 40%, 45%, 50%
To: "Typo rates": [your desired percentages]
```

---

## Understanding Results

### What is Semantic Distance?

Semantic distance measures how different two pieces of text are in meaning, not in words.

**Example**:
- "The cat sat on the mat" vs "A feline rested on the rug" = **Low distance** (similar meaning)
- "The cat sat on the mat" vs "The dog ran in the park" = **High distance** (different meaning)

### How Cosine Distance Works

1. **Text → Vector**: Each text is converted to a 384-dimensional vector
2. **Angle Measurement**: Cosine distance measures the angle between vectors
3. **Range**:
   - 0 = vectors point in same direction (identical meaning)
   - 1 = vectors are perpendicular (unrelated)
   - 2 = vectors point in opposite directions (opposite meaning)

### Interpreting Your Results

**Low Distance (< 0.3)**:
- Translation preserved meaning well
- Spelling errors had minimal impact
- The final text conveys the original intent

**Medium Distance (0.3 - 0.6)**:
- Some semantic drift occurred
- Spelling errors introduced ambiguity
- Core meaning partially preserved

**High Distance (> 0.6)**:
- Significant semantic drift
- Spelling errors severely impacted translation
- Final meaning diverged substantially

### Expected Patterns

Generally, you should observe:
1. **Positive correlation**: More typos → higher distance
2. **Non-linear growth**: Distance may increase faster at higher typo rates
3. **Language effects**: Some language pairs preserve meaning better than others

---

## Example Runs

### Example 1: User Input Experiment

**Input**:
```
User: "Please analyze this sentence with typos: 'The quik brown fox jumps ovr the lazi dog'"
```

**Execution Flow**:
```
Main Orchestrator:
  ✓ Saved original sentence to /tmp/original_sentence.txt
  ✓ Launching translator_1...

Translator 1 (English → French):
  ✓ Received: "The quik brown fox jumps ovr the lazi dog"
  ✓ Translated: "Le renard brun rapide saute par-dessus le chien paresseux"
  ✓ Written to /tmp/first_hop_translation.md

Translator 2 (French → Italian):
  ✓ Read from /tmp/first_hop_translation.md
  ✓ Translated: "La volpe marrone veloce salta sopra il cane pigro"
  ✓ Written to /tmp/second_hop_translation.md

Translator 3 (Italian → Spanish):
  ✓ Read from /tmp/second_hop_translation.md
  ✓ Translated: "El zorro marron rapido salta sobre el perro perezoso"
  ✓ Written to /tmp/third_hop_translation.md

Embedding Analyzer:
  ✓ Computing embeddings...
  ✓ Original: [384-dim vector]
  ✓ Final: [384-dim vector]
  ✓ Distance: 0.7996

========================================
SEMANTIC DRIFT ANALYSIS
========================================

Original Sentence (English):
"The quik brown fox jumps ovr the lazi dog"

Final Translation (Spanish):
"El zorro marron rapido salta sobre el perro perezoso"

Semantic Distance: 0.7996

Interpretation:
Result: High drift (significant semantic change)

The translation chain shows substantial semantic drift.
This reflects cross-lingual embedding differences and
the compound effect of multiple translation hops.
========================================
```

### Example 2: Automated Batch Experiment

**Command** (via Claude Code):
```
User: "Run automated experiment"
```

**Sample Output**:
```
================================================================================
MULTI-HOP TRANSLATION EXPERIMENT WITH SPELLING ERROR INJECTION
================================================================================

Original Sentence (17 words):
  'The quick brown fox jumps over the lazy dog in the beautiful sunny park'

Translation Chain:
  - English to French (en -> fr)
  - French to Spanish (fr -> es)
  - Spanish to Hebrew (es -> he)

Typo Rates: ['0%', '5%', '10%', '15%', '20%', '25%']

================================================================================

Executing experiment for each typo rate...
--------------------------------------------------------------------------------

[Typo Rate: 0%]
  Corrupted: 'The quick brown fox jumps over the lazy dog in the beautiful sunny park'
    English to French: 'Le renard brun rapide saute par-dessus le chien paresseux dans le beau parc ensoleillé'
    French to Spanish: 'El zorro marrón rápido salta sobre el perro perezoso en el hermoso parque soleado'
    Spanish to Hebrew: 'השועל החום המהיר קופץ מעל הכלב העצלן בפארק השמשי היפה'
  Semantic Distance: 0.2156

[Typo Rate: 5%]
  Corrupted: 'The quick brown fox jumpe over the lazy dog in the beautiful sunny park'
    English to French: 'Le renard brun rapide saute par-dessus le chien paresseux dans le beau parc ensoleillé'
    French to Spanish: 'El zorro marrón rápido salta sobre el perro perezoso en el hermoso parque soleado'
    Spanish to Hebrew: 'השועל החום המהיר קופץ מעל הכלב העצלן בפארק השמשי היפה'
  Semantic Distance: 0.2189

[...continues for all typo rates...]

================================================================================
EXPERIMENT COMPLETE
================================================================================

Generating visualizations and saving results...
  Chart saved: results/semantic_drift_chart.png
  Data saved: results/experiment_results.csv

================================================================================
SUMMARY STATISTICS
================================================================================

Semantic Distance Statistics:
  Minimum: 0.2156
  Maximum: 0.3421
  Average: 0.2734
  Range: 0.1265

  Drift Increase (0% to 25% typos): 0.1265 (58.7%)

================================================================================
KEY FINDINGS
================================================================================

  Pattern: Semantic distance increases monotonically with typo rate
  Largest semantic shift: Between 20% and 25% typo rates (+0.0542)
  Translation Chain: English -> French -> Italian -> English
  Each translation hop compounds the semantic drift from spelling errors
  Higher typo rates in the initial sentence lead to greater cumulative drift

================================================================================

Experiment complete!
  Chart: results/semantic_drift_chart.png
  Data: results/experiment_results.csv
```

---

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'sentence_transformers'**
```bash
pip install -r requirements.txt
```

**2. Translation Issues**
- Claude handles translation natively
- No external API or internet required for translation
- Only embeddings require model download (first run only)

**3. Model Download Delays**
- First run downloads the embedding model (~90MB)
- This happens once; subsequent runs are fast
- Ensure stable internet connection

**4. File Not Found: /tmp/...**
- Ensure agents ran in sequence
- Check that each agent completed successfully
- Verify tmp/ directory exists in project root

**5. Experiment Fails**
- Check Python path and dependencies
- Ensure `results/` directory is writable
- Verify all agents completed their tasks

---

## Academic Context

### Learning Objectives

This project demonstrates:
1. **Multi-agent orchestration**: Coordinating autonomous agents
2. **Inter-agent communication**: File-based message passing
3. **Separation of concerns**: Agents vs skills vs Python scripts
4. **NLP pipeline design**: Translation → embedding → analysis
5. **Semantic evaluation**: Using embeddings to measure quality
6. **Error propagation**: How noise compounds through transformations
7. **Experimental design**: User input vs automated batch testing

### Research Questions

- How do spelling errors affect semantic drift?
- Is the relationship linear or non-linear?
- Do different language chains show different patterns?
- At what typo rate does meaning break down completely?
- How do multi-agent systems compare to monolithic approaches?

### Extensions

Possible project extensions:
- Test different language chains (e.g., English → Chinese → Arabic → Russian)
- Compare different embedding models (e.g., multilingual-BERT)
- Add more translation hops (4, 5, 6 hops)
- Inject different types of errors (grammar, punctuation, word order)
- Create real-time visualization dashboards
- Implement error recovery mechanisms
- Add confidence scoring for translations

---

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Test embeddings
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); print('Embeddings: OK')"

# Test distance calculator
python calculate_distance.py "Hello world" "Bonjour monde"

# Run manual mode experiment (within Claude Code)
# Ask Claude: "Analyze this sentence: [your sentence with typos]"

# Run automated experiment (within Claude Code)
# Ask Claude: "Run automated experiment"
```

---

## License

This is an academic assignment project for "LLMs and Multi-Agent Orchestration" course.
Feel free to use and modify for educational purposes.

---

## Author

Created as part of the MLDS program assignment on multi-agent systems.

**Key Takeaway**: This project shows how multi-agent systems can handle complex, multi-step workflows with both interactive user input and automated batch processing. The separation between coordination (agents), translation (skills), computation (Python), and experimentation (automated scripts) creates a modular, maintainable system that supports both research and interactive exploration.

---

**Happy experimenting! 🚀**
