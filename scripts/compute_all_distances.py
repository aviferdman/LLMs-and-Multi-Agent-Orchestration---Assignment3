"""
Compute semantic distances for all 21 sentence pairs.
Compares corrupted English (with typos) vs final Spanish translations.
"""
import sys
from pathlib import Path

# Add embeddings skill to path
base_dir = Path(__file__).parent
sys.path.append(str(base_dir / '.claude' / 'skills' / 'embeddings'))

from embedding_utils import compute_embedding, cosine_distance

def load_sentence_pairs():
    """Load sentence pairs from the prepared file."""
    pairs_file = base_dir / 'tmp' / 'sentence_pairs_for_analysis.txt'

    sentence_pairs = []
    with open(pairs_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '|' in line and not line.startswith('SENTENCE') and not line.startswith('Format'):
                parts = line.split('|')
                if len(parts) == 4:
                    sent_id = int(parts[0])
                    typo_rate = int(parts[1])
                    english = parts[2]
                    spanish = parts[3]
                    sentence_pairs.append({
                        'id': sent_id,
                        'typo_rate': typo_rate,
                        'english': english,
                        'spanish': spanish
                    })

    return sentence_pairs

def calculate_all_distances():
    """Calculate semantic distances for all sentence pairs."""
    print("=" * 80)
    print("SEMANTIC DISTANCE CALCULATION")
    print("Comparing: Corrupted English (with typos) vs Final Spanish (after 3 hops)")
    print("=" * 80)

    sentence_pairs = load_sentence_pairs()
    print(f"\nLoaded {len(sentence_pairs)} sentence pairs\n")

    results = []

    for pair in sentence_pairs:
        print(f"Processing Sentence {pair['id']:02d} ({pair['typo_rate']}% typo rate)...")
        print(f"  English: {pair['english'][:60]}...")
        print(f"  Spanish: {pair['spanish'][:60]}...")

        try:
            # Compute embeddings
            emb_en = compute_embedding(pair['english'])
            emb_es = compute_embedding(pair['spanish'])

            # Calculate cosine distance
            distance = cosine_distance(emb_en, emb_es)

            print(f"  Distance: {distance:.6f}\n")

            results.append({
                'id': pair['id'],
                'typo_rate': pair['typo_rate'],
                'distance': distance,
                'english': pair['english'],
                'spanish': pair['spanish']
            })

        except Exception as e:
            print(f"  ERROR: {str(e)}\n")
            results.append({
                'id': pair['id'],
                'typo_rate': pair['typo_rate'],
                'distance': None,
                'error': str(e)
            })

    return results

def calculate_statistics(results):
    """Calculate statistics by typo rate."""
    from collections import defaultdict

    by_typo_rate = defaultdict(list)

    for result in results:
        if result['distance'] is not None:
            by_typo_rate[result['typo_rate']].append(result['distance'])

    stats = {}
    for typo_rate in sorted(by_typo_rate.keys()):
        distances = by_typo_rate[typo_rate]
        stats[typo_rate] = {
            'count': len(distances),
            'mean': sum(distances) / len(distances) if distances else 0,
            'min': min(distances) if distances else 0,
            'max': max(distances) if distances else 0,
            'distances': distances
        }

    return stats

def save_results(results, stats):
    """Save results to file."""
    output_file = base_dir / 'tmp' / 'distance_results.txt'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("SEMANTIC DISTANCE RESULTS\n")
        f.write("=" * 80 + "\n\n")

        f.write("Individual Sentence Results:\n")
        f.write("-" * 80 + "\n")
        for result in results:
            if result['distance'] is not None:
                f.write(f"Sentence {result['id']:02d} | {result['typo_rate']:2d}% typos | Distance: {result['distance']:.6f}\n")
            else:
                f.write(f"Sentence {result['id']:02d} | {result['typo_rate']:2d}% typos | ERROR\n")

        f.write("\n" + "=" * 80 + "\n\n")
        f.write("Statistics by Typo Rate:\n")
        f.write("-" * 80 + "\n")

        for typo_rate in sorted(stats.keys()):
            s = stats[typo_rate]
            f.write(f"\n{typo_rate}% Typo Rate:\n")
            f.write(f"  Count: {s['count']}\n")
            f.write(f"  Mean Distance: {s['mean']:.6f}\n")
            f.write(f"  Min Distance: {s['min']:.6f}\n")
            f.write(f"  Max Distance: {s['max']:.6f}\n")
            f.write(f"  Individual: {', '.join([f'{d:.4f}' for d in s['distances']])}\n")

    print(f"\nResults saved to: {output_file}")

def print_summary(stats):
    """Print summary table."""
    print("\n" + "=" * 80)
    print("SUMMARY: Average Semantic Distance by Typo Rate")
    print("=" * 80)
    print(f"{'Typo Rate':<12} {'Count':<8} {'Mean Distance':<18} {'Min':<12} {'Max':<12}")
    print("-" * 80)

    for typo_rate in sorted(stats.keys()):
        s = stats[typo_rate]
        print(f"{typo_rate}%{'':<10} {s['count']:<8} {s['mean']:<18.6f} {s['min']:<12.6f} {s['max']:<12.6f}")

    print("=" * 80)

if __name__ == "__main__":
    results = calculate_all_distances()
    stats = calculate_statistics(results)
    save_results(results, stats)
    print_summary(stats)
    print("\nQuantitative analysis complete!")
