# Usage Guide

## Overview

This system analyzes semantic drift through multi-hop translation with spelling errors using a multi-agent architecture.

### Translation Chain
**English → French → Italian → English** (3 hops, ends back in English)

### Key Components

1. **Main Orchestrator** ([.claude/main.md](.claude/main.md)):
   - Detects user intent (ad-hoc vs batch mode)
   - Launches appropriate agents
   - Coordinates workflow

2. **Translation Agents**:
   - [translator-1-en-fr](.claude/agents/translators/translator-1-en-fr.md): English → French
   - [translator-2-fr-it](.claude/agents/translators/translator-2-fr-it.md): French → Italian
   - [translator-3-it-en](.claude/agents/translators/translator-3-it-en.md): Italian → English

3. **Orchestrator Agents**:
   - [translation-experiment-orchestrator](.claude/agents/orchestrators/translation-experiment-orchestrator.md): Manages single/batch experiments
   - [embedding-analyzer](.claude/agents/orchestrators/embedding-analyzer.md): Computes semantic distance

4. **Python Scripts** (ONLY for embeddings and math):
   - `scripts/calculate_distance.py`: Computes embeddings and distance
   - `scripts/batch_calculate_distances.py`: Batch processing and visualization
   - **Does NOT handle translation or typo injection**

---

## Modes of Operation

### Ad-hoc Mode (Single Sentence)
**When to use**: Analyze a specific sentence

**How to trigger**:
```
Please execute the pipeline on the sentence: 'The quik brown fox jumps ovr the lazi dog'
```

**What happens automatically**:
1. Main orchestrator detects the request
2. Launches translation-experiment-orchestrator agent
3. That agent:
   - Saves sentence to `tmp/original_sentence.txt` and `tmp/input_sentence.txt`
   - Launches translator-1-en-fr → writes `tmp/first_hop_translation.md`
   - Launches translator-2-fr-it → writes `tmp/second_hop_translation.md`
   - Launches translator-3-it-en → writes `tmp/third_hop_translation.md`
   - Launches embedding-analyzer → calculates semantic distance via Python
4. Results displayed immediately

**Output**:
- Original sentence
- Translation chain (EN→FR→IT→EN)
- Final English translation
- Semantic distance value (0-2 range)
- Interpretation (minimal/low/moderate/high/severe drift)

---

### Batch/Automated Mode
**When to use**: Systematic testing across multiple typo rates with statistical analysis

**How to trigger**:
```
Run automated experiment
```
or
```
Run batch experiment
```

**Configuration**:
- Sentences: >15 words each
- Typo rates: 20%, 25%, 30%, 35%, 40%, 45%, 50% (7 levels)
- Samples: 3 sentences per typo rate = 21 total sentences

**What happens** (Step-by-step):

**Phase 1: Sentence Generation (Claude Only - NO Python)**
1. Claude creates 21 unique English sentences (>15 words)
2. Claude manually introduces typos at specified rates
3. For each sentence:
   - Original version documented
   - Typo-injected version created
   - Word count calculated
   - Typo count calculated
   - Percentage verified

**Phase 2: Translation Processing (Claude Agents)**
3. For each of the 21 sentences:
   - Run through translator_1 (EN→FR)
   - Run through translator_2 (FR→IT)
   - Run through translator_3 (IT→EN)
   - Document all intermediate translations
   - Note qualitative observations (drift, meaning changes)

**Phase 3: Report Generation (Claude Only)**
4. Create comprehensive markdown report containing:
   - Structured table: all 21 sentences with complete stats
   - Typo level analysis: average stability per rate
   - Conceptual graph description
   - Qualitative insights and patterns
   - ALL in ONE consolidated file

**Phase 4: Quantitative Analysis (Python - FINAL STEP ONLY)**
5. After report is complete:
   - Call Python to calculate embedding distances (21 calculations)
   - Generate quantitative graph (matplotlib)
   - Append numerical data to report

**Output**:
- Single comprehensive report with qualitative AND quantitative data
- Graph embedded in report
- Statistical tables
- Agent descriptions
- Semantic drift analysis

---

## Architecture: Claude vs Python

### What Claude Does (LLM Capabilities)

**Sentence Creation:**
- Generate original English sentences (>15 words)
- Create varied content (science, daily life, technology, nature)
- Ensure grammatical correctness and semantic richness

**Typo Injection:**
- Manually introduce spelling errors at precise rates (20%-50%)
- Strategic placement (not all consecutive)
- Character-level modifications (substitution, deletion, transposition)
- Manual counting and verification

**Translation:**
- Coordinate translator agents (translator_1, translator_2, translator_3)
- Handle file-based communication between agents
- Extract and document intermediate translations

**Qualitative Analysis:**
- Observe semantic drift patterns
- Note meaning preservation or loss
- Identify translation artifacts
- Describe qualitative trends

**Report Writing:**
- Create structured markdown reports
- Build comprehensive tables
- Write conceptual graph descriptions
- Synthesize insights and conclusions

### What Python Does (Mathematical Computation)

**Embedding Calculation:**
```python
# sentence-transformers library
embedding = model.encode(sentence)  # 384-dim vector
```

**Distance Measurement:**
```python
# Cosine distance calculation
distance = 1 - cosine_similarity(emb1, emb2)
```

**Graph Generation:**
```python
# matplotlib visualization
plt.plot(typo_rates, distances)
plt.savefig('graph.png')
```

### Why This Separation?

**Claude's Strengths:**
- Natural language generation
- Context understanding
- Qualitative reasoning
- Report synthesis

**Python's Strengths:**
- Numerical precision
- Matrix operations
- Statistical computation
- Data visualization

---

## File Structure

### Input/Output Files
```
tmp/
  ├── original_sentence.txt          # Original clean sentence
  ├── input_sentence.txt              # Typo-injected variant
  ├── first_hop_translation.md        # English → French
  ├── second_hop_translation.md       # French → Italian
  └── third_hop_translation.md        # Italian → English

results/
  ├── manual_report.md                # Manual mode results
  ├── automated_report.md             # Automated mode results
  └── semantic_drift_graph.png        # Graph (automated only)
```

---

## Example Commands

### Manual Mode Examples

Single sentence:
```
"Please execute the pipeline on the sentence: 'The quik brown fox jumps ovr the lazi dog in the beatiful park'"
```

Multiple sentences (execute them one by one):
```
"Please execute the pipeline on the sentence: 'The quik brown fox jumps ovr the lazi dog'"
"Please execute the pipeline on the sentence: 'Th qck brwn fx jmps vr th lz dg'"
"Please execute the pipeline on the sentence: 'The kwik brwn foks jmps ovr the lasy dg'"
```

### Automated Mode Examples

Default experiment:
```
"Run automated experiment"
```

Custom typo range:
```
"Run automated experiment with typo rates from 0% to 50%"
```

---

## Understanding Results

### Semantic Distance Interpretation
- **0.0 - 0.3**: Low drift (meaning well preserved)
- **0.3 - 0.6**: Moderate drift (some semantic change)
- **0.6 - 2.0**: High drift (significant meaning change)

### What affects distance?
1. **Typo rate**: More typos → more ambiguity → larger drift
2. **Translation chain**: Each hop adds cumulative error
3. **Word importance**: Typos in key words have bigger impact
4. **Language pairs**: Some languages preserve meaning better

---

## Deliverables (Auto-Generated)

### Both modes provide:
✅ Original and typo-injected sentences
✅ Sentence lengths (word count)
✅ Agent skill descriptions
✅ Vector distances

### Automated mode additionally provides:
✅ Graph (typo % vs distance)
✅ Statistical analysis (per typo rate)
✅ Trend analysis

---

## Technical Details

### Translation
- **Handler**: Claude's native multilingual capabilities via translate skill
- **Languages**: English, French, Italian (extensible to others)
- **Method**: Direct translation by Claude agents (no external API)

### Embeddings
- **Model**: all-MiniLM-L6-v2 (sentence-transformers)
- **Dimensions**: 384
- **Distance metric**: Cosine distance
- **Range**: 0 (identical) to 2 (opposite)
- **Handled by**: Python scripts only

### Graph Generation
- **Library**: matplotlib
- **Format**: PNG
- **Types**: Scatter plots, box plots, histograms
- **Generated by**: `scripts/batch_calculate_distances.py`

---

## Common Issues

### Translation Issues
- Claude's translate skill should handle most cases
- If translation seems incorrect, the agent may need clearer instructions
- Check that the translate skill is available in .claude/skills/

### "Module not found"
- Run: `pip install -r requirements.txt`
- Ensure you're in the project directory

### "File not found: tmp/..."
- Agents must run in sequence
- Check that tmp/ directory exists
- Review agent outputs for errors

---

## Quick Reference

**Want to test one sentence?**
→ Use Manual Mode

**Want to see how typo rate affects meaning?**
→ Use Automated Mode

**Need the graph?**
→ Use Automated Mode (manual doesn't generate graphs)

**Need statistics across many runs?**
→ Use Automated Mode

**Want to test specific error patterns?**
→ Use Manual Mode (craft your own typos)

---

## Architecture Summary

```
USER REQUEST
    ↓
MAIN ORCHESTRATOR (.claude/main.md)
    ↓
[Detects mode: Ad-hoc or Batch]
    ↓
TRANSLATION-EXPERIMENT-ORCHESTRATOR
    ↓
┌─────────────────────────────────────┐
│  FOR EACH SENTENCE:                 │
│                                     │
│  1. Save to tmp/original_sentence.txt│
│  2. Launch translator-1-en-fr       │
│  3. Launch translator-2-fr-it       │
│  4. Launch translator-3-it-en       │
│  5. Launch embedding-analyzer       │
│     → Calls Python for distance     │
│  6. Record result                   │
└─────────────────────────────────────┘
    ↓
GENERATE REPORT
(+ GRAPH for batch mode)
    ↓
PRESENT RESULTS TO USER
```

---

**Key Principle**:
- Translation & Orchestration = Claude Agents
- Embeddings & Distance Math = Python Scripts
