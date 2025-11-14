"""
Generate visualization of semantic distance vs typo rate.
"""
import matplotlib.pyplot as plt
from pathlib import Path

# Data from the analysis
typo_rates = [20, 25, 30, 35, 40, 45, 50]
mean_distances = [0.419234, 0.472238, 0.633496, 0.438959, 0.424658, 0.480778, 0.450693]

# Individual sentence distances by typo rate
individual_distances = {
    20: [0.433148, 0.439270, 0.385284],
    25: [0.593068, 0.463744, 0.359901],
    30: [0.685558, 0.824023, 0.390907],
    35: [0.307152, 0.631901, 0.377825],
    40: [0.334788, 0.294879, 0.644306],
    45: [0.533552, 0.448569, 0.460213],
    50: [0.412904, 0.543321, 0.395854]
}

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Mean distances with error bars showing range
mins = [min(individual_distances[r]) for r in typo_rates]
maxs = [max(individual_distances[r]) for r in typo_rates]
errors = [[mean_distances[i] - mins[i] for i in range(len(typo_rates))],
          [maxs[i] - mean_distances[i] for i in range(len(typo_rates))]]

ax1.errorbar(typo_rates, mean_distances, yerr=errors, fmt='o-', linewidth=2,
             markersize=10, capsize=5, capthick=2, color='#2E86AB',
             ecolor='#A23B72', label='Mean ± Range')
ax1.set_xlabel('Typo Error Percentage (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Semantic Distance (Cosine)', fontsize=12, fontweight='bold')
ax1.set_title('Mean Semantic Distance by Typo Rate\n(English → French → Italian → Spanish)',
              fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xticks(typo_rates)
ax1.legend(fontsize=11)

# Plot 2: All individual data points
colors = ['#E63946', '#F77F00', '#06A77D', '#118AB2', '#073B4C', '#A23B72', '#7209B7']
for i, rate in enumerate(typo_rates):
    distances = individual_distances[rate]
    ax2.scatter([rate] * len(distances), distances, s=150, alpha=0.7,
               color=colors[i], edgecolors='black', linewidths=1.5,
               label=f'{rate}%')

# Add mean line
ax2.plot(typo_rates, mean_distances, 'k--', linewidth=2, alpha=0.5, label='Mean Trend')

ax2.set_xlabel('Typo Error Percentage (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Semantic Distance (Cosine)', fontsize=12, fontweight='bold')
ax2.set_title('Individual Sentence Semantic Distances\n(21 Sentences Across 7 Typo Rates)',
              fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xticks(typo_rates)
ax2.legend(fontsize=9, ncol=2, title='Typo Rate', title_fontsize=10)

plt.tight_layout()

# Save figure
output_path = Path(__file__).parent / 'results' / 'semantic_drift_visualization.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Visualization saved to: {output_path}")

# Create ASCII art version for markdown
print("\nASCII Visualization:")
print("=" * 70)
print("SEMANTIC DISTANCE vs TYPO RATE")
print("=" * 70)
print(f"{'Typo %':<10} {'Mean Distance':<18} {'Visual Bar':<42}")
print("-" * 70)

max_dist = max(mean_distances)
for i, rate in enumerate(typo_rates):
    bar_length = int((mean_distances[i] / max_dist) * 40)
    bar = '█' * bar_length
    print(f"{rate:>3}%{'':<6} {mean_distances[i]:<18.6f} {bar}")

print("=" * 70)

plt.show()
