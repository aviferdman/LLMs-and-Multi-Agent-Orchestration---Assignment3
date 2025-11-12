"""
Utility functions for generating charts and visualizations.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def plot_typo_vs_distance(typo_rates: list, distances: list, output_path: str = None, show: bool = True):
    """
    Creates a chart showing the relationship between typo rate and semantic distance.

    Args:
        typo_rates: List of typo rates (0.0 to 1.0)
        distances: List of corresponding semantic distances
        output_path: Optional path to save the chart (e.g., 'results/chart.png')
        show: Whether to display the chart interactively
    """
    # Convert typo rates to percentages
    typo_percentages = [rate * 100 for rate in typo_rates]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(typo_percentages, distances, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    plt.xlabel('Percentage of Spelling Errors in Initial Sentence (%)', fontsize=12)
    plt.ylabel('Semantic Distance (Cosine Distance)', fontsize=12)
    plt.title('Effect of Spelling Errors on Multi-Translation Semantic Drift', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)

    # Add value labels on points
    for x, y in zip(typo_percentages, distances):
        plt.annotate(f'{y:.3f}', xy=(x, y), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=9)

    plt.tight_layout()

    # Save if path provided
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved to: {output_path}")

    # Show if requested
    if show:
        plt.show()

    plt.close()


def plot_detailed_analysis(results_dict: dict, output_path: str = None, show: bool = True):
    """
    Creates a detailed multi-panel chart showing the translation experiment results.

    Args:
        results_dict: Dictionary containing experimental results with keys:
            - 'typo_rates': List of typo rates
            - 'distances': List of semantic distances
            - 'original_sentences': List of original sentences
            - 'final_sentences': List of final translated sentences
        output_path: Optional path to save the chart
        show: Whether to display the chart interactively
    """
    typo_rates = results_dict['typo_rates']
    distances = results_dict['distances']
    typo_percentages = [rate * 100 for rate in typo_rates]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Left panel: Main plot
    ax1.plot(typo_percentages, distances, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    ax1.set_xlabel('Percentage of Spelling Errors (%)', fontsize=12)
    ax1.set_ylabel('Semantic Distance (Cosine Distance)', fontsize=12)
    ax1.set_title('Spelling Errors vs Semantic Distance', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Right panel: Distance distribution
    ax2.bar(typo_percentages, distances, width=3, color='#A23B72', alpha=0.7)
    ax2.set_xlabel('Percentage of Spelling Errors (%)', fontsize=12)
    ax2.set_ylabel('Semantic Distance', fontsize=12)
    ax2.set_title('Distance Distribution Across Error Rates', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Detailed chart saved to: {output_path}")

    if show:
        plt.show()

    plt.close()


def save_results_table(results_dict: dict, output_path: str):
    """
    Saves experimental results to a CSV file.

    Args:
        results_dict: Dictionary containing experimental results
        output_path: Path to save the CSV file
    """
    import csv

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Typo Rate (%)', 'Semantic Distance', 'Original Sentence', 'Final Sentence'])

        for i, rate in enumerate(results_dict['typo_rates']):
            writer.writerow([
                f"{rate * 100:.1f}",
                f"{results_dict['distances'][i]:.4f}",
                results_dict.get('original_sentences', [''])[i] if i < len(results_dict.get('original_sentences', [])) else '',
                results_dict.get('final_sentences', [''])[i] if i < len(results_dict.get('final_sentences', [])) else ''
            ])

    print(f"Results table saved to: {output_path}")
