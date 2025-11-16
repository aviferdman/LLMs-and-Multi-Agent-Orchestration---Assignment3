Run the multi-hop translation experiment with spelling errors and semantic drift analysis.

Use the translation-experiment-orchestrator agent to:
1. Accept an English sentence (approximately 15 words)
2. Create variants with different typo rates (20% to 50%)
3. Translate each variant through 3 languages: English → French → Italian → English
4. Compute semantic embeddings for the original and final sentences
5. Measure the cosine distance between embeddings
6. Generate a chart showing typo rate (x-axis) vs semantic distance (y-axis)
7. Save results to the 'results/' directory

Translation chain: English (en) → French (fr) → Italian (it) → English (en)
Typo rates to test: 20%, 25%, 30%, 35%, 40%, 45%, 50%
Distance metric: Cosine distance (0 = identical, 2 = opposite)

Output files:
- results/semantic_drift_analysis.png (visualization with 4 subplots)
- results/quantitative_analysis.md (statistical summary)

Report progress at each step and show the analysis to the user.
