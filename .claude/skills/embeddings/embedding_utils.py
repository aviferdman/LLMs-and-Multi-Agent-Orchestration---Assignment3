"""
Utility functions for computing embeddings and measuring semantic distance.
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.linalg import norm


# Global model instance (loaded once)
_model = None


def get_model():
    """Lazy-load the sentence transformer model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
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
