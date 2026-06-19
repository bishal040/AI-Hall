# The Debugging Decay Index: Rethinking Debugging Strategies for Code LLMs

## Metadata
**Authors**: Muntasir Adnan, Carlos C. N. Kuhn
**Topic**: Quantifying and Optimizing Iterative LLM Debugging

## Problem Statement
Automated code generation increasingly relies on iterative debugging (where the LLM refines code based on compiler/error feedback). However, there is no systematic framework to measure how effective these repeated debugging attempts are. Traditional metrics like `pass@k` evaluate static code generation but fail to capture the diminishing returns of iterative debugging.

## Methodology
- **Debugging Decay Index (DDI)**: Introduced a mathematical framework that models the effectiveness of sequential LLM debugging attempts as an exponential decay function.
- **Evaluation**: Evaluated 18 state-of-the-art LLMs (including GPT-4, Claude-3.7, DeepSeek-Coder, Llama-3) on HumanEval.
- **Strategic Fresh Starts**: Tested an intervention strategy where the debugging process is completely reinitialized (clearing context) once the DDI predicts that effectiveness has decayed past a specific threshold (e.g., 50% or 80% loss of effectiveness).

## Key Findings
- **Exponential Decay**: AI debugging effectiveness decays rapidly. Most models lose 60-80% of their debugging capability within just 2 to 3 attempts.
- **DDI Metrics**: DDI characterizes models using initial effectiveness ($E_0$), decay rate ($\lambda$), and optimal intervention points ($t_\theta$).
- **Reasoning Models**: Models specifically fine-tuned for reasoning (e.g., phi4-reasoning) show significantly better "debugging sustainability" (a slower decay rate) compared to their standard counterparts, meaning they can extract more value from extended debugging sessions.
- **Fresh Starts Overcome Decay**: Implementing "strategic fresh starts" at the DDI-calculated thresholds breaks the exponential decay pattern. This simple intervention improves overall debugging accuracy without increasing the total computational budget (token usage).

## Limitations & Future Work
- **Limitations**: DDI parameters (like decay rate) are currently dataset-specific and require calibration for different coding benchmarks.
- **Future Work**: Proposes cross-dataset validation, developing adaptive threshold selection methods, and comparing AI debugging decay patterns to human cognitive decay during problem-solving.
