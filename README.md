# Drug ECMO Analysis Tool

A configurable system for analyzing drug effects and recommendations for ECMO use in pediatric patients using the paper-qa library.

## Features

- **Configurable drug name**: No hard-coded drug names
- **7 analysis fields**: Comprehensive analysis covering all aspects of drug use in ECMO
- **Separate queries**: Each field runs independently for maximum accuracy
- **JSON output**: Structured results with metadata and citations
- **Extensible**: Easy to add new drugs or modify analysis fields

## Quick Start

```python
from drug_ecmo_analyzer import DrugECMOAnalyzer

# Analyze meropenem (your original use case)
analyzer = DrugECMOAnalyzer(
    drug_name="meropenem",
    paper_directory="./drugs/meropenem"
)

# Run single field analysis
result = analyzer.analyze_field("Effect on ECMO")
print(result)

# Run all fields
all_results = analyzer.analyze_all_fields()
analyzer.save_results(all_results)
```

## Analysis Fields

The tool analyzes 7 key aspects:

1. **Effect on ECMO**: How ECMO affects the drug's pharmacokinetics
2. **Final Recommendation**: Compiled dosing recommendations
3. **Volume of distribution (Vd)**: Changes in Vd during ECMO
4. **Circuit sequestration**: Drug binding to ECMO tubing
5. **ECMO dosage**: Recommended dosing ranges
6. **PK Properties - LogP**: Lipophilicity coefficient
7. **PK Properties - Protein Binding**: Protein binding percentage

## Output Format

Each field returns:

```json
{
  "Field Name": {
    "answer": "Main answer from paper-qa",
    "formatted_answer": "Answer with citations",
    "metadata": {
      "exact_citation": "Direct quotes from papers",
      "reference": "Formatted citations",
      "ref_details": "Study details and quality assessment"
    }
  }
}
```

## Configuration

### Different Drugs

```python
# Vancomycin analysis
vancomycin_analyzer = DrugECMOAnalyzer(
    drug_name="vancomycin",
    paper_directory="./drugs/vancomycin"
)

# Gentamicin analysis
gentamicin_analyzer = DrugECMOAnalyzer(
    drug_name="gentamicin",
    paper_directory="./drugs/gentamicin"
)
```

### Custom Paper Directory

```python
analyzer = DrugECMOAnalyzer(
    drug_name="meropenem",
    paper_directory="/custom/path/to/papers"
)
```

## Running the Analysis

### Option 1: Use the provided script
```bash
python run_analysis.py
```

### Option 2: Custom analysis
```python
# Single field (faster, cheaper)
result = analyzer.analyze_field("Final Recommendation")

# All fields (comprehensive but more expensive)
all_results = analyzer.analyze_all_fields()
```

## Requirements

- paper-qa library (latest version)
- PDF papers in the specified directory
- OpenAI API key (or other supported LLM provider)

## Tips for Best Results

1. **Separate queries**: Run each field independently for best accuracy
2. **Quality papers**: Ensure your PDF directory contains relevant, high-quality research papers
3. **Specific questions**: The tool generates targeted questions for each field
4. **Cost consideration**: Running all 7 fields will make 7 separate API calls

## Extending the Tool

### Add new analysis fields:
```python
analyzer.analysis_fields["New Field"] = {
    "definition": "What this field analyzes",
    "structure": "Expected output format",
    "question_template": "Question for {drug_name}...",
    "system_prompt": "Specialized prompt for this field"
}
```

### Modify existing fields:
```python
# Customize system prompt for specific use case
analyzer.analysis_fields["Effect on ECMO"]["system_prompt"] = "Your custom prompt here"
```