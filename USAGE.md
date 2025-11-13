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

### Manual Mode
**When to use**: You have specific sentences with typos to analyze

**How to trigger**: Provide your sentences directly

**Example**:
```
"Analyze this sentence: 'The quik brown fox jumps ovr the lazi dog in the beatiful park'"
```

**What happens**:
1. Orchestrator saves your sentence
2. Runs it through 3 translator agents
3. Calls Python to calculate distance
4. Generates report with results

**Output**:
- Individual sentence analysis
- Vector distance for each
- Agent skill descriptions
- Summary statistics

---

### Automated Mode
**When to use**: Test systematic experiments across multiple typo rates

**How to trigger**: Use keywords like:
- "Run automated experiment"
- "Test 0-50% typo rates"
- "Batch experiment"

**What happens**:
1. System generates base sentence
2. Creates typo-injected variants (0%, 10%, 20%, 25%, 30%, 35%, 40%, 45%, 50%)
3. For each typo rate:
   - Generates 3 different sentences
   - Runs each through translation chain
   - Calculates distances
4. Aggregates statistics
5. Generates graph and report

**Output**:
- Comprehensive data table
- Graph: Typo % vs Distance
- Statistical analysis (avg, min, max, std)
- Agent descriptions
- Consolidated report

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
