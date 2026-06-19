# TGPR: Tree-Guided Policy Refinement for Robust Self-Debugging of LLMs

## Metadata
**Authors**: Daria Ozerova, Ekaterina Trofimova
**Topic**: Reinforcement Learning for LLM Self-Debugging

## Problem Statement
Iterative refinement allows Large Language Models to debug their own code based on execution feedback. However, standard reinforcement learning approaches (like GRPO) used to train models for self-debugging struggle with the exploration-exploitation dilemma. They often fail to efficiently navigate the massive search space of possible code repairs, getting stuck in local optima.

## Methodology
- **TGPR Framework**: Introduced "Tree-Guided Policy Refinement" (TGPR), combining Group Relative Policy Optimization (GRPO) with a Thompson Sampling-guided tree search.
- **Training-Time Data Augmentation**: Crucially, the tree search is used *only during training* to generate highly diverse and high-quality refinement trajectories (both successful and informative failures). This teaches the model a robust debugging policy without incurring the massive computational cost of tree search during inference.
- **Custom Reward Function**: Used a dense, hybrid reward function that combines `CodeBLEU` (for syntactic and semantic progress) with unit test pass rates (`pass@k`).
- **Evaluation**: Fine-tuned a Qwen-7B model using TGPR and evaluated it on HumanEval, MBPP, and APPS benchmarks against standard GRPO and PPO baselines.

## Key Findings
- **Superior Performance**: TGPR significantly outperforms standard GRPO and pretrained baselines across all benchmarks.
- **Metrics**: 
  - On MBPP, TGPR improved pass@1 by 4.2 percentage points (to 31.0%).
  - On APPS (the most complex benchmark), it achieved an impressive +12.51 percentage points absolute improvement in pass@10 (reaching 46.7%).
- **Better Exploration**: The Thompson Sampling approach successfully balances exploring uncertain code edits and exploiting promising ones, providing a much richer learning signal to the policy than naive on-policy exploration.
- **Steeper Learning Curve**: TGPR demonstrates a steeper learning curve during refinement iterations compared to baseline prompting, reaching higher final performance faster.

## Limitations & Future Work
- The approach is computationally intensive during the training phase due to the parallel environment rollouts required for the tree search.
- The framework currently focuses on code debugging but presents a generalized paradigm for combining learned policies with structured search methods for any complex, stateful reasoning tasks.
