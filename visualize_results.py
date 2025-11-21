#!/usr/bin/env python3
"""
Generate visualization of semantic drift experiment results
"""
import matplotlib.pyplot as plt
import numpy as np

# Data from the experiment
typo_rates = [20, 25, 30, 35, 40, 45, 50]

# Mean distances per typo rate
mean_distances = [0.419234, 0.472238, 0.633496, 0.438959, 0.424658, 0.480778, 0.450693]

# Individual distances per typo rate
individual_data = {
    20: [0.433148, 0.439270, 0.385284],
    25: [0.593068, 0.463744, 0.359901],
    30: [0.685558, 0.824023, 0.390907],
    35: [0.307152, 0.631901, 0.377825],
    40: [0.334788, 0.294879, 0.644306],
    45: [0.533552, 0.448569, 0.460213],
    50: [0.412904, 0.543321, 0.395854]
}

# Calculate standard deviations
std_devs = [np.std(individual_data[rate]) for rate in typo_rates]

# Create figure with 4 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Multi-Agent Translation Semantic Drift Analysis\nEnglish → French → Italian → English', 
             fontsize=16, fontweight='bold')

# Subplot 1: Mean distance with error bars
ax1.errorbar(typo_rates, mean_distances, yerr=std_devs, fmt='o-', linewidth=2, 
             markersize=10, capsize=5, color='#2E86AB', ecolor='#A23B72')
ax1.axhline(y=0.3, color='green', linestyle='--', alpha=0.3, label='Low drift threshold')
ax1.axhline(y=0.6, color='red', linestyle='--', alpha=0.3, label='High drift threshold')
ax1.set_xlabel('Typo Rate (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Mean Semantic Distance', fontsize=12, fontweight='bold')
ax1.set_title('Mean Semantic Drift by Typo Rate', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_ylim(0, 0.9)

# Annotate peak
peak_idx = mean_distances.index(max(mean_distances))
ax1.annotate(f'Peak: {max(mean_distances):.3f}', 
            xy=(typo_rates[peak_idx], max(mean_distances)),
            xytext=(typo_rates[peak_idx]-5, max(mean_distances)+0.05),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=11, fontweight='bold', color='red')

# Subplot 2: Individual data points
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', '#BC4B51', '#8B5A3C']
for i, rate in enumerate(typo_rates):
    x_positions = [rate] * len(individual_data[rate])
    ax2.scatter(x_positions, individual_data[rate], s=150, alpha=0.7, 
               color=colors[i], label=f'{rate}%', edgecolors='black', linewidth=1.5)

ax2.plot(typo_rates, mean_distances, 'k--', linewidth=2, alpha=0.5, label='Mean')
ax2.set_xlabel('Typo Rate (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Semantic Distance', fontsize=12, fontweight='bold')
ax2.set_title('Individual Sentence Semantic Distances', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right', ncol=2)
ax2.set_ylim(0.2, 0.9)

# Subplot 3: Distribution histogram
all_distances = []
for distances in individual_data.values():
    all_distances.extend(distances)

ax3.hist(all_distances, bins=15, color='#2E86AB', alpha=0.7, edgecolor='black', linewidth=1.5)
ax3.axvline(x=np.mean(all_distances), color='red', linestyle='--', linewidth=2, 
           label=f'Mean: {np.mean(all_distances):.3f}')
ax3.axvline(x=np.median(all_distances), color='orange', linestyle='--', linewidth=2,
           label=f'Median: {np.median(all_distances):.3f}')
ax3.set_xlabel('Semantic Distance', fontsize=12, fontweight='bold')
ax3.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax3.set_title('Distribution of All Semantic Distances (n=21)', fontsize=14, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# Subplot 4: Box plot
box_data = [individual_data[rate] for rate in typo_rates]
bp = ax4.boxplot(box_data, labels=typo_rates, patch_artist=True, notch=True)

# Color the boxes
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax4.set_xlabel('Typo Rate (%)', fontsize=12, fontweight='bold')
ax4.set_ylabel('Semantic Distance', fontsize=12, fontweight='bold')
ax4.set_title('Distribution by Typo Rate (Box Plots)', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_ylim(0.2, 0.9)

plt.tight_layout()
plt.savefig('/Users/ariellenapadensky/LLMs-and-Multi-Agent-Orchestration---Assignment3/results/semantic_drift_analysis.png', 
            dpi=300, bbox_inches='tight')
print("✓ Visualization saved to: results/semantic_drift_analysis.png")

# Print statistics
print("\n" + "="*80)
print("EXPERIMENT STATISTICS")
print("="*80)
print(f"Total sentences tested: 21")
print(f"Typo rates: 20% - 50% (7 levels, 3 sentences each)")
print(f"Overall mean distance: {np.mean(all_distances):.4f}")
print(f"Overall std deviation: {np.std(all_distances):.4f}")
print(f"Minimum distance: {min(all_distances):.4f}")
print(f"Maximum distance: {max(all_distances):.4f}")
print(f"Range: {max(all_distances) - min(all_distances):.4f}")
print("\nKEY FINDING: Non-linear pattern with peak at 30% typos!")
print("="*80)

