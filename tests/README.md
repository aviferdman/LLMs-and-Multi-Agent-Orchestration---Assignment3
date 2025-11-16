# Test Suite for LLMs and Multi-Agent Orchestration - Assignment 3

## Overview
Comprehensive test suite for the Python scripts used in semantic distance calculations and batch experiment processing.

## Test Coverage

### 1. `test_embedding_utils.py` (38 tests)
Tests for the core embedding utility functions.

**Test Classes:**
- `TestEmbeddingComputation` (8 tests) - Tests for `compute_embedding()` function
  - Vector shape and type validation
  - Identical vs different sentence handling
  - Empty strings, special characters, Unicode, long text
  
- `TestBatchEmbedding` (5 tests) - Tests for `compute_embeddings_batch()` function
  - Batch processing correctness
  - Empty lists and single sentence handling
  
- `TestCosineDistance` (6 tests) - Tests for `cosine_distance()` function
  - Distance calculations for identical/similar/different vectors
  - Range validation [0, 2]
  - Symmetry property
  
- `TestEuclideanDistance` (4 tests) - Tests for `euclidean_distance()` function
  - Zero distance for identical vectors
  - Symmetry and triangle inequality properties
  
- `TestSemanticSimilarity` (4 tests) - Tests for `semantic_similarity()` function
  - Both cosine and euclidean metrics
  - Invalid metric handling
  
- `TestModelLoading` (2 tests) - Tests for `get_model()` function
  - Model caching behavior
  
- `TestEdgeCases` (6 tests) - Edge cases
  - Very short text, numbers only, whitespace
  - Newlines, tabs, multilingual text
  
- `TestRealWorldScenarios` (3 tests) - Real-world scenarios
  - Translation chains, typo injection, semantic drift

### 2. `test_calculate_distance.py` (30 tests)
Tests for the distance calculation CLI script.

**Test Classes:**
- `TestCalculateDistanceFunction` (10 tests) - Core function tests
  - Return type validation
  - Identical, similar, different sentences
  - Empty strings, punctuation, numbers
  - Multilingual, long sentences, case sensitivity
  
- `TestCalculateDistanceCLI` (6 tests) - Command-line interface tests
  - Valid/invalid argument handling
  - Output format validation
  - Quotes and special characters
  
- `TestExperimentScenarios` (5 tests) - Experiment simulation
  - Translation round trips
  - Typo injection at 20% and 50%
  - Perfect translation and high drift cases
  
- `TestErrorHandling` (4 tests) - Error handling
  - None input, very long input
  - Unicode and emoji handling
  
- `TestIntegration` (2 tests) - Integration with embedding_utils
  - Model verification (384 dimensions)
  - Consistency with direct embedding calls
  
- `TestPerformance` (2 tests) - Performance validation
  - Reasonable execution time (<5s)
  - Model caching effectiveness

### 3. `test_batch_calculate_distances.py` (43 tests)
Tests for the batch processing script with 21 sentence pairs.

**Test Classes:**
- `TestSentencePairsData` (10 tests) - Data structure validation
  - 21 sentence pairs with correct structure
  - Sequential IDs (1-21)
  - Typo rates (20-50% in 5% increments)
  - 3 sentences per typo rate
  - Non-empty originals, finals, domains
  - Domain variety (15+ unique domains)
  
- `TestCalculateAllDistances` (7 tests) - Batch distance calculation
  - Returns list of 21 results
  - Adds distance field
  - Numeric distances in valid range
  - Preserves original fields
  - Handles long sentences
  
- `TestGenerateStatistics` (7 tests) - Statistical summary generation
  - Dictionary return with all typo rates
  - Statistics include avg, std, n, distances
  - Reasonable averages [0, 1]
  - Correct sample counts (3 per rate)
  - Handles filtered results
  
- `TestCreateVisualizationsMocked` (4 tests) - Visualization (mocked matplotlib)
  - Figure creation
  - 4 subplots (2x2 layout)
  - Figure saving
  - Output path validation
  
- `TestSaveDetailedResults` (3 tests) - Markdown output
  - File creation
  - Proper headers
  - Table formatting
  
- `TestIntegrationWithEmbeddingUtils` (3 tests) - Integration tests
  - Uses compute_embedding and cosine_distance
  - Results consistent with manual calculation
  
- `TestEdgeCases` (3 tests) - Edge cases
  - Empty results list
  - All None distances
  - Sorted typo rates
  
- `TestStatisticalProperties` (3 tests) - Statistical validation
  - Semantic drift trend with typo rate
  - Reasonable standard deviations
  - Distance variation
  
- `TestPerformance` (2 tests) - Performance validation
  - Batch processing completes (<2 minutes)
  - Fast statistics generation (<1 second)
  
- `TestDataQuality` (3 tests) - Data quality checks
  - No duplicate originals
  - Meaningful sentences (10+ words)
  - Semantic overlap in all pairs

## Running the Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run specific test file:
```bash
pytest tests/test_embedding_utils.py -v
pytest tests/test_calculate_distance.py -v
pytest tests/test_batch_calculate_distances.py -v
```

### Run specific test class:
```bash
pytest tests/test_embedding_utils.py::TestCosineDistance -v
```

### Run with coverage:
```bash
pytest tests/ --cov=.claude/skills/embeddings --cov=scripts --cov-report=html
```

### Run with short traceback:
```bash
pytest tests/ -v --tb=short
```

## Test Results Summary

**Total Tests:** 111
**Status:** ✅ All Passing
**Execution Time:** ~90-180 seconds (depending on hardware)
**Warnings:** 10 (expected numpy warnings for edge cases with empty arrays)

### Coverage:
- `embedding_utils.py` - Comprehensive coverage of all functions
- `calculate_distance.py` - Function, CLI, integration, edge cases
- `batch_calculate_distances.py` - Data validation, computation, statistics, visualization

## Test Categories

### Unit Tests
- Individual function behavior
- Input/output validation
- Type checking
- Range validation

### Integration Tests
- Cross-module interaction
- Embedding model integration
- Distance metric consistency

### Edge Cases
- Empty inputs
- Extreme values
- Special characters
- Unicode and multilingual text
- Error conditions

### Real-World Scenarios
- Translation chains
- Typo injection
- Semantic drift measurement
- Batch processing workflows

### Performance Tests
- Execution time limits
- Model caching
- Batch processing efficiency

## Dependencies

```python
pytest>=7.0.0
numpy>=1.20.0
sentence-transformers>=2.0.0
matplotlib>=3.5.0  # For batch_calculate_distances
```

## Notes

- Tests use the actual embedding model (all-MiniLM-L6-v2) for realistic validation
- Matplotlib tests are mocked to avoid GUI dependencies
- Some tests may be slower due to model loading on first run
- Floating-point tolerances account for numerical precision (1e-6)
- CLI tests use subprocess for true end-to-end validation

## Maintenance

When adding new functionality:
1. Add corresponding unit tests
2. Update integration tests if cross-module interaction changes
3. Add edge case tests for new input types
4. Verify all 111 tests still pass
5. Update this README with new test descriptions

## Test Philosophy

Following QA engineering best practices:
- **Comprehensive Coverage:** Test happy paths, edge cases, and error conditions
- **Isolation:** Each test is independent and can run in any order
- **Clarity:** Descriptive test names and docstrings
- **Maintainability:** Organized into logical test classes
- **Real-World Validation:** Tests mirror actual usage patterns
- **Performance Aware:** Tests complete in reasonable time

---

**Last Updated:** November 16, 2025  
**Test Suite Version:** 1.0.0  
**Python Version:** 3.11+
