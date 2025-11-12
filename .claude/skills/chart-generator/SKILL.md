---
name: chart-generator
description: Creates charts and visualizations showing the relationship between spelling errors and semantic distance. Use when you need to visualize experimental results.
allowed-tools: Bash, Read, Write
---

# Chart Generator Skill

This skill creates professional charts and visualizations for displaying experimental results, particularly for the translation semantic drift experiment.

## Instructions

To generate charts:
1. Accept experimental data (typo rates and semantic distances)
2. Use matplotlib to create professional visualizations
3. Save charts to the specified output path
4. Optionally display charts interactively

## Chart Types

### 1. Simple Typo vs Distance Plot
Shows the relationship between spelling error rate (x-axis) and semantic distance (y-axis).

### 2. Detailed Analysis Plot
Multi-panel visualization showing both line plot and bar chart distribution.

### 3. Results Table
CSV export of experimental results for further analysis.

## Python Code Usage

```python
import sys
sys.path.append('.claude/skills/chart-generator')
from chart_utils import (
    plot_typo_vs_distance,
    plot_detailed_analysis,
    save_results_table
)

# Example data
typo_rates = [0.0, 0.10, 0.15, 0.20, 0.25]
distances = [0.45, 0.52, 0.58, 0.63, 0.68]

# Generate simple plot
plot_typo_vs_distance(
    typo_rates=typo_rates,
    distances=distances,
    output_path='results/semantic_drift.png',
    show=True
)

# Generate detailed analysis
results = {
    'typo_rates': typo_rates,
    'distances': distances,
    'original_sentences': [...],
    'final_sentences': [...]
}

plot_detailed_analysis(
    results_dict=results,
    output_path='results/detailed_analysis.png'
)

# Save results table
save_results_table(
    results_dict=results,
    output_path='results/results.csv'
)
```

## Chart Features

- **Professional styling**: Clean, publication-ready appearance
- **Value annotations**: Distance values labeled on data points
- **Grid lines**: Easy-to-read grid overlay
- **High resolution**: 300 DPI output for presentations
- **Customizable**: Colors, sizes, and labels can be modified

## Usage Example

Input data:
```python
typo_rates = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25]
distances = [0.42, 0.48, 0.54, 0.60, 0.65, 0.70]
```

Output:
- PNG chart saved to specified path
- X-axis: "Percentage of Spelling Errors in Initial Sentence (%)"
- Y-axis: "Semantic Distance (Cosine Distance)"
- Title: "Effect of Spelling Errors on Multi-Translation Semantic Drift"

## Output Formats

- **PNG**: Raster image, good for presentations and documents
- **CSV**: Tabular data export for Excel or further analysis
- **Interactive**: Can display plot windows when `show=True`

## Functions Available

1. `plot_typo_vs_distance(typo_rates, distances, output_path, show)` - Basic line plot
2. `plot_detailed_analysis(results_dict, output_path, show)` - Multi-panel visualization
3. `save_results_table(results_dict, output_path)` - Export to CSV

## Notes

- Requires `matplotlib` and `numpy` packages
- Creates output directories automatically if they don't exist
- Charts are closed after saving to free memory
- Can be used for both interactive exploration and batch processing
