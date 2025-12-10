#!/usr/bin/env python3
"""
Simple test for a single field to avoid rate limits
"""

import json
from drug_ecmo_analyzer import DrugECMOAnalyzer

def test_single_field():
    """Test just one field to verify the system works"""
    print("=== Testing Single Field Analysis ===")

    analyzer = DrugECMOAnalyzer(
        drug_name="meropenem",
        paper_directory="./drugs/meropenem"
    )

    # Test just the Effect on ECMO field
    print("Testing 'Effect on ECMO' field...")
    try:
        result = analyzer.analyze_field("Effect on ECMO")

        print("\n=== RESULTS ===")
        print(f"Answer: {result['answer']}")
        print(f"\nFormatted Answer: {result['formatted_answer']}")
        print(f"\nMetadata:")
        print(f"  Citation: {result['metadata']['exact_citation'][:100]}...")
        print(f"  Reference: {result['metadata']['reference']}")
        print(f"  Details: {result['metadata']['ref_details']}")

        # Save to file
        with open('test_single_result.json', 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\nResult saved to test_single_result.json")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_single_field()
    if success:
        print("\n✅ Single field test completed successfully!")
    else:
        print("\n❌ Single field test failed!")