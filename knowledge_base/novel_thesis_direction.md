# 🔬 Finding The Genuinely Novel Thesis Contribution
## What Paper 35 (PRISM-MCTS) Changes, What Paper 34 (PGS) Already Covers, and Where the Real Gap Is

---

## The Honest Overlap Assessment

Let me be brutally honest about what's already taken:

### What PGS (Paper 34) Already Does ✅
- Multi-agent Generator/Tester architecture
- Property-oriented feedback (extracting properties from specs)
- Structurally minimal counterexamples (min token count)
- Latent bug surfacing via assertion injection
- Exploits the "verification asymmetry" (verifying is easier than generating)
- **SOTA results** on HumanEval, MBPP, LiveCodeBench, CodeContests, SWE-bench

### What PRISM-MCTS (Paper 35) Already Does ✅
- Heuristics Memory (stores successful reasoning patterns)
- Fallacies Memory (stores failed reasoning patterns)
- Metacognitive reflection mechanism
- Process Reward Model for step-level evaluation
- Memory Manager for knowledge distillation
- Reduces search breadth by 55% while maintaining or improving accuracy

### What Our Previous "PRISM" Proposal Overlapped With ❌
| Our Claim | Already Exists In |
|:---|:---|
| Property-based verification with multi-agent | PGS (Paper 34) — exact same architecture |
| Metacognitive gating | PRISM-MCTS (Paper 35) — same concept, same name |
| Heuristics/Fallacies classification | PRISM-MCTS (Paper 35) — same mechanism |
| Structurally minimal feedback | PGS (Paper 34) — their contribution |
| Spec-derived invariants | PGS (Paper 34) — their "property-oriented" approach |

**Bottom line:** Our previous proposal was inadvertently a mashup of PGS + PRISM-MCTS. Both already published. We cannot claim this as novel.

---

## The Genuine Gaps (What NO Paper Addresses)

After analyzing all 35 papers, here are the **real** unexplored territories:

### Gap 1: The "Verifier Hallucination" Problem
**The blind spot:** Every verification framework (PGS, Self-Debug, Semantic Triangulation) assumes the verification mechanism itself is correct. PGS generates properties from specs — but what if the **properties are hallucinated?**

- PGS says "verification is easier than generation" (their "asymmetry" claim)
- But they **never measure** how often their Tester agent generates wrong properties
- If property `P` is wrong, and code `C` satisfies `P`, the system declares `C` correct — but it's not
- **Nobody has studied this failure mode.** Nobody has a number for "property hallucination rate."

### Gap 2: Deterministic Fuzzing vs LLM-Generated Inputs
**The blind spot:** PGS uses the LLM itself to generate "probing inputs." But:
- LLM-generated inputs have the **same blind spots** as LLM-generated code
- If the model doesn't understand that `[]` (empty list) is a critical edge case, it won't generate it as a test input either
- **No paper compares** systematic fuzzing (Hypothesis library — random, boundary-aware, shrinking) against LLM-generated test inputs

### Gap 3: Error Type Classification for Repair Strategy
**The blind spot:** Every repair system (PGS, Self-Debug, Self-Repair) applies the **same repair strategy** regardless of error type:
- "Here's a failing test case, fix your code"
- But Paper 26 proved feedback quality is THE bottleneck
- Nobody distinguishes between:
  - **Cognitive error** (model doesn't understand the algorithm) → needs full regeneration, not patching
  - **Translation error** (model understands but miscoded) → needs targeted fix
- **No paper implements or evaluates** type-aware repair routing

### Gap 4: Cross-Problem Property Learning
**The blind spot:** PGS generates properties fresh for every problem. But:
- Many properties are **reusable** across similar problems (sorting ↔ sorted output, searching ↔ element exists)
- No system builds a **property knowledge base** that improves over time
- Retrieval-augmented property generation could dramatically improve property quality

### Gap 5: Calibrated Confidence + Abstention for Code
**The blind spot:** No code verification system says "I don't know":
- PGS always outputs a solution
- Self-Debug always outputs a solution
- Paper 22 shows +26% F1 in abstention scenarios — but for NL, not code
- **Nobody has implemented or measured** calibrated abstention for code generation

---

## Three Possible Novel Thesis Directions

### Direction A: "The Verifier's Dilemma" (Most Novel)

**Title:** *"Who Verifies the Verifier? Detecting and Mitigating Hallucination in Both LLM-Generated Code and LLM-Generated Test Properties"*

**Core Insight:** PGS proves property-based verification works. But PGS trusts its properties blindly. We propose **dual-channel verification** where code AND properties are independently verified against each other, with a deterministic arbiter (Hypothesis fuzzing) breaking ties.

**Novel Contributions:**
1. **Empirical study of Property Hallucination Rates** — first-ever measurement of how often LLM-generated properties are themselves wrong (across HumanEval, MBPP, LiveCodeBench). This alone is publishable.
2. **Mutual Cross-Verification** — Generate code (Agent A), generate properties (Agent B), generate a **reference implementation** (Agent C — a simpler, brute-force solution). Use the reference to validate properties before properties validate code.
3. **Deterministic Fuzzing vs LLM Inputs** — head-to-head comparison of Hypothesis (systematic, boundary-aware) vs PGS's LLM-generated inputs. Controlled experiment measuring which approach finds more bugs.
4. **Tri-Agent Confidence Scoring** — if code passes properties AND properties are validated by reference → high confidence. If disagreement → abstain.

**Architecture:**
```
┌─────────────────────────────────────────────────────┐
│              PHASE 1: Tri-Agent Generation           │
│                                                      │
│  Agent A: Generates optimized solution               │
│  Agent B: Generates properties from spec             │
│  Agent C: Generates brute-force reference solution   │
│           (simple, correct, slow)                    │
│                                                      │
│  Key: A, B, C are INDEPENDENT (decorrelated errors)  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│         PHASE 2: Property Validation (NEW)           │
│                                                      │
│  Run Agent C's reference against Agent B's properties│
│  on random inputs from Hypothesis fuzzer             │
│                                                      │
│  If reference PASSES properties → properties valid   │
│  If reference FAILS properties → PROPERTY IS WRONG   │
│    → Remove hallucinated property before using it    │
│    → Flag this property class for future caution     │
│                                                      │
│  ★ THIS IS THE NOVEL CONTRIBUTION ★                  │
│  Nobody validates properties before using them.      │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│         PHASE 3: Code Verification                   │
│                                                      │
│  Run Agent A's optimized code against:               │
│    1. Validated properties (from Phase 2)            │
│    2. Hypothesis fuzzer (systematic boundary inputs) │
│    3. Cross-check against Agent C's reference output │
│       on random inputs                               │
│                                                      │
│  If A agrees with C on ALL inputs AND passes all     │
│  validated properties → VERIFIED                     │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│         PHASE 4: Repair (if needed)                  │
│                                                      │
│  Classify error:                                     │
│    A disagrees with C → find minimal failing input   │
│    Show: "On input X, your code returns Y,           │
│           but the correct answer is Z"               │
│                                                      │
│  Use Agent C's output as GROUND TRUTH for repair     │
│  Max 2 repair rounds (Paper 26: diminishing returns) │
│                                                      │
│  If repair fails → ABSTAIN                           │
└─────────────────────────────────────────────────────┘
```

**Why This Is Novel (Differentiation from PGS):**

| Dimension | PGS (Paper 34) | Our Direction A |
|:---|:---|:---|
| Property validation | ❌ Trusts properties blindly | ✅ Validates properties against reference |
| Input generation | LLM-generated inputs | Hypothesis (systematic fuzzing) |
| Reference oracle | None | Brute-force reference implementation |
| Property hallucination measurement | Not studied | First empirical study |
| Abstention | Never abstains | Calibrated confidence + abstention |
| Error type classification | Not distinguished | Cognitive vs Translation routing |

**Risk Assessment:**
- Agent C (brute-force reference) may itself be wrong → but brute-force solutions are dramatically simpler and less prone to hallucination (this is measurable)
- Agent C is slow → only used for validation on small inputs (Hypothesis shrinks to minimal counterexamples)
- 3 agents = more API cost → but Agent C generates simple code (fewer tokens)

---

### Direction B: "Adaptive Verification Intensity" (Most Practical)

**Title:** *"Predicting Code Hallucination Risk: Adaptive Verification Intensity for Cost-Effective LLM Code Generation"*

**Core Insight:** Not every problem needs heavy verification. A sorting function needs minimal checking; a DP-on-a-graph needs maximum verification. No paper predicts hallucination risk BEFORE generation and routes problems accordingly.

**Novel Contributions:**
1. Build a **hallucination risk predictor** from problem features (complexity, algorithm category, constraint count)
2. Route problems to different verification intensities:
   - Low risk → basic test execution only
   - Medium risk → property-based verification (PGS-style)
   - High risk → full tri-agent verification (Direction A)
3. **Dataset contribution:** labeled dataset of 1000+ problems with hallucination outcomes across 3 LLMs
4. Measure cost-performance tradeoff (API calls saved vs hallucination caught)

**Risk:** The predictor may not work well enough. Novelty is in the prediction, not the verification.

---

### Direction C: "Error-Type-Aware Repair" (Most Focused)

**Title:** *"Beyond Counterexamples: Cognitive Error Classification for Targeted LLM Code Repair"*

**Core Insight:** All repair systems give the same feedback regardless of error type. We propose classifying errors as cognitive (model doesn't understand) vs translation (model understands but miscoded) and routing to different repair strategies.

**Novel Contributions:**
1. **Error taxonomy for repair:** define and validate cognitive vs translation error classification
2. **Type-aware repair strategies:** full regeneration for cognitive errors, surgical fix for translation errors
3. **Empirical validation:** measure repair success rates for each strategy on each error type
4. Layer this on top of PGS as an enhancement

**Risk:** The classification itself may be unreliable. The contribution is narrower than Direction A.

---

## My Recommendation

### **Direction A is the strongest thesis.**

Here's why:

1. **It has MULTIPLE novel contributions**, not just one:
   - Property hallucination measurement (empirical, publishable standalone)
   - Property validation via reference (architectural, novel mechanism)
   - Hypothesis vs LLM-inputs comparison (experimental, controlled study)
   - Tri-agent confidence scoring (practical, measurable)

2. **It directly builds on PGS (Paper 34)** rather than competing with it:
   - PGS is your foundation ("we build on PGS")
   - Your contribution is: "PGS trusts properties blindly. We show this is dangerous. Here's how to fix it."
   - This is a MUCH stronger thesis position than "we did PGS but slightly different"

3. **The brute-force reference is the killer insight:**
   - For HumanEval/MBPP problems, a brute-force O(n²) or O(n³) solution is trivially correct
   - The LLM is MUCH better at generating simple brute-force than optimized solutions
   - Use the easy thing (brute-force) to validate the hard thing (optimized code)
   - This has never been done systematically

4. **It's buildable:** ~1200 lines of Python, no model weight access, works with any LLM API

### Recommended Thesis Title:

> **"Who Verifies the Verifier? Mitigating Dual Hallucination in LLM-Generated Code and Test Properties through Reference-Validated Invariants and Deterministic Fuzzing"**

### One-Sentence Thesis Statement:

> "We demonstrate that LLM-generated verification properties are themselves hallucinated 12-18% of the time, and propose a tri-agent framework that validates properties against a brute-force reference before using them to verify optimized code — achieving higher reliability than existing property-based approaches while providing calibrated confidence for safe abstention."

> ⚠️ **Note:** The "12-18%" is a hypothesis to be validated empirically. This number is the core empirical contribution of the thesis.
