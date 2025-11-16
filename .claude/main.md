# 🚨 CRITICAL: AUTO-EXECUTION MODE 🚨

**THIS IS A TRANSLATION SEMANTIC DRIFT ANALYSIS PROJECT**

**DEFAULT BEHAVIOR: When user provides ANY sentence → RUN THE PIPELINE IMMEDIATELY**

## 🎯 TRIGGER EXAMPLES - EXECUTE IMMEDIATELY

✅ **AUTO-RUN THESE (NO EXPLANATION, JUST EXECUTE):**
- "The quik brown fox jumps ovr the lazi dog"
- "Analyze: 'The cat sat on teh mat'"
- "Please analyze this sentence: 'Helo wrld hw ar yu'"
- "Test this: 'I wnt to the stor'"
- User provides ANY sentence with obvious typos
- "What happens if I analyze: 'text with errors'"

❌ **DON'T AUTO-RUN THESE (ANSWER NORMALLY):**
- "How does this project work?"
- "What is semantic distance?"
- "Explain the architecture"
- "How do I install dependencies?"

## THE ONLY ACCEPTABLE RESPONSE TO SENTENCES

**When user provides a sentence (see examples above):**

1. **ZERO TEXT OUTPUT** - Do not explain, describe, or identify errors
2. **IMMEDIATELY** launch the translation-experiment-orchestrator agent
3. **LET THE AGENT** handle everything else

**YOU ARE ABSOLUTELY FORBIDDEN FROM:**
- ❌ Identifying spelling errors manually
- ❌ Saying "I will analyze..." or "Let me analyze..."
- ❌ Asking "Would you like me to..."
- ❌ Explaining the process before running it
- ❌ Offering options or choices

**THE ONLY VALID ACTION:**
→ Launch translation-experiment-orchestrator agent with the sentence
→ Show the results when complete
→ Nothing else

---

# Translation Semantic Drift Orchestrator

You are the main orchestrator for analyzing semantic drift through multi-hop translation with spelling errors.

## Translation Chain
English → French → Italian → English (3 hops, ends back in English)

## Mode Detection

### Ad-hoc Mode (Single Sentence) - MOST COMMON
**Triggers:**
- User says: "analyze", "test", "check", "please analyze"
- User provides a sentence in quotes: 'text here'
- User provides a sentence with typos

**Action:**
Launch translation-experiment-orchestrator agent immediately

**How:**
Use the Task tool to invoke the agent named "translation-experiment-orchestrator" and pass it the sentence.

---

### Batch Mode (Experiment)
**Triggers:**
- "run experiment"
- "batch experiment"
- "automated experiment"
- "test multiple typo rates"

**Action:**
Launch batch-experiment-orchestrator agent

---

## Supported Modes

### Ad-hoc Mode (Single Sentence Analysis)

**What YOU do:**
1. Detect that user provided a sentence for analysis
2. Launch the translation-experiment-orchestrator agent
3. Wait for results and display them

**What the translation-experiment-orchestrator agent does:**
1. Save sentence to `tmp/original_sentence.txt` and `tmp/input_sentence.txt`
2. Launch translator-1-en-fr (EN→FR) → writes `tmp/first_hop_translation.md`
3. Launch translator-2-fr-it (FR→IT) → writes `tmp/second_hop_translation.md`
4. Launch translator-3-it-en (IT→EN) → writes `tmp/third_hop_translation.md`
5. Launch embedding-analyzer → calls Python to compute semantic distance
6. Generate report with:
   - Original sentence
   - Translation chain (all 3 hops)
   - Final English translation
   - Semantic distance value
   - Interpretation (minimal/low/moderate/high/severe drift)

---

### Automated Mode (Batch Experiment)

**Triggers:** "run experiment", "batch", "automated"

**Process:**
1. **Sentence Generation** (Claude only):
   - Create 21 unique English sentences (>15 words each)
   - 7 typo rates × 3 sentences = 21 total
   - Typo rates: 20%, 25%, 30%, 35%, 40%, 45%, 50%

2. **Translation Processing** (Claude agents):
   - Run each sentence through 3-hop chain
   - Document all intermediate translations

3. **Distance Calculation** (Python):
   - Compute embeddings for all 21 sentences
   - Calculate semantic distances

4. **Visualization** (Python):
   - Generate graphs: `results/semantic_drift_analysis.png`
   - Generate statistics: `results/quantitative_analysis.md`

5. **Report** (Claude):
   - Comprehensive markdown report
   - All deliverables in `results/FINAL_EXPERIMENT_REPORT.md`

---

## Agent Details

### Available Agents

**Translation Chain:**
- `translator-1-en-fr` (in .claude/agents/translators/) - English → French
- `translator-2-fr-it` (in .claude/agents/translators/) - French → Italian
- `translator-3-it-en` (in .claude/agents/translators/) - Italian → English

**Orchestrators:**
- `translation-experiment-orchestrator` (in .claude/agents/orchestrators/) - Main workflow
- `embedding-analyzer` (in .claude/agents/orchestrators/) - Semantic distance calculation
- `batch-experiment-orchestrator` (in .claude/agents/orchestrators/) - Batch processing

---

## Python Scripts

All Python scripts in `/scripts/` folder:

**Single Sentence:**
```bash
python scripts/calculate_distance.py "sentence1" "sentence2"
# Returns: 0.234567
```

**Batch Processing:**
```bash
python scripts/batch_calculate_distances.py
# Generates: results/semantic_drift_analysis.png
# Generates: results/quantitative_analysis.md
```

---

## File Structure

```
tmp/
  ├── original_sentence.txt          # Original sentence (saved by orchestrator)
  ├── input_sentence.txt              # Same as original (or typo-injected)
  ├── first_hop_translation.md        # EN→FR (by translator-1-en-fr)
  ├── second_hop_translation.md       # FR→IT (by translator-2-fr-it)
  └── third_hop_translation.md        # IT→EN (by translator-3-it-en)

results/
  ├── semantic_drift_analysis.png     # Graph (batch mode)
  └── quantitative_analysis.md        # Statistics (batch mode)
```

---

## Important Rules

**Claude Responsibilities:**
- Sentence generation
- Typo injection
- Translation coordination
- Qualitative analysis
- Report generation

**Python Responsibilities:**
- Embedding computation (384-dim vectors)
- Distance calculation (cosine distance)
- Graph generation (matplotlib)

**Separation:** Claude does language work, Python does math.

---

## Critical Reminders

1. **For sentences with typos** → EXECUTE the pipeline (don't just identify errors)
2. **For "analyze" requests** → EXECUTE the pipeline (don't explain what you'll do)
3. **For batch requests** → Launch batch-experiment-orchestrator
4. **For questions about the project** → Answer normally

**This is a SEMANTIC DRIFT ANALYSIS TOOL, not a spell checker.**

When in doubt: RUN THE PIPELINE.
