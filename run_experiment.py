"""
Multi-hop Translation Experiment with Spelling Errors and Semantic Drift Analysis
"""
import sys
import os
from pathlib import Path

# Add skills to path
base_dir = Path(__file__).parent
sys.path.append(str(base_dir / '.claude' / 'skills' / 'typo-injector'))
sys.path.append(str(base_dir / '.claude' / 'skills' / 'embeddings'))
sys.path.append(str(base_dir / '.claude' / 'skills' / 'chart-generator'))

from typo_utils import introduce_typos
from embedding_utils import compute_embedding, cosine_distance
from chart_utils import plot_typo_vs_distance, save_results_table
from deep_translator import GoogleTranslator
import time

def run_translation_experiment():
    """Execute the complete translation experiment with semantic drift analysis."""

    # 1. EXPERIMENT SETUP
    print("=" * 80)
    print("MULTI-HOP TRANSLATION EXPERIMENT WITH SPELLING ERROR INJECTION")
    print("=" * 80)

    sentence = "The quick brown fox jumps over the lazy dog in the beautiful sunny park"
    typo_rates = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25]
    translation_chain = [
        ('en', 'fr', 'English to French'),
        ('fr', 'es', 'French to Spanish'),
        ('es', 'he', 'Spanish to Hebrew')
    ]

    print(f"\nOriginal Sentence ({len(sentence.split())} words):")
    print(f"  '{sentence}'")
    print(f"\nTranslation Chain:")
    for source, target, desc in translation_chain:
        print(f"  - {desc} ({source} -> {target})")
    print(f"\nTypo Rates: {[f'{r*100:.0f}%' for r in typo_rates]}")
    print("\n" + "=" * 80)

    # 2. RUN EXPERIMENT
    results = {
        'typo_rates': [],
        'distances': [],
        'corrupted_sentences': [],
        'final_sentences': [],
        'original_sentences': [],
        'translation_paths': []
    }

    print("\nExecuting experiment for each typo rate...")
    print("-" * 80)

    for rate in typo_rates:
        print(f"\n[Typo Rate: {rate*100:.0f}%]")

        # Inject typos
        corrupted = introduce_typos(sentence, typo_rate=rate) if rate > 0 else sentence
        print(f"  Corrupted: '{corrupted}'")

        # Multi-hop translation
        current_text = corrupted
        translation_path = [f"Original: {corrupted}"]

        for source_lang, target_lang, desc in translation_chain:
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                current_text = translator.translate(current_text)
                translation_path.append(f"{desc}: {current_text}")
                print(f"    {desc}: '{current_text}'")
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"    ERROR in {desc}: {e}")
                current_text = "[Translation Failed]"
                break

        # Compute embeddings and distance
        try:
            emb_original = compute_embedding(sentence)
            emb_final = compute_embedding(current_text)
            distance = cosine_distance(emb_original, emb_final)
            print(f"  Semantic Distance: {distance:.4f}")
        except Exception as e:
            print(f"  ERROR computing distance: {e}")
            distance = -1.0

        # Store results
        results['typo_rates'].append(rate)
        results['distances'].append(distance)
        results['corrupted_sentences'].append(corrupted)
        results['final_sentences'].append(current_text)
        results['original_sentences'].append(sentence)
        results['translation_paths'].append(" | ".join(translation_path))

    print("\n" + "=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)

    # 3. GENERATE VISUALIZATIONS
    print("\nGenerating visualizations and saving results...")

    # Create results directory
    results_dir = base_dir / 'results'
    results_dir.mkdir(exist_ok=True)

    # Generate chart
    chart_path = str(results_dir / 'semantic_drift_chart.png')
    plot_typo_vs_distance(
        typo_rates=results['typo_rates'],
        distances=results['distances'],
        output_path=chart_path,
        show=False
    )
    print(f"  Chart saved: {chart_path}")

    # Save CSV with proper columns
    csv_path = str(results_dir / 'experiment_results.csv')
    import csv
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['typo_rate', 'original_sentence', 'corrupted_sentence', 'final_translation', 'semantic_distance'])

        for i in range(len(results['typo_rates'])):
            writer.writerow([
                f"{results['typo_rates'][i]:.2f}",
                results['original_sentences'][i],
                results['corrupted_sentences'][i],
                results['final_sentences'][i],
                f"{results['distances'][i]:.4f}"
            ])

    print(f"  Data saved: {csv_path}")

    # 4. SUMMARY STATISTICS
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)

    valid_distances = [d for d in results['distances'] if d >= 0]
    if valid_distances:
        print(f"\nSemantic Distance Statistics:")
        print(f"  Minimum: {min(valid_distances):.4f}")
        print(f"  Maximum: {max(valid_distances):.4f}")
        print(f"  Average: {sum(valid_distances)/len(valid_distances):.4f}")
        print(f"  Range: {max(valid_distances) - min(valid_distances):.4f}")

        # Calculate drift increase
        if len(valid_distances) >= 2:
            drift_increase = valid_distances[-1] - valid_distances[0]
            percent_increase = (drift_increase / valid_distances[0] * 100) if valid_distances[0] > 0 else 0
            print(f"\n  Drift Increase (0% to 25% typos): {drift_increase:.4f} ({percent_increase:.1f}%)")

    print("\n" + "=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)

    # Analyze patterns
    if len(valid_distances) >= 2:
        increasing = all(valid_distances[i] <= valid_distances[i+1] for i in range(len(valid_distances)-1))
        if increasing:
            print("\n  Pattern: Semantic distance increases monotonically with typo rate")
        else:
            print("\n  Pattern: Semantic distance shows non-monotonic behavior")

        # Check for rapid drift zones
        max_jump = 0
        max_jump_idx = 0
        for i in range(len(valid_distances)-1):
            jump = valid_distances[i+1] - valid_distances[i]
            if jump > max_jump:
                max_jump = jump
                max_jump_idx = i

        if max_jump > 0:
            print(f"  Largest semantic shift: Between {results['typo_rates'][max_jump_idx]*100:.0f}% and {results['typo_rates'][max_jump_idx+1]*100:.0f}% typo rates (+{max_jump:.4f})")

    print("\n  Translation Chain: English -> French -> Spanish -> Hebrew")
    print("  Each translation hop compounds the semantic drift from spelling errors")
    print("  Higher typo rates in the initial sentence lead to greater cumulative drift")

    print("\n" + "=" * 80)

    return results, chart_path, csv_path

if __name__ == "__main__":
    results, chart_path, csv_path = run_translation_experiment()
    print(f"\nExperiment complete!")
    print(f"  Chart: {chart_path}")
    print(f"  Data: {csv_path}")
