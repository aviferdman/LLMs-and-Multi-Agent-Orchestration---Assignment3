# 🚀 Quick Start Guide - Run the Project Yourself!

## ✅ Prerequisites Installed
- ✓ Python 3.12
- ✓ All dependencies installed (sentence-transformers, torch, numpy, scipy, matplotlib)

---

## 🎯 Interactive Mode - Test Your Own Sentences!

### Option 1: Simple Interactive Script (Recommended for Quick Testing)

Run the interactive analyzer:

```bash
python3 run_interactive.py
```

**What it does:**
1. You input an original sentence
2. You input the same sentence with typos
3. It calculates the semantic distance
4. Shows you how much the meaning "drifted"

**Example Session:**
```
Enter 'original' to input a sentence, 'example' for demo, or 'quit' to exit: example

📖 EXAMPLE ANALYSIS
Original sentence:
  → The quick brown fox jumps over the lazy dog

Corrupted sentence (25% typos):
  → The quik brown fox jumps ovr the lazi dog

Semantic Distance: 0.123456
Interpretation: Low drift (very similar meaning)
```

---

### Option 2: Try Pre-Made Examples

The script includes 3 examples with different typo rates (25%, 30%, 35%). Just type `example` when prompted!

---

## 📝 How to Use

### Step 1: Start the interactive script
```bash
cd /Users/ariellenapadensky/LLMs-and-Multi-Agent-Orchestration---Assignment3
python3 run_interactive.py
```

### Step 2: Choose what to do
- Type `original` - Enter your own sentences
- Type `example` - See a demonstration
- Type `quit` - Exit

### Step 3: Input your sentences
When you choose `original`:
1. **First prompt**: Enter your original sentence (without typos)
   - Example: `The quick brown fox jumps over the lazy dog`

2. **Second prompt**: Enter the same sentence with typos
   - Example: `The quik brown fox jumps ovr the lazi dog`

3. **Result**: See the semantic distance and interpretation!

---

## 🎨 Understanding Your Results

### Semantic Distance Scale

| Distance Range | Meaning | Example |
|---------------|---------|---------|
| 0.00 - 0.20 | **Minimal drift** | Nearly identical meaning |
| 0.20 - 0.35 | **Low drift** | Very similar, minor differences |
| 0.35 - 0.50 | **Moderate drift** | Noticeable semantic changes |
| 0.50 - 0.70 | **High drift** | Significant meaning changes |
| 0.70+ | **Severe drift** | Substantially altered meaning |

### Real Results from Our Experiment
- **Lowest distance**: 0.295 (Historical novel with 40% typos)
- **Highest distance**: 0.824 (Symphony orchestra with 30% typos)
- **Average distance**: 0.474

---

## 💡 Tips for Testing

### Good Sentences to Try:
1. **Technical vocabulary** (tends to show higher drift)
   - "Quantum computing algorithms solve complex optimization problems"
   - "Pharmaceutical companies develop revolutionary treatment protocols"

2. **Common concepts** (tends to show lower drift)
   - "The children played happily in the park yesterday"
   - "Scientists study climate change patterns worldwide"

3. **Cultural references** (can show unpredictable drift)
   - "The symphony orchestra performed classical compositions"
   - "Traditional culinary techniques preserve cultural heritage"

### How to Add Typos:
1. **Substitution**: "quick" → "quik"
2. **Deletion**: "over" → "ovr"  
3. **Duplication**: "happy" → "hapyy"
4. **Transposition**: "the" → "teh"

**Recommended typo rate**: 25-30% of words (2-3 typos in a 10-word sentence)

---

## 🔧 Advanced: Using Python Scripts Directly

### Calculate Distance Between Two Sentences
```bash
python3 scripts/calculate_distance.py "sentence 1" "sentence 2"
```

**Example:**
```bash
python3 scripts/calculate_distance.py \
  "The quick brown fox jumps over the lazy dog" \
  "The fast brown fox leaps across the sleepy canine"
```

**Output:** A single number (e.g., `0.423156`)

---

## 📊 View Existing Experiment Results

### See the Visualization
```bash
open results/semantic_drift_analysis.png
```

### Read the Statistical Analysis
```bash
cat results/quantitative_analysis.md
```

### View Raw Data
```bash
# See all 21 original sentences
ls data/experiment_raw_data/sentence_*_original.txt

# See all corrupted versions
ls data/experiment_raw_data/sentence_*_corrupted.txt

# View distance results
cat data/experiment_raw_data/distance_results.txt
```

---

## 🎯 Example Testing Scenarios

### Scenario 1: Test Your Own Essay/Text
1. Copy a paragraph from your writing
2. Introduce some typos (aim for 25-30%)
3. Run the analyzer
4. See how much the meaning changes!

### Scenario 2: Compare Different Typo Rates
Test the same sentence with increasing typo levels:
- 10% typos (1-2 typos)
- 25% typos (4-5 typos)
- 50% typos (8-10 typos)

Watch how the distance changes!

### Scenario 3: Test Domain Robustness
Try sentences from different domains:
- Scientific: "Photosynthesis converts solar energy into chemical bonds"
- Technical: "The algorithm optimizes database query performance"
- Casual: "I really enjoyed the movie we watched together"

See which domain is most robust to typos!

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Reinstall dependencies
```bash
pip3 install -r requirements.txt
```

### Issue: "SSL Certificate Error"
**Solution**: The script includes SSL verification bypass. If it persists:
```bash
export SSL_CERT_FILE=""
python3 run_interactive.py
```

### Issue: "Model download takes forever"
**Solution**: First run downloads ~90MB model. Be patient! Subsequent runs are instant.

### Issue: Script freezes or crashes
**Solution**: Make sure you have enough RAM (model needs ~500MB). Close other applications.

---

## 📚 What's Happening Under the Hood?

When you input sentences, the script:

1. **Loads the embedding model** (`all-MiniLM-L6-v2`)
   - This converts text to 384-dimensional vectors
   - Each dimension captures semantic features

2. **Generates embeddings** for both sentences
   - Original: `[0.234, -0.567, 0.891, ...]` (384 numbers)
   - Corrupted: `[0.241, -0.559, 0.887, ...]` (384 numbers)

3. **Calculates cosine distance**
   - Measures angle between vectors in 384-D space
   - Distance = 1 - (dot product / magnitudes)

4. **Interprets the result**
   - Compares to experimental thresholds
   - Provides human-readable interpretation

---

## 🎓 Educational Value

This tool helps you understand:

✓ How spelling affects semantic meaning  
✓ How robust NLP systems are to errors  
✓ How embeddings capture meaning mathematically  
✓ How distance metrics quantify similarity  

---

## 🔗 Next Steps

After trying the interactive mode:

1. **Read the full results**: `RESULTS_EXPLANATION.md`
2. **View the visualization**: `results/semantic_drift_analysis.png`
3. **Explore the architecture**: `docs/ARCHITECTURE.md`
4. **Understand the math**: `docs/MATHEMATICAL_FOUNDATIONS.md`

---

## 💬 Quick Command Reference

```bash
# Run interactive mode
python3 run_interactive.py

# Calculate distance directly
python3 scripts/calculate_distance.py "text1" "text2"

# View experiment visualization
open results/semantic_drift_analysis.png

# Read statistical results
cat results/quantitative_analysis.md

# View all results explained
cat RESULTS_EXPLANATION.md
```

---

**Ready to explore semantic drift? Run `python3 run_interactive.py` and start testing! 🚀**

