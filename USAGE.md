# Quick Start Guide

## Architecture Overview

This system analyzes semantic drift through multi-hop translation with spelling errors.

### Translation Chain
**English → French → Italian → English** (3 hops, ends back in English)

### Key Components

1. **Claude Agents** (handle translations):
   - `translator_1.claude`: English → French
   - `translator_2.claude`: French → Italian
   - `translator_3.claude`: Italian → English

2. **Python Script** (ONLY for math):
   - `calculate_distance.py`: Computes embeddings and distance
   - **Does NOT handle translation**

3. **Main Orchestrator** (`main.claude`):
   - Coordinates all agents
   - Manages file communication
   - Generates reports and graphs

---

## Modes of Operation

### Ad-hoc Mode (Single Sentence)
**When to use**: You want to analyze a single sentence

**How to trigger**: Provide a sentence directly

**Example**:
```
"Analyze: The quik brown fox jumps ovr the lazi dog"
"Translate this sentence: Hello world, how are you today?"
```

**What happens**:
1. Orchestrator saves your sentence to `tmp/original_sentence.txt`
2. Launches translator_1 → saves to `tmp/first_hop_translation.md`
3. Launches translator_2 → saves to `tmp/second_hop_translation.md`
4. Launches translator_3 → saves to `tmp/third_hop_translation.md`
5. Launches embedding-analyzer → calculates semantic distance
6. Shows you the results immediately

**Output**:
- Original sentence
- Translation chain (EN→FR→IT→EN)
- Final English translation
- Semantic distance value
- Interpretation (low/medium/high drift)

---

### Automated Mode
**When to use**: Systematic testing across multiple typo rates with comprehensive analysis

**How to trigger**: Use keywords like:
- "Run automated experiment"
- "Test 20-50% typo rates"
- "Batch experiment"

**Requirements**:
- Sentences: >15 words each
- Typo rates: 20%, 25%, 30%, 35%, 40%, 45%, 50%
- Samples: 3 sentences per typo rate (21 total sentences)

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
"Analyze: 'The quik brown fox jumps ovr the lazi dog in the beatiful park'"
```

Multiple sentences:
```
"Analyze these sentences:
1. 'The quik brown fox jumps ovr the lazi dog'
2. 'Th qck brwn fx jmps vr th lz dg'
3. 'The kwik brwn foks jmps ovr the lasy dg'"
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
- **Tool**: Google Translate API (via deep-translator)
- **Handler**: Claude agents (NOT Python)
- **Rate limiting**: 0.5s between calls

### Embeddings
- **Model**: all-MiniLM-L6-v2 (sentence-transformers)
- **Dimensions**: 384
- **Distance metric**: Cosine distance
- **Range**: 0 (identical) to 2 (opposite)

### Graph Generation
- **Library**: matplotlib
- **Format**: PNG (300 DPI)
- **Style**: Scatter plot with trend line

---

## Common Issues

### "Translation Failed"
- Check internet connection
- Google Translate may have rate limits
- Wait a few seconds and retry

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
MAIN ORCHESTRATOR (.claude/main.claude)
    ↓
[Detects mode: Manual or Automated]
    ↓
┌─────────────────────────────────────┐
│  FOR EACH SENTENCE:                 │
│                                     │
│  1. Save to tmp/original_sentence.txt│
│  2. Launch translator_1 (EN→FR)     │
│  3. Launch translator_2 (FR→IT)     │
│  4. Launch translator_3 (IT→EN)     │
│  5. Call Python calculate_distance  │
│  6. Record result                   │
└─────────────────────────────────────┘
    ↓
GENERATE REPORT + GRAPH
    ↓
PRESENT RESULTS TO USER
```

---

**Remember**: Translation = Claude Agents | Math = Python Script
