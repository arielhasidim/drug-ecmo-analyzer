#!/usr/bin/env python3
"""
Test script for refined metadata structure
"""

import json
from drug_ecmo_analyzer import DrugECMOAnalyzer

def test_refined_metadata():
    """Test the refined metadata structure with arrays"""
    print("=== Testing Refined Metadata Structure ===")

    analyzer = DrugECMOAnalyzer(
        drug_name="meropenem",
        paper_directory="./drugs/meropenem"
    )

    # Test just one field to verify the structure
    print("Testing 'Effect on ECMO' field with refined metadata...")
    try:
        result = analyzer.analyze_field("Effect on ECMO")

        print("\n=== STRUCTURE VALIDATION ===")

        # Check main structure
        expected_keys = ["answer", "formatted_answer", "metadata"]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"
            print(f"✅ {key}: Present")

        # Check metadata structure
        metadata = result["metadata"]
        expected_metadata_keys = ["exact_citation", "reference", "ref_details"]
        for key in expected_metadata_keys:
            assert key in metadata, f"Missing metadata key: {key}"
            assert isinstance(metadata[key], list), f"{key} should be a list, got {type(metadata[key])}"
            print(f"✅ metadata.{key}: List with {len(metadata[key])} items")

        print("\n=== CONTENT PREVIEW ===")

        # Show answer (raw)
        print(f"Answer (first 100 chars): {result['answer'][:100]}...")

        # Show metadata arrays
        print(f"\nExact Citations ({len(metadata['exact_citation'])} items):")
        for i, citation in enumerate(metadata['exact_citation'][:2], 1):
            print(f"  {i}. {citation[:80]}...")

        print(f"\nReferences ({len(metadata['reference'])} items):")
        for i, ref in enumerate(metadata['reference'][:2], 1):
            print(f"  {i}. {ref[:80]}...")

        print(f"\nReference Details ({len(metadata['ref_details'])} items):")
        for i, detail in enumerate(metadata['ref_details'][:2], 1):
            print(f"  {i}. {detail}")

        # Save refined result
        with open('test_refined_result.json', 'w') as f:
            json.dump(result, f, indent=2)

        print(f"\n✅ Refined result saved to test_refined_result.json")

        # Validate arrays are same length
        lengths = [len(metadata[key]) for key in expected_metadata_keys]
        if len(set(lengths)) == 1:
            print(f"✅ All metadata arrays have consistent length: {lengths[0]}")
        else:
            print(f"⚠️  Metadata arrays have different lengths: {dict(zip(expected_metadata_keys, lengths))}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_refined_metadata()
    if success:
        print("\n🎉 Refined metadata structure test completed successfully!")
    else:
        print("\n💥 Refined metadata structure test failed!")