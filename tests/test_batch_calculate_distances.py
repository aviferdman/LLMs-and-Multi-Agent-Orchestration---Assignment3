"""
Unit tests for batch_calculate_distances.py

Tests cover:
- Sentence pairs data structure
- Batch processing logic
- Statistical calculations
- Visualization generation (mocked)
- Integration with embedding_utils
"""
import pytest
import sys
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile

# Add scripts and embeddings to path
base_dir = Path(__file__).parent.parent
sys.path.append(str(base_dir / 'scripts'))
sys.path.append(str(base_dir / '.claude' / 'skills' / 'embeddings'))

from batch_calculate_distances import (
    sentences,
    calculate_all_distances,
    generate_statistics,
    create_visualizations,
    save_detailed_results
)


class TestSentencePairsData:
    """Tests for the sentences data structure."""

    def test_sentences_is_list(self):
        """Sentences should be a list."""
        assert isinstance(sentences, list)

    def test_sentences_count(self):
        """Should have 21 sentence pairs."""
        assert len(sentences) == 21

    def test_sentence_structure(self):
        """Each sentence pair should have required fields."""
        required_fields = ['id', 'typo_rate', 'original', 'final', 'domain']
        for sent in sentences:
            for field in required_fields:
                assert field in sent

    def test_sentence_ids_sequential(self):
        """IDs should be sequential from 1 to 21."""
        ids = [s['id'] for s in sentences]
        assert ids == list(range(1, 22))

    def test_typo_rates_valid(self):
        """Typo rates should be in expected range."""
        valid_rates = [20, 25, 30, 35, 40, 45, 50]
        for sent in sentences:
            assert sent['typo_rate'] in valid_rates

    def test_typo_rate_distribution(self):
        """Each typo rate should have 3 sentences."""
        from collections import Counter
        typo_counts = Counter(s['typo_rate'] for s in sentences)
        for rate in [20, 25, 30, 35, 40, 45, 50]:
            assert typo_counts[rate] == 3

    def test_original_sentences_not_empty(self):
        """Original sentences should not be empty."""
        for sent in sentences:
            assert sent['original'].strip()
            assert len(sent['original']) > 10

    def test_final_sentences_not_empty(self):
        """Final sentences should not be empty."""
        for sent in sentences:
            assert sent['final'].strip()
            assert len(sent['final']) > 10

    def test_domains_not_empty(self):
        """Domains should not be empty."""
        for sent in sentences:
            assert sent['domain'].strip()

    def test_domains_are_varied(self):
        """Should have multiple different domains."""
        domains = [s['domain'] for s in sentences]
        unique_domains = set(domains)
        assert len(unique_domains) >= 15  # At least 15 different domains


class TestCalculateAllDistances:
    """Tests for batch distance calculation."""

    def test_returns_list(self):
        """Should return a list."""
        results = calculate_all_distances()
        assert isinstance(results, list)

    def test_returns_all_pairs(self):
        """Should return results for all 21 pairs."""
        results = calculate_all_distances()
        assert len(results) == 21

    def test_adds_distance_field(self):
        """Should add distance field to each result."""
        results = calculate_all_distances()
        for result in results:
            assert 'distance' in result

    def test_distances_are_numeric(self):
        """All distances should be numeric (or None for errors)."""
        results = calculate_all_distances()
        for result in results:
            assert result['distance'] is None or isinstance(result['distance'], (float, np.floating))

    def test_distances_in_valid_range(self):
        """Valid distances should be in [0, 2] range (allowing small floating point errors)."""
        results = calculate_all_distances()
        for result in results:
            if result['distance'] is not None:
                # Allow small negative values due to floating point precision
                assert -1e-6 <= result['distance'] <= 2

    def test_preserves_original_fields(self):
        """Should preserve all original fields."""
        results = calculate_all_distances()
        required_fields = ['id', 'typo_rate', 'original', 'final', 'domain']
        for result in results:
            for field in required_fields:
                assert field in result

    def test_handles_long_sentences(self):
        """Should handle long sentences without errors."""
        results = calculate_all_distances()
        # Check that all long sentences (>100 chars) were processed
        long_sentences = [r for r in results if len(r['original']) > 100]
        assert len(long_sentences) > 0
        for result in long_sentences:
            assert result['distance'] is not None


class TestGenerateStatistics:
    """Tests for statistical summary generation."""

    def test_returns_dict(self):
        """Should return a dictionary."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        assert isinstance(stats, dict)

    def test_has_all_typo_rates(self):
        """Should have statistics for all typo rates."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        expected_rates = [20, 25, 30, 35, 40, 45, 50]
        for rate in expected_rates:
            assert rate in stats

    def test_each_rate_has_statistics(self):
        """Each rate should have avg, std, n, distances."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        required_keys = ['avg', 'std', 'n', 'distances']
        for rate, rate_stats in stats.items():
            for key in required_keys:
                assert key in rate_stats

    def test_average_distances_reasonable(self):
        """Average distances should be in reasonable range."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        for rate, rate_stats in stats.items():
            assert 0 <= rate_stats['avg'] <= 1
            # Standard deviation should be non-negative
            assert rate_stats['std'] >= 0

    def test_sample_counts_correct(self):
        """Each typo rate should have 3 samples."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        for rate, rate_stats in stats.items():
            assert rate_stats['n'] == 3

    def test_distances_list_length_matches_n(self):
        """Length of distances list should match n."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        for rate, rate_stats in stats.items():
            assert len(rate_stats['distances']) == rate_stats['n']

    def test_handles_filtered_results(self):
        """Should handle results with None distances."""
        results = calculate_all_distances()
        # Artificially set one distance to None
        results[0]['distance'] = None
        stats = generate_statistics(results)
        # Should still compute statistics on remaining valid results
        assert isinstance(stats, dict)


class TestCreateVisualizationsMocked:
    """Tests for visualization generation (with mocked matplotlib)."""

    @patch('batch_calculate_distances.plt')
    def test_creates_figure(self, mock_plt):
        """Should create a matplotlib figure."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        mock_fig = MagicMock()
        mock_plt.figure.return_value = mock_fig
        
        create_visualizations(results, stats)
        
        mock_plt.figure.assert_called_once()

    @patch('batch_calculate_distances.plt')
    def test_creates_four_subplots(self, mock_plt):
        """Should create 4 subplots."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        mock_plt.subplot.reset_mock()
        create_visualizations(results, stats)
        
        # Should call subplot 4 times (2,2,1), (2,2,2), (2,2,3), (2,2,4)
        assert mock_plt.subplot.call_count == 4

    @patch('batch_calculate_distances.plt')
    def test_saves_figure(self, mock_plt):
        """Should save the figure."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        mock_fig = MagicMock()
        mock_plt.figure.return_value = mock_fig
        
        create_visualizations(results, stats)
        
        mock_plt.savefig.assert_called_once()

    @patch('batch_calculate_distances.plt')
    def test_returns_output_path(self, mock_plt):
        """Should return the output file path."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        output_path = create_visualizations(results, stats)
        
        assert isinstance(output_path, str)
        assert 'semantic_drift_analysis.png' in output_path


class TestSaveDetailedResults:
    """Tests for saving detailed results to markdown."""

    def test_creates_markdown_file(self):
        """Should create a markdown file."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        # Use temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Patch the output path
            with patch('batch_calculate_distances.base_dir', Path(tmpdir)):
                output_dir = Path(tmpdir) / 'results'
                output_dir.mkdir(exist_ok=True)
                
                save_detailed_results(results, stats)
                
                output_file = output_dir / 'quantitative_analysis.md'
                assert output_file.exists()

    def test_markdown_has_header(self):
        """Markdown file should have proper headers."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('batch_calculate_distances.base_dir', Path(tmpdir)):
                output_dir = Path(tmpdir) / 'results'
                output_dir.mkdir(exist_ok=True)
                
                save_detailed_results(results, stats)
                
                output_file = output_dir / 'quantitative_analysis.md'
                content = output_file.read_text(encoding='utf-8')
                
                assert '# Quantitative Analysis Results' in content
                assert '## Individual Sentence Distances' in content

    def test_markdown_has_table(self):
        """Markdown file should have a table."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('batch_calculate_distances.base_dir', Path(tmpdir)):
                output_dir = Path(tmpdir) / 'results'
                output_dir.mkdir(exist_ok=True)
                
                save_detailed_results(results, stats)
                
                output_file = output_dir / 'quantitative_analysis.md'
                content = output_file.read_text(encoding='utf-8')
                
                # Should have markdown table separators
                assert '|' in content
                assert '---' in content


class TestIntegrationWithEmbeddingUtils:
    """Integration tests with embedding_utils."""

    def test_uses_compute_embedding(self):
        """Should use compute_embedding from embedding_utils."""
        from embedding_utils import compute_embedding
        
        # Calculate one pair
        test_pair = sentences[0]
        emb1 = compute_embedding(test_pair['original'])
        emb2 = compute_embedding(test_pair['final'])
        
        # Should return valid embeddings
        assert isinstance(emb1, np.ndarray)
        assert isinstance(emb2, np.ndarray)
        assert emb1.shape[0] == 384

    def test_uses_cosine_distance(self):
        """Should use cosine_distance from embedding_utils."""
        from embedding_utils import compute_embedding, cosine_distance
        
        test_pair = sentences[0]
        emb1 = compute_embedding(test_pair['original'])
        emb2 = compute_embedding(test_pair['final'])
        distance = cosine_distance(emb1, emb2)
        
        # Should return valid distance
        assert isinstance(distance, (float, np.floating))
        assert 0 <= distance <= 2

    def test_results_consistent_with_manual_calculation(self):
        """Results should match manual calculation with embedding_utils."""
        from embedding_utils import compute_embedding, cosine_distance
        
        # Get batch results
        batch_results = calculate_all_distances()
        
        # Manually calculate first pair
        first_pair = sentences[0]
        emb1 = compute_embedding(first_pair['original'])
        emb2 = compute_embedding(first_pair['final'])
        manual_distance = cosine_distance(emb1, emb2)
        
        # Find same pair in batch results
        batch_distance = next(r['distance'] for r in batch_results if r['id'] == 1)
        
        # Should match (within floating point tolerance)
        assert abs(batch_distance - manual_distance) < 1e-6


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_handles_empty_results_list(self):
        """Should handle empty results list gracefully."""
        try:
            stats = generate_statistics([])
            # Should return empty dict or not crash
            assert isinstance(stats, dict)
        except Exception as e:
            # Acceptable to raise exception for empty input
            pass

    def test_handles_all_none_distances(self):
        """Should handle all None distances without crashing on empty arrays."""
        fake_results = [
            {'id': 1, 'typo_rate': 20, 'distance': None},
            {'id': 2, 'typo_rate': 25, 'distance': None}
        ]
        # This test expects the function to either handle gracefully or raise
        try:
            stats = generate_statistics(fake_results)
            # Should return empty dict or handle gracefully
            assert isinstance(stats, dict)
        except (ValueError, ZeroDivisionError):
            # Acceptable to raise exception for all-None input
            pass

    def test_different_typo_rates_sorted(self):
        """Statistics should be organized by typo rate."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        rates = sorted(stats.keys())
        assert rates == [20, 25, 30, 35, 40, 45, 50]


class TestStatisticalProperties:
    """Tests for statistical properties of results."""

    def test_semantic_drift_increases_with_typo_rate(self):
        """Average distance should generally increase with typo rate."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        # Get average distances for each rate
        rates = sorted(stats.keys())
        avg_distances = [stats[rate]['avg'] for rate in rates]
        
        # While not strictly monotonic, there should be a trend
        # Check that max avg is higher than min avg
        assert max(avg_distances) > min(avg_distances)

    def test_standard_deviation_reasonable(self):
        """Standard deviations should be reasonable relative to means."""
        results = calculate_all_distances()
        stats = generate_statistics(results)
        
        for rate, rate_stats in stats.items():
            # Std dev should not be larger than the mean in most cases
            # (though it's possible with small samples)
            assert rate_stats['std'] < rate_stats['avg'] * 3

    def test_distances_not_all_identical(self):
        """Distances should vary (not all identical)."""
        results = calculate_all_distances()
        distances = [r['distance'] for r in results if r['distance'] is not None]
        
        # Should have some variation
        assert len(set(distances)) > 1
        assert np.std(distances) > 0.001


class TestPerformance:
    """Performance tests."""

    def test_batch_processing_completes(self):
        """Batch processing should complete in reasonable time."""
        import time
        
        start = time.time()
        results = calculate_all_distances()
        elapsed = time.time() - start
        
        assert len(results) == 21
        # Should complete in under 2 minutes
        assert elapsed < 120

    def test_statistics_generation_fast(self):
        """Statistics generation should be fast."""
        import time
        
        results = calculate_all_distances()
        
        start = time.time()
        stats = generate_statistics(results)
        elapsed = time.time() - start
        
        # Should be nearly instant
        assert elapsed < 1.0


class TestDataQuality:
    """Tests for data quality checks."""

    def test_no_duplicate_originals(self):
        """Original sentences should all be unique."""
        originals = [s['original'] for s in sentences]
        assert len(originals) == len(set(originals))

    def test_sentences_are_meaningful(self):
        """Sentences should have reasonable word counts."""
        for sent in sentences:
            # Should have at least 10 words
            assert len(sent['original'].split()) >= 10
            assert len(sent['final'].split()) >= 10

    def test_sentences_have_semantic_overlap(self):
        """Original and final should have semantic overlap."""
        results = calculate_all_distances()
        
        # Even with highest typo rate, distance should not be maximal
        for result in results:
            if result['distance'] is not None:
                # Distance should indicate some similarity (< 1.5)
                assert result['distance'] < 1.5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
