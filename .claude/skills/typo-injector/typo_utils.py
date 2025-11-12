"""
Utility functions for introducing spelling errors into text.
"""
import random
import string


def introduce_typos(sentence: str, typo_rate: float) -> str:
    """
    Introduces spelling errors into a sentence at the specified rate.

    Args:
        sentence: The input sentence
        typo_rate: Percentage of characters to corrupt (0.0 to 1.0)

    Returns:
        The sentence with introduced typos
    """
    if not sentence or typo_rate <= 0:
        return sentence

    chars = list(sentence)
    letter_indices = [i for i, c in enumerate(chars) if c.isalpha()]

    if not letter_indices:
        return sentence

    num_typos = max(1, int(len(letter_indices) * typo_rate))
    typo_positions = random.sample(letter_indices, min(num_typos, len(letter_indices)))

    typo_types = ['substitute', 'delete', 'duplicate', 'swap']

    for pos in typo_positions:
        typo_type = random.choice(typo_types)

        if typo_type == 'substitute':
            # Replace with a random letter
            chars[pos] = random.choice(string.ascii_lowercase if chars[pos].islower() else string.ascii_uppercase)

        elif typo_type == 'delete' and len(chars) > 1:
            # Delete the character
            chars[pos] = ''

        elif typo_type == 'duplicate':
            # Duplicate the character
            chars[pos] = chars[pos] * 2

        elif typo_type == 'swap' and pos < len(chars) - 1 and chars[pos + 1].isalpha():
            # Swap with next character
            chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]

    return ''.join(chars)


def generate_typo_variants(sentence: str, typo_rates: list) -> dict:
    """
    Generates multiple variants of a sentence with different typo rates.

    Args:
        sentence: The input sentence
        typo_rates: List of typo rates to generate

    Returns:
        Dictionary mapping typo rates to corrupted sentences
    """
    variants = {}
    for rate in typo_rates:
        variants[rate] = introduce_typos(sentence, rate)
    return variants
