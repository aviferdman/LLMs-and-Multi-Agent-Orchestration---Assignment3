---
name: typo-injector
description: Introduces spelling errors into text at a specified rate. Use when you need to corrupt text with typos for testing or analysis.
allowed-tools: Bash, Read
---

# Typo Injector Skill

This skill introduces realistic spelling errors into text at a controlled rate for testing purposes.

## Instructions

To introduce typos:
1. Accept the input text and typo rate (0.0 to 1.0) as parameters
2. Use the typo_utils.py helper functions in this skill directory
3. Apply various typo types: substitution, deletion, duplication, and swapping
4. Return the corrupted text

## Typo Types

The skill introduces four types of spelling errors:

1. **Substitution**: Replace a letter with a random letter
   - Example: "hello" → "hxllo"

2. **Deletion**: Remove a letter
   - Example: "hello" → "helo"

3. **Duplication**: Duplicate a letter
   - Example: "hello" → "helllo"

4. **Swap**: Swap a letter with its neighbor
   - Example: "hello" → "ehllo"

## Python Code Usage

```python
import sys
sys.path.append('.claude/skills/typo-injector')
from typo_utils import introduce_typos, generate_typo_variants

# Introduce typos at 25% rate
corrupted = introduce_typos("The quick brown fox", typo_rate=0.25)

# Generate multiple variants
variants = generate_typo_variants(
    "The quick brown fox",
    typo_rates=[0.0, 0.10, 0.25, 0.50]
)
```

## Usage Example

Input: "The quick brown fox jumps over the lazy dog"
Typo Rate: 0.25 (25%)
Possible Output: "Teh qiuck brwon fox jmps ovver teh lzy dog"

## Parameters

- `sentence` (str): The text to corrupt
- `typo_rate` (float): Percentage of characters to corrupt (0.0 = no errors, 1.0 = maximum errors)

## Notes

- Only alphabetic characters are corrupted; spaces and punctuation remain unchanged
- The actual number of typos introduced is proportional to the number of letters in the text
- Each invocation produces different random errors
- Useful for testing robustness of NLP systems and translation pipelines
