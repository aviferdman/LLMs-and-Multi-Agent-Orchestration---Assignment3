---
name: typo-injector
description: Introduces spelling errors into text at a specified rate. Use when you need to corrupt text with typos for testing or analysis.
allowed-tools: Read, Write
---

# Typo Injector Skill

This skill introduces realistic spelling errors into text at a controlled rate for testing purposes using Claude's native text processing capabilities.

## Instructions

To introduce typos:
1. Accept the input text and typo rate (0.0 to 1.0) as parameters
2. Use Claude's native logic to randomly introduce spelling errors
3. Apply various typo types: substitution, deletion, duplication, and swapping
4. Write the corrupted text to `/tmp/corrupted_sentence.txt`
5. Return confirmation with the corrupted text

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

## Implementation

Use Claude's native text manipulation to:
- Iterate through each alphabetic character in the text
- Based on the typo rate, randomly decide whether to corrupt each character
- For characters to be corrupted, randomly choose one of the four typo types
- Apply the corruption and continue
- Preserve spaces and punctuation unchanged

## Usage Example

Input: "The quick brown fox jumps over the lazy dog"
Typo Rate: 0.25 (25%)
Possible Output: "Teh qiuck brwon fox jmps ovver teh lzy dog"

## Parameters

- `sentence` (str): The text to corrupt
- `typo_rate` (float): Percentage of characters to corrupt (0.0 = no errors, 1.0 = maximum errors)

## Output

Write the corrupted text to `/tmp/corrupted_sentence.txt` in plain text format.

## Notes

- Only alphabetic characters are corrupted; spaces and punctuation remain unchanged
- The actual number of typos introduced is proportional to the number of letters in the text
- Each invocation produces different random errors
- Useful for testing robustness of NLP systems and translation pipelines
- **NO PYTHON CODE** - Use Claude's native text processing only
