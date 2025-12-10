#!/usr/bin/env python3
"""
Test script to demonstrate configurability of the drug analyzer
"""

import json
from drug_ecmo_analyzer import DrugECMOAnalyzer

def test_configurability():
    """Test that the system works with different drug names"""

    # Test 1: Meropenem (we know this works)
    print("=== Test 1: Meropenem ===")
    mero_analyzer = DrugECMOAnalyzer("meropenem", "./drugs/meropenem")
    print(f"Drug: {mero_analyzer.drug_name}")
    print(f"Directory: {mero_analyzer.paper_directory}")
    print(f"Available fields: {list(mero_analyzer.analysis_fields.keys())}")

    # Show how questions adapt to drug name
    effect_field = mero_analyzer.analysis_fields["Effect on ECMO"]
    print(f"Question template: {effect_field['question_template']}")
    actual_question = effect_field['question_template'].format(drug_name=mero_analyzer.drug_name)
    print(f"Actual question: {actual_question}")

    # Test 2: Hypothetical vancomycin
    print("\n=== Test 2: Vancomycin (Hypothetical) ===")
    vanco_analyzer = DrugECMOAnalyzer("vancomycin", "./drugs/vancomycin")
    print(f"Drug: {vanco_analyzer.drug_name}")
    print(f"Directory: {vanco_analyzer.paper_directory}")

    # Show how the same field adapts
    vanco_effect_field = vanco_analyzer.analysis_fields["Effect on ECMO"]
    vanco_question = vanco_effect_field['question_template'].format(drug_name=vanco_analyzer.drug_name)
    print(f"Adapted question: {vanco_question}")

    # Test 3: Show system prompt adaptation
    print("\n=== Test 3: System Prompt Adaptation ===")
    mero_prompt = mero_analyzer.analysis_fields["Effect on ECMO"]["system_prompt"]
    vanco_prompt = vanco_analyzer.analysis_fields["Effect on ECMO"]["system_prompt"]

    print(f"Meropenem system prompt: {mero_prompt[:100]}...")
    print(f"Vancomycin system prompt: {vanco_prompt[:100]}...")

    # Test 4: Show available fields
    print(f"\n=== Test 4: All Analysis Fields ===")
    for i, field_name in enumerate(mero_analyzer.analysis_fields.keys(), 1):
        print(f"{i}. {field_name}")

    print("\n✅ Configurability test completed!")

if __name__ == "__main__":
    test_configurability()