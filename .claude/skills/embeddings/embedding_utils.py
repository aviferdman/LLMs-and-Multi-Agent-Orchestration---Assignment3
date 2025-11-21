"""
Utility functions for computing embeddings and measuring semantic distance.

This module uses the centralized model_loader for fault-tolerant model loading.
"""
import sys
from pathlib import Path
import numpy as np
from numpy.linalg import norm

# Add project root to path to import model_loader
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from model_loader import get_model as load_model_safely
    MODEL_LOADER_AVAILABLE = True
except ImportError:
    # Fallback to direct import if model_loader not available
    MODEL_LOADER_AVAILABLE = False
    from sentence_transformers import SentenceTransformer


# Global model instance (loaded once)
_model = None


def get_model():
    """
    Lazy-load the sentence transformer model with fault-tolerant handling.
    
    Uses the centralized model_loader module which handles:
    - SSL certificate errors
    - Local model detection
    - Offline mode
    - Clear error messages
    
    Returns:
        Loaded SentenceTransformer model
        
    Raises:
        SystemExit: If model cannot be loaded
    """
    global _model
    if _model is None:
        if MODEL_LOADER_AVAILABLE:
            # Use fault-tolerant loader
            _model = load_model_safely(verbose=True)
        else:
            # Fallback to simple loading (legacy)
            import os
            local_model_path = os.path.expanduser('~/models/all-MiniLM-L6-v2')
            if os.path.exists(local_model_path):
                _model = SentenceTransformer(local_model_path)
            else:
                try:
                    _model = SentenceTransformer('all-MiniLM-L6-v2')
                except Exception as e:
                    print(f"\n❌ Failed to load model: {e}")
                    print("\n💡 Run setup first: python3 setup.py")
                    sys.exit(1)
    return _model


def compute_embedding(sentence: str) -> np.ndarray:
    """
    Computes the embedding vector for a sentence.

    Args:
        sentence: The input sentence

    Returns:
        Numpy array containing the embedding vector
    """
    model = get_model()
    embedding = model.encode(sentence)
    return embedding


def compute_embeddings_batch(sentences: list) -> list:
    """
    Computes embeddings for a batch of sentences.

    Args:
        sentences: List of input sentences

    Returns:
        List of numpy arrays containing embedding vectors
    """
    model = get_model()
    embeddings = model.encode(sentences)
    return embeddings


def cosine_distance(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Computes the cosine distance between two embeddings.

    Cosine distance = 1 - cosine similarity
    Range: [0, 2], where 0 means identical and 2 means opposite

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        The cosine distance between the two embeddings
    """
    cosine_similarity = np.dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))
    return 1 - cosine_similarity


def euclidean_distance(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Computes the Euclidean (L2) distance between two embeddings.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        The Euclidean distance between the two embeddings
    """
    return norm(embedding1 - embedding2)


def semantic_similarity(sentence1: str, sentence2: str, distance_metric: str = 'cosine') -> float:
    """
    Computes the semantic distance between two sentences.

    Args:
        sentence1: First sentence
        sentence2: Second sentence
        distance_metric: 'cosine' or 'euclidean'

    Returns:
        The semantic distance between the sentences
    """
    emb1 = compute_embedding(sentence1)
    emb2 = compute_embedding(sentence2)

    if distance_metric == 'cosine':
        return cosine_distance(emb1, emb2)
    elif distance_metric == 'euclidean':
        return euclidean_distance(emb1, emb2)
    else:
        raise ValueError(f"Unknown distance metric: {distance_metric}")
