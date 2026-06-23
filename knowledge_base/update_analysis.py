import re

with open('/Users/istiakahmmedbishal/Desktop/Thesis/knowledge_base/papers_18_31_analysis.md', 'r') as f:
    content = f.read()

content = content.replace(
    '# Papers 18–31: Deep Analysis & Knowledge Extraction',
    '# Papers 18–34: Deep Analysis & Knowledge Extraction'
)

new_analysis = """
## Paper 32: "Beyond Functional Correctness: Investigating Coding Style Inconsistencies in Large Language Models"
**Authors:** Yanlin Wang, Tianyue Jiang, et al. (Sun Yat-sen University, Huawei)
**arXiv:** 2407.00456v2 (Jun 2025)

### Key Contribution
Presents a comprehensive taxonomy of **coding style inconsistencies** between LLM-generated code and human-written code.

### Taxonomy
- **24 inconsistency types** across 5 dimensions:
  1. Formatting (e.g., spaces, blank lines)
  2. Semantic (e.g., naming, comment detail)
  3. Expression/Statement (e.g., assignment, data structure construction)
  4. Control Flow (e.g., loop structures, conditionals)
  5. Fault Tolerance (e.g., input/runtime validation presence and style)

### How This Informs Our Thesis
- **Orthogonal but useful:** While our thesis focuses on *functional/semantic* hallucinations, style inconsistencies (especially in Fault Tolerance) can be seen as a milder form of "hallucination" where the model fails to follow best practices.
- Not a core component for CPV, but provides a good context on LLM behavior.

---

## Paper 33: "AST-Based Deep Learning for Detecting Malicious PowerShell"
**Authors:** Gili Rusak, et al. (MIT CSAIL)
**arXiv:** 1810.09230v1 (Oct 2018)

### Key Contribution
Uses Abstract Syntax Trees (AST) and deep learning for malware detection in PowerShell scripts.
- **Status for our thesis:** ❌ Irrelevant to LLM code hallucination.

---

## Paper 34: "PGS: Effective LLM Code Refinement via Property-Oriented and Structurally Minimal Feedback"
**Authors:** Lehan He, Zeren Chen, Xiang Gao, Zhe Zhang, Lu Sheng (Beihang University, Shanghai AI Lab)
**arXiv:** 2506.18315v2 (May 2026)

### Key Contribution
Introduces the **Property-Generated Solver (PGS)**, a multi-agent framework that uses **Property-Oriented** and **Structurally Minimal** feedback to refine LLM-generated code. This is exactly what we were looking for (previously marked as missing Paper 28)!

### Core Principles
1. **Property-Oriented Feedback:** Shifts from simple I/O mismatch feedback to checking high-level program properties. This prevents the "cycle of self-deception" where models repeat the same logical biases in both code and test generation.
2. **Structurally Minimal Feedback:** Reduces cognitive load by providing the *simplest failing counterexample* (defined empirically as the one with the minimal input token count).

### Framework (Generator & Tester Agents)
- **Generator:** Produces initial code and refines it based on feedback.
- **Tester:** Defines high-level properties from the spec, translates them into executable checks, generates diverse probing inputs, and selects the structurally minimal counterexample.
- **Asymmetry of Verification:** Verifying correctness (writing properties) is inherently easier than generating the solution. PGS exploits this to provide robust guidance.
- **Latent Bug Surfacing:** Property checks injected into code transform silent "Wrong Answer" failures into explicit, machine-checkable "AssertionError"s.

### Results
- Achieves State-of-the-Art (SOTA) on HumanEval, MBPP, LiveCodeBench, CodeContests, and SWE-bench.
- Outperforms heavy debugging frameworks (e.g., MGDebugger, LDB).
- Token count minimization is proven to be the best proxy for feedback simplicity.

### How This Informs Our Thesis
- **Our Closest Competitor & Validation:** PGS completely validates our CPV framework's direction. CPV and PGS share the same core DNA (property-based verification, multi-agent generator/tester).
- **Differentiation:** 
  - PGS relies on an LLM to synthesize inputs (`{IP}`) for property probing. CPV uses **Hypothesis** (property-based fuzzing) which allows for massive, systematic boundary exploration (100s of inputs) rather than relying on LLM-synthesized inputs which might still have blind spots.
  - PGS's "Structurally Minimal" insight (minimal token count) is brilliant and should be integrated into CPV's feedback mechanism (Layer 5).

---
"""

content = content.replace(
    '## The Optimal Thesis Solution (Grounded in Evidence)',
    new_analysis + '\n## The Optimal Thesis Solution (Grounded in Evidence)'
)

content = content.replace(
    '1. **PGS (Property-Generated Solver)** — Our closest competitor. Search: "Property-Generated Solver PBT LLM code generation 2025"\n',
    '~~1. **PGS (Property-Generated Solver)** — FOUND as Paper 34!~~\n'
)

with open('/Users/istiakahmmedbishal/Desktop/Thesis/knowledge_base/papers_18_31_analysis.md', 'w') as f:
    f.write(content)
