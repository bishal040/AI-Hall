# Hallucination by Code Generation LLMs: Taxonomy, Benchmarks, Mitigation, and Challenges

## Metadata
**Authors**: Yunseo Lee, John Youngeun Song, Dongsun Kim, Jindae Kim, Mijung Kim, Jaechang Nam
**Topic**: Systematic Survey on CodeLLM Hallucinations

## Problem Statement
Despite the proliferation of Large Language Models (LLMs) for code generation, there remains a lack of standardized methods to assess, detect, and mitigate "hallucinations" specific to code. General hallucination surveys largely focus on natural language, missing the unique syntactic and functional constraints of code.

## Methodology
- **Systematic Literature Review**: Conducted a systematic review and snowballing of papers addressing both LLM code generation and LLM hallucinations.
- **Categorization**: Grouped the existing literature into three core dimensions: Taxonomy, Benchmarking, and Mitigation.

## Key Findings
- **Taxonomy of Code Hallucinations**: Synthesized existing studies into a four-category taxonomy:
  1. *Syntactic Hallucinations* (Syntax violations, incomplete code)
  2. *Runtime Execution Hallucinations* (API knowledge conflicts, invalid references)
  3. *Functional Correctness Hallucinations* (Incorrect logic flow, requirement deviation)
  4. *Code Quality Hallucinations* (Resource mishandling, security vulnerabilities, code smells)
- **Benchmarks & Metrics**: Analyzed datasets tailored for hallucination evaluation (e.g., CodeHaluEval, CodeMirage, LMDefects, EvalPlus) and standard metrics (Pass@k, Hallucination Rate, Valid Rate).
- **Causes**: Traced root causes to three domains:
  - *Training Data* (flawed data, incomplete APIs)
  - *Trained Model* (reasoning/context limitations, token limits, temperature)
  - *Prompt Issues* (ambiguity, lack of context)
- **Mitigation Strategies**: Highlighted several promising approaches from recent research:
  - *Iterative Grounding / RAG* (e.g., De-Hallucinator) to provide project-specific API contexts.
  - *Self-Revision* via simple or static-analysis feedback.
  - *Grammar Augmentation* (e.g., SynCode) to enforce syntax rules.
  - *Requirements Clarification* (e.g., ClarifyGPT) to prompt the user for ambiguity resolution.

## Limitations & Future Work
- Existing benchmarks lack diversity in programming languages and often fail to reflect real-world repository-level complexities.
- Future directions include developing adaptive, real-time context-specific mitigation techniques integrated into actual software development workflows.
