# ADR-003: Translation Chain Design - English → French → Italian → English

## Status
**Accepted** - November 2025

## Context
The semantic drift experiment requires a multi-hop translation chain that introduces progressive semantic degradation while demonstrating multi-agent coordination. We need to select:
- The number of translation hops
- The specific languages in the chain
- The direction of translation (circular vs. linear)
- The complexity level appropriate for academic demonstration

## Decision
We will implement a **3-hop circular translation chain**: **English → French → Italian → English**

## Translation Chain Specification

### Language Sequence
```
Input:  English (with typos)
Hop 1:  English → French    (translator_1 agent)
Hop 2:  French → Italian    (translator_2 agent)  
Hop 3:  Italian → English   (translator_3 agent)
Output: English (potentially degraded)
```

### Agent Mapping
```
translator_1.claude: EN → FR specialist
translator_2.claude: FR → IT specialist
translator_3.claude: IT → EN specialist

Each agent:
- Has single language pair responsibility
- Operates autonomously
- Validates input language
- Provides quality metrics
```

## Rationale

### Language Selection Criteria

**French (Hop 1)**
- High-quality translation from English
- Rich grammatical structure
- Well-supported by Claude LLM
- Similar alphabet (easier typo handling)

**Italian (Hop 2)**  
- Romance language like French (smooth transition)
- Different grammatical patterns from French
- Introduces additional semantic drift
- Good Claude LLM support

**Return to English (Hop 3)**
- Enables direct semantic comparison with original
- Familiar language for result interpretation
- Completes the circular translation loop

### Chain Length Justification

**3 Hops (Chosen)**
- Sufficient complexity for semantic drift demonstration
- Manageable execution time (~30 seconds total)
- Clear multi-agent coordination
- Academic project appropriate scope

### Compared Alternatives

**Alternative 1: 2-hop chain (EN → FR → EN)**
- Pros: Simpler, faster execution
- Cons: Insufficient complexity, limited semantic drift
- Rejected: Too simple for multi-agent demonstration

**Alternative 2: Extended chain (EN → FR → IT → DE → EN)**
- Pros: More complex, greater drift potential
- Cons: Longer execution, diminishing research value
- Rejected: Execution time too long for interactive use

**Alternative 3: Linear chain (EN → FR → IT)**
- Pros: No return translation needed
- Cons: Can't directly compare with original English
- Rejected: Makes semantic distance calculation impossible

**Alternative 4: Multiple parallel chains**
- Pros: Could compare different language paths
- Cons: Much more complex, resource intensive
- Rejected: Beyond scope of assignment requirements

### Language Alternatives Considered

**German instead of French**
- Pros: Different language family, more structural differences
- Cons: More complex grammar might break with typos
- Rejected: May cause translation failures rather than gradual drift

**German instead of Italian**
- Pros: Different language family, more semantic distance potential
- Cons: Too different from French, less smooth transition
- Rejected: May increase error rates rather than semantic drift

**Chinese/Japanese instead of Italian**
- Pros: Maximum linguistic distance, interesting semantic challenges
- Cons: Different writing systems, potential character encoding issues
- Rejected: Too complex for typo injection and analysis

## Implementation Strategy

### Quality Control
```python
# Each agent validates input language
def validate_input_language(text, expected_lang):
    detected = language_detector.detect(text)
    if detected != expected_lang:
        raise ValidationError(f"Expected {expected_lang}, got {detected}")
```

### Error Handling
```python
# Graceful degradation for translation failures
def translate_with_fallback(text, source_lang, target_lang):
    try:
        return primary_translation(text, source_lang, target_lang)
    except TranslationError:
        return fallback_translation(text, source_lang, target_lang)
```

### Performance Optimization
```python
# Parallel agent execution where possible
async def execute_translation_chain(input_text):
    # Sequential execution required for dependency chain
    fr_result = await translator_1.translate(input_text)
    it_result = await translator_2.translate(fr_result)
    en_result = await translator_3.translate(it_result)
    return en_result
```

## Expected Semantic Drift Patterns

### Linguistic Phenomena
1. **Vocabulary Shifts**: Words may change meaning through translation
2. **Grammatical Restructuring**: Sentence structure adapts to each language
3. **Idiomatic Loss**: Expressions may lose cultural meaning
4. **Typo Amplification**: Spelling errors may compound through chain

### Drift Measurement
```python
# Semantic distance calculation
original_embedding = model.encode(original_english)
final_embedding = model.encode(translated_english)
drift = cosine_distance(original_embedding, final_embedding)

# Expected ranges:
# 0% typos: 0.1-0.3 (minimal drift)
# 25% typos: 0.3-0.5 (moderate drift)  
# 50% typos: 0.5-0.8 (significant drift)
```

## Quality Assurance

### Translation Validation
- Language detection at each hop
- Minimum/maximum length checks
- Character encoding validation
- Semantic coherence scoring

### Chain Integrity
- File format validation between hops
- Timestamp tracking for performance analysis
- Error propagation prevention
- Recovery from partial failures

## Performance Characteristics

### Execution Timing
```
translator_1 (EN→FR): ~8 seconds
translator_2 (FR→IT): ~8 seconds  
translator_3 (IT→EN): ~8 seconds
Total chain time: ~25 seconds
File I/O overhead: ~5 seconds
```

### Resource Usage
```
Memory: Constant per agent (~100MB each)
CPU: Sequential spikes during translation
Storage: ~5KB per intermediate file
Network: None (local Claude translation)
```

## Risk Assessment

### Translation Quality Risks
- **Risk**: Poor translation breaks semantic chain
- **Mitigation**: Quality validation, fallback strategies
- **Impact**: Medium - affects research validity

### Performance Risks
- **Risk**: Chain execution too slow for interactive use
- **Mitigation**: Optimize file I/O, parallel preparation
- **Impact**: Low - still within acceptable bounds

### Scalability Risks
- **Risk**: Adding more languages becomes unwieldy
- **Mitigation**: Modular agent design enables easy extension
- **Impact**: Low - current scope sufficient

## Validation Strategy

### Correctness Testing
```python
# Test with known translation pairs
test_cases = [
    "The quick brown fox jumps over the lazy dog",
    "To be or not to be, that is the question",
    "All human beings are born free and equal",
]

for test_input in test_cases:
    result = execute_translation_chain(test_input)
    # Verify result is coherent English
    assert is_coherent_english(result)
    # Verify semantic similarity within reasonable bounds
    assert 0.1 <= semantic_distance(test_input, result) <= 0.6
```

### Typo Impact Analysis
```python
# Validate typo rate vs. drift correlation
typo_rates = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
base_sentence = "The quick brown fox jumps over the lazy dog"

for rate in typo_rates:
    corrupted = inject_typos(base_sentence, rate)
    final = execute_translation_chain(corrupted)
    drift = semantic_distance(base_sentence, final)
    
    # Expect positive correlation
    assert drift >= previous_drift  # Monotonic increase
```

## Success Metrics

### Academic Metrics
- **Multi-agent coordination**: 100% successful handoffs
- **Translation quality**: Readable output for all valid inputs
- **Semantic drift**: Clear correlation with typo rates
- **Execution reliability**: <1% failure rate for valid inputs

### Technical Metrics  
- **Performance**: <30 seconds total execution time
- **Resource efficiency**: <500MB peak memory usage
- **Error handling**: Graceful recovery from all failure modes
- **Reproducibility**: Identical results for same inputs

## Future Extensions

### Additional Language Chains
- Asian language path: EN → JP → KO → EN
- Semitic language path: EN → AR → HE → EN
- Germanic language path: EN → DE → NL → EN

### Chain Modifications
- Longer chains (4-5 hops) for extreme drift studies
- Bidirectional chains for symmetry analysis
- Parallel chains for comparative studies

## References
- Claude LLM translation capabilities documentation
- Multilingual semantic similarity benchmarks
- Translation quality evaluation methodologies
- Academic standards for translation chain experiments

---
*This ADR establishes the translation pathway that enables meaningful semantic drift measurement while maintaining system complexity appropriate for academic multi-agent demonstration.*
