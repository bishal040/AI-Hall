# ChatDBG: Augmenting Debugging with Large Language Models

## Metadata
**Authors**: Kyla H. Levin, Nicolas van Kempen, Emery D. Berger, Stephen N. Freund
**Topic**: AI-Augmented Interactive Debugging

## Problem Statement
Finding and fixing software defects remains a time-consuming and cognitively demanding task. Standard debuggers (like GDB, LLDB, and Pdb) provide tools to inspect state and step through execution, but they lack semantic understanding. Programmers still bear the full burden of reasoning about program logic to uncover root causes.

## Methodology
- **ChatDBG**: Developed an AI-powered debugging assistant that integrates directly into standard debuggers (GDB, LLDB, Pdb).
- **Agentic Autonomy ("Taking the Wheel")**: Instead of just passing static error messages to an LLM, ChatDBG gives the LLM autonomy to act as an agent. The LLM can actively issue debugger commands (like checking variable values, navigating the stack, or running program slices) to gather necessary context before formulating an answer.
- **Evaluation**: Tested on a suite of unpublished Python scripts and Jupyter notebooks with real-world student errors, as well as C/C++ applications with known memory bugs (from BugBench and BugsC++).

## Key Findings
- **High Success Rate**: For Python programs, ChatDBG correctly diagnosed the root cause and provided an actionable fix 67% of the time after a single targeted query. With just one follow-up dialogue, the success rate jumped to 85%.
- **Unmanaged Code (C/C++)**: ChatDBG successfully identified and fixed the root cause 36% of the time, and fixed the proximate cause an additional 55% of the time for memory errors.
- **Feature Ablation**: The agentic "take the wheel" capability is critical. Providing an enriched stack trace alone is helpful for crashes but insufficient for semantic errors; allowing the LLM to dynamically interrogate the debugger state significantly boosts success rates.
- **Cost**: The cost of a debugging query using GPT-4 was extremely low, typically well under $0.20 USD per session.

## Limitations & Future Work
- **Limitations**: Relies heavily on prompt engineering specific to the underlying LLM (e.g., GPT-4). Susceptible to typical LLM stochasticity, though it showed stable aggregate performance.
- **Future Work**: Proposes integrating traditional fault localization tools to narrow the LLM's search space, using delta debugging to find failure-inducing inputs automatically, and integrating with time-travel debuggers to let the LLM analyze historical program states.
