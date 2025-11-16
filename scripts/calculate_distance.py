"""
Simple script to calculate semantic distance between two sentences.
This script ONLY handles embeddings and distance calculation.
Translation is handled by Claude agents.
"""
import sys
from pathlib import Path

# Add embeddings skill to path
base_dir = Path(__file__).parent.parent
sys.path.append(str(base_dir / '.claude' / 'skills' / 'embeddings'))

from embedding_utils import compute_embedding, cosine_distance


def calculate_distance(sentence1, sentence2):
    """
    Calculate semantic distance between two sentences.

    Args:
        sentence1: First sentence (original)
        sentence2: Second sentence (final translation)

    Returns:
        float: Cosine distance between the two sentences
    """
    try:
        emb1 = compute_embedding(sentence1)
        emb2 = compute_embedding(sentence2)
        distance = cosine_distance(emb1, emb2)
        return distance
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return -1.0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python calculate_distance.py 'sentence1' 'sentence2'")
        print("Example: python calculate_distance.py 'Hello world' 'Bonjour le monde'")
        sys.exit(1)

    sentence1 = sys.argv[1]
    sentence2 = sys.argv[2]

    distance = calculate_distance(sentence1, sentence2)

    if distance >= 0:
        print(f"{distance:.6f}")
    else:
        sys.exit(1)
