# Multi-Agent Translation Semantic Drift Experiment

## Table of Contents
- [Overview](#overview)
- [What is This Project?](#what-is-this-project)
- [Multi-Agent Architecture](#multi-agent-architecture)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Agent and Skill Descriptions](#agent-and-skill-descriptions)
- [Experiment Configuration](#experiment-configuration)
- [Understanding Results](#understanding-results)
- [Example Run](#example-run)

---

## Overview

This project demonstrates **multi-agent orchestration** with Claude Code to measure semantic drift caused by spelling errors across multiple language translations. It showcases how autonomous agents can communicate through files and coordinate complex workflows.

**Key Concept**: When text with spelling errors is translated through multiple languages (English → French → Italian → Spanish), how much does the semantic meaning change?

---

## What is This Project?

Imagine you have a sentence in English, but some words are misspelled. You translate it to French, then to Spanish, then to Hebrew. When you compare the final Hebrew translation back to the original English (using semantic embeddings), how different is the meaning?

This project **automates that entire process** using:
- **Multiple Claude agents** that work together autonomously
- **File-based communication** between agents
- **Python skills** for mathematical computations (embeddings, distances)
- **Translation skills** for language conversion

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
│   - Translates: French → Spanish        │
│   - Writes: /tmp/second_hop_translation.md│
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│   TRANSLATOR 3 AGENT                    │
│   - Reads: /tmp/second_hop_translation.md│
│   - Translates: Spanish → Hebrew        │
│   - Writes: /tmp/third_hop_translation.md│
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│   EMBEDDING ANALYZER AGENT              │
│   - Reads: original + final translation │
│   - Calls Python: compute_embeddings.py │
│   - Calls Python: measure_distance.py   │
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
   - **Translator 2**: Reads French file, translates to Spanish, saves to `/tmp/second_hop_translation.md`
   - **Translator 3**: Reads Spanish file, translates to Hebrew, saves to `/tmp/third_hop_translation.md`

4. **Semantic Analysis**:
   - **Embedding Analyzer** reads both original and final translation files
   - Calls `compute_embeddings.py` to convert text → vectors
   - Calls `measure_distance.py` to compute cosine distance
   - Reports the semantic drift

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
- Claude Code CLI
- Internet connection (for translation API)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `deep-translator` - Google Translate API wrapper
- `sentence-transformers` - Semantic embedding models
- `torch` - Deep learning framework (required by sentence-transformers)
- `numpy` - Numerical computations
- `scipy` - Distance calculations
- `matplotlib` - Visualization
- `transformers` - NLP utilities

### Step 2: Verify Installation

Test the translation library:
```bash
python -c "from deep_translator import GoogleTranslator; print('Translation: OK')"
```

Test the embeddings library:
```bash
python -c "from sentence_transformers import SentenceTransformer; print('Embeddings: OK')"
```

On first run, the embedding model (~90MB) will be downloaded automatically.

---

## Usage

### Method 1: Single Sentence Test

From within Claude Code:

```
Please run the translation drift experiment with this sentence:
"The quik brown fox jumps ovr the lazi dog"
```

Claude will automatically:
1. Activate the main orchestrator
2. Run the translation chain
3. Compute semantic distance
4. Report results

### Method 2: Batch Experiment (Multiple Typo Rates)

Create and run `experiment_runner.py`:

```python
"""
Run the full experiment with varying typo rates (20% to 50%)
"""
import subprocess
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Add skills to path
import sys
sys.path.append('.claude/skills/semantic_analysis')
from compute_embeddings import compute_embedding
from measure_distance import cosine_distance

# Original sentence
original = "The quick brown fox jumps over the lazy dog in the beautiful sunny park"

# Typo rates to test
typo_rates = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

# For demonstration: manually create typos at different rates
# In practice, you'd use the typo-injector skill or similar

results = {'rates': [], 'distances': []}

print("Running experiment with typo rates from 20% to 50%...")
print("="*60)

# Note: This is a simplified example
# Full implementation would call Claude agents for each iteration

print("\nExperiment complete! Check results_chart.png for visualization.")
```

### Method 3: Direct Python Script Execution

Test the Python skills directly:

```bash
# Compute embedding for a text
python .claude/skills/semantic_analysis/compute_embeddings.py "Hello world"

# Measure distance between two texts
python .claude/skills/semantic_analysis/measure_distance.py "Hello world" "שלום עולם"

# With verbose output
python .claude/skills/semantic_analysis/measure_distance.py \
    --file1 /tmp/original_sentence.txt \
    --file2 /tmp/third_hop_translation.md \
    --verbose
```

---

## Project Structure

```
.
├── .claude/
│   ├── main.claude                              # Main orchestrator agent
│   │
│   ├── agents/
│   │   ├── translator_1.claude                  # English → French
│   │   ├── translator_2.claude                  # French → Spanish
│   │   ├── translator_3.claude                  # Spanish → Hebrew
│   │   └── embedding_analyzer.claude            # Semantic distance analyzer
│   │
│   ├── skills/
│   │   ├── translate_language/
│   │   │   └── SKILL.md                         # Translation skill documentation
│   │   │
│   │   └── semantic_analysis/
│   │       ├── compute_embeddings.py            # Embedding computation (Python)
│   │       └── measure_distance.py              # Distance measurement (Python)
│   │
│   └── settings.local.json                       # Local settings
│
├── requirements.txt                              # Python dependencies
├── README.md                                     # This file
└── run_experiment.py                             # Optional batch runner

Temporary Files (created during execution):
├── /tmp/original_sentence.txt                    # Saved by main orchestrator
├── /tmp/first_hop_translation.md                 # Output of translator_1
├── /tmp/second_hop_translation.md                # Output of translator_2
└── /tmp/third_hop_translation.md                 # Output of translator_3
```

---

## Agent and Skill Descriptions

### Agents

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
- Translates French → Spanish using translate skill
- Writes Spanish translation to `/tmp/second_hop_translation.md`

**Input**: `/tmp/first_hop_translation.md`
**Output**: `/tmp/second_hop_translation.md`

**Tools**: Read, Skill (translate), Write

---

#### 4. Translator 3 (`agents/translator_3.claude`)
**Purpose**: Third and final hop in translation chain

**Responsibilities**:
- Reads Spanish text from `/tmp/second_hop_translation.md`
- Translates Spanish → Hebrew using translate skill
- Writes Hebrew translation to `/tmp/third_hop_translation.md`

**Input**: `/tmp/second_hop_translation.md`
**Output**: `/tmp/third_hop_translation.md`

**Tools**: Read, Skill (translate), Write

---

#### 5. Embedding Analyzer (`agents/embedding_analyzer.claude`)
**Purpose**: Compute semantic drift

**Responsibilities**:
- Reads original English sentence from `/tmp/original_sentence.txt`
- Reads final Hebrew translation from `/tmp/third_hop_translation.md`
- Calls `compute_embeddings.py` for both texts
- Calls `measure_distance.py` to compute cosine distance
- Interprets and reports results

**Input**: `/tmp/original_sentence.txt`, `/tmp/third_hop_translation.md`
**Output**: Semantic distance value + interpretation

**Tools**: Read, Bash (to call Python scripts)

---

### Skills

#### 1. Translation Skill (`skills/translate_language/SKILL.md`)
**Purpose**: Translate text between languages

**Technology**: Uses `deep-translator` library (Google Translate API)

**Capabilities**:
- Supports 100+ languages
- Handles text with spelling errors
- Works with UTF-8 encoding (Hebrew, Arabic, Chinese, etc.)

**Usage**: Invoked by translator agents

**Important**: Requires internet connection

---

#### 2. Compute Embeddings (`skills/semantic_analysis/compute_embeddings.py`)
**Purpose**: Convert text to semantic vector representation

**Technology**: Uses `sentence-transformers` library with `all-MiniLM-L6-v2` model

**Input**: Text string (any language)
**Output**: 384-dimensional vector (normalized)

**CLI Usage**:
```bash
python compute_embeddings.py "Your text here"
python compute_embeddings.py --file input.txt --output embedding.json
```

**What it does**:
- Converts text into a mathematical vector
- Captures semantic meaning (not just words)
- Normalized vectors enable distance comparison

---

#### 3. Measure Distance (`skills/semantic_analysis/measure_distance.py`)
**Purpose**: Compute semantic distance between two texts or embeddings

**Technology**: Uses cosine distance formula from `scipy`

**Input**: Two text strings or embedding files
**Output**: Distance value (0-2 scale)

**CLI Usage**:
```bash
python measure_distance.py "Text 1" "Text 2"
python measure_distance.py --file1 text1.txt --file2 text2.txt --verbose
python measure_distance.py --embedding1 emb1.json --embedding2 emb2.json
```

**Distance Scale**:
- **0.0 - 0.2**: Minimal drift (excellent preservation)
- **0.2 - 0.4**: Low drift (good preservation)
- **0.4 - 0.6**: Moderate drift (acceptable)
- **0.6 - 0.8**: High drift (significant change)
- **0.8+**: Severe drift (meaning largely lost)

---

## Experiment Configuration

### Current Setup

- **Original Language**: English
- **Translation Chain**: English → French → Spanish → Hebrew
- **Typo Rates Tested**: 20%, 25%, 30%, 35%, 40%, 45%, 50% (7 data points)
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Distance Metric**: Cosine distance

### Customization Options

#### Change Translation Languages

Edit the agent files to use different language codes:
- `en` = English
- `fr` = French
- `es` = Spanish
- `he` = Hebrew
- `de` = German
- `ja` = Japanese
- `zh` = Chinese
- `ar` = Arabic
- `ru` = Russian

Example: For English → German → Italian → Japanese:
- Modify translator_1: `en` → `de`
- Modify translator_2: `de` → `it`
- Modify translator_3: `it` → `ja`

#### Change Number of Hops

To add a 4th translation hop:
1. Create `agents/translator_4.claude` (copy and modify translator_3)
2. Update translator_3 to write to `/tmp/third_hop_translation.md` instead of final
3. Update translator_4 to read from translator_3 and write to `/tmp/fourth_hop_translation.md`
4. Update embedding_analyzer to read from translator_4's output

#### Change Typo Rates

Modify the typo rates list in your experiment runner:
```python
typo_rates = [0.10, 0.20, 0.30, 0.40, 0.50]  # Example: 10% to 50%
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

After running the experiment:

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

## Example Run

### Input

```
User: "Please analyze this sentence with 25% typos: 'The quik browwn fox jmps ovr the lazi dg'"
```

### Execution Flow

```
Main Orchestrator:
  ✓ Saved original sentence to /tmp/original_sentence.txt
  ✓ Launching translator_1...

Translator 1 (English → French):
  ✓ Received: "The quik browwn fox jmps ovr the lazi dg"
  ✓ Translated: "Le renard brun rapide saute sur le chien paresseux"
  ✓ Written to /tmp/first_hop_translation.md

Translator 2 (French → Spanish):
  ✓ Read from /tmp/first_hop_translation.md
  ✓ Translated: "El zorro marrón rápido salta sobre el perro perezoso"
  ✓ Written to /tmp/second_hop_translation.md

Translator 3 (Spanish → Hebrew):
  ✓ Read from /tmp/second_hop_translation.md
  ✓ Translated: "השועל החום המהיר קופץ מעל הכלב העצלן"
  ✓ Written to /tmp/third_hop_translation.md

Embedding Analyzer:
  ✓ Computing embeddings...
  ✓ Original: [384-dim vector]
  ✓ Final: [384-dim vector]
  ✓ Distance: 0.3542

========================================
SEMANTIC DRIFT ANALYSIS
========================================

Original Sentence (English):
"The quik browwn fox jmps ovr the lazi dg"

Final Translation (Hebrew):
"השועל החום המהיר קופץ מעל הכלב העצלן"

Semantic Distance: 0.3542

Interpretation:
Result: Low drift (good preservation)

The translation chain successfully preserved
the core meaning despite 25% spelling errors.
========================================
```

---

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'deep_translator'**
```bash
pip install deep-translator
```

**2. Translation API Errors / Rate Limiting**
- Wait a few seconds between requests
- Check internet connection
- Google Translate API is free but has rate limits

**3. Hebrew Text Appears Garbled**
- Ensure your terminal supports UTF-8 encoding
- Use a font that includes Hebrew characters (Arial, Courier New)
- Check that files are saved with UTF-8 encoding

**4. Model Download Delays**
- First run downloads the embedding model (~90MB)
- This happens once; subsequent runs are fast
- Ensure stable internet connection

**5. File Not Found: /tmp/...**
- Ensure agents ran in sequence
- Check that each agent completed successfully
- On Windows, files may be in `C:\tmp\` instead of `/tmp/`

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

### Research Questions

- How do spelling errors affect semantic drift?
- Is the relationship linear or non-linear?
- Do different language chains show different patterns?
- At what typo rate does meaning break down completely?

### Extensions

Possible project extensions:
- Test different language chains (e.g., English → Chinese → Arabic → Russian)
- Compare different embedding models (e.g., multilingual-BERT)
- Add more translation hops (4, 5, 6 hops)
- Inject different types of errors (grammar, punctuation, word order)
- Create visualization dashboards with real-time updates

---

## License

This is an academic assignment project for "LLMs and Multi-Agent Orchestration" course.
Feel free to use and modify for educational purposes.

---

## Author

Created as part of the MLDS program assignment on multi-agent systems.

**Key Takeaway**: This project shows how Claude Code can orchestrate complex, multi-step workflows using autonomous agents that communicate through files. The separation between coordination (agents), translation (skills), and computation (Python) creates a modular, maintainable system.

---

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Test translation
python -c "from deep_translator import GoogleTranslator; print(GoogleTranslator(source='en', target='fr').translate('Hello world'))"

# Test embeddings
python .claude/skills/semantic_analysis/compute_embeddings.py "Test sentence"

# Test distance measurement
python .claude/skills/semantic_analysis/measure_distance.py "Hello world" "Bonjour le monde" --verbose

# Run within Claude Code
# Just ask Claude: "Run the translation drift experiment with this sentence: [your sentence]"
```

---

**Happy experimenting! 🚀**
