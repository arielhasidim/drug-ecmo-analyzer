#!/usr/bin/env python3
"""
Example script for running drug ECMO analysis.
This demonstrates how to use the configurable DrugECMOAnalyzer.
"""

import json
from drug_ecmo_analyzer import DrugECMOAnalyzer


def run_meropenem_analysis():
    """Run analysis for meropenem - your original use case."""
    print("=== Meropenem ECMO Analysis ===")

    analyzer = DrugECMOAnalyzer(
        drug_name="meropenem",
        paper_directory="./drugs/meropenem"
    )

    # Run complete analysis for all 7 fields
    print("\nRunning complete analysis for all 7 fields...")
    all_results = analyzer.analyze_all_fields()

    # Save results
    analyzer.save_results(all_results, "meropenem_complete_analysis.json")

    print("\n=== Analysis Summary ===")
    for field_name, result in all_results.items():
        print(f"\n{field_name}:")
        # Show first 100 characters of the answer
        answer_preview = result['answer'][:100] + "..." if len(result['answer']) > 100 else result['answer']
        print(f"  {answer_preview}")

    return all_results


def run_custom_drug_analysis(drug_name: str):
    """Run analysis for any drug - demonstrates configurability."""
    print(f"=== {drug_name.title()} ECMO Analysis ===")

    analyzer = DrugECMOAnalyzer(
        drug_name=drug_name,
        paper_directory=f"./drugs/{drug_name.lower()}"
    )

    # Example: Just analyze a few key fields
    key_fields = ["Effect on ECMO", "Final Recommendation", "ECMO dosage"]

    results = {}
    for field in key_fields:
        print(f"\nAnalyzing {field}...")
        results[field] = analyzer.analyze_field(field)
        print(f"Result: {results[field]['answer']}")

    # Save partial results
    filename = f"{drug_name.lower()}_key_analysis.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {filename}")
    return results


def demonstrate_field_customization():
    """Show how to access and customize analysis fields."""
    analyzer = DrugECMOAnalyzer("example_drug")

    print("=== Available Analysis Fields ===")
    for i, (field_name, field_info) in enumerate(analyzer.analysis_fields.items(), 1):
        print(f"\n{i}. {field_name}")
        print(f"   Definition: {field_info['definition']}")
        print(f"   Structure: {field_info['structure']}")


if __name__ == "__main__":
    # Show available fields
    demonstrate_field_customization()

    # Run your original meropenem analysis
    meropenem_results = run_meropenem_analysis()

    # Example with different drugs (uncomment to test)
    # vancomycin_results = run_custom_drug_analysis("vancomycin")
    # gentamicin_results = run_custom_drug_analysis("gentamicin")

    print("\n=== Analysis Complete ===")
    print("Check the generated JSON files for detailed results.")