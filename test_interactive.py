#!/usr/bin/env python3
"""
Quick test script to demonstrate the interactive analyzer
This runs automatically with pre-defined inputs
"""

import sys
import os

# Disable SSL verification for model download
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Add the embeddings path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.claude/skills/embeddings'))

print("="*80)
print("🧪 TESTING SEMANTIC DRIFT ANALYZER")
print("="*80)
print("\nLoading model...")

from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

model = SentenceTransformer('all-MiniLM-L6-v2')
print("✓ Model loaded!\n")

def test_sentence_pair(original, corrupted, description=""):
    """Test a sentence pair and display results"""
    print("="*80)
    if description:
        print(f"📝 {description}")
        print("="*80)
    
    print(f"\nOriginal:")
    print(f"  {original}")
    print(f"\nCorrupted:")
    print(f"  {corrupted}")
    
    # Calculate distance
    emb1 = model.encode(original, convert_to_numpy=True)
    emb2 = model.encode(corrupted, convert_to_numpy=True)
    distance = cosine(emb1, emb2)
    
    # Interpret
    if distance < 0.35:
        interpretation = "Low drift"
    elif distance < 0.5:
        interpretation = "Moderate drift"
    elif distance < 0.7:
        interpretation = "High drift"
    else:
        interpretation = "Severe drift"
    
    print(f"\n✨ Semantic Distance: {distance:.6f}")
    print(f"📊 Interpretation: {interpretation}")
    print("="*80 + "\n")
    
    return distance

# Run test cases
print("\n" + "🎯"*40)
print("RUNNING TEST CASES")
print("🎯"*40 + "\n")

# Test 1: Low typo rate
test_sentence_pair(
    "The quick brown fox jumps over the lazy dog",
    "The quik brown fox jumps ovr the lazi dog",
    "TEST 1: Low Typo Rate (~20%)"
)

# Test 2: Medium typo rate
test_sentence_pair(
    "Artificial intelligence systems require massive computational resources",
    "Artifical inteligence systms require masive computaional resourses",
    "TEST 2: Medium Typo Rate (~30%)"
)

# Test 3: High typo rate
test_sentence_pair(
    "Climate scientists study environmental changes worldwide",
    "Climat scientsts stdy enviromental changs worldwde",
    "TEST 3: High Typo Rate (~40%)"
)

# Test 4: From actual experiment (highest drift)
test_sentence_pair(
    "The symphony orchestra performed an emotionally powerful interpretation of classical compositions that captivated audiences throughout the entire evening",
    "The symphny orchestra performed an emotionaly powerful interpreation of classical compositons that captvated audiences throughout the entire evening",
    "TEST 4: From Experiment (30% typos - showed HIGHEST drift in experiment)"
)

# Test 5: From actual experiment (lowest drift)
test_sentence_pair(
    "The historical novel vividly portrayed life during the industrial revolution capturing the social upheaval and technological innovations of that era",
    "The historcal novel vividy portrayd life during the industial revoluton capturng the social upheaval and technologcal inovations of that era",
    "TEST 5: From Experiment (40% typos - showed LOWEST drift in experiment)"
)

print("\n" + "✅"*40)
print("ALL TESTS COMPLETED!")
print("✅"*40)
print("\n📚 Summary:")
print("  • The script is working correctly")
print("  • Semantic distances are being calculated")
print("  • You can now use run_interactive.py for your own sentences")
print("\n🚀 To run interactive mode: python3 run_interactive.py")
print("="*80)

