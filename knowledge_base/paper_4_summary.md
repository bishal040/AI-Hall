# A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions

## Metadata
**Authors**: Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, Ting Liu
**Topic**: General Survey on LLM Hallucinations (Focusing on Factuality and Faithfulness)

## Problem Statement
The open-ended nature of Large Language Models (LLMs) makes them highly susceptible to generating plausible but nonfactual or unfaithful content. The scale and versatility of LLMs necessitate a broader, redefined taxonomy for hallucinations compared to traditional natural language generation tasks, along with an updated understanding of causes, detection methods, and mitigations.

## Methodology
- **Comprehensive Survey**: Conducted a deep dive into the literature surrounding LLM hallucinations, covering principles, taxonomies, and challenges.
- **Redefined Taxonomy**: Proposed an updated taxonomy suited for general-purpose LLMs rather than task-specific models.
- **Root Cause Analysis**: Deconstructed hallucination causes across three stages: Data, Training, and Inference.

## Key Findings
- **Taxonomy**: Hallucinations are split into two core types:
  1. *Factuality Hallucinations*: Factual contradictions (entity/relation errors) and Factual fabrications (unverifiable claims or overclaims).
  2. *Faithfulness Hallucinations*: Instruction inconsistency, context inconsistency, and logical inconsistency.
- **Causes**:
  - *Data*: Misinformation/biases in pre-training corpora, knowledge boundaries (long-tail, recent, or copyrighted data), and poor alignment data.
  - *Training*: Issues like unidirectional representation, attention glitches, supervised fine-tuning pushing models beyond their actual knowledge limits, and RLHF-induced sycophancy (telling the user what they want to hear instead of the truth).
  - *Inference*: Flaws in decoding strategies (e.g., stochastic sampling introducing errors), over-confidence, softmax bottlenecks, and reasoning failures.
- **Detection & Benchmarks**: Reviewed methods ranging from fact-checking (external/internal retrieval) to uncertainty estimation (using internal states or multi-debate behavior).
- **RAG Limitations**: Highlighted that Retrieval-Augmented Generation (RAG) is highly effective but has severe bottlenecks, including retrieval failures (from ambiguous/complex queries) and generation failures (due to noisy contexts, context conflicts, and the "lost-in-the-middle" phenomenon).

## Limitations & Future Work
- The survey points to the urgent need for researching hallucinations in Large Vision-Language Models (LVLMs).
- Recommends further probing into understanding the strict "knowledge boundaries" within LLMs so models can reliably output "I don't know" rather than hallucinate.
