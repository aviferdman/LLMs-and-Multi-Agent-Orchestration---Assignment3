"""
Compute Embeddings for Text

This script computes semantic embeddings for input text using sentence-transformers.
It converts text into a high-dimensional vector representation that captures meaning.

Usage:
    python compute_embeddings.py "Your text here"
    python compute_embeddings.py --file /path/to/file.txt

Output:
    Prints the embedding as a JSON array of floats
"""

import sys
import json
import argparse
from sentence_transformers import SentenceTransformer
import numpy as np

# Global model (loaded once for efficiency)
_model = None

def load_model(model_name='all-MiniLM-L6-v2'):
    """
    Load the sentence transformer model.

    Args:
        model_name: Name of the model to use (default: all-MiniLM-L6-v2)

    Returns:
        SentenceTransformer model instance
    """
    global _model
    if _model is None:
        print(f"Loading embedding model: {model_name}...", file=sys.stderr)
        _model = SentenceTransformer(model_name)
        print(f"Model loaded successfully (embedding dim: {_model.get_sentence_embedding_dimension()})", file=sys.stderr)
    return _model

def compute_embedding(text):
    """
    Compute embedding for a single text string.

    Args:
        text: Input text string

    Returns:
        numpy array of shape (embedding_dim,)
    """
    model = load_model()

    # Encode the text
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

    return embedding

def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(description='Compute semantic embeddings for text')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('text', nargs='?', help='Text to compute embedding for')
    group.add_argument('--file', '-f', help='Read text from file')
    parser.add_argument('--output', '-o', help='Save embedding to file (JSON format)')
    parser.add_argument('--model', '-m', default='all-MiniLM-L6-v2',
                       help='Model name (default: all-MiniLM-L6-v2)')

    args = parser.parse_args()

    # Get input text
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        print(f"Read text from: {args.file}", file=sys.stderr)
    else:
        text = args.text

    print(f"Input text: {text[:100]}..." if len(text) > 100 else f"Input text: {text}", file=sys.stderr)

    # Compute embedding
    embedding = compute_embedding(text)

    print(f"Embedding computed: shape={embedding.shape}, norm={np.linalg.norm(embedding):.4f}", file=sys.stderr)

    # Output embedding as JSON
    embedding_json = {
        'text': text,
        'embedding': embedding.tolist(),
        'dimension': len(embedding),
        'model': args.model
    }

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(embedding_json, f, indent=2)
        print(f"Embedding saved to: {args.output}", file=sys.stderr)
    else:
        print(json.dumps(embedding_json, indent=2))

if __name__ == '__main__':
    main()
