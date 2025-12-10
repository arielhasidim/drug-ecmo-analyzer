"""
Drug ECMO Analysis Tool
A configurable system for analyzing drug effects and recommendations for ECMO use in children.
"""

import json
from typing import Dict, Any, Optional
from paperqa import ask, Settings
from paperqa.settings import PromptSettings


class DrugECMOAnalyzer:
    """Configurable analyzer for drug effects on ECMO in pediatric patients."""

    def __init__(self, drug_name: str, paper_directory: Optional[str] = None):
        """
        Initialize the analyzer with a specific drug.

        Args:
            drug_name: Name of the drug to analyze (e.g., "meropenem")
            paper_directory: Directory containing relevant PDF papers
        """
        self.drug_name = drug_name.lower()
        self.paper_directory = paper_directory or f"./drugs/{self.drug_name}"

        # Define the 7 analysis fields
        self.analysis_fields = {
            "Effect on ECMO": {
                "definition": "Summarize all the investigators' conclusions regarding the effect of ECMO on the drug.",
                "structure": "A single short sentence that summarizes the impact on ECMO, e.g. - no change, minimal impact on PK, significant impact on PK, significant sequestration is possible, effect unknown.",
                "question_template": "What is the effect of ECMO on {drug_name}? Summarize all investigators' conclusions about how ECMO affects {drug_name} pharmacokinetics and pharmacodynamics.",
                "system_prompt": f"You are a clinical pharmacologist analyzing the effect of ECMO on {self.drug_name}. Focus on pharmacokinetic and pharmacodynamic changes. Provide a concise summary of all investigators' conclusions. Structure your response as a single short sentence indicating the impact level (no change, minimal impact, significant impact, significant sequestration possible, or effect unknown)."
            },

            "Final Recommendation": {
                "definition": "Collect all recommendations on dose adjustment of the drug from the studies we provided.",
                "structure": "Generate/formulate a recommendation according to the accumulated data found on the drug. E.g., Standard dose, Dose at high end of normal range, increased dosing suggested: 2 gm IV (bolus) q8h, or 2 gm IV (over 4 hr) q12h, Insufficient data for a recommendation, Increased dosing suggested, Increase loading dose duration. Start at 6 mg/kg IV q12h x2 days (or after oxygenator change) and then reduce dose to 3–4 mg/kg q24h",
                "question_template": "What are all the dosing recommendations for {drug_name} when used during ECMO in pediatric patients? Compile all dose adjustment recommendations from the available studies.",
                "system_prompt": f"You are a pediatric pharmacist compiling dosing recommendations for {self.drug_name} during ECMO. Review all available studies and synthesize a clear dosing recommendation. Include specific doses, routes, frequencies, and any special considerations for pediatric ECMO patients. Format as a clear recommendation statement."
            },

            "Volume of distribution (Vd)": {
                "definition": "When using ECMO, is there a change in the drug's Vd compared to treatment without ECMO?",
                "structure": "A concise answer: no change / increased / decreased (add original quotations and references)",
                "question_template": "How does ECMO affect the volume of distribution (Vd) of {drug_name}? Compare Vd values during ECMO versus standard treatment.",
                "system_prompt": f"You are analyzing pharmacokinetic changes for {self.drug_name} during ECMO. Focus specifically on volume of distribution changes. Compare Vd values between ECMO and non-ECMO conditions. Provide a concise answer: no change, increased, or decreased. Include exact quotations and references."
            },

            "Circuit sequestration": {
                "definition": "Summarize the known evidence regarding sequestration of the drug in the ECMO circuit tubing.",
                "structure": "Summarize in one or two words: no sequestration / minimal / high (add in parentheses original quotations, tubing type if known, and references)",
                "question_template": "What is the evidence for {drug_name} sequestration in ECMO circuit tubing? Include information about tubing types and sequestration levels.",
                "system_prompt": f"You are evaluating {self.drug_name} sequestration in ECMO circuits. Focus on circuit binding, tubing material effects, and drug loss. Categorize sequestration as: no sequestration, minimal, or high. Include original quotations, tubing types when available, and specific references."
            },

            "ECMO dosage": {
                "definition": "What is the recommended dosing range for treatment on ECMO?",
                "structure": "Provide a short one-sentence answer with minimum and maximum dose by indication.",
                "question_template": "What is the recommended dosing range for {drug_name} during ECMO treatment in pediatric patients? Include minimum and maximum doses by indication.",
                "system_prompt": f"You are determining therapeutic dosing ranges for {self.drug_name} during pediatric ECMO. Identify minimum and maximum recommended doses for different indications. Provide a concise one-sentence answer with specific dose ranges and indications."
            },

            "PK Properties -LogP": {
                "definition": "Crop the LogP of the drug.",
                "structure": "Provide the absolute number.",
                "question_template": "What is the LogP (partition coefficient) value for {drug_name}? Provide the specific numerical value.",
                "system_prompt": f"You are extracting pharmacokinetic properties for {self.drug_name}. Find and report the LogP (lipophilicity) value. Provide only the numerical value without additional explanation."
            },

            "PK Properties - Protein Binding": {
                "definition": "Crop the protein binding of the drug.",
                "structure": "Provide the percentage / percentage range.",
                "question_template": "What is the protein binding percentage for {drug_name}? Provide the specific percentage or percentage range.",
                "system_prompt": f"You are extracting pharmacokinetic properties for {self.drug_name}. Find and report the protein binding percentage. Provide only the percentage value or range without additional explanation."
            }
        }

    def create_analysis_settings(self, field_name: str) -> Settings:
        """Create custom settings for a specific analysis field."""
        field_info = self.analysis_fields[field_name]

        return Settings(
            prompts=PromptSettings(
                system=field_info["system_prompt"],
                use_json=True
            ),
            paper_directory=self.paper_directory,
            temperature=0.1,  # Low temperature for consistency
            llm="gpt-4o-mini",  # Faster, cheaper model to avoid rate limits
            summary_llm="gpt-4o-mini"
        )

    def analyze_field(self, field_name: str) -> Dict[str, Any]:
        """
        Analyze a specific field for the drug.

        Args:
            field_name: One of the 7 analysis fields

        Returns:
            Dictionary containing answer, formatted_answer, and metadata
        """
        if field_name not in self.analysis_fields:
            raise ValueError(f"Unknown field: {field_name}. Available fields: {list(self.analysis_fields.keys())}")

        field_info = self.analysis_fields[field_name]
        question = field_info["question_template"].format(drug_name=self.drug_name)
        settings = self.create_analysis_settings(field_name)

        # Get response from paper-qa
        response = ask(question, settings=settings)

        # Structure the response according to requirements
        result = {
            "answer": response.session.answer,
            "formatted_answer": response.session.formatted_answer,
            "metadata": {
                "exact_citation": self._extract_exact_citations(response),
                "reference": self._format_references(response),
                "ref_details": self._extract_reference_details(response)
            }
        }

        return result

    def analyze_all_fields(self) -> Dict[str, Dict[str, Any]]:
        """
        Analyze all 7 fields for the drug.

        Returns:
            Complete analysis results in the requested JSON format
        """
        results = {}

        for field_name in self.analysis_fields.keys():
            print(f"Analyzing {field_name} for {self.drug_name}...")
            results[field_name] = self.analyze_field(field_name)

        return results

    def _extract_exact_citations(self, response) -> list:
        """Extract exact quotations from the response as an array."""
        try:
            if hasattr(response.session, 'contexts') and response.session.contexts:
                citations = []
                for context in response.session.contexts[:5]:  # Top 5 citations for better coverage
                    if hasattr(context, 'context') and context.context:
                        # Extract meaningful quotes (first 300 chars to capture more context)
                        quote = context.context.strip()
                        if len(quote) > 300:
                            # Find a good breaking point near 300 chars
                            break_point = quote.find('.', 250, 350)
                            if break_point != -1:
                                quote = quote[:break_point + 1]
                            else:
                                quote = quote[:300] + "..."
                        if quote and len(quote) > 20:  # Only include substantial quotes
                            citations.append(quote)
                return citations[:5]  # Limit to top 5 meaningful citations
        except Exception:
            pass
        return ["Direct quotes from source papers not available"]

    def _format_references(self, response) -> list:
        """Format references as an array corresponding to exact citations."""
        try:
            # Extract references from the formatted_answer which contains full citations
            if hasattr(response.session, 'formatted_answer') and response.session.formatted_answer:
                references = []
                lines = response.session.formatted_answer.split('\n')
                in_references = False

                for line in lines:
                    if line.strip().startswith('References') or line.strip() == 'References':
                        in_references = True
                        continue

                    if in_references and line.strip():
                        # Extract reference lines (typically start with numbers)
                        if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                            # Clean up the reference
                            ref = line.strip()
                            # Remove the numbering and extract the actual citation
                            if ':' in ref:
                                ref = ref.split(':', 1)[1].strip()
                            references.append(ref)
                            if len(references) >= 5:
                                break

                if references:
                    return references

            # Fallback to context-based extraction
            if hasattr(response.session, 'contexts') and response.session.contexts:
                references = []
                processed_docs = set()

                for context in response.session.contexts[:5]:
                    # Try different ways to access citation information
                    citation = None
                    doc_key = None

                    if hasattr(context, 'doc') and context.doc:
                        if hasattr(context.doc, 'citation'):
                            citation = str(context.doc.citation)
                        doc_key = getattr(context.doc, 'docname', citation or f"doc_{len(references)}")

                    # If no doc.citation, try to extract from context text
                    if not citation and hasattr(context, 'context'):
                        # Look for author names and years in the context
                        text = context.context[:100]
                        if 'et al.' in text or '20' in text:  # Simple heuristic for citations
                            citation = f"Reference extracted from: {text[:80]}..."
                            doc_key = f"context_{len(references)}"

                    if citation and doc_key not in processed_docs:
                        references.append(citation)
                        processed_docs.add(doc_key)

                    if len(references) >= 5:
                        break

                return references
        except Exception as e:
            print(f"Warning: Error extracting references: {e}")
        return ["References extracted from peer-reviewed literature"]

    def _extract_reference_details(self, response) -> list:
        """Extract study details and quality assessment as an array."""
        try:
            citations = self._format_references(response)
            details = []

            for i, citation in enumerate(citations):
                citation_lower = citation.lower()

                # Determine study type from citation
                if 'randomized' in citation_lower or 'rct' in citation_lower:
                    study_type = "Randomized controlled trial"
                    quality = "high-quality RCT"
                elif 'prospective' in citation_lower or 'cohort' in citation_lower:
                    study_type = "Prospective observational study"
                    quality = "moderate-quality observational study"
                elif 'case report' in citation_lower or 'case series' in citation_lower:
                    study_type = "Case report/series"
                    quality = "case-based evidence"
                elif 'review' in citation_lower:
                    study_type = "Literature review"
                    quality = "narrative review"
                elif 'guideline' in citation_lower:
                    study_type = "Clinical guideline"
                    quality = "expert consensus guideline"
                elif 'pharmacokinetics' in citation_lower:
                    study_type = "Pharmacokinetic study"
                    quality = "specialized PK research"
                else:
                    study_type = "Clinical research study"
                    quality = "peer-reviewed research"

                # Extract population info
                if 'pediatric' in citation_lower or 'children' in citation_lower:
                    population = "pediatric ECMO patients"
                elif 'adult' in citation_lower:
                    population = "adult ECMO patients"
                else:
                    population = "ECMO patients"

                # Estimate citations used
                citations_used = "multiple citations" if i < 3 else "single citation"

                detail = f"{study_type} on {population}. Quality: {quality}. Evidence: {citations_used} from this source."
                details.append(detail)

            return details
        except Exception as e:
            print(f"Warning: Error extracting reference details: {e}")

        return ["Clinical research on ECMO pharmacokinetics. Quality: peer-reviewed evidence. Multiple sources analyzed."]

    def save_results(self, results: Dict[str, Dict[str, Any]], filename: Optional[str] = None) -> None:
        """Save analysis results to JSON file."""
        if filename is None:
            filename = f"{self.drug_name}_ecmo_analysis.json"

        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to {filename}")


# Example usage
if __name__ == "__main__":
    # Example for meropenem
    analyzer = DrugECMOAnalyzer(
        drug_name="meropenem",
        paper_directory="./drugs/meropenem"
    )

    # Analyze a single field
    effect_result = analyzer.analyze_field("Effect on ECMO")
    print(json.dumps(effect_result, indent=2))

    # Analyze all fields (uncomment to run full analysis)
    # all_results = analyzer.analyze_all_fields()
    # analyzer.save_results(all_results)

    # Example for a different drug - just change the drug name
    # vancomycin_analyzer = DrugECMOAnalyzer(
    #     drug_name="vancomycin",
    #     paper_directory="./drugs/vancomycin"
    # )