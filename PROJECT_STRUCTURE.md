# 📁 Project Structure

**Last Updated:** November 21, 2025  
**Status:** Organized and Ready

---

## 🎯 Quick Navigation

### 🚀 Start Here (Root Files)
```
📄 START_HERE.md              - Project overview (read this first!)
📄 README.md                  - Complete documentation
📄 SETUP_INSTRUCTIONS.md      - Setup guide with fault-tolerant loading
📄 CHANGELOG.md               - Version history
```

### 🔧 Core Scripts (Root)
```
🐍 setup.py                   - Automated setup (run this first!)
🐍 model_loader.py            - Fault-tolerant model loading
🐍 run_interactive.py         - Interactive semantic drift analyzer
🐍 simple_demo.py             - Explore experiment results
🐍 visualize_results.py       - Generate visualizations
```

---

## 📚 Documentation (`docs/`)

### Main Documentation
```
docs/
├── ARCHITECTURE.md           - System architecture and design
├── RESEARCH_METHODOLOGY.md   - Research approach and methods
├── MATHEMATICAL_FOUNDATIONS.md - Math behind semantic embeddings
├── TESTING.md                - Test documentation and coverage
├── SECURITY.md               - Security considerations
├── PRD.md                    - Product requirements document
├── PROMPT_BOOK.md            - Prompt engineering guide
├── COST_ANALYSIS.md          - Cost analysis and optimization
├── EDGE_CASES.md             - Edge case handling
└── ISO_IEC_25010_COMPLIANCE.md - Quality compliance
```

### Quick Reference Guides (Moved from Root)
```
docs/
├── HOW_TO_RUN.md             - How to run (old, see SETUP_INSTRUCTIONS.md)
├── QUICK_START.md            - Quick start (old, see SETUP_INSTRUCTIONS.md)
├── USAGE.md                  - Usage examples
└── RESULTS_EXPLANATION.md    - Explanation of experiment results
```

### Project Management
```
docs/
├── PROJECT_INDEX.md          - Project file index
├── SUBMISSION_CHECKLIST.md   - Submission requirements checklist
├── SELF_ASSESSMENT.md        - Project self-assessment
└── OPEN_SOURCE_CONTRIBUTION.md - Open source contribution guide
```

### Architecture Decision Records
```
docs/ADRs/
├── ADR-001-multi-agent-design.md
├── ADR-002-embedding-model-selection.md
└── ADR-003-translation-chain-design.md
```

### Setup Documentation (New)
```
docs/setup/
├── FAULT_TOLERANT_SETUP_SUMMARY.md  - Implementation details
└── PULL_REQUEST.md                   - PR description for fault-tolerant loading
```

### User Session Results (New)
```
docs/results-user-session/
├── FINAL_RESULTS.md          - User's "hello world what a god dey" analysis
├── SUCCESS_SUMMARY.md        - Session success summary
└── your_results_summary.md   - Detailed comparison with experiment
```

---

## 🧪 Scripts (`scripts/`)

```
scripts/
├── calculate_distance.py           - CLI semantic distance calculator
└── batch_calculate_distances.py    - Batch processing with visualization
```

---

## 🧠 Multi-Agent System (`.claude/`)

```
.claude/
├── main.md                         - Main orchestrator agent
├── settings.local.json             - Local settings
│
├── agents/                         - All agent definitions
│   ├── translators/
│   │   ├── translator-1-en-fr.md  - English → French
│   │   ├── translator-2-fr-it.md  - French → Italian
│   │   └── translator-3-it-en.md  - Italian → English
│   │
│   ├── orchestrators/
│   │   ├── translation-experiment-orchestrator.md
│   │   ├── batch-experiment-orchestrator.md
│   │   └── embedding-analyzer.md
│   │
│   ├── code-reviewer/
│   │   └── code-reviewer.md
│   │
│   └── qa-expert/
│       └── qa-expert.md
│
├── commands/
│   └── run-translation-experiment.md
│
└── skills/
    ├── translate/SKILL.md
    ├── typo-injector/SKILL.md
    ├── embeddings/
    │   ├── SKILL.md
    │   └── embedding_utils.py
    └── chart-generator/SKILL.md
```

---

## 📊 Results & Data

```
results/
├── semantic_drift_analysis.png     - Visualization (4 subplots)
└── quantitative_analysis.md        - Statistics table

data/experiment_raw_data/
├── sentence_XX_original.txt        - Original sentences (21 files)
├── sentence_XX_corrupted.txt       - Corrupted sentences (21 files)
├── test_sentences.txt
├── sentence_pairs_for_analysis.txt
├── distance_results.txt
├── verification_summary.txt
└── translation_results.json
```

---

## 🧪 Tests (`tests/`)

```
tests/
├── __init__.py
├── README.md
├── test_calculate_distance.py
├── test_batch_calculate_distances.py
└── test_embedding_utils.py
```

---

## 🔧 Configuration & Dependencies

```
requirements.txt                    - Python dependencies
.gitignore                          - Git ignore rules
.env                                - Configuration (auto-generated, gitignored)
```

---

## 📦 Model Storage (Not in Repo)

```
~/models/all-MiniLM-L6-v2/         - Local embedding model (930MB)
```

---

## 🎯 File Organization Summary

### Root Directory (User-Facing)
**Purpose:** Essential files users need to see immediately

| File | Purpose | Action |
|------|---------|--------|
| `START_HERE.md` | Project overview | ✅ Read first |
| `README.md` | Complete docs | ✅ Comprehensive |
| `SETUP_INSTRUCTIONS.md` | Setup guide | ✅ Run setup |
| `CHANGELOG.md` | Version history | ℹ️ Reference |
| `setup.py` | Setup script | 🔧 Run first |
| `model_loader.py` | Model loading | 📦 Core utility |
| `run_interactive.py` | Interactive mode | 🎮 User-facing |
| `simple_demo.py` | Demo explorer | 🎮 User-facing |
| `visualize_results.py` | Visualization | 📊 Generate graphs |

### docs/ (Reference Documentation)
**Purpose:** Detailed technical documentation, old guides, and project management

**Categories:**
1. **Technical Docs** - Architecture, math, research, security
2. **Quick Guides** - HOW_TO_RUN, QUICK_START (superseded by SETUP_INSTRUCTIONS)
3. **Project Management** - Assessment, checklist, contribution guide
4. **ADRs** - Architecture decision records
5. **Setup** - Fault-tolerant loading implementation
6. **User Session** - Session-specific results

### scripts/ (Utilities)
**Purpose:** Command-line utilities for calculations

### .claude/ (Multi-Agent System)
**Purpose:** Agent definitions, skills, and orchestration

### results/ & data/ (Experiment Data)
**Purpose:** Experimental results and raw data

### tests/ (Test Suite)
**Purpose:** Automated tests for the codebase

---

## 🚀 Typical User Journey

### First Time Setup
```bash
1. Read: START_HERE.md
2. Run: python3 setup.py
3. Try: python3 simple_demo.py
```

### Running Experiments
```bash
1. Interactive: python3 run_interactive.py
2. Calculate: python3 scripts/calculate_distance.py "text1" "text2"
3. Visualize: python3 visualize_results.py
```

### Learning More
```bash
1. Project overview: START_HERE.md
2. Complete docs: README.md
3. Technical details: docs/ARCHITECTURE.md
4. Math foundations: docs/MATHEMATICAL_FOUNDATIONS.md
5. Research method: docs/RESEARCH_METHODOLOGY.md
```

### Troubleshooting
```bash
1. Setup issues: SETUP_INSTRUCTIONS.md
2. SSL errors: docs/setup/FAULT_TOLERANT_SETUP_SUMMARY.md
3. General help: README.md
```

---

## 📋 What Changed (November 21, 2025)

### Files Moved to `docs/`
✅ Moved from root to docs:
- `HOW_TO_RUN.md` → `docs/`
- `QUICK_START.md` → `docs/`
- `USAGE.md` → `docs/`
- `RESULTS_EXPLANATION.md` → `docs/`
- `PROJECT_INDEX.md` → `docs/`
- `SUBMISSION_CHECKLIST.md` → `docs/`
- `SELF_ASSESSMENT.md` → `docs/`
- `OPEN_SOURCE_CONTRIBUTION.md` → `docs/`

### Files Organized into Subdirectories
✅ Created `docs/setup/`:
- `FAULT_TOLERANT_SETUP_SUMMARY.md`
- `PULL_REQUEST.md`

✅ Created `docs/results-user-session/`:
- `FINAL_RESULTS.md`
- `SUCCESS_SUMMARY.md`
- `your_results_summary.md`
- `demo_user_input.py`

### Files Kept in Root
✅ Essential user-facing files:
- `README.md` - Main documentation
- `START_HERE.md` - Quick overview
- `SETUP_INSTRUCTIONS.md` - Setup guide (NEW)
- `CHANGELOG.md` - Version history
- All core scripts (`setup.py`, `model_loader.py`, etc.)

---

## 🎯 Benefits of New Organization

### Before
❌ Too many files in root (20+ markdown files)  
❌ Hard to find what you need  
❌ Unclear which files are important  
❌ Redundant documentation scattered  

### After
✅ Clean root with only essential files (4 docs + scripts)  
✅ Organized docs by category  
✅ Clear separation: user-facing vs reference  
✅ Easy to find what you need  
✅ Logical grouping (setup, results, project management)  

---

## 📊 File Count Summary

| Location | Count | Purpose |
|----------|-------|---------|
| Root .md files | 4 | Essential user guides |
| Root .py files | 5 | Core scripts |
| docs/ | 20 | Reference documentation |
| docs/setup/ | 2 | Setup implementation docs |
| docs/results-user-session/ | 4 | Session-specific results |
| docs/ADRs/ | 3 | Architecture decisions |
| scripts/ | 2 | CLI utilities |
| .claude/ | ~15 | Multi-agent system |
| tests/ | 4 | Test suite |

**Total: ~59 organized files** (vs 20+ in root before)

---

## 🎉 Result

**Clean, organized, professional project structure!**

- ✅ Root directory is clean and focused
- ✅ Documentation is organized by purpose
- ✅ Easy to navigate
- ✅ Clear separation of concerns
- ✅ User-facing files prominent
- ✅ Reference docs accessible but not cluttering

---

## 📚 Quick Links

**Getting Started:**
- 🚀 [START_HERE.md](../START_HERE.md)
- 📖 [README.md](../README.md)
- ⚙️ [SETUP_INSTRUCTIONS.md](../SETUP_INSTRUCTIONS.md)

**Technical Documentation:**
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md)
- 🧮 [MATHEMATICAL_FOUNDATIONS.md](MATHEMATICAL_FOUNDATIONS.md)
- 🔬 [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md)

**Setup & Troubleshooting:**
- 🛠️ [FAULT_TOLERANT_SETUP_SUMMARY.md](setup/FAULT_TOLERANT_SETUP_SUMMARY.md)
- 🔧 [HOW_TO_RUN.md](HOW_TO_RUN.md)
- ⚡ [QUICK_START.md](QUICK_START.md)

---

**Last Updated:** November 21, 2025  
**Organization:** Complete ✅  
**Status:** Production-Ready 🚀

