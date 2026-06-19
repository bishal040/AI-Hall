# CodeHalu: Investigating Code Hallucinations in LLMs via Execution-based Verification

## Metadata
**Authors**: Yuchen Tian, Weixiang Yan, Qian Yang, Xuandong Zhao, Qian Chen, Wen Wang, Ziyang Luo, Lei Ma, Dawn Song
**Topic**: Code Hallucinations in Large Language Models (LLMs)

## Problem Statement
While LLMs have made significant progress in code generation, they often produce code that is syntactically correct but fails to execute as expected or meet specific requirements. This phenomenon, termed "code hallucination," has not been systematically defined, classified, or quantified in previous research, unlike natural language hallucinations.

## Methodology
- **Concept Definition**: Defined code hallucinations specifically around execution failures or unfulfilled requirements (distinct from mere syntactic errors).
- **CodeHalu Algorithm**: Developed a dynamic detection algorithm that employs a statistical induction method based on execution validation.
- **Classification**: Categorized code hallucinations into four main types: Mapping, Naming, Resource, and Logic hallucinations (further divided into eight subcategories).
- **CodeHaluEval Benchmark**: Constructed a benchmark with 8,883 samples across 699 tasks.
- **Evaluation**: Systematically evaluated 17 popular LLMs (e.g., GPT-4, LLaMA-3, Claude-3) to reveal the distribution and patterns of their code hallucinations.

## Key Findings
- **Hallucination Types**: Identified that logical hallucinations are the most prevalent across models, while naming and resource hallucinations are less common.
- **Model Performance**: GPT-4 and LLaMA-3 perform robustly across hallucination categories, whereas models like Gemma and CodeGeeX-2 show higher tendencies to lose semantic consistency (stuttering/infinite loops).
- **Hallucination Rate (HR)**: Proposed the HR metric to accurately reflect the hallucination phenomenon based on execution tests.
- **Underlying Causes**: Hallucinations stem from token-based generation lacking higher-level structure insight, inability to track long-distance dependencies, lack of resource consumption data in training, and over-reliance on pattern matching without rigorous logic verification.

## Limitations & Future Work
- **Limitations**: The study focuses exclusively on Python and correctness, rather than higher-level security risks.
- **Future Work**: Mitigating code hallucinations by:
  - Improving training data quality and diversity.
  - Employing alignment strategies based on compilation and execution verification.
  - Introducing static code verification modules into model architectures.
  - Incorporating code graph modules for deeper understanding of patterns and logical relationships.
