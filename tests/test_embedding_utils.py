"""
Unit tests for embedding_utils.py

Tests cover:
- Embedding computation
- Distance calculations (cosine, euclidean)
- Batch processing
- Edge cases and error handling
"""
import pytest
import numpy as np
import sys
from pathlib import Path

# Add embeddings to path
base_dir = Path(__file__).parent.parent
sys.path.append(str(base_dir / '.claude' / 'skills' / 'embeddings'))

from embedding_utils import (
    compute_embedding,
    compute_embeddings_batch,
    cosine_distance,
    euclidean_distance,
    semantic_similarity,
    get_model
)


class TestEmbeddingComputation:
    """Tests for embedding computation functions."""

    def test_compute_embedding_returns_numpy_array(self):
        """Embedding should return a numpy array."""
        result = compute_embedding("Hello world")
        assert isinstance(result, np.ndarray)

    def test_compute_embedding_correct_dimensions(self):
        """all-MiniLM-L6-v2 produces 384-dimensional embeddings."""
        result = compute_embedding("Test sentence")
        assert result.shape == (384,)

    def test_compute_embedding_identical_sentences(self):
        """Identical sentences should produce identical embeddings."""
        emb1 = compute_embedding("The quick brown fox")
        emb2 = compute_embedding("The quick brown fox")
        np.testing.assert_array_almost_equal(emb1, emb2, decimal=6)

    def test_compute_embedding_different_sentences(self):
        """Different sentences should produce different embeddings."""
        emb1 = compute_embedding("The quick brown fox")
        emb2 = compute_embedding("A slow red dog")
        assert not np.array_equal(emb1, emb2)

    def test_compute_embedding_empty_string(self):
        """Should handle empty string gracefully."""
        result = compute_embedding("")
        assert isinstance(result, np.ndarray)
        assert result.shape == (384,)

    def test_compute_embedding_special_characters(self):
        """Should handle special characters."""
        result = compute_embedding("Hello! @#$%^&*() 123")
        assert isinstance(result, np.ndarray)
        assert result.shape == (384,)

    def test_compute_embedding_long_text(self):
        """Should handle long text."""
        long_text = "This is a very long sentence. " * 50
        result = compute_embedding(long_text)
        assert isinstance(result, np.ndarray)
        assert result.shape == (384,)

    def test_compute_embedding_unicode(self):
        """Should handle Unicode characters."""
        result = compute_embedding("Hello 世界 🌍")
        assert isinstance(result, np.ndarray)
        assert result.shape == (384,)


class TestBatchEmbedding:
    """Tests for batch embedding computation."""

    def test_compute_embeddings_batch_returns_list(self):
        """Batch embedding should return a list."""
        sentences = ["First sentence", "Second sentence", "Third sentence"]
        results = compute_embeddings_batch(sentences)
        assert isinstance(results, (list, np.ndarray))

    def test_compute_embeddings_batch_correct_count(self):
        """Should return same number of embeddings as input sentences."""
        sentences = ["One", "Two", "Three"]
        results = compute_embeddings_batch(sentences)
        assert len(results) == 3

    def test_compute_embeddings_batch_correct_dimensions(self):
        """Each embedding should have correct dimensions."""
        sentences = ["First", "Second"]
        results = compute_embeddings_batch(sentences)
        for emb in results:
            assert emb.shape == (384,)

    def test_compute_embeddings_batch_empty_list(self):
        """Should handle empty list."""
        results = compute_embeddings_batch([])
        assert len(results) == 0

    def test_compute_embeddings_batch_single_sentence(self):
        """Should handle single sentence."""
        results = compute_embeddings_batch(["Only one"])
        assert len(results) == 1
        assert results[0].shape == (384,)


class TestCosineDistance:
    """Tests for cosine distance calculation."""

    def test_cosine_distance_identical_vectors(self):
        """Distance between identical vectors should be 0."""
        emb = compute_embedding("Test sentence")
        distance = cosine_distance(emb, emb)
        assert abs(distance) < 1e-6

    def test_cosine_distance_similar_sentences(self):
        """Similar sentences should have small distance."""
        emb1 = compute_embedding("The cat sat on the mat")
        emb2 = compute_embedding("A cat was sitting on the mat")
        distance = cosine_distance(emb1, emb2)
        assert 0 <= distance < 0.5  # Should be small but not zero

    def test_cosine_distance_different_sentences(self):
        """Very different sentences should have larger distance."""
        emb1 = compute_embedding("The weather is sunny today")
        emb2 = compute_embedding("Quantum physics is complex")
        distance = cosine_distance(emb1, emb2)
        assert 0 < distance < 2  # In valid range

    def test_cosine_distance_range(self):
        """Cosine distance should be in range [0, 2]."""
        emb1 = compute_embedding("First sentence")
        emb2 = compute_embedding("Completely different sentence")
        distance = cosine_distance(emb1, emb2)
        assert 0 <= distance <= 2

    def test_cosine_distance_symmetric(self):
        """Distance should be symmetric: d(a,b) = d(b,a)."""
        emb1 = compute_embedding("Hello world")
        emb2 = compute_embedding("Bonjour monde")
        dist1 = cosine_distance(emb1, emb2)
        dist2 = cosine_distance(emb2, emb1)
        assert abs(dist1 - dist2) < 1e-6

    def test_cosine_distance_opposite_vectors(self):
        """Opposite vectors should have distance close to 2."""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([-1.0, 0.0, 0.0])
        distance = cosine_distance(vec1, vec2)
        assert abs(distance - 2.0) < 1e-6


class TestEuclideanDistance:
    """Tests for Euclidean distance calculation."""

    def test_euclidean_distance_identical_vectors(self):
        """Distance between identical vectors should be 0."""
        emb = compute_embedding("Test sentence")
        distance = euclidean_distance(emb, emb)
        assert abs(distance) < 1e-6

    def test_euclidean_distance_positive(self):
        """Euclidean distance should always be non-negative."""
        emb1 = compute_embedding("First")
        emb2 = compute_embedding("Second")
        distance = euclidean_distance(emb1, emb2)
        assert distance >= 0

    def test_euclidean_distance_symmetric(self):
        """Distance should be symmetric: d(a,b) = d(b,a)."""
        emb1 = compute_embedding("Hello")
        emb2 = compute_embedding("World")
        dist1 = euclidean_distance(emb1, emb2)
        dist2 = euclidean_distance(emb2, emb1)
        assert abs(dist1 - dist2) < 1e-6

    def test_euclidean_distance_triangle_inequality(self):
        """Triangle inequality: d(a,c) <= d(a,b) + d(b,c)."""
        emb1 = compute_embedding("First sentence")
        emb2 = compute_embedding("Second sentence")
        emb3 = compute_embedding("Third sentence")
        
        d_12 = euclidean_distance(emb1, emb2)
        d_23 = euclidean_distance(emb2, emb3)
        d_13 = euclidean_distance(emb1, emb3)
        
        assert d_13 <= d_12 + d_23 + 1e-6  # Small tolerance for floating point


class TestSemanticSimilarity:
    """Tests for the semantic_similarity function."""

    def test_semantic_similarity_cosine_default(self):
        """Should use cosine distance by default."""
        distance = semantic_similarity("Hello", "Hi")
        assert isinstance(distance, (float, np.floating))
        assert 0 <= distance < 2

    def test_semantic_similarity_euclidean(self):
        """Should work with euclidean metric."""
        distance = semantic_similarity("Hello", "Hi", distance_metric='euclidean')
        assert isinstance(distance, (float, np.floating))
        assert distance >= 0

    def test_semantic_similarity_invalid_metric(self):
        """Should raise error for invalid metric."""
        with pytest.raises(ValueError, match="Unknown distance metric"):
            semantic_similarity("Hello", "World", distance_metric='invalid')

    def test_semantic_similarity_identical_sentences(self):
        """Identical sentences should have near-zero distance."""
        distance = semantic_similarity("Test", "Test")
        assert abs(distance) < 1e-6


class TestModelLoading:
    """Tests for model loading and caching."""

    def test_get_model_returns_model(self):
        """Should return a SentenceTransformer model."""
        from sentence_transformers import SentenceTransformer
        model = get_model()
        assert isinstance(model, SentenceTransformer)

    def test_get_model_caching(self):
        """Should return the same model instance (cached)."""
        model1 = get_model()
        model2 = get_model()
        assert model1 is model2  # Same object in memory


class TestEdgeCases:
    """Tests for edge cases and robustness."""

    def test_very_short_text(self):
        """Should handle single character."""
        emb = compute_embedding("a")
        assert emb.shape == (384,)

    def test_numbers_only(self):
        """Should handle numeric text."""
        emb = compute_embedding("123456789")
        assert emb.shape == (384,)

    def test_whitespace_only(self):
        """Should handle whitespace."""
        emb = compute_embedding("   ")
        assert emb.shape == (384,)

    def test_newlines_and_tabs(self):
        """Should handle newlines and tabs."""
        emb = compute_embedding("Hello\nWorld\tTest")
        assert emb.shape == (384,)

    def test_multilingual_text(self):
        """Should handle multiple languages."""
        emb = compute_embedding("Hello Bonjour Hola 你好")
        assert emb.shape == (384,)


class TestRealWorldScenarios:
    """Tests simulating real experiment scenarios."""

    def test_translation_chain_scenario(self):
        """Simulate a translation chain from the experiment."""
        original = "The quick brown fox jumps over the lazy dog"
        final = "The fast brown fox jumps over the lazy dog"
        
        distance = semantic_similarity(original, final)
        # Should be small but not zero (words changed: quick->fast)
        assert 0 < distance < 0.3

    def test_typo_scenario(self):
        """Test with typos as in the experiment."""
        original = "The quick brown fox"
        with_typos = "The quik brown fox"  # 'quick' -> 'quik'
        
        distance = semantic_similarity(original, with_typos)
        # Should be very small (only spelling difference)
        assert distance < 0.2

    def test_high_semantic_drift(self):
        """Test completely different meanings."""
        original = "The weather is sunny and warm"
        final = "Mathematics is a difficult subject"
        
        distance = semantic_similarity(original, final)
        # Should be large (completely different topics)
        assert distance > 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
