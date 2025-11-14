# Project Index - Multi-Agent Translation Semantic Drift Experiment

**Last Updated**: November 14, 2025

This document provides a quick navigation guide to all project files and their purposes.

---

## 🎯 Start Here

**For reviewers and first-time users:**

1. **📊 Main Results**: `results/FINAL_EXPERIMENT_REPORT.md` - Complete experimental report
2. **📈 Visualization**: `results/semantic_drift_visualization.png` - Graph of all results
3. **📖 Overview**: `README.md` - Full project documentation
4. **🚀 Quick Start**: `USAGE.md` - How to run experiments

---

## 📁 Directory Structure

### `/results/` - Experiment Results (November 14, 2025)

| File | Purpose | Size |
|------|---------|------|
| `FINAL_EXPERIMENT_REPORT.md` | Main comprehensive report with all 4 phases | 17 KB |
| `EXPERIMENT_SUMMARY.md` | Executive summary and key findings | 9 KB |
| `automated_experiment_report.md` | Detailed qualitative analysis | 23 KB |
| `semantic_drift_visualization.png` | Dual-panel visualization chart | 399 KB |

**Key Finding**: Non-linear relationship - peak drift at 30% typos, not 50%!

---

### `/data/experiment_raw_data/` - Raw Experiment Data

Contains all raw data from the November 14, 2025 experiment:

- **Original sentences**: `sentence_XX_original.txt` (21 files)
- **Corrupted sentences**: `sentence_XX_corrupted.txt` (21 files)
- **Translation chains**: `sentence_XX_translations.txt` (21 files)
- **All translations**: `all_translations_complete.txt` (complete record)
- **Distances**: `distance_results.txt` (all semantic distances)
- **Verification**: `verification_summary.txt` (typo rate verification)

Total: 66 files, ~150 KB

---

### `/scripts/` - Python Analysis Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `calculate_distance.py` | Single sentence semantic distance | Testing individual sentences |
| `batch_calculate_distances.py` | Batch distance calculation | Processing multiple sentences |
| `compute_all_distances.py` | Compute embeddings for all | Recomputing experiment results |
| `generate_visualization.py` | Create matplotlib graphs | Regenerating visualizations |
| `batch_analysis_custom.py` | Custom batch analysis | Advanced analysis tasks |

**Usage**: All scripts called by the orchestrator agent, not run directly.

---

### `/.claude/` - Multi-Agent System

#### Agents

| Agent | Purpose |
|-------|---------|
| `agents/translation-experiment-orchestrator.md` | Main orchestrator - coordinates full experiment |

#### Skills

| Skill | Technology | Purpose |
|-------|-----------|---------|
| `translate/SKILL.md` | Claude native | Language translation |
| `typo-injector/SKILL.md` | Claude native | Word-based typo injection |
| `embeddings/SKILL.md` | sentence-transformers | Semantic embedding computation |
| `chart-generator/SKILL.md` | matplotlib | Visualization generation |
| `semantic_analysis/` | Python | Distance measurement |

---

### `/docs/` - Technical Documentation

#### Core Documentation

| Document | Content |
|----------|---------|
| `ARCHITECTURE.md` | System architecture and design |
| `MATHEMATICAL_FOUNDATIONS.md` | Mathematical basis (embeddings, cosine distance) |
| `RESEARCH_METHODOLOGY.md` | Research approach and experimental design |
| `TESTING.md` | Testing strategy and validation |

#### Supporting Documentation

| Document | Content |
|----------|---------|
| `PROMPT_BOOK.md` | Prompt engineering guide |
| `PRD.md` | Product requirements document |
| `SECURITY.md` | Security considerations |
| `COST_ANALYSIS.md` | Cost analysis |
| `EDGE_CASES.md` | Edge case handling |
| `ISO_IEC_25010_COMPLIANCE.md` | Quality compliance |

#### Architecture Decision Records (ADRs)

| ADR | Decision |
|-----|----------|
| `ADR-001-multi-agent-design.md` | Multi-agent system architecture |
| `ADR-002-embedding-model-selection.md` | Sentence-transformers model choice |
| `ADR-003-translation-chain-design.md` | Translation chain configuration |

---

## 📄 Root Files

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation (30+ KB) |
| `USAGE.md` | Quick start guide and usage instructions |
| `CHANGELOG.md` | Version history and changes |
| `SELF_ASSESSMENT.md` | Project self-assessment against rubric |
| `OPEN_SOURCE_CONTRIBUTION.md` | Open source contributions and learnings |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git ignore patterns |

---

## 🔍 Finding Specific Information

### Research Questions

**Q: What were the main findings?**
→ `results/EXPERIMENT_SUMMARY.md`

**Q: How were typos injected?**
→ `.claude/skills/typo-injector/SKILL.md` + `results/FINAL_EXPERIMENT_REPORT.md` (Phase 1)

**Q: What translation chain was used?**
→ English → French → Italian → Spanish (3 hops)

**Q: How was verification done?**
→ `results/FINAL_EXPERIMENT_REPORT.md` (Verification Summary Table)

**Q: What were the exact semantic distances?**
→ `data/experiment_raw_data/distance_results.txt`

### Technical Questions

**Q: How do embeddings work?**
→ `docs/MATHEMATICAL_FOUNDATIONS.md`

**Q: Why this architecture?**
→ `docs/ARCHITECTURE.md` + `docs/ADRs/ADR-001-multi-agent-design.md`

**Q: How to run the experiment?**
→ `USAGE.md` + `README.md` (Usage section)

**Q: What are the dependencies?**
→ `requirements.txt` (Python) + `README.md` (Installation section)

---

## 📊 Experiment Quick Facts

- **Date**: November 14, 2025
- **Sentences Tested**: 21
- **Typo Rates**: 20%, 25%, 30%, 35%, 40%, 45%, 50%
- **Sentences per Rate**: 3
- **Translation Chain**: English → French → Italian → Spanish
- **Verification Pass Rate**: 100% (21/21)
- **Average Typo Deviation**: 1.5%
- **Key Finding**: Non-linear semantic drift with peak at 30%

---

## 🎓 For Academic Review

**Essential Reading Order**:
1. `results/FINAL_EXPERIMENT_REPORT.md` - Complete results
2. `README.md` - Project overview
3. `docs/RESEARCH_METHODOLOGY.md` - Methodology
4. `SELF_ASSESSMENT.md` - Self-assessment

**Supporting Evidence**:
- `results/semantic_drift_visualization.png` - Visual results
- `data/experiment_raw_data/verification_summary.txt` - Verification audit
- `docs/MATHEMATICAL_FOUNDATIONS.md` - Technical rigor

---

## 📝 Quick Stats

- **Total Files**: ~150
- **Total Documentation**: ~200 KB markdown
- **Code**: ~50 KB Python
- **Data**: ~150 KB raw data
- **Visualization**: 399 KB PNG
- **Lines of Documentation**: ~3,000+

---

**Need Help?** Consult `USAGE.md` for common tasks or `README.md` for comprehensive documentation.
