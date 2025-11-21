# 🚀 Setup Instructions - Fault-Tolerant Model Loading

**Quick Start:** Just run `python3 setup.py` - That's it!

---

## ✨ What's New

Your project now has **fault-tolerant model loading** that handles SSL certificate errors automatically!

### Key Features
- ✅ **One-command setup**: `python3 setup.py`
- ✅ **SSL error handling**: Automatically detects and recovers
- ✅ **Offline capable**: Works without internet after setup
- ✅ **Clear error messages**: Always explains what went wrong
- ✅ **Multiple fallback strategies**: Never fails silently
- ✅ **Environment variable support**: Customize behavior

---

## 🎯 Quick Start (For First-Time Users)

```bash
# 1. Install dependencies and download model (one command!)
python3 setup.py

# 2. That's it! Now run the project
python3 simple_demo.py
python3 run_interactive.py
python3 scripts/calculate_distance.py "hello world" "hi earth"
```

**What the setup script does:**
1. ✓ Checks Python version
2. ✓ Installs required packages
3. ✓ Downloads embedding model (930MB)
4. ✓ Handles SSL errors automatically
5. ✓ Validates the installation
6. ✓ Creates configuration file

---

## 📚 For Existing Users

If you already have the model installed:

```bash
# Run setup to integrate new fault-tolerant loading
python3 setup.py

# It will detect your existing model and complete in seconds
```

Your existing workflows continue to work - just more robustly now!

---

## 🌐 Behind Corporate/School Firewall?

**No problem!** The setup script handles SSL certificate issues automatically.

```bash
python3 setup.py
# If SSL issues detected, automatically falls back to Git clone
# No manual intervention needed!
```

---

## 🔧 Advanced Options

### Setup Script Options

```bash
# Normal setup (recommended)
python3 setup.py

# Force re-download model
python3 setup.py --force

# Check status without installing
python3 setup.py --check-only

# Skip validation (faster)
python3 setup.py --skip-validation
```

### Environment Variables

```bash
# Enable offline mode (no download attempts)
export HF_HUB_OFFLINE=1

# Use custom model path
export MODEL_LOCAL_PATH=/my/custom/path

# Run project
python3 run_interactive.py
```

### Manual Model Download

If you prefer to download manually:

```bash
# Install Git LFS
git lfs install

# Download model
mkdir -p ~/models
cd ~/models
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

# Set offline mode
export HF_HUB_OFFLINE=1
export MODEL_LOCAL_PATH=~/models/all-MiniLM-L6-v2
```

---

## 🧪 Test Your Setup

### Test 1: Model Loader
```bash
python3 model_loader.py
# Should show: ✅ Model loaded successfully
```

### Test 2: Distance Calculator
```bash
python3 scripts/calculate_distance.py "hello world" "hi earth"
# Should output a number (e.g., 0.456789)
```

### Test 3: Interactive Analyzer
```bash
python3 run_interactive.py
# Should start interactive mode
```

### Test 4: Demo
```bash
python3 simple_demo.py
# Should show experiment results menu
```

---

## ❓ Troubleshooting

### "SSL certificate error"
**Solution:** Run `python3 setup.py` - it handles this automatically!

### "Model not found"
**Solution:**
```bash
python3 setup.py
```

### "Git LFS not installed"
**Solution:**
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Then run setup
python3 setup.py
```

### "Package import error"
**Solution:**
```bash
pip install -r requirements.txt
python3 setup.py
```

### Still having issues?
See the comprehensive troubleshooting in:
- `README.md` - Installation section
- `FAULT_TOLERANT_SETUP_SUMMARY.md` - Implementation details
- `PULL_REQUEST.md` - Complete technical description

---

## 📁 New Files

| File | Purpose |
|------|---------|
| `setup.py` | Automated setup script (run this first!) |
| `model_loader.py` | Fault-tolerant model loading |
| `.env` | Auto-generated configuration (in .gitignore) |
| `PULL_REQUEST.md` | Complete PR description |
| `FAULT_TOLERANT_SETUP_SUMMARY.md` | Implementation details |
| `SETUP_INSTRUCTIONS.md` | This file |

---

## 🎯 What Changed in Existing Files

### Core Scripts Now Use Fault-Tolerant Loading
- ✅ `.claude/skills/embeddings/embedding_utils.py`
- ✅ `run_interactive.py`
- ✅ `scripts/calculate_distance.py`

### Documentation Updated
- ✅ `README.md` - New "Quick Setup" section

### All Changes Are Backwards Compatible
- ✅ No breaking changes
- ✅ Existing workflows work unchanged
- ✅ Just more robust!

---

## 🚦 Before vs After

### Before
```
❌ SSL errors crash the program
❌ Confusing error messages
❌ Manual intervention required
❌ No offline mode
❌ Each script loads model differently
```

### After
```
✅ SSL errors handled automatically
✅ Clear, actionable error messages
✅ One-command setup
✅ Full offline capability
✅ Centralized, robust model loading
```

---

## 📊 Quick Reference

### For First-Time Setup
```bash
python3 setup.py
```

### For Regular Use
```bash
# Interactive analyzer
python3 run_interactive.py

# Distance calculator
python3 scripts/calculate_distance.py "text 1" "text 2"

# Explore results
python3 simple_demo.py
```

### For Offline Mode
```bash
export HF_HUB_OFFLINE=1
# Now all scripts work offline
```

### For Custom Model Path
```bash
export MODEL_LOCAL_PATH=/custom/path
python3 run_interactive.py
```

---

## 🎉 You're All Set!

The project now has enterprise-grade fault-tolerant model loading that:
- ✅ Works on any network
- ✅ Handles SSL issues automatically
- ✅ Provides clear error messages
- ✅ Supports offline mode
- ✅ Never crashes silently

**Just run:** `python3 setup.py`

Then enjoy using the project! 🚀

---

## 📞 Need Help?

1. **Run setup:** `python3 setup.py`
2. **Read docs:** Check `README.md` and `FAULT_TOLERANT_SETUP_SUMMARY.md`
3. **Test components:** Run `python3 model_loader.py` to test loading

---

**Status:** ✅ All systems operational  
**Date:** November 21, 2025  
**Impact:** Critical usability improvement  
**Migration:** One command - `python3 setup.py`

