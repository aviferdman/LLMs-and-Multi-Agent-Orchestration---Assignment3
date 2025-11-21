#!/usr/bin/env python3
"""
Interactive Semantic Drift Analyzer
Run this to test your own sentences with typos!

This version uses fault-tolerant model loading that handles:
- SSL certificate errors
- Local model detection
- Offline mode
- Clear error messages

If model loading fails, run: python3 setup.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables if .env exists
env_file = project_root / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# Import fault-tolerant model loader
try:
    from model_loader import load_model
    USE_MODEL_LOADER = True
except ImportError:
    USE_MODEL_LOADER = False
    from sentence_transformers import SentenceTransformer

from scipy.spatial.distance import cosine
import numpy as np

print("="*80)
print("🎯 INTERACTIVE SEMANTIC DRIFT ANALYZER")
print("="*80)

# Load the model with fault-tolerant handling
if USE_MODEL_LOADER:
    print("\n💡 Using fault-tolerant model loader...")
    try:
        model = load_model(verbose=True, fail_on_error=True)
    except SystemExit:
        print("\n" + "="*80)
        print("❌ Cannot start without embedding model")
        print("="*80)
        print("\nTo fix this, run the setup script:")
        print("   python3 setup.py")
        print("\nThis will automatically:")
        print("   • Download the model (930MB)")
        print("   • Handle SSL issues")
        print("   • Set up offline mode")
        sys.exit(1)
else:
    # Fallback to simple loading
    print("\n⚠️  Model loader not available, using fallback...")
    print("   (Run 'python3 setup.py' for better error handling)\n")
    try:
        local_model_path = os.path.expanduser('~/models/all-MiniLM-L6-v2')
        if os.path.exists(local_model_path):
            model = SentenceTransformer(local_model_path)
            print("✓ Model loaded from local directory!\n")
        else:
            print("Attempting to download model...")
            model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✓ Model loaded successfully!\n")
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print("\n💡 Run setup to fix: python3 setup.py")
        sys.exit(1)

def compute_semantic_distance(text1, text2):
    """Compute semantic distance between two texts"""
    # Generate embeddings
    emb1 = model.encode(text1, convert_to_numpy=True)
    emb2 = model.encode(text2, convert_to_numpy=True)
    
    # Calculate cosine distance
    distance = cosine(emb1, emb2)
    return distance

def interpret_distance(distance):
    """Provide interpretation of the distance value"""
    if distance < 0.2:
        return "Minimal drift (nearly identical meaning)"
    elif distance < 0.35:
        return "Low drift (very similar meaning)"
    elif distance < 0.5:
        return "Moderate drift (noticeable differences)"
    elif distance < 0.7:
        return "High drift (significant semantic change)"
    else:
        return "Severe drift (meaning substantially altered)"

def simulate_translation(text):
    """
    Simulate multi-hop translation.
    NOTE: For full translation, use the Claude agent system.
    This is just a placeholder to show the concept.
    """
    print("\n" + "-"*80)
    print("📝 TRANSLATION SIMULATION")
    print("-"*80)
    print("In the full system, your sentence would go through:")
    print("  1. English → French (Translator Agent 1)")
    print("  2. French → Italian (Translator Agent 2)")
    print("  3. Italian → English (Translator Agent 3)")
    print("\nFor this demo, we'll just measure the semantic distance between")
    print("your original and corrupted sentences.")
    print("-"*80 + "\n")

print("="*80)
print("USAGE:")
print("="*80)
print("1. Enter an original sentence (without typos)")
print("2. Enter the same sentence with typos")
print("3. Get the semantic distance measurement!")
print("\nType 'quit' or 'exit' to stop, 'example' to see an example.")
print("="*80)

# Example sentences for quick testing
examples = [
    {
        'original': 'The quick brown fox jumps over the lazy dog',
        'corrupted': 'The quik brown fox jumps ovr the lazi dog',
        'typo_rate': '25%'
    },
    {
        'original': 'Artificial intelligence systems require massive computational resources to process natural language effectively',
        'corrupted': 'Artifical inteligence systems require masive computaional resources to proces natural languae effectivly',
        'typo_rate': '30%'
    },
    {
        'original': 'Climate scientists warn that rising ocean temperatures will fundamentally alter marine ecosystems',
        'corrupted': 'Climat scientsts warn that risng ocean tempertures will fundmentally alter marine ecossystems',
        'typo_rate': '35%'
    }
]

def show_example():
    """Show an example analysis"""
    import random
    ex = random.choice(examples)
    print("\n" + "="*80)
    print("📖 EXAMPLE ANALYSIS")
    print("="*80)
    print(f"\nOriginal sentence:")
    print(f"  → {ex['original']}")
    print(f"\nCorrupted sentence ({ex['typo_rate']} typos):")
    print(f"  → {ex['corrupted']}")
    
    simulate_translation(ex['original'])
    
    distance = compute_semantic_distance(ex['original'], ex['corrupted'])
    interpretation = interpret_distance(distance)
    
    print("="*80)
    print("📊 SEMANTIC DRIFT ANALYSIS")
    print("="*80)
    print(f"\nSemantic Distance: {distance:.6f}")
    print(f"Interpretation: {interpretation}")
    print("\nDistance Scale:")
    print("  0.00 - 0.20: Minimal drift")
    print("  0.20 - 0.35: Low drift")
    print("  0.35 - 0.50: Moderate drift")
    print("  0.50 - 0.70: High drift")
    print("  0.70+     : Severe drift")
    print("="*80 + "\n")

# Main interactive loop
while True:
    print("\n" + "="*80)
    user_input = input("Enter 'original' to input a sentence, 'example' for demo, or 'quit' to exit: ").strip().lower()
    
    if user_input in ['quit', 'exit', 'q']:
        print("\n👋 Thank you for using the Semantic Drift Analyzer!")
        print("="*80)
        break
    
    elif user_input in ['example', 'demo', 'ex']:
        show_example()
        continue
    
    elif user_input in ['original', 'start', 'begin', '']:
        print("\n" + "-"*80)
        print("📝 ENTER YOUR SENTENCES")
        print("-"*80)
        
        original = input("\n1️⃣  Enter ORIGINAL sentence (without typos):\n   → ").strip()
        
        if not original:
            print("⚠️  Empty input. Please try again.")
            continue
        
        if original.lower() in ['quit', 'exit']:
            print("\n👋 Thank you for using the Semantic Drift Analyzer!")
            print("="*80)
            break
        
        corrupted = input("\n2️⃣  Enter CORRUPTED sentence (with typos):\n   → ").strip()
        
        if not corrupted:
            print("⚠️  Empty input. Please try again.")
            continue
        
        if corrupted.lower() in ['quit', 'exit']:
            print("\n👋 Thank you for using the Semantic Drift Analyzer!")
            print("="*80)
            break
        
        # Calculate semantic distance
        print("\n⏳ Computing semantic distance...")
        
        simulate_translation(original)
        
        try:
            distance = compute_semantic_distance(original, corrupted)
            interpretation = interpret_distance(distance)
            
            print("="*80)
            print("📊 SEMANTIC DRIFT ANALYSIS RESULTS")
            print("="*80)
            print(f"\nOriginal Sentence:")
            print(f"  {original}")
            print(f"\nCorrupted Sentence:")
            print(f"  {corrupted}")
            print(f"\n{'─'*80}")
            print(f"\n✨ Semantic Distance: {distance:.6f}")
            print(f"📈 Interpretation: {interpretation}")
            print(f"\n{'─'*80}")
            print("\nDistance Scale Reference:")
            print("  0.00 - 0.20: Minimal drift (nearly identical)")
            print("  0.20 - 0.35: Low drift (very similar)")
            print("  0.35 - 0.50: Moderate drift (noticeable changes)")
            print("  0.50 - 0.70: High drift (significant changes)")
            print("  0.70+     : Severe drift (substantially altered)")
            print("="*80)
            
            # Comparison with experiment data
            print("\n📚 Comparison with Experiment Data:")
            print(f"  • Your distance: {distance:.3f}")
            print(f"  • Experiment mean: 0.474")
            print(f"  • Experiment range: 0.295 - 0.824")
            
            if distance < 0.474:
                print(f"  ➜ Your sentence shows LOWER drift than average")
            else:
                print(f"  ➜ Your sentence shows HIGHER drift than average")
            
            print("="*80)
            
        except Exception as e:
            print(f"\n✗ Error computing distance: {e}")
            continue
    
    else:
        print(f"\n⚠️  Unknown command: '{user_input}'")
        print("    Valid commands: 'original', 'example', 'quit'")

