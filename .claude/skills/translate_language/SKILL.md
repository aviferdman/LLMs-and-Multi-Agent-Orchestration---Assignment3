# Translation Skill

Translates text between languages using Google Translate API.

## Description

This skill provides language translation capabilities using the `deep-translator` library. It supports translation between multiple languages and handles text with spelling errors gracefully.

## Invocation

This skill is invoked by saying "translate" or when translation is needed.

## Usage

When this skill is active, you can:

1. **Translate text** between any supported languages
2. **Handle noisy input** (text with spelling errors)
3. **Support multiple language pairs**

## Supported Languages

- **English** (en)
- **French** (fr)
- **Spanish** (es)
- **Hebrew** (he)
- **German** (de)
- **Italian** (it)
- **Portuguese** (pt)
- **Russian** (ru)
- **Japanese** (ja)
- **Chinese** (zh)
- And many more...

## Examples

### Example 1: Simple Translation

User: "Translate 'Hello world' to French"
You:
```python
from deep_translator import GoogleTranslator
text = "Hello world"
translation = GoogleTranslator(source='en', target='fr').translate(text)
print(translation)  # "Bonjour le monde"
```

### Example 2: Translation with Typos

User: "Translate 'The quik brown fox' from English to Spanish"
You:
```python
from deep_translator import GoogleTranslator
text = "The quik brown fox"  # Contains typo
translation = GoogleTranslator(source='en', target='es').translate(text)
print(translation)  # "El zorro marrón rápido" (handles typo gracefully)
```

### Example 3: Multi-hop Translation Chain

User: "Translate 'Good morning' from English to French, then to Spanish"
You:
```python
from deep_translator import GoogleTranslator

original = "Good morning"

# Hop 1: English to French
french = GoogleTranslator(source='en', target='fr').translate(original)
print(f"French: {french}")  # "Bonjour"

# Hop 2: French to Spanish
spanish = GoogleTranslator(source='fr', target='es').translate(french)
print(f"Spanish: {spanish}")  # "Buenos días"
```

### Example 4: Translation for File-based Communication

User: "Read from /tmp/input.txt, translate to Hebrew, save to /tmp/output.txt"
You:
```python
from deep_translator import GoogleTranslator

# Read input
with open('/tmp/input.txt', 'r', encoding='utf-8') as f:
    text = f.read().strip()

# Translate
translation = GoogleTranslator(source='en', target='he').translate(text)

# Write output
with open('/tmp/output.txt', 'w', encoding='utf-8') as f:
    f.write(translation)

print(f"Translated and saved: {translation}")
```

## Important Notes

- **Encoding**: Always use UTF-8 encoding for files (especially for Hebrew, Arabic, Chinese, etc.)
- **Rate Limiting**: Google Translate may rate-limit requests; add delays if translating many texts
- **Error Handling**: Translations can fail; always wrap in try-except blocks
- **Typo Resilience**: The API handles common spelling errors reasonably well

## Best Practices

1. **Use appropriate language codes**: 'en', 'fr', 'es', 'he', etc.
2. **Handle errors gracefully**: Network issues or API limits can cause failures
3. **Preserve formatting**: Be careful with newlines and special characters
4. **Test with edge cases**: Very short text, very long text, special characters

## Error Handling Example

```python
from deep_translator import GoogleTranslator
import time

def safe_translate(text, source='en', target='fr', retries=3):
    """Translate with retry logic."""
    for attempt in range(retries):
        try:
            translator = GoogleTranslator(source=source, target=target)
            result = translator.translate(text)
            return result
        except Exception as e:
            print(f"Translation attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(1)  # Wait before retry
            else:
                raise
    return None
```

## Dependencies

- `deep-translator` - Main translation library
- Internet connection required

## Limitations

- Requires internet connectivity
- Free tier has rate limits
- Translation quality depends on Google Translate's capabilities
- Some languages may have better support than others

When using this skill, leverage the `deep-translator` library and handle text robustly.
