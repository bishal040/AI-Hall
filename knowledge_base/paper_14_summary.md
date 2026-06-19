# Detecting and Correcting Hallucinations in LLM-Generated Code via Deterministic AST Analysis

## Metadata
**Authors**: Dipin Khati, Daniel Rodriguez-Cardenas, Paul Pantzer, Denys Poshyvanyk
**Topic**: Static Analysis for Hallucination Detection and Correction

## Problem Statement
Large Language Models frequently produce "Knowledge Conflicting Hallucinations" (KCHs)—inventing API parameters or calling non-existent functions. These errors are syntactically valid (so standard linters miss them) but fail at runtime. Current mitigation strategies, like asking the LLM to fix its own code ("LLM-in-the-loop"), are non-deterministic, expensive, and often unreliable.

## Methodology
Proposed a lightweight, completely static, and deterministic post-processing framework:
1. **AST Parsing**: Parses the LLM-generated Python code into an Abstract Syntax Tree (AST) to extract all imports, function calls, and string literal arguments.
2. **Dynamic Knowledge Base (KB)**: Rather than using a static whitelist, the tool dynamically introspects the imported libraries in the user's environment (e.g., pandas, numpy) to enumerate valid methods and build a version-specific KB.
3. **Validation & Correction**: Deterministically cross-references AST nodes against the KB. If a call doesn't exist, it flags it. It then applies localized AST edits to auto-correct the code (e.g., fixing misspelled API calls using edit-distance matching, or injecting missing module imports).
- **Evaluation**: Tested on 200 manually curated Python snippets spanning 5 major libraries (numpy, pandas, matplotlib, requests, json).

## Key Findings
- **High Detection Accuracy**: The deterministic AST approach achieved 100% precision (zero false positives) and 87.6% recall.
- **Auto-Correction**: The framework successfully auto-corrected 77.0% of the detected hallucinations without ever running the code or re-querying the LLM. 
- **Bug Types**: It was highly effective at fixing "Missing Imports" (97.9% fixed) and "Mis-typed API Calls" (70.0% fixed). 

## Limitations & Future Work
- **Limitations**: Struggled with "Contextual Mismatches" (e.g., using a `.csv` read function for an `.xlsx` file) and heavily object-oriented/aliased libraries like `matplotlib`. It is currently limited to single-file, function-level analysis.
- **Future Work**: Proposes integrating this deterministic tool as a real-time semantic linter inside IDEs (like VS Code) to fix high-confidence hallucinations instantly while developers type.
