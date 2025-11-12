Run the multi-hop translation experiment with spelling errors and semantic drift analysis.

Use the translation-experiment-orchestrator agent to:
1. Accept an English sentence (approximately 15 words)
2. Create variants with different typo rates (0% to 25%)
3. Translate each variant through 3 languages: English → French → Spanish → Hebrew
4. Compute semantic embeddings for the original and final sentences
5. Measure the cosine distance between embeddings
6. Generate a chart showing typo rate (x-axis) vs semantic distance (y-axis)
7. Save results to the 'results/' directory

Default sentence: "The quick brown fox jumps over the lazy dog in the beautiful sunny park"

If the user provides a custom sentence, use that instead. The sentence should have approximately 15 words.

Translation chain: English (en) → French (fr) → Spanish (es) → Hebrew (he)
Typo rates to test: 0%, 5%, 10%, 15%, 20%, 25%
Distance metric: Cosine distance

Output files:
- results/semantic_drift_chart.png (visualization)
- results/experiment_results.csv (tabular data)

Report progress at each step and show the final chart to the user.
