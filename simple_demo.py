#!/usr/bin/env python3
"""
Simple demo that shows the experiment results without needing model download
This uses the pre-computed results from the experiment
"""

import json

print("="*80)
print("🎯 SEMANTIC DRIFT EXPERIMENT - INTERACTIVE DEMO")
print("="*80)
print("\nThis demo lets you explore the experiment results that were already")
print("computed. No model download needed!\n")

# Load the experiment data
sentences_data = {
    1: {
        'original': 'The ancient library contained thousands of manuscripts documenting the scientific discoveries made by scholars throughout medieval European history.',
        'corrupted': 'The ancent library contained thousands of manuscripst documenting the scientfic discoveries made by scholars througout medieval European history.',
        'typo_rate': 20,
        'distance': 0.433148,
        'topic': 'Ancient libraries'
    },
    2: {
        'original': 'Modern artificial intelligence systems require massive computational resources to process natural language and generate coherent responses effectively.',
        'corrupted': 'Modern artifical intelligence systems require massive computaional resources to process natural languae and generate coherent responses effectively.',
        'typo_rate': 20,
        'distance': 0.439270,
        'topic': 'AI systems'
    },
    8: {
        'original': 'The symphony orchestra performed an emotionally powerful interpretation of classical compositions that captivated audiences throughout the entire evening.',
        'corrupted': 'The symphny orchestra performed an emotionaly powerful interpreation of classical compositons that captvated audiences throughout the entire evening.',
        'typo_rate': 30,
        'distance': 0.824023,
        'topic': 'Symphony orchestra (HIGHEST DRIFT!)'
    },
    14: {
        'original': 'The historical novel vividly portrayed life during the industrial revolution capturing the social upheaval and technological innovations of that era.',
        'corrupted': 'The historcal novel vividy portrayd life during the industial revoluton capturng the social upheaval and technologcal inovations of that era.',
        'typo_rate': 40,
        'distance': 0.294879,
        'topic': 'Historical novel (LOWEST DRIFT!)'
    },
    19: {
        'original': 'Urban planners design sustainable transportation networks that reduce traffic congestion minimize environmental impact and improve accessibility for residents.',
        'corrupted': 'Urban planors design sustainble transportaton networs that reduce trafic congestoin minimize enviromental impact and improve accesibility for resients.',
        'typo_rate': 50,
        'distance': 0.412904,
        'topic': 'Urban planning'
    },
}

# Statistics by typo rate
stats_by_rate = {
    20: {'mean': 0.419234, 'min': 0.385284, 'max': 0.439270, 'count': 3},
    25: {'mean': 0.472238, 'min': 0.359901, 'max': 0.593068, 'count': 3},
    30: {'mean': 0.633496, 'min': 0.390907, 'max': 0.824023, 'count': 3},
    35: {'mean': 0.438959, 'min': 0.307152, 'max': 0.631901, 'count': 3},
    40: {'mean': 0.424658, 'min': 0.294879, 'max': 0.644306, 'count': 3},
    45: {'mean': 0.480778, 'min': 0.448569, 'max': 0.533552, 'count': 3},
    50: {'mean': 0.450693, 'min': 0.395854, 'max': 0.543321, 'count': 3},
}

def show_menu():
    print("\n" + "="*80)
    print("MENU OPTIONS:")
    print("="*80)
    print("1. View a sample sentence analysis")
    print("2. View statistics by typo rate")
    print("3. See the surprising finding (non-linear pattern!)")
    print("4. Compare sentences with same typo rate")
    print("5. View all 21 sentences summary")
    print("6. Quit")
    print("="*80)

def interpret_distance(distance):
    if distance < 0.35:
        return "Low drift (similar meaning)"
    elif distance < 0.5:
        return "Moderate drift (noticeable changes)"
    elif distance < 0.7:
        return "High drift (significant changes)"
    else:
        return "Severe drift (substantially altered)"

def show_sentence(sentence_id):
    data = sentences_data[sentence_id]
    print("\n" + "="*80)
    print(f"📝 SENTENCE {sentence_id} - {data['topic']}")
    print("="*80)
    print(f"\n🔤 Original:")
    print(f"   {data['original']}")
    print(f"\n❌ Corrupted ({data['typo_rate']}% typo rate):")
    print(f"   {data['corrupted']}")
    print(f"\n📊 Semantic Distance: {data['distance']:.6f}")
    print(f"📈 Interpretation: {interpret_distance(data['distance'])}")
    print("\n" + "-"*80)
    print("Translation Chain: English → French → Italian → English")
    print("-"*80)

def show_stats():
    print("\n" + "="*80)
    print("📊 STATISTICS BY TYPO RATE")
    print("="*80)
    print("\n{:<12} {:<15} {:<15} {:<15}".format("Typo Rate", "Mean Distance", "Min Distance", "Max Distance"))
    print("-"*80)
    for rate in sorted(stats_by_rate.keys()):
        stats = stats_by_rate[rate]
        marker = " 👈 PEAK!" if rate == 30 else ""
        print(f"{rate}%{' '*9} {stats['mean']:.3f}{' '*10} {stats['min']:.3f}{' '*10} {stats['max']:.3f}{marker}")
    print("="*80)

def show_finding():
    print("\n" + "="*80)
    print("🚨 SURPRISING FINDING: NON-LINEAR PATTERN!")
    print("="*80)
    print("\nWe expected: More typos → More semantic drift (linear increase)")
    print("We found: PEAK drift at 30%, then DECREASES!")
    print("\n" + "-"*80)
    print("Typo Rate  |  Mean Distance  |  Interpretation")
    print("-"*80)
    print("20%        |     0.419       |  Moderate drift")
    print("25%        |     0.472       |  Increasing...")
    print("30%        |     0.633       |  🔴 PEAK! (Highest)")
    print("35%        |     0.439       |  Recovery begins")
    print("40%        |     0.425       |  Surprisingly low")
    print("45%        |     0.481       |  Slight increase")
    print("50%        |     0.451       |  Still moderate")
    print("="*80)
    print("\n💡 WHY? LLMs act as error correctors!")
    print("   • Low typos (<25%): Easy to correct")
    print("   • Medium typos (30%): Creates ambiguity (peak drift)")
    print("   • High typos (>40%): Obviously corrupted, careful translation")
    print("="*80)

def show_comparison():
    print("\n" + "="*80)
    print("🔬 EXTREME EXAMPLES COMPARISON")
    print("="*80)
    
    print("\n🔴 HIGHEST DRIFT (0.824) - Sentence 8:")
    show_sentence(8)
    
    print("\n\n🟢 LOWEST DRIFT (0.295) - Sentence 14:")
    show_sentence(14)
    
    print("\n" + "="*80)
    print("KEY INSIGHT: Topic matters MORE than typo rate!")
    print("  • Symphony orchestra (30% typos): 0.824 drift")
    print("  • Historical novel (40% typos): 0.295 drift")
    print("  • Higher typos, but LOWER drift! Domain vocabulary matters.")
    print("="*80)

def show_all_summary():
    print("\n" + "="*80)
    print("📚 ALL 21 SENTENCES SUMMARY")
    print("="*80)
    print("\nTotal sentences tested: 21")
    print("Typo rates: 20%, 25%, 30%, 35%, 40%, 45%, 50%")
    print("Sentences per rate: 3")
    print("\nOverall Statistics:")
    print("  • Mean distance: 0.474")
    print("  • Minimum: 0.295 (Historical novel, 40% typos)")
    print("  • Maximum: 0.824 (Symphony orchestra, 30% typos)")
    print("  • Standard deviation: 0.133")
    print("\nTopics tested:")
    topics = [
        "Ancient libraries", "AI systems", "Climate science",
        "Pharmaceuticals", "Digital transformation", "Archaeology",
        "Quantum computing", "Symphony orchestra", "Sustainable agriculture",
        "Educational research", "International trade", "Renewable energy",
        "Neuroscience", "Historical novel", "Cybersecurity",
        "Wildlife conservation", "Space exploration", "Culinary tradition",
        "Urban planning", "Medical breakthrough", "Behavioral psychology"
    ]
    for i, topic in enumerate(topics, 1):
        print(f"  {i}. {topic}")
    print("\nVerification: 100% pass rate (all 21 sentences)")
    print("Average typo deviation: 1.5% (within 3% tolerance)")
    print("="*80)

# Main loop
while True:
    show_menu()
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == '1':
        print("\nAvailable sentences: 1, 2, 8 (highest), 14 (lowest), 19")
        sid = input("Enter sentence ID: ").strip()
        try:
            show_sentence(int(sid))
        except:
            print("Invalid sentence ID. Try: 1, 2, 8, 14, or 19")
    
    elif choice == '2':
        show_stats()
    
    elif choice == '3':
        show_finding()
    
    elif choice == '4':
        show_comparison()
    
    elif choice == '5':
        show_all_summary()
    
    elif choice == '6' or choice.lower() in ['quit', 'exit', 'q']:
        print("\n" + "="*80)
        print("👋 Thank you for exploring the semantic drift experiment!")
        print("="*80)
        print("\nTo see the visualization:")
        print("  open results/semantic_drift_analysis.png")
        print("\nTo read full analysis:")
        print("  cat RESULTS_EXPLANATION.md")
        print("="*80)
        break
    
    else:
        print("\n⚠️  Invalid choice. Please enter 1-6.")

