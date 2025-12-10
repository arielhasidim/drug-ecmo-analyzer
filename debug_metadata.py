#!/usr/bin/env python3
"""
Debug script to understand the response structure for metadata extraction
"""

from paperqa import ask, Settings
from paperqa.settings import PromptSettings

def debug_response_structure():
    """Debug the response structure to understand context attributes"""

    settings = Settings(
        prompts=PromptSettings(
            system="Debug metadata extraction",
            use_json=True
        ),
        paper_directory="./drugs/meropenem",
        temperature=0.1,
        llm="gpt-4o-mini",
        summary_llm="gpt-4o-mini"
    )

    question = "What is the effect of ECMO on meropenem?"
    response = ask(question, settings=settings)

    print("=== RESPONSE STRUCTURE DEBUG ===")
    print(f"Response type: {type(response)}")
    print(f"Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")

    if hasattr(response, 'session'):
        print(f"\nSession type: {type(response.session)}")
        print(f"Session attributes: {[attr for attr in dir(response.session) if not attr.startswith('_')]}")

        if hasattr(response.session, 'contexts'):
            print(f"\nContexts type: {type(response.session.contexts)}")
            print(f"Number of contexts: {len(response.session.contexts)}")

            if response.session.contexts:
                first_context = response.session.contexts[0]
                print(f"\nFirst context type: {type(first_context)}")
                print(f"First context attributes: {[attr for attr in dir(first_context) if not attr.startswith('_')]}")

                if hasattr(first_context, 'doc'):
                    print(f"\nDoc type: {type(first_context.doc)}")
                    if first_context.doc:
                        print(f"Doc attributes: {[attr for attr in dir(first_context.doc) if not attr.startswith('_')]}")

                        if hasattr(first_context.doc, 'citation'):
                            print(f"\nCitation: {first_context.doc.citation}")

                        if hasattr(first_context.doc, 'docname'):
                            print(f"Docname: {first_context.doc.docname}")

if __name__ == "__main__":
    debug_response_structure()