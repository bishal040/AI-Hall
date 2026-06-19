# DebugBench: Evaluating Debugging Capability of Large Language Models

## Metadata
**Authors**: Runchu Tian, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Yinxu Pan, Yesai Wu, Haotian Hui, Weichuan Liu, Zhiyuan Liu, Maosong Sun
**Topic**: Benchmarking LLM Debugging Capabilities

## Problem Statement
While code generation by LLMs has been extensively studied, their capability to *debug* existing code remains relatively unexplored. Existing debugging benchmarks (like QuixBugs or Defects4J) are small-scale, lack diversity in bug types, and carry a severe risk of data leakage (models likely saw the bugs and fixes during pre-training).

## Methodology
- **DebugBench Creation**: Created a dataset of 4,253 debugging instances in C++, Java, and Python. 
- **Data Source**: Collected solutions from LeetCode released *after* July 2022 to strictly prevent data leakage from models' pre-training cutoffs.
- **Bug Implantation**: Used GPT-4 to inject bugs into correct solutions based on a taxonomy of 4 major categories (Syntax, Reference, Logic, Multiple) and 18 minor types. Ensured quality via automated testing and manual human inspection.
- **Evaluation**: Assessed 2 closed-source (GPT-3.5, GPT-4) and 4 open-source models (CodeLlama, Llama-3, DeepSeek, Mixtral) using zero-shot prompting to fix the bugs.

## Key Findings
- **Human vs. LLM**: LLM debugging currently falls short of human performance. Closed-source models (GPT-4) perform decently but still trail human developers, while open-source models perform poorly in zero-shot debugging tasks.
- **Bug Difficulty**: The difficulty of fixing errors varies dramatically. Syntax and reference errors are relatively easy for LLMs to fix. Logic errors and instances with multiple bugs are significantly harder—sometimes even harder than generating the code from scratch.
- **Impact of Runtime Feedback**: Providing the LLM with execution traceback/error messages improves performance for syntax and reference errors, but provides little to no help for logic errors (where the traceback is often too low-level to be useful).
- **Coding vs. Debugging**: There is a positive correlation between an LLM's code generation capability and its debugging capability.

## Limitations & Future Work
- The bugs are synthetically generated and may not perfectly capture the intricacies of real-world, repository-scale defects.
- Future work should expand to repository-level debugging, scenarios involving human-in-the-loop interaction, and testing LLMs' abilities to write reliable test cases for debugging.
