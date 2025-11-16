"""
Batch calculation of semantic distances for all 21 sentences.
Generates visualizations and statistical analysis.
"""
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Add embeddings skill to path
base_dir = Path(__file__).parent.parent  # Go up to project root
sys.path.append(str(base_dir / '.claude' / 'skills' / 'embeddings'))

from embedding_utils import compute_embedding, cosine_distance

# All 21 sentence pairs (Original, Final English Translation)
sentences = [
    # 20% Typo Rate
    {
        "id": 1,
        "typo_rate": 20,
        "original": "The quantum computer successfully solved complex optimization problems that would take classical computers thousands of years to complete.",
        "final": "The quantum computer succeeded in solving complex optimization problems that would take classical computers thousands of years to complete them.",
        "domain": "Quantum Computing"
    },
    {
        "id": 2,
        "typo_rate": 20,
        "original": "Marine biologists discovered a new species of bioluminescent jellyfish living in the deepest trenches of the Pacific Ocean.",
        "final": "Marine biologists have discovered a new species of bioluminescent jellyfish that lives in the deepest trenches of the Pacific Ocean.",
        "domain": "Marine Biology"
    },
    {
        "id": 3,
        "typo_rate": 20,
        "original": "The ancient manuscript contained detailed astronomical observations that challenged our understanding of early civilizations and their scientific capabilities.",
        "final": "The ancient manuscript contained detailed astronomical observations that called into question our understanding of early civilizations and their scientific capabilities.",
        "domain": "Archaeology"
    },
    # 25% Typo Rate
    {
        "id": 4,
        "typo_rate": 25,
        "original": "Climate scientists are developing advanced modeling techniques to predict extreme weather patterns and their potential impact on vulnerable coastal communities.",
        "final": "Climate scientists are developing advanced modeling techniques to predict extreme weather patterns and their potential impact on vulnerable coastal communities.",
        "domain": "Climate Science"
    },
    {
        "id": 5,
        "typo_rate": 25,
        "original": "The artificial intelligence system demonstrated remarkable abilities in understanding natural language context and generating coherent responses across multiple domains.",
        "final": "The artificial intelligence system has demonstrated remarkable abilities in understanding natural language context and generating coherent responses in different areas.",
        "domain": "Artificial Intelligence"
    },
    {
        "id": 6,
        "typo_rate": 25,
        "original": "Archaeologists unearthed a previously unknown temple complex that provided crucial evidence about trade routes connecting ancient Mediterranean civilizations.",
        "final": "Archaeologists have discovered a previously unknown temple complex that has provided crucial evidence about trade routes connecting ancient Mediterranean civilizations.",
        "domain": "Archaeology"
    },
    # 30% Typo Rate
    {
        "id": 7,
        "typo_rate": 30,
        "original": "Neuroscientists identified specific neural pathways responsible for memory consolidation during sleep and their importance in long-term learning processes.",
        "final": "Neuroscientists have identified specific neural pathways responsible for memory consolidation during sleep and their importance in long-term learning processes.",
        "domain": "Neuroscience"
    },
    {
        "id": 8,
        "typo_rate": 30,
        "original": "The revolutionary solar panel technology achieved unprecedented efficiency rates by incorporating nanomaterials that capture previously wasted infrared radiation.",
        "final": "The revolutionary solar panel technology has achieved unprecedented efficiency rates by incorporating nanomaterials that capture previously wasted infrared radiation.",
        "domain": "Solar Technology"
    },
    {
        "id": 9,
        "typo_rate": 30,
        "original": "Economic historians analyzed centuries of financial data to understand the underlying patterns that trigger market crashes and subsequent recovery periods.",
        "final": "Economic historians have analyzed centuries of financial data to understand the underlying patterns that trigger stock market crashes and subsequent recovery periods.",
        "domain": "Economic History"
    },
    # 35% Typo Rate
    {
        "id": 10,
        "typo_rate": 35,
        "original": "The experimental treatment showed promising results in clinical trials by targeting specific genetic mutations responsible for rare autoimmune disorders.",
        "final": "The experimental treatment has shown promising results in clinical studies by targeting specific genetic mutations responsible for rare autoimmune diseases.",
        "domain": "Medical Research"
    },
    {
        "id": 11,
        "typo_rate": 35,
        "original": "Urban planners are redesigning metropolitan transportation systems to reduce carbon emissions while improving accessibility for residents in underserved neighborhoods.",
        "final": "Urban planners are redesigning metropolitan transportation systems to reduce carbon emissions while improving accessibility for residents of underserved neighborhoods.",
        "domain": "Urban Planning"
    },
    {
        "id": 12,
        "typo_rate": 35,
        "original": "Particle physicists confirmed the existence of previously theoretical subatomic particles using data collected from billions of high-energy collisions.",
        "final": "Particle physicists have confirmed the existence of previously theoretical subatomic particles using data collected from billions of high-energy collisions.",
        "domain": "Particle Physics"
    },
    # 40% Typo Rate
    {
        "id": 13,
        "typo_rate": 40,
        "original": "The pioneering space mission will deploy autonomous robots to explore subsurface oceans on distant moons searching for signs of microbial life.",
        "final": "The pioneering space mission will deploy autonomous robots to explore subsurface oceans on distant moons in search of signs of microbial life.",
        "domain": "Space Exploration"
    },
    {
        "id": 14,
        "typo_rate": 40,
        "original": "Linguistic researchers documented the rapid evolution of communication patterns in isolated communities and their adaptation to digital communication technologies.",
        "final": "Linguistic researchers have documented the rapid evolution of communication patterns in isolated communities and their adaptation to digital communication technologies.",
        "domain": "Linguistics"
    },
    {
        "id": 15,
        "typo_rate": 40,
        "original": "Agricultural scientists developed drought-resistant crop varieties through advanced genetic engineering techniques that preserve nutritional value and yield capacity.",
        "final": "Agricultural scientists have developed drought-resistant crop varieties through advanced genetic engineering techniques that preserve nutritional value and yield capacity.",
        "domain": "Agriculture"
    },
    # 45% Typo Rate
    {
        "id": 16,
        "typo_rate": 45,
        "original": "The comprehensive environmental study revealed complex relationships between deforestation rates and regional precipitation patterns affecting biodiversity across tropical ecosystems.",
        "final": "The comprehensive environmental study has revealed complex relationships between deforestation rates and regional precipitation patterns that affect biodiversity in tropical ecosystems.",
        "domain": "Environmental Science"
    },
    {
        "id": 17,
        "typo_rate": 45,
        "original": "Renaissance art historians uncovered hidden layers beneath famous paintings that revealed significant details about artistic techniques and workshop practices.",
        "final": "Renaissance art historians have discovered hidden layers beneath famous paintings that have revealed important details about artistic techniques and workshop practices.",
        "domain": "Art History"
    },
    {
        "id": 18,
        "typo_rate": 45,
        "original": "Geologists discovered mineral formations in remote mountain ranges that indicate ancient volcanic activity and dramatic shifts in continental plate movements.",
        "final": "Geologists have discovered mineral formations in remote mountain ranges that indicate ancient volcanic activity and dramatic shifts in continental plates.",
        "domain": "Geology"
    },
    # 50% Typo Rate
    {
        "id": 19,
        "typo_rate": 50,
        "original": "The interdisciplinary research team integrated machine learning algorithms with traditional statistical methods to identify subtle correlations in massive healthcare datasets.",
        "final": "The interdisciplinary research team has integrated machine learning algorithms with traditional statistical methods to identify subtle correlations in huge healthcare datasets.",
        "domain": "Healthcare Data Science"
    },
    {
        "id": 20,
        "typo_rate": 50,
        "original": "Astronomers detected unprecedented gravitational wave signatures from merging black holes located billions of light-years away in distant galactic clusters.",
        "final": "Astronomers have detected unprecedented gravitational wave signals from merging black holes located billions of light-years away in distant galactic clusters.",
        "domain": "Astrophysics"
    },
    {
        "id": 21,
        "typo_rate": 50,
        "original": "The innovative educational program combined virtual reality simulations with hands-on experiments to enhance students understanding of complex molecular chemistry concepts.",
        "final": "The innovative educational program combined virtual reality simulations with hands-on experiments to improve students' understanding of complex molecular chemistry concepts.",
        "domain": "Educational Technology"
    }
]


def calculate_all_distances():
    """Calculate distances for all sentence pairs."""
    print("Calculating semantic distances for all 21 sentences...")
    print("=" * 80)

    results = []

    for i, sent_pair in enumerate(sentences, 1):
        print(f"\nProcessing Sentence {sent_pair['id']} ({sent_pair['typo_rate']}% typo rate)...")
        print(f"Domain: {sent_pair['domain']}")

        try:
            emb1 = compute_embedding(sent_pair['original'])
            emb2 = compute_embedding(sent_pair['final'])
            distance = cosine_distance(emb1, emb2)

            sent_pair['distance'] = distance
            results.append(sent_pair)

            print(f"Distance: {distance:.6f}")

        except Exception as e:
            print(f"ERROR: {e}")
            sent_pair['distance'] = None
            results.append(sent_pair)

    print("\n" + "=" * 80)
    print("Calculation complete!")

    return results


def generate_statistics(results):
    """Generate statistical summaries."""
    print("\n" + "=" * 80)
    print("STATISTICAL SUMMARY")
    print("=" * 80)

    # Filter out any failed calculations
    valid_results = [r for r in results if r['distance'] is not None]

    # Overall statistics
    all_distances = [r['distance'] for r in valid_results]
    print(f"\nOverall Statistics (n={len(all_distances)}):")
    print(f"  Mean Distance: {np.mean(all_distances):.6f}")
    print(f"  Std Dev: {np.std(all_distances):.6f}")
    print(f"  Min Distance: {np.min(all_distances):.6f}")
    print(f"  Max Distance: {np.max(all_distances):.6f}")
    print(f"  Median: {np.median(all_distances):.6f}")

    # By typo rate
    print("\n" + "-" * 80)
    print("Average Distance by Typo Rate:")
    print("-" * 80)

    typo_rates = [20, 25, 30, 35, 40, 45, 50]
    typo_rate_stats = {}

    for rate in typo_rates:
        rate_results = [r for r in valid_results if r['typo_rate'] == rate]
        if rate_results:
            distances = [r['distance'] for r in rate_results]
            avg_dist = np.mean(distances)
            std_dist = np.std(distances)
            typo_rate_stats[rate] = {
                'avg': avg_dist,
                'std': std_dist,
                'n': len(distances),
                'distances': distances
            }
            print(f"  {rate}%: {avg_dist:.6f} (±{std_dist:.6f}, n={len(distances)})")

    return typo_rate_stats


def create_visualizations(results, typo_rate_stats):
    """Create matplotlib visualizations."""
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)

    # Filter valid results
    valid_results = [r for r in results if r['distance'] is not None]

    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))

    # 1. Main plot: Distance vs Typo Rate with all points
    ax1 = plt.subplot(2, 2, 1)
    typo_rates = [r['typo_rate'] for r in valid_results]
    distances = [r['distance'] for r in valid_results]

    ax1.scatter(typo_rates, distances, alpha=0.6, s=100, c='steelblue', edgecolors='navy', linewidths=1.5)

    # Add trend line
    avg_rates = sorted(typo_rate_stats.keys())
    avg_distances = [typo_rate_stats[rate]['avg'] for rate in avg_rates]
    ax1.plot(avg_rates, avg_distances, 'r-', linewidth=2.5, marker='o', markersize=8, label='Average')

    ax1.set_xlabel('Typo Rate (%)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cosine Distance', fontsize=12, fontweight='bold')
    ax1.set_title('Semantic Drift vs. Typo Rate\n(All 21 Sentences)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(fontsize=10)
    ax1.set_xlim(15, 55)

    # 2. Average distance by typo rate with error bars
    ax2 = plt.subplot(2, 2, 2)
    avg_rates = sorted(typo_rate_stats.keys())
    avg_distances = [typo_rate_stats[rate]['avg'] for rate in avg_rates]
    std_distances = [typo_rate_stats[rate]['std'] for rate in avg_rates]

    ax2.errorbar(avg_rates, avg_distances, yerr=std_distances,
                 fmt='o-', linewidth=2.5, markersize=10, capsize=5, capthick=2,
                 color='darkred', ecolor='red', alpha=0.8)
    ax2.fill_between(avg_rates,
                      [avg_distances[i] - std_distances[i] for i in range(len(avg_distances))],
                      [avg_distances[i] + std_distances[i] for i in range(len(avg_distances))],
                      alpha=0.2, color='red')

    ax2.set_xlabel('Typo Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Cosine Distance', fontsize=12, fontweight='bold')
    ax2.set_title('Average Semantic Drift by Typo Rate\n(with Standard Deviation)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_xlim(15, 55)

    # 3. Distribution histogram
    ax3 = plt.subplot(2, 2, 3)
    ax3.hist(distances, bins=15, color='teal', alpha=0.7, edgecolor='black', linewidth=1.2)
    ax3.axvline(np.mean(distances), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(distances):.4f}')
    ax3.axvline(np.median(distances), color='orange', linestyle='--', linewidth=2, label=f'Median: {np.median(distances):.4f}')

    ax3.set_xlabel('Cosine Distance', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax3.set_title('Distribution of Semantic Distances\n(All Sentences)', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y', linestyle='--')

    # 4. Box plot by typo rate
    ax4 = plt.subplot(2, 2, 4)
    box_data = [typo_rate_stats[rate]['distances'] for rate in sorted(typo_rate_stats.keys())]
    box_labels = [f"{rate}%" for rate in sorted(typo_rate_stats.keys())]

    bp = ax4.boxplot(box_data, labels=box_labels, patch_artist=True,
                     boxprops=dict(facecolor='lightblue', alpha=0.7),
                     medianprops=dict(color='red', linewidth=2),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5))

    ax4.set_xlabel('Typo Rate', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Cosine Distance', fontsize=12, fontweight='bold')
    ax4.set_title('Distance Distribution by Typo Rate\n(Box Plot)', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y', linestyle='--')

    plt.tight_layout()

    # Save figure
    output_path = base_dir / 'results' / 'semantic_drift_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nVisualization saved to: {output_path}")

    return str(output_path)


def save_detailed_results(results, typo_rate_stats):
    """Save detailed numerical results to markdown."""
    output_path = base_dir / 'results' / 'quantitative_analysis.md'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Quantitative Analysis Results\n\n")
        f.write("## Individual Sentence Distances\n\n")
        f.write("| ID | Typo% | Domain | Cosine Distance | Similarity % |\n")
        f.write("|----|-------|--------|-----------------|-------------|\n")

        for r in results:
            if r['distance'] is not None:
                similarity = (1 - r['distance']) * 100
                f.write(f"| {r['id']} | {r['typo_rate']}% | {r['domain']} | {r['distance']:.6f} | {similarity:.2f}% |\n")

        f.write("\n## Summary Statistics by Typo Rate\n\n")
        f.write("| Typo Rate | Avg Distance | Std Dev | Avg Similarity | N |\n")
        f.write("|-----------|--------------|---------|----------------|---|\n")

        for rate in sorted(typo_rate_stats.keys()):
            stats = typo_rate_stats[rate]
            avg_sim = (1 - stats['avg']) * 100
            f.write(f"| {rate}% | {stats['avg']:.6f} | {stats['std']:.6f} | {avg_sim:.2f}% | {stats['n']} |\n")

        all_distances = [r['distance'] for r in results if r['distance'] is not None]
        f.write("\n## Overall Statistics\n\n")
        f.write(f"- **Total Sentences**: {len(all_distances)}\n")
        f.write(f"- **Mean Distance**: {np.mean(all_distances):.6f}\n")
        f.write(f"- **Median Distance**: {np.median(all_distances):.6f}\n")
        f.write(f"- **Std Deviation**: {np.std(all_distances):.6f}\n")
        f.write(f"- **Min Distance**: {np.min(all_distances):.6f}\n")
        f.write(f"- **Max Distance**: {np.max(all_distances):.6f}\n")
        f.write(f"- **Mean Similarity**: {(1-np.mean(all_distances))*100:.2f}%\n")

    print(f"\nDetailed results saved to: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("MULTI-HOP TRANSLATION SEMANTIC DRIFT EXPERIMENT")
    print("Batch Quantitative Analysis")
    print("=" * 80)

    # Calculate all distances
    results = calculate_all_distances()

    # Generate statistics
    typo_rate_stats = generate_statistics(results)

    # Create visualizations
    viz_path = create_visualizations(results, typo_rate_stats)

    # Save detailed results
    results_path = save_detailed_results(results, typo_rate_stats)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nGenerated files:")
    print(f"  1. Visualization: {viz_path}")
    print(f"  2. Detailed results: {results_path}")
    print("\nReview the results directory for complete analysis.\n")
