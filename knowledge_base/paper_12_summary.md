# Leveraging Print Debugging to Improve Code Generation in Large Language Models

## Metadata
**Authors**: Xueyu Hu, Kun Kuang, Jiankai Sun, Hongxia Yang, Fei Wu
**Topic**: Print Debugging (Tracing) via In-Context Learning

## Problem Statement
While LLMs can write basic code, they frequently fail on complex algorithmic problems (e.g., Leetcode medium/hard). Existing self-debugging methods (like Rubber Duck Debugging or Reflexion) rely only on static error messages or failed test inputs. They do not trace the runtime execution flow or variable states, which is how human developers typically debug complex logic.

## Methodology
- **Print Debugging Framework**: Proposed a multi-step in-context learning approach that mimics human tracing:
  1. **Add Print Statements**: If the generated code fails a test case, the LLM is prompted to insert `print()` statements into the buggy code to track intermediate variable states (e.g., inside loops).
  2. **Execution & Logging**: The code is executed, and the output logs from the print statements are collected.
  3. **Analysis & Fixing**: The LLM is prompted to provide a step-by-step explanation of what *should* happen for the test case, and compare it line-by-line with the actual logs. By finding the inconsistency between the expected state and the logged state, the LLM identifies and patches the bug.
- **Evaluation**: Evaluated using GPT-4 on a dataset of 132 easy, 39 medium, and 40 hard Leetcode problems, comparing against "Rubber Duck Debugging" and other baseline feedback mechanisms.

## Key Findings
- **Significant Gains on Medium Problems**: Print debugging outperformed Rubber Duck Debugging by a massive 17.9% absolute margin on medium-level Leetcode problems, and by 1.5% on easy problems.
- **Sustained Iterative Improvement**: Unlike standard debugging methods that saturate after 1 or 2 attempts, print debugging allowed the LLM to continuously improve the code over up to 7 rounds of debugging, as new logs provided fresh insights.
- **Failure on Hard Problems**: All debugging methods, including print debugging, failed to improve performance on Hard Leetcode problems (stuck at 5% accuracy). This suggests that tracing state is insufficient if the underlying algorithm chosen by the LLM is fundamentally flawed or if it completely misunderstands the problem requirements.

## Limitations & Future Work
- **Limitations**: The context window limits how many logs can be processed (logs had to be truncated in infinite loops or very long outputs). It cannot fix fundamental algorithmic misunderstandings.
- **Future Work**: Proposes integrating external knowledge (e.g., algorithm documentation or hints) to help the model solve hard-level problems where tracing alone is not enough.
