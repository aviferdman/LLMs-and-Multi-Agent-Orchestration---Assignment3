"""
Measure Semantic Distance Between Two Embeddings

This script computes the cosine distance between two text embeddings.
Cosine distance = 1 - cosine similarity, ranging from 0 (identical) to 2 (opposite).

Usage:
    python measure_distance.py "Text 1" "Text 2"
    python measure_distance.py --file1 text1.txt --file2 text2.txt
    python measure_distance.py --embedding1 emb1.json --embedding2 emb2.json

Output:
    Prints the semantic distance as a float
"""

import sys
import json
import argparse
import numpy as np
from scipy.spatial.distance import cosine
from compute_embeddings import compute_embedding

def cosine_distance(embedding1, embedding2):
    """
    Compute cosine distance between two embeddings.

    Args:
        embedding1: First embedding (numpy array or list)
        embedding2: Second embedding (numpy array or list)

    Returns:
        Float distance value (0 = identical, 2 = opposite)
    """
    # Convert to numpy arrays if needed
    emb1 = np.array(embedding1)
    emb2 = np.array(embedding2)

    # Verify same dimensions
    if emb1.shape != emb2.shape:
        raise ValueError(f"Embedding dimension mismatch: {emb1.shape} vs {emb2.shape}")

    # Compute cosine distance (1 - cosine similarity)
    distance = cosine(emb1, emb2)

    return float(distance)

def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(description='Measure semantic distance between two texts')

    # Input methods
    parser.add_argument('text1', nargs='?', help='First text string')
    parser.add_argument('text2', nargs='?', help='Second text string')
    parser.add_argument('--file1', '-f1', help='Read first text from file')
    parser.add_argument('--file2', '-f2', help='Read second text from file')
    parser.add_argument('--embedding1', '-e1', help='Load first embedding from JSON file')
    parser.add_argument('--embedding2', '-e2', help='Load second embedding from JSON file')

    # Output options
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Determine input method and load data
    embeddings = []
    texts = []

    for i, (text_arg, file_arg, emb_arg) in enumerate([
        (args.text1, args.file1, args.embedding1),
        (args.text2, args.file2, args.embedding2)
    ], 1):
        if emb_arg:
            # Load pre-computed embedding
            with open(emb_arg, 'r', encoding='utf-8') as f:
                data = json.load(f)
            embeddings.append(np.array(data['embedding']))
            texts.append(data.get('text', f'[from {emb_arg}]'))
            if args.verbose:
                print(f"Text {i} loaded from embedding: {emb_arg}", file=sys.stderr)
        elif file_arg:
            # Read text from file and compute embedding
            with open(file_arg, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            texts.append(text)
            if args.verbose:
                print(f"Text {i} read from: {file_arg}", file=sys.stderr)
            embeddings.append(compute_embedding(text))
        elif text_arg:
            # Use text directly
            texts.append(text_arg)
            if args.verbose:
                print(f"Text {i}: {text_arg[:50]}...", file=sys.stderr)
            embeddings.append(compute_embedding(text_arg))
        else:
            parser.error(f"Must provide text{i}, --file{i}, or --embedding{i}")

    # Compute distance
    distance = cosine_distance(embeddings[0], embeddings[1])

    # Output results
    if args.json:
        result = {
            'text1': texts[0],
            'text2': texts[1],
            'distance': distance,
            'similarity': 1.0 - distance,
            'interpretation': interpret_distance(distance)
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if args.verbose:
            print("\n" + "="*60, file=sys.stderr)
            print("SEMANTIC DISTANCE ANALYSIS", file=sys.stderr)
            print("="*60, file=sys.stderr)
            print(f"\nText 1: {texts[0][:100]}..." if len(texts[0]) > 100 else f"\nText 1: {texts[0]}", file=sys.stderr)
            print(f"\nText 2: {texts[1][:100]}..." if len(texts[1]) > 100 else f"\nText 2: {texts[1]}", file=sys.stderr)
            print(f"\nCosine Distance: {distance:.4f}", file=sys.stderr)
            print(f"Cosine Similarity: {1.0 - distance:.4f}", file=sys.stderr)
            print(f"Interpretation: {interpret_distance(distance)}", file=sys.stderr)
            print("="*60, file=sys.stderr)

        # Always print the distance value to stdout (for easy parsing)
        print(f"{distance:.4f}")

def interpret_distance(distance):
    """
    Provide a human-readable interpretation of the distance value.

    Args:
        distance: Cosine distance value

    Returns:
        String interpretation
    """
    if distance < 0.2:
        return "Minimal drift (excellent semantic preservation)"
    elif distance < 0.4:
        return "Low drift (good semantic preservation)"
    elif distance < 0.6:
        return "Moderate drift (acceptable semantic preservation)"
    elif distance < 0.8:
        return "High drift (significant semantic change)"
    else:
        return "Severe drift (meaning largely lost)"

if __name__ == '__main__':
    main()
