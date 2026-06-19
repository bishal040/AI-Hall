# Demystifying Errors in LLM Reasoning Traces: An Empirical Study of Code Execution Simulation

## Metadata
**Authors**: Mohammad Abdollahi, Khandaker Rifah Tasnia, Soumit Kanti Saha, Jinqiu Yang, Song Wang, Hadi Hemmati
**Topic**: Empirical Analysis of Code Execution Reasoning in LLMs

## Problem Statement
Recent "reasoning LLMs" (like OpenAI o1/o4, DeepSeek-R1) generate explicit intermediate reasoning steps (Chain-of-Thought) before providing an answer. While they excel at code generation, there is little systematic understanding of how they fail when attempting to mentally simulate program execution (tracing states, control flows) and what kinds of errors exist within their reasoning traces.

## Methodology
- **Dataset Creation**: Curated 427 Python code snippets from HumanEval+ and LiveCodeBench.
- **Testing Regimes**: Evaluated programs using three types of inputs: *Regular*, *Edge-Case*, and *Invalid* inputs, to stress-test the models.
- **Model Evaluation**: Tested four cutting-edge reasoning models: DeepSeek-R1, OpenAI o4-mini, Gemini 2.5 Flash, and Claude 4 Sonnet.
- **Error Annotation**: Conducted manual, fine-grained analysis of the generated reasoning traces where models failed, classifying errors at the statement level (where the logic first broke down) and the trace level (the overarching failure pattern).

## Key Findings
- **High Performance**: Reasoning models are incredibly good at code execution simulation, achieving between 85% and 98% accuracy across the board, with GPT-o4 mini and DeepSeek-R1 leading.
- **Failure Locations**: Reasoning breaks down most frequently at basic statements (arithmetic, assignments) and control flow structures (if conditions, loop tracking) rather than high-level algorithmic logic.
- **Error Taxonomy**: Developed a 9-category taxonomy of reasoning errors. The most common was **Computation Errors** (e.g., simple arithmetic or bitwise miscalculations), followed by Indexing Errors and Control Flow Errors.
- **Complexity Paradox**: Paradoxically, reasoning failures occurred more frequently on code with lower Halstead Difficulty. Models often succeeded on highly complex structures but stumbled on seemingly straightforward arithmetic or logic loops.
- **Tool Augmentation**: Implementing a "tool-augmented" approach—allowing the LLM to offload basic arithmetic to an external Python interpreter during its reasoning process—successfully mitigated 58% of the computation errors.

## Limitations & Future Work
- The manual classification of reasoning traces carries inherent subjectivity. The study was also limited exclusively to Python.
- Future work should focus on seamlessly integrating external tools (like code interpreters) directly into the reasoning loops of LLMs to offload deterministic computations.
