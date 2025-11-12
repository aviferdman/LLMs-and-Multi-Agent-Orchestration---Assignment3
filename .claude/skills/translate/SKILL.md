---
name: translate
description: Translates text between languages using Google Translate. Use when you need to translate text from one language to another.
allowed-tools: Bash
---

# Translate Skill

This skill translates text between different languages using the deep-translator library.

## Instructions

To translate text:
1. Accept the text to translate, source language, and target language as parameters
2. Use the deep-translator library's GoogleTranslator
3. Return the translated text

## Supported Languages

Common language codes:
- `en` - English
- `fr` - French
- `es` - Spanish
- `he` - Hebrew (עברית)
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `zh-CN` - Chinese (Simplified)
- `ja` - Japanese
- `ar` - Arabic

## Python Code Example

```python
from deep_translator import GoogleTranslator

def translate_text(text, source_lang='en', target_lang='fr'):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)
```

## Usage Example

Input: "The quick brown fox jumps over the lazy dog"
Source: English (en)
Target: French (fr)
Output: "Le rapide renard brun saute par-dessus le chien paresseux"

## Notes

- The skill requires the `deep-translator` package to be installed
- Translation quality depends on the Google Translate API
- Very long texts may need to be split into chunks
- Some languages may not preserve formatting or special characters
