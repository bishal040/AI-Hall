# Eliminating Hallucination-Induced Errors in LLM Code Generation with Functional Clustering

## Metadata
**Authors**: Chaitanya Ravuri, Saman Amarasinghe
**Topic**: Functional Clustering for Confidence Estimation and Hallucination Mitigation

## Problem Statement
Despite high capabilities, LLMs frequently hallucinate subtle bugs (like off-by-one errors or mistyped logical operators) that make autonomous deployment risky. Existing confidence metrics (token probabilities or embedding-based clustering) fail to capture functional equivalence—two syntactically different programs might be functionally identical, while a single character change (`<` to `<=`) can fundamentally alter the program's correctness without significantly changing its embedding.

## Methodology
- **Functional Clustering Wrapper**: Proposed a black-box wrapper that clusters candidate programs based entirely on their Input/Output (I/O) behavior rather than their syntax or embeddings.
- **Workflow**:
  1. Sample multiple candidate programs ($n$) from the LLM for the given task.
  2. Prompt the LLM to generate a diverse suite of test inputs ($m$). Crucially, no ground-truth outputs are needed.
  3. Execute all $n$ programs on all $m$ inputs in a sandbox.
  4. Cluster the programs based on exact I/O matching.
  5. The empirical mass (size) of the largest cluster becomes the exact confidence score. If it exceeds a threshold $\tau$, the system outputs the code; otherwise, it abstains.

## Key Findings
- **Statistical Rigor**: The method provides an exact, mathematically sound confidence estimate with exponential Chernoff bounds. If a cluster dominates, it is exponentially unlikely to be a random hallucination.
- **Drastic Error Reduction**: On LiveCodeBench, applying the functional clustering wrapper slashed the error rate of returned answers from ~65% down to 2%. At a more conservative threshold, the error rate dropped to a provable 0% while still answering 15.6% of the prompts.
- **Shifting the Bottleneck**: Manual audits revealed that the *only* residual errors that slip through the functional clustering threshold are caused by the LLM fundamentally misinterpreting the prompt's specifications (e.g., ignoring a constraint), not from random generation noise or typical hallucinations. 

## Limitations & Future Work
- **Limitations**: The method assumes the programming task has a single functionally correct equivalence class. It fails on tasks that accept multiple valid outputs (e.g., returning an unordered list, where different sorting orders are valid but produce different exact outputs). It also requires a secure sandbox to execute potentially untrusted LLM code.
- **Future Work**: Extend the method to handle property-based testing or coverage-guided testing to support tasks with multiple valid outputs.
