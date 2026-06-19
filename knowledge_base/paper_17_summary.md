# Large Language Model Powered Symbolic Execution

## Metadata
**Authors**: Yihe Li, Ruijie Meng, Gregory J. Duck
**Topic**: Hybrid Symbolic Execution using LLMs as Theorem Provers

## Problem Statement
Traditional symbolic execution is highly precise but suffers from path explosion, inability to handle unbounded loops, and requires manual modeling for external libraries/APIs (environment). Conversely, Large Language Models (LLMs) can naturally reason about loops and external libraries, but they struggle to maintain accuracy and context when fed large, complex codebases.

## Methodology
- **AutoBug Framework**: Proposed an "LLM-based symbolic execution" engine that combines the path-decomposition of traditional symbolic execution with the approximate reasoning capabilities of LLMs.
- **Decomposition without Translation**: 
  1. The code is parsed into a Control Flow Graph (CFG).
  2. The CFG is partitioned into "truncated slices" representing generalized execution paths.
  3. *Crucially*, instead of translating these paths into a formal logic (like SMT-LIB for a Z3 solver), AutoBug renders the slices back into the original programming language (C, Java, Python).
- **LLM as the Solver**: The LLM is prompted with these much smaller, targeted code slices and asked to verify if the specific post-condition holds. The LLM acts as an approximate theorem prover.

## Key Findings
- **Overcoming Traditional Limits**: The approach easily handles unbounded loops and external API calls without explicit modeling, because the LLM uses its pre-trained knowledge to infer what standard libraries do (abductive reasoning).
- **Improved Accuracy and Scalability**: By slicing the code before prompting the LLM, the prompt size is reduced by up to 26%. This targeted prompting significantly improves the LLM's accuracy. AutoBug averaged 86-90% accuracy across multiple benchmarks, outperforming standard LLM prompting and traditional tools like KLEE and CrossHair (which stalled at 46.7% due to modeling limits).
- **Language Agnostic**: Because the solver (the LLM) natively reads code, the engine works seamlessly across C, Java, and Python with minimal configuration.

## Limitations & Future Work
- **Limitations**: LLMs are approximate oracles; they will never have the 100% deductive certainty of an SMT solver, so this approach is complementary rather than a complete replacement. The framework can still theoretically suffer from path explosion during the partitioning phase.
