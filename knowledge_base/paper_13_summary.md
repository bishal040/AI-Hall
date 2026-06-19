# Debug like a Human: A Large Language Model Debugger via Verifying Runtime Execution Step by Step

## Metadata
**Authors**: Li Zhong, Zilong Wang, Jingbo Shang
**Topic**: Large Language Model Debugger (LDB) using Runtime States

## Problem Statement
Current LLM code generation and refinement methods typically treat a program as an indivisible black box. When a program fails, they rely on post-execution feedback (like a failed test case or error message). However, human developers debug by setting breakpoints and inspecting intermediate variable states step-by-step. Existing LLMs struggle to mentally simulate these complex execution flows accurately.

## Methodology
- **LDB Framework**: Proposed a debugging framework that mimics human breakpoint debugging.
- **Profiling (Block-level Segmentation)**: LDB breaks the generated program down into basic blocks using a Control Flow Graph (CFG). It executes the program on a failed test case and captures the actual runtime variables and their values at the end of each basic block.
- **Debugging Verdicts**: LDB queries the LLM with these intermediate states block-by-step. The LLM acts as a verifier, checking if the state after block $i$ aligns with the intended logic of the task description.
- **Regeneration**: Once the buggy block is identified via the intermediate states, LDB prompts the LLM to regenerate and fix the code.

## Key Findings
- **State-of-the-Art Performance**: LDB improves code generation accuracy by up to 9.8% across HumanEval, MBPP, and TransCoder datasets (using models like GPT-3.5, CodeLlama, and StarCoder).
- **Outperforming Self-Debugging**: LDB beats existing self-debugging methods that rely on the LLM "dry-running" the code or explaining it statically. Real runtime information prevents the LLM from hallucinating correct execution flows.
- **Sustained Iterative Improvement**: While traditional self-debugging saturates after 2-3 iterations (because the LLM cannot figure out *why* it failed), LDB's performance continues to climb even after 10-20 iterations because the runtime data acts as an objective anchor.
- **Optimal Granularity**: Segmenting the code at the *basic block level* is more accurate and token-efficient than doing it line-by-line (which loses semantic meaning) or function-by-function (which is too coarse).

## Limitations & Future Work
- **Limitation**: The system strictly requires visible, executable test cases to generate the runtime execution trace. It cannot perform "test-case-free" debugging or static analysis debugging where no test inputs are provided.
