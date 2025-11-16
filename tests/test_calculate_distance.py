"""
Unit tests for calculate_distance.py

Tests cover:
- Distance calculation function
- Command-line interface
- Error handling
- Integration with embedding_utils
"""
import pytest
import sys
import subprocess
from pathlib import Path
from io import StringIO

# Add scripts and embeddings to path
base_dir = Path(__file__).parent.parent
sys.path.append(str(base_dir / 'scripts'))
sys.path.append(str(base_dir / '.claude' / 'skills' / 'embeddings'))

from calculate_distance import calculate_distance


class TestCalculateDistanceFunction:
    """Tests for the calculate_distance function."""

    def test_calculate_distance_returns_float(self):
        """Should return a float value."""
        result = calculate_distance("Hello world", "Bonjour monde")
        assert isinstance(result, float)

    def test_calculate_distance_identical_sentences(self):
        """Identical sentences should have near-zero distance."""
        result = calculate_distance("Test sentence", "Test sentence")
        assert abs(result) < 1e-5

    def test_calculate_distance_similar_sentences(self):
        """Similar sentences should have small distance."""
        result = calculate_distance(
            "The cat sat on the mat",
            "A cat was sitting on the mat"
        )
        assert 0 < result < 0.5

    def test_calculate_distance_different_sentences(self):
        """Very different sentences should have larger distance."""
        result = calculate_distance(
            "The weather is sunny",
            "Quantum physics is complex"
        )
        assert result > 0.3

    def test_calculate_distance_empty_strings(self):
        """Should handle empty strings without crashing."""
        result = calculate_distance("", "")
        assert isinstance(result, float)
        assert result >= -1  # Check for error case

    def test_calculate_distance_with_punctuation(self):
        """Should handle punctuation correctly."""
        result = calculate_distance(
            "Hello, world!",
            "Hello world"
        )
        assert isinstance(result, float)
        assert result < 0.2  # Very similar despite punctuation

    def test_calculate_distance_with_numbers(self):
        """Should handle sentences with numbers."""
        result = calculate_distance(
            "There are 42 apples",
            "There are 100 apples"
        )
        assert isinstance(result, float)
        assert result < 0.5  # Similar structure, different numbers

    def test_calculate_distance_multilingual(self):
        """Should handle multilingual text."""
        result = calculate_distance(
            "Hello world",
            "Bonjour le monde"
        )
        assert isinstance(result, float)
        assert 0 < result < 1

    def test_calculate_distance_long_sentences(self):
        """Should handle long sentences."""
        long1 = "This is a very long sentence that contains many words and spans multiple clauses to test the system."
        long2 = "This is a lengthy sentence with numerous words spanning several clauses to evaluate the system."
        result = calculate_distance(long1, long2)
        assert isinstance(result, float)
        assert 0 < result < 0.5  # Similar meaning

    def test_calculate_distance_case_sensitivity(self):
        """Should be somewhat case-insensitive (semantic meaning)."""
        result = calculate_distance(
            "HELLO WORLD",
            "hello world"
        )
        assert result < 0.2  # Should be very similar


class TestCalculateDistanceCLI:
    """Tests for the command-line interface."""

    def test_cli_with_valid_arguments(self):
        """Should run successfully with valid arguments."""
        script_path = base_dir / 'scripts' / 'calculate_distance.py'
        result = subprocess.run(
            [sys.executable, str(script_path), "Hello world", "Bonjour monde"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert result.stdout.strip()  # Should produce output
        # Check if output is a valid float
        try:
            float(result.stdout.strip())
            valid_float = True
        except ValueError:
            valid_float = False
        assert valid_float

    def test_cli_no_arguments(self):
        """Should exit with error when no arguments provided."""
        script_path = base_dir / 'scripts' / 'calculate_distance.py'
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
        assert "Usage:" in result.stdout

    def test_cli_one_argument(self):
        """Should exit with error when only one argument provided."""
        script_path = base_dir / 'scripts' / 'calculate_distance.py'
        result = subprocess.run(
            [sys.executable, str(script_path), "Only one"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode != 0
        assert "Usage:" in result.stdout

    def test_cli_output_format(self):
        """Output should be a float with 6 decimal places."""
        script_path = base_dir / 'scripts' / 'calculate_distance.py'
        result = subprocess.run(
            [sys.executable, str(script_path), "Test one", "Test two"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        output = result.stdout.strip()
        # Check format: should be like "0.123456"
        parts = output.split('.')
        assert len(parts) == 2
        assert len(parts[1]) == 6  # 6 decimal places

    def test_cli_with_quotes(self):
        """Should handle sentences with quotes."""
        script_path = base_dir / 'scripts' / 'calculate_distance.py'
        result = subprocess.run(
            [sys.executable, str(script_path), 
             'She said "hello"',
             'She said hello'],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert result.stdout.strip()

    def test_cli_with_special_characters(self):
        """Should handle special characters."""
        script_path = base_dir / 'scripts' / 'calculate_distance.py'
        result = subprocess.run(
            [sys.executable, str(script_path),
             "Hello! @#$%",
             "Hello"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert result.stdout.strip()


class TestExperimentScenarios:
    """Tests simulating actual experiment scenarios."""

    def test_translation_round_trip(self):
        """Test EN->FR->IT->EN translation scenario."""
        original = "The quick brown fox jumps over the lazy dog"
        final = "The fast brown fox jumps over the lazy dog"
        
        distance = calculate_distance(original, final)
        assert isinstance(distance, float)
        assert distance >= 0
        # Small semantic shift (quick -> fast)
        assert distance < 0.5

    def test_typo_injection_20_percent(self):
        """Test with 20% typos as in experiment."""
        original = "The quantum computer successfully solved complex optimization problems"
        with_typos = "The quantum computer succesfully solved complex optimiztion problms"
        
        distance = calculate_distance(original, with_typos)
        # Should be small - typos but same meaning
        assert 0 < distance < 0.3

    def test_typo_injection_50_percent(self):
        """Test with 50% typos as in experiment."""
        original = "The weather is sunny and warm"
        with_typos = "Th wethr is suny ad wrm"
        
        distance = calculate_distance(original, with_typos)
        # Should be larger but still recognizable
        assert 0.2 < distance < 0.8

    def test_perfect_translation(self):
        """Test perfect translation (no semantic drift)."""
        original = "Hello world"
        final = "Hello world"
        
        distance = calculate_distance(original, final)
        assert abs(distance) < 1e-5

    def test_high_semantic_drift(self):
        """Test high semantic drift scenario."""
        original = "The cat sat on the mat"
        final = "Mathematics is a complex subject"
        
        distance = calculate_distance(original, final)
        assert distance > 0.7  # Very different meanings


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_none_input(self):
        """Should handle None gracefully (will convert to string)."""
        try:
            result = calculate_distance(None, "test")
            # If it doesn't crash, check for error return value
            assert result == -1.0 or isinstance(result, float)
        except (TypeError, AttributeError):
            # Expected to fail
            pass

    def test_very_long_input(self):
        """Should handle very long input."""
        long_text = "word " * 10000
        result = calculate_distance(long_text, "short text")
        assert isinstance(result, float)
        # Should either return distance or error code
        assert result >= -1.0

    def test_unicode_input(self):
        """Should handle Unicode characters."""
        result = calculate_distance("Hello 世界", "Hello world")
        assert isinstance(result, float)
        assert result >= 0

    def test_emoji_input(self):
        """Should handle emoji."""
        result = calculate_distance("Hello 😊", "Hello")
        assert isinstance(result, float)
        assert result >= 0


class TestIntegration:
    """Integration tests with embedding_utils."""

    def test_uses_correct_embedding_model(self):
        """Should use all-MiniLM-L6-v2 model."""
        from embedding_utils import get_model
        model = get_model()
        # Check model name/type indirectly through embedding dimensions
        test_emb = model.encode("test")
        assert test_emb.shape[0] == 384  # Correct model dimensions

    def test_consistent_with_direct_embedding_call(self):
        """Results should match direct embedding_utils calls."""
        from embedding_utils import compute_embedding, cosine_distance
        
        sentence1 = "Test sentence one"
        sentence2 = "Test sentence two"
        
        # Direct call
        emb1 = compute_embedding(sentence1)
        emb2 = compute_embedding(sentence2)
        direct_distance = cosine_distance(emb1, emb2)
        
        # Through calculate_distance
        function_distance = calculate_distance(sentence1, sentence2)
        
        assert abs(direct_distance - function_distance) < 1e-6


class TestPerformance:
    """Performance-related tests."""

    def test_runs_in_reasonable_time(self):
        """Should complete in reasonable time."""
        import time
        start = time.time()
        calculate_distance(
            "This is a test sentence",
            "This is another test sentence"
        )
        elapsed = time.time() - start
        assert elapsed < 5.0  # Should complete in under 5 seconds

    def test_multiple_calls_cached_model(self):
        """Subsequent calls should be faster (model cached)."""
        import time
        
        # First call (may load model)
        start1 = time.time()
        calculate_distance("First", "Second")
        time1 = time.time() - start1
        
        # Second call (model already loaded)
        start2 = time.time()
        calculate_distance("Third", "Fourth")
        time2 = time.time() - start2
        
        # Second call should not be slower (model is cached)
        # Allow some variation due to system load
        assert time2 < time1 * 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
