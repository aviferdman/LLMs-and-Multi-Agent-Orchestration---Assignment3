# 🚀 How to Run the Project - Complete Guide

## 🔐 Understanding the SSL Issue

### What is SSL?
**SSL (Secure Sockets Layer)** is security encryption for internet connections.
- When you visit `https://` websites, SSL encrypts your data
- It's like putting your data in a locked box before sending it
- SSL certificates verify that websites are who they claim to be

### What's the Problem?
The error `SSL: CERTIFICATE_VERIFY_FAILED` means:
```
Python script → trying to download AI model from huggingface.co
              → Your network has security software checking connections
              → Python doesn't trust this "middle man"
              → Download blocked for security
```

**Common in:**
- 🏢 Corporate networks
- 🎓 School/university networks  
- 🛡️ Networks with antivirus/firewall
- 📡 VPN connections

### Why It's Actually OK
The experiment **already ran successfully** before! The model was downloaded then, so we can:
✅ Use the existing results
✅ Explore the data without re-downloading
✅ Run demonstrations with pre-computed values

---

## ✅ Solutions (Pick the One That Works for You)

### 🎯 Solution 1: Interactive Demo (NO DOWNLOAD NEEDED) ⭐ RECOMMENDED

This works **right now** without any downloads or SSL fixes:

```bash
cd /Users/ariellenapadensky/LLMs-and-Multi-Agent-Orchestration---Assignment3
python3 simple_demo.py
```

**What you can do:**
- ✅ View all 21 sentence examples
- ✅ See semantic distances
- ✅ Explore statistics by typo rate
- ✅ Understand the surprising non-linear finding
- ✅ Compare high vs low drift examples

**Menu options:**
1. View sample sentence analysis (pick from 5 examples)
2. View statistics by typo rate
3. See the surprising finding (30% peak!)
4. Compare extreme examples
5. View all 21 sentences summary
6. Quit

---

### 🎯 Solution 2: View Pre-Generated Results

All the results are already available:

```bash
# View the visualization (4-panel chart)
open results/semantic_drift_analysis.png

# Read statistical analysis
cat results/quantitative_analysis.md

# See the complete explanation
cat RESULTS_EXPLANATION.md

# View raw distances
cat data/experiment_raw_data/distance_results.txt

# View verification summary
cat data/experiment_raw_data/verification_summary.txt
```

---

### 🎯 Solution 3: Run With Your Own Sentences (If SSL Can Be Fixed)

**Option A: Fix SSL certificates**
```bash
# For macOS
/Applications/Python\ 3.12/Install\ Certificates.command

# Then try
python3 run_interactive.py
```

**Option B: Download model manually** (if on different network)
```bash
# When on a network without SSL issues (home, coffee shop, etc.)
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

The model will download once (~90MB) and cache forever.

---

## 📊 What Each Script Does

### `simple_demo.py` ⭐ (Works NOW, no SSL needed)
- Interactive exploration of pre-computed results
- Shows all 21 sentences
- Displays statistics and findings
- **No internet or model download needed**

**Run it:**
```bash
python3 simple_demo.py
```

### `run_interactive.py` (Needs model download)
- Let's you input your OWN sentences with typos
- Calculates semantic distance in real-time
- Requires downloaded AI model
- **Blocked by SSL issue currently**

### `scripts/calculate_distance.py` (Needs model)
- Command-line tool for calculating distance
- Usage: `python3 scripts/calculate_distance.py "text1" "text2"`
- **Blocked by SSL issue currently**

### `scripts/batch_calculate_distances.py` (Needs model)
- Processes all 21 sentences
- Generates visualization chart
- **Blocked by SSL issue currently**

---

## 🎮 Quick Demo - Try This Now!

```bash
cd /Users/ariellenapadensky/LLMs-and-Multi-Agent-Orchestration---Assignment3
python3 simple_demo.py
```

Then try these menu options:
1. Enter `3` - See the surprising non-linear finding
2. Enter `4` - Compare highest vs lowest drift
3. Enter `1` then `8` - See the sentence with highest drift
4. Enter `1` then `14` - See the sentence with lowest drift
5. Enter `5` - View summary of all 21 sentences

---

## 📖 What You Can Learn From the Results

### The Experiment Tested:
- **21 sentences** with different typo rates (20%-50%)
- **3-hop translation**: English → French → Italian → English
- **Semantic distance**: How much meaning changed

### Key Findings:

1. **🚨 NON-LINEAR PATTERN (Surprising!)**
   ```
   20% typos → 0.419 distance
   30% typos → 0.633 distance (PEAK!)
   50% typos → 0.451 distance (LOWER than 30%!)
   ```

2. **Topic Matters More Than Typos**
   - Symphony orchestra (30% typos): 0.824 drift (HIGH)
   - Historical novel (40% typos): 0.295 drift (LOW)
   - More typos, but LESS drift!

3. **LLMs Are Error Correctors**
   - At high corruption (>40%), translators become conservative
   - They "play it safe" which reduces drift
   - Context helps recover meaning

---

## 🔍 Explore the Data Files

All the raw data is available:

```bash
# Original sentences (21 files)
cat data/experiment_raw_data/sentence_01_original.txt
cat data/experiment_raw_data/sentence_08_original.txt  # Highest drift
cat data/experiment_raw_data/sentence_14_original.txt  # Lowest drift

# Corrupted versions (21 files)
cat data/experiment_raw_data/sentence_01_corrupted.txt
cat data/experiment_raw_data/sentence_08_corrupted.txt
cat data/experiment_raw_data/sentence_14_corrupted.txt

# All distances
cat data/experiment_raw_data/distance_results.txt

# Verification data
cat data/experiment_raw_data/verification_summary.txt
```

---

## 🎨 The Visualization

Open the pre-generated chart:
```bash
open results/semantic_drift_analysis.png
```

**What it shows (4 panels):**
1. **Top-Left**: Mean drift by typo rate (with error bars)
   - Shows the 30% peak clearly
   
2. **Top-Right**: Individual sentence distances
   - Each dot = one sentence
   - Shows high variability
   
3. **Bottom-Left**: Distribution histogram
   - Most distances around 0.40-0.50
   
4. **Bottom-Right**: Box plots by typo rate
   - 30% has widest spread (most variability)

---

## 💡 Summary

| What You Want | What To Run | SSL Issue? |
|--------------|-------------|------------|
| Explore results interactively | `python3 simple_demo.py` | ✅ No issue |
| View visualization | `open results/semantic_drift_analysis.png` | ✅ No issue |
| Read statistical analysis | `cat results/quantitative_analysis.md` | ✅ No issue |
| Read complete explanation | `cat RESULTS_EXPLANATION.md` | ✅ No issue |
| View raw data | `cat data/experiment_raw_data/*.txt` | ✅ No issue |
| Test your own sentences | `python3 run_interactive.py` | ❌ SSL blocks download |

---

## 🚀 Start Here (Right Now!)

```bash
# 1. Run the interactive demo
python3 simple_demo.py

# 2. View the visualization
open results/semantic_drift_analysis.png

# 3. Read the full explanation
cat RESULTS_EXPLANATION.md
```

**You can do ALL of this without solving the SSL issue!**

---

## 🔧 If You Want to Fix SSL (Optional)

**Why the SSL error happens:**
Your network (likely corporate/school) has security software that inspects HTTPS traffic. This creates a "self-signed certificate" that Python doesn't trust.

**To fix:**
1. **Run on different network** (home WiFi, mobile hotspot)
2. **Install certificates** (macOS): `/Applications/Python\ 3.12/Install\ Certificates.command`
3. **Disable SSL verification** (not recommended for production, but OK for learning)
4. **Download model elsewhere** and copy cache folder

**But remember:** You don't NEED to fix this to explore the results!

---

## 📚 Additional Resources

- `README.md` - Complete project documentation
- `USAGE.md` - Usage guide
- `docs/ARCHITECTURE.md` - System architecture
- `docs/MATHEMATICAL_FOUNDATIONS.md` - How embeddings work
- `SUBMISSION_CHECKLIST.md` - Project checklist

---

**Ready? Start with:** `python3 simple_demo.py` 🎯

