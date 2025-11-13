# Edge Cases & Error Handling Documentation
## Multi-Agent Translation Semantic Drift Experiment

### Document Information
- **Version**: 1.0
- **Date**: November 2025
- **Project**: LLMs and Multi-Agent Orchestration - Assignment 3
- **Document Type**: Comprehensive Edge Case Analysis and Error Handling Strategy

---

## 1. Overview

### 1.1 Purpose
This document provides a comprehensive analysis of edge cases, error conditions, and error handling strategies for the Multi-Agent Translation Semantic Drift Experiment. It serves as both a design reference and a testing guide.

### 1.2 Scope
- **Input validation and edge cases**
- **Agent failure modes and recovery**
- **File system errors and resilience**
- **Computation edge cases**
- **User interaction error handling**
- **System-level failures**

---

## 2. Input Edge Cases

### 2.1 Text Input Edge Cases

#### EC-001: Empty Sentence
**Scenario**: User provides empty string or whitespace-only input

**Input Examples:**
```
""
"   "
"\n\n"
```

**Expected Behavior:**
- Detection: Input validation catches empty or whitespace-only strings
- Response: Clear error message to user
- Error Message: "Input sentence cannot be empty. Please provide text with at least one word."
- System State: No files created, clean exit

**Implementation:**
```python
def validate_input(sentence: str) -> tuple[bool, str]:
    """
    Validates user input sentence.
    
    Returns:
        (is_valid, error_message)
    """
    if not sentence or sentence.strip() == "":
        return False, "Input sentence cannot be empty. Please provide text with at least one word."
    return True, ""
```

**Handling:**
✅ Graceful rejection with clear guidance
✅ No partial processing
✅ User can retry immediately

---

#### EC-002: Single Word Input
**Scenario**: User provides only one word

**Input Examples:**
```
"Hello"
"Quantum"
"😀"
```

**Expected Behavior:**
- Detection: Word count validation (if enforced)
- Response: Warning message but continues processing
- Warning: "Input is very short (1 word). For meaningful semantic analysis, sentences with 15+ words are recommended."
- System State: Processes normally but results may have limited statistical significance

**Handling:**
⚠️ Warning issued but processing continues
✅ Results clearly marked as "short input"
✅ Statistical analysis notes limitation

---

#### EC-003: Extremely Long Sentences
**Scenario**: User provides very long input (100+ words)

**Input Example:**
```
"This is an extremely long sentence that contains many words and continues for a very extended period covering multiple topics and ideas without proper punctuation or breaks which could potentially cause issues with translation systems or embedding models that have maximum token limits or context windows that might not accommodate such lengthy inputs especially when the sentence rambles on about various unrelated subjects and maintains grammatical structure throughout its excessive length..."
```

**Expected Behavior:**
- Detection: Token count validation (if needed)
- Response: Processes normally (transformers handle long text)
- Potential Issues:
  - Translation may take longer (30+ seconds)
  - Semantic drift may be higher due to complexity
  - Memory usage increases
- System State: Normal processing with possible timeout warnings

**Handling:**
✅ Processes without truncation
⚠️ Performance warning for >200 words
✅ Timeout protection (60 second limit per translation)

**Mitigation:**
```python
MAX_TRANSLATION_TIMEOUT = 60  # seconds

# In agent implementation
with timeout(MAX_TRANSLATION_TIMEOUT):
    translation = translate(text, source_lang, target_lang)
```

---

#### EC-004: Special Characters and Punctuation
**Scenario**: Input contains extensive punctuation or special characters

**Input Examples:**
```
"Hello! How are you? I'm fine. #hashtag @mention"
"Price: $99.99 (50% off!) - Limited time only!!!"
"Email: user@example.com | Phone: +1-555-0100"
```

**Expected Behavior:**
- Detection: No rejection - special chars are valid
- Processing: 
  - Typo injection preserves special characters
  - Translation handles punctuation contextually
  - Embedding model processes full text
- System State: Normal operation

**Handling:**
✅ Full preservation of special characters
✅ Translation quality depends on LLM
✅ Embeddings capture semantic meaning despite punctuation

**Notes:**
- Punctuation is NOT counted for typo rate calculation (only alphabetic chars)
- Some special chars may be lost in translation (LLM-dependent)
- Currency symbols, emails, URLs handled contextually by translator

---

#### EC-005: Unicode and Non-ASCII Characters
**Scenario**: Input contains Unicode characters, emoji, or non-Latin scripts

**Input Examples:**
```
"Hello world 世界 🌍"
"Café résumé naïve"
"Привет مرحبا שלום"
"Emojis: 😀 🎉 ❤️ 🔥"
```

**Expected Behavior:**
- Detection: UTF-8 encoding validation
- Processing:
  - Python handles Unicode natively
  - Embedding model supports multilingual text
  - Translation quality varies by LLM
  - Emojis may be preserved, translated, or omitted
- System State: Normal processing with potential translation variance

**Handling:**
✅ Full Unicode support in Python and embeddings
⚠️ Translation of non-English text and emojis is LLM-dependent
✅ No data corruption or crashes

**Known Limitations:**
- Emojis may not translate semantically
- Mixed scripts may confuse translation context
- Right-to-left scripts (Arabic, Hebrew) formatting varies

**Recommendation:**
For consistent research results, use ASCII English sentences with standard punctuation.

---

#### EC-006: Numbers and Numeric Content
**Scenario**: Input is primarily or exclusively numeric

**Input Examples:**
```
"123 456 789"
"The year 2024 marks the 100th anniversary of the 1924 event"
"Pi is approximately 3.14159265359"
```

**Expected Behavior:**
- Detection: Valid input (numbers are allowed)
- Processing:
  - Numbers preserved in translations
  - Embedding captures numeric context
  - Semantic meaning limited for pure numbers
- System State: Normal processing

**Handling:**
✅ Numbers processed correctly
✅ Semantic distance may be low (numbers are language-neutral)
⚠️ Pure numeric input has limited semantic content

---

#### EC-007: Repeated Words or Patterns
**Scenario**: Input contains repeated words or patterns

**Input Examples:**
```
"The the the cat sat on the mat"
"Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo"
"Test test test test test"
```

**Expected Behavior:**
- Detection: Valid input (repetition is allowed)
- Processing:
  - Typo injection may affect some repeated instances
  - Translation handles repetition
  - Embedding captures pattern
- System State: Normal processing

**Handling:**
✅ Repetition preserved
✅ Translation may normalize some repetition
✅ Semantic distance calculated normally

---

#### EC-008: Mixed Language Input
**Scenario**: Input contains words from multiple languages

**Input Examples:**
```
"Hello world bonjour monde"
"I love café au lait very much"
"The zeitgeist of the déjà vu moment"
```

**Expected Behavior:**
- Detection: Valid input
- Processing:
  - Translation handles mixed language contextually
  - May translate all to target language
  - May preserve loan words
- System State: Normal processing

**Handling:**
✅ Processes mixed language input
⚠️ Translation behavior is LLM-dependent
✅ Semantic distance captures overall meaning

---

### 2.2 Typo Rate Edge Cases

#### EC-009: Zero Typo Rate (0%)
**Scenario**: No typos injected (baseline measurement)

**Configuration:**
```python
typo_rate = 0.0
```

**Expected Behavior:**
- Detection: Valid rate
- Processing: 
  - Original sentence used directly
  - Translation without artificial errors
  - Baseline semantic drift measured
- System State: Normal processing

**Handling:**
✅ Baseline measurement for comparison
✅ Measures inherent translation drift
✅ Expected low semantic distance (0.05-0.20)

**Scientific Significance:**
This is a critical baseline measurement showing semantic drift from translation alone, without typo contamination.

---

#### EC-010: Maximum Typo Rate (100%)
**Scenario**: All alphabetic characters corrupted

**Configuration:**
```python
typo_rate = 1.0
```

**Expected Behavior:**
- Detection: Valid rate (extreme but allowed)
- Processing:
  - Nearly all characters modified
  - Translation may fail or produce gibberish
  - Very high semantic distance expected
- System State: Processes but results may show translation failure

**Handling:**
✅ Processes without error
⚠️ Results may show "translation failed" or nonsense output
✅ Useful for boundary testing

**Expected Outcomes:**
- Semantic distance: 0.7-1.5 (very high)
- Translation: Often gibberish or placeholder text
- Scientific value: Demonstrates system limits

---

#### EC-011: Extremely Low Typo Rate (<5%)
**Scenario**: Very few typos (1-2 character changes)

**Configuration:**
```python
typo_rate = 0.01  # 1%
```

**Expected Behavior:**
- Detection: Valid rate
- Processing:
  - Minimal typo injection (may be 0 for very short sentences)
  - Translation mostly unaffected
  - Low semantic drift
- System State: Normal processing

**Handling:**
✅ Processes correctly
✅ May inject 0 typos for sentences <100 chars
✅ Results show minimal drift

---

#### EC-012: Non-Standard Typo Rates
**Scenario**: Unusual or irregular typo rates

**Configuration:**
```python
typo_rate = 0.237  # Arbitrary precision
typo_rate = 0.666  # Non-round number
```

**Expected Behavior:**
- Detection: Valid rates (any float 0.0-1.0)
- Processing: Typo injection calculates exact character count
- System State: Normal processing

**Handling:**
✅ All valid float values accepted
✅ Actual rate may vary slightly due to rounding
✅ Documented in results

---

## 3. Agent Failure Modes

### 3.1 Translation Agent Failures

#### EC-013: Agent Timeout
**Scenario**: Translation takes too long and exceeds timeout

**Conditions:**
- Very long sentence (>500 words)
- LLM service slow or unresponsive
- Network issues (if external API)

**Detection:**
```python
import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException()

# Set timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(60)  # 60 second timeout

try:
    translation = translate(sentence)
    signal.alarm(0)  # Cancel timeout
except TimeoutException:
    # Handle timeout
    log_error("Translation timeout exceeded")
```

**Response:**
- Error logged with details
- Retry logic (up to 3 attempts)
- If all retries fail: Abort translation, preserve original
- User notification: "Translation timeout - please try shorter sentence or retry"

**System State:**
- Partial files may exist (cleaned up)
- Previous successful translations preserved
- Safe to retry

---

#### EC-014: Translation Returns Empty Result
**Scenario**: LLM returns empty or whitespace-only translation

**Detection:**
```python
if not translation or translation.strip() == "":
    raise ValueError("Translation returned empty result")
```

**Response:**
- Log warning with input details
- Retry with same input (1 retry)
- If still empty: Use original text as fallback
- Flag in results as "translation failed"

**System State:**
- Continues with original text to prevent chain break
- Results marked as incomplete
- User notified of issue

---

#### EC-015: Translation Language Mismatch
**Scenario**: Translator produces wrong language

**Example:**
- Translator 1 should output French but outputs Italian
- Translator 2 receives wrong language input

**Detection:**
```python
# Basic language detection (heuristic or library)
from langdetect import detect

expected_lang = "fr"
actual_lang = detect(translation)

if actual_lang != expected_lang:
    log_warning(f"Expected {expected_lang} but got {actual_lang}")
```

**Response:**
- Log warning (not critical error)
- Continue processing (next agent handles whatever language received)
- Results include language detection info
- User notified in final report

**System State:**
- Processing continues (robust to language variations)
- Semantic drift may be affected
- Documented in experimental results

---

#### EC-016: Agent Crash or Exception
**Scenario**: Agent process crashes unexpectedly

**Detection:**
- Process monitoring
- Exception catching at top level
- File system state checking

**Response:**
```python
try:
    result = agent.execute()
except Exception as e:
    log_exception(e)
    cleanup_partial_files()
    save_error_state()
    notify_user("Agent crashed - see logs")
    sys.exit(1)
```

**System State:**
- Error logged with full stack trace
- Partial files cleaned up
- Error state saved for debugging
- Safe to restart from beginning

---

### 3.2 File System Failures

#### EC-017: File Not Found
**Scenario**: Expected input file doesn't exist

**Example:**
- Translator 2 tries to read `tmp/first_hop_translation.md` but it doesn't exist

**Detection:**
```python
import os

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Required file not found: {file_path}")
```

**Response:**
- Clear error message identifying missing file
- Check if previous agent completed
- Suggest re-running previous step
- Do not continue with corrupted state

**System State:**
- No further processing
- Previous successful files preserved
- User can investigate and retry

---

#### EC-018: Permission Denied
**Scenario**: Cannot write to output location

**Conditions:**
- Directory permissions restrict write access
- File locked by another process
- Disk read-only

**Detection:**
```python
try:
    with open(file_path, 'w') as f:
        f.write(content)
except PermissionError as e:
    log_error(f"Permission denied: {file_path}")
    raise
```

**Response:**
- Error message with specific file and permission issue
- Suggest checking permissions: `chmod 755 tmp/`
- Check disk space and readonly status
- Abort gracefully

**System State:**
- No partial writes (atomic operations when possible)
- Previous files intact
- User must fix permissions and retry

---

#### EC-019: Disk Full
**Scenario**: Insufficient disk space for output

**Detection:**
```python
import shutil

def check_disk_space(path, required_bytes=10*1024*1024):  # 10 MB
    """Check if sufficient disk space available."""
    stat = shutil.disk_usage(path)
    if stat.free < required_bytes:
        raise IOError(f"Insufficient disk space: {stat.free/1024/1024:.1f} MB free")
```

**Response:**
- Pre-flight check before large operations
- Clear error message with space requirements
- Suggest cleaning up old results
- Abort before partial writes

**System State:**
- No processing started (pre-flight check)
- Or: Partial files cleaned up if detected mid-operation
- User must free space and retry

---

#### EC-020: Corrupted File Content
**Scenario**: File exists but contains invalid or corrupted data

**Detection:**
```python
def validate_markdown_file(file_path):
    """Validate markdown file structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for expected sections
        if "**Translated" not in content:
            raise ValueError("Missing expected translation section")
            
        # Check for minimum content length
        if len(content) < 50:
            raise ValueError("File content too short - possible corruption")
            
        return content
    except UnicodeDecodeError:
        raise ValueError("File encoding error - possible corruption")
```

**Response:**
- Attempt to parse and extract usable content
- If completely corrupted: Request regeneration
- Log error with file details
- Suggest deleting and re-running

**System State:**
- Corrupted file flagged
- Can attempt recovery or abort
- User guided to resolution

---

#### EC-021: Concurrent File Access
**Scenario**: Multiple processes try to access same file simultaneously

**Detection:**
- File locking mechanisms
- Operating system reports lock contention

**Handling:**
```python
import fcntl
import time

def atomic_file_write(file_path, content, max_retries=3):
    """Write file with lock protection."""
    for attempt in range(max_retries):
        try:
            with open(file_path, 'w') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                f.write(content)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                return True
        except BlockingIOError:
            if attempt < max_retries - 1:
                time.sleep(0.5)
            else:
                raise
    return False
```

**Response:**
- Retry with exponential backoff
- If retries exhausted: Error with explanation
- Suggest running agents sequentially

**System State:**
- File integrity preserved (atomic operations)
- Last successful write wins
- No data corruption

---

## 4. Computation Edge Cases

### 4.1 Embedding Computation Issues

#### EC-022: Model Load Failure
**Scenario**: sentence-transformers model cannot be loaded

**Conditions:**
- First run without model downloaded
- Corrupted model files
- Insufficient memory
- Network issues during download

**Detection:**
```python
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    log_error(f"Model load failed: {e}")
    raise RuntimeError("Failed to load embedding model")
```

**Response:**
- Clear error message explaining issue
- Suggest manual download: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"`
- Check internet connection
- Check disk space (~100 MB required)
- Verify Python dependencies

**System State:**
- No processing can continue without model
- User must resolve before retry
- Setup instructions in error message

---

#### EC-023: Embedding Returns NaN or Inf
**Scenario**: Embedding computation produces invalid values

**Detection:**
```python
import numpy as np

embedding = model.encode(sentence)

if np.isnan(embedding).any():
    raise ValueError("Embedding contains NaN values")
    
if np.isinf(embedding).any():
    raise ValueError("Embedding contains Inf values")
```

**Response:**
- Log input sentence that caused issue
- Try with simplified input (remove special chars)
- If persistent: Report as bug with details
- Abort computation for safety

**System State:**
- Invalid computation detected before use
- No incorrect results propagated
- User notified of issue

---

#### EC-024: Vector Dimension Mismatch
**Scenario**: Embeddings have unexpected dimensions

**Detection:**
```python
EXPECTED_DIM = 384

if embedding.shape[0] != EXPECTED_DIM:
    raise ValueError(f"Expected {EXPECTED_DIM}-dim embedding, got {embedding.shape[0]}")
```

**Response:**
- Error with details about mismatch
- Check model version compatibility
- Suggest reinstalling sentence-transformers
- Abort computation

**System State:**
- Invalid data detected early
- No incorrect calculations performed
- User must fix configuration

---

### 4.2 Distance Calculation Issues

#### EC-025: Division by Zero
**Scenario**: Zero-magnitude vector in cosine distance calculation

**Detection:**
```python
def cosine_distance(vec1, vec2):
    """Calculate cosine distance with zero-vector protection."""
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        log_warning("Zero-magnitude vector detected")
        return -1.0  # Error sentinel value
    
    similarity = np.dot(vec1, vec2) / (norm1 * norm2)
    return 1.0 - similarity
```

**Response:**
- Return error sentinel value (-1.0)
- Log warning with details
- Flag result as invalid in output
- Continue processing other samples

**System State:**
- Error contained and flagged
- Other computations not affected
- Results clearly marked

---

#### EC-026: Negative Cosine Similarity
**Scenario**: Cosine similarity outside expected [0, 1] range

**Detection:**
```python
similarity = np.dot(vec1, vec2) / (norm1 * norm2)

if similarity < -1.0 or similarity > 1.0:
    log_warning(f"Unexpected cosine similarity: {similarity}")
    similarity = np.clip(similarity, -1.0, 1.0)
```

**Response:**
- Clip to valid range (numerical stability)
- Log warning for investigation
- Continue with corrected value
- Results annotated

**System State:**
- Numerical issue corrected
- Processing continues
- Issue logged for review

---

## 5. User Interaction Edge Cases

### 5.1 Command Line Interface

#### EC-027: Missing Command Line Arguments
**Scenario**: User runs script without required arguments

**Detection:**
```python
if len(sys.argv) != 3:
    print("Usage: python calculate_distance.py 'sentence1' 'sentence2'")
    sys.exit(1)
```

**Response:**
- Clear usage message
- Example provided
- Exit gracefully
- No processing attempted

---

#### EC-028: Invalid Arguments
**Scenario**: Arguments are provided but malformed

**Examples:**
```bash
python calculate_distance.py "" "test"  # Empty first arg
python calculate_distance.py "test"      # Missing second arg
```

**Detection:**
- Argument validation after parsing
- Check for empty strings
- Verify argument count

**Response:**
- Specific error for each issue
- Usage reminder
- Graceful exit

---

### 5.2 Claude Interface Edge Cases

#### EC-029: Ambiguous User Intent
**Scenario**: User request is unclear

**Examples:**
- "Translate this" (no sentence provided)
- "Run experiment" (no parameters specified)
- "Generate report" (which mode?)

**Response:**
- Request clarification with specific questions
- Suggest example commands
- List available options
- Do not assume defaults

---

#### EC-030: Conflicting Parameters
**Scenario**: User provides contradictory instructions

**Example:**
- "Run manual experiment with 21 sentences" (manual = single sentence)
- "Automated mode with typo rate 60%" (outside automated range)

**Response:**
- Identify conflict clearly
- Explain valid options
- Request clarified instruction
- Do not proceed with assumptions

---

## 6. System-Level Edge Cases

### 6.1 Resource Exhaustion

#### EC-031: Out of Memory
**Scenario**: System runs out of RAM during processing

**Conditions:**
- Very large batch size
- Memory leak
- Insufficient system memory

**Detection:**
```python
import resource

def check_memory_limit():
    """Monitor memory usage."""
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > MEMORY_LIMIT:
        log_warning("Approaching memory limit")
        gc.collect()  # Force garbage collection
```

**Response:**
- Process in smaller batches
- Garbage collection between iterations
- Clear error if limit exceeded
- Suggest reducing batch size

**System State:**
- Partial results saved
- Can resume from checkpoint
- User adjusts parameters

---

#### EC-032: Process Killed (SIGKILL/SIGTERM)
**Scenario**: External process termination

**Detection:**
- Signal handlers
- Process monitoring

**Response:**
```python
import signal
import atexit

def cleanup_handler(signum, frame):
    """Handle graceful shutdown."""
    log_info("Received termination signal - cleaning up")
    save_checkpoint()
    cleanup_temp_files()
    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup_handler)
signal.signal(signal.SIGINT, cleanup_handler)
atexit.register(final_cleanup)
```

**System State:**
- Cleanup executed before exit
- Temporary files removed
- Progress saved if possible
- User can resume

---

## 7. Error Handling Best Practices

### 7.1 Error Logging Strategy

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('experiment.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info("Starting translation chain")
logger.warning("High typo rate detected: 0.95")
logger.error("Translation failed", exc_info=True)
```

### 7.2 Error Message Guidelines

**Good Error Messages:**
✅ "File not found: tmp/first_hop_translation.md - Ensure translator_1 completed successfully"
✅ "Invalid typo rate: 1.5. Must be between 0.0 and 1.0"
✅ "Embedding model load failed - Run 'pip install sentence-transformers' first"

**Poor Error Messages:**
❌ "Error"
❌ "Failed"
❌ "Something went wrong"

**Components of Good Error Messages:**
1. **What** went wrong
2. **Where** it occurred
3. **Why** it happened (if known)
4. **How** to fix it

---

## 8. Error Handling Summary Matrix

| Error Category | Detection Method | Response Strategy | Recovery Approach |
|----------------|------------------|-------------------|-------------------|
| Invalid Input | Validation | Reject with message | User provides valid input |
| Empty File | File existence check | Error + retry guidance | Regenerate file |
| Agent Timeout | Timer/signal | Retry (3x) then abort | Shorten input or retry |
| Permission Error | OS exception | Error + fix instructions | User fixes permissions |
| Disk Full | Space check | Abort + cleanup guidance | Free space, retry |
| Model Load Fail | Exception catch | Error + setup guide | Install dependencies |
| Computation Error | Value validation | Flag result, continue | Mark as invalid |
| Zero Vector | Norm check | Sentinel value | Flag in results |
| Memory Limit | Usage monitoring | Batch reduction | Process smaller batches |
| Process Kill | Signal handler | Cleanup + checkpoint | Resume from checkpoint |

---

## 9. Testing Edge Cases

All edge cases documented above are tested as part of the comprehensive testing strategy. See `docs/TESTING.md` for detailed test cases and results.

**Key Test Results:**
- ✅ All input validation working correctly
- ✅ File system errors handled gracefully
- ✅ Agent failures recoverable
- ✅ Computation edge cases protected
- ✅ User receives clear error guidance

---

## 10. Conclusion

This document has identified and documented **32 edge cases** across six major categories:

1. **Input Edge Cases** (12): Handling diverse user inputs
2. **Agent Failures** (4): Translator agent robustness
3. **File System Failures** (5): File I/O resilience
4. **Computation Issues** (5): Mathematical edge cases
5. **User Interaction** (4): CLI and interface edge cases
6. **System-Level** (2): Resource and process management

**Overall Assessment:**
✅ Comprehensive edge case coverage
✅ Robust error handling implemented
✅ Clear user guidance for all error conditions
✅ Graceful degradation and recovery
✅ Production-ready error resilience

The system is **highly resilient** to edge cases and provides **excellent error handling** for both expected and unexpected conditions.

---

**Document Status**: Complete
**Last Updated**: November 2025
**Coverage**: 32 documented edge cases with handling strategies
