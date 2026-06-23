# VERTEX: The Genuinely Novel Thesis Direction
## Verified-Property Extraction with Reference Cross-Testing and Execution-Based Validation
### Comprehensive Analysis After Paper 35 — Honest Overlap Assessment & Novel Contribution

> **Context:** Our previous recommendation (PRISM) was invalidated by Papers 34 (PGS) and 35 (PRISM-MCTS), which already publish the core mechanisms we proposed. This document presents an honest overlap audit and identifies a genuinely novel thesis contribution grounded in the gaps across ALL 35 papers.

---

## Executive Summary

After analyzing all 35 research papers and 10 proposed solution frameworks, **two critical discoveries** emerged:

1. **PGS (Paper 34)** already implements the core of our CPV/PRISM proposal: multi-agent property-based verification with structurally minimal counterexamples. It achieves SOTA on all major benchmarks.

2. **PRISM-MCTS (Paper 35)** already implements metacognitive reflection with heuristics/fallacies memory — overlapping with our metacognitive gating and error classification mechanisms.

**However, a genuine gap exists across ALL 35 papers:** No system validates whether its *verification properties* are themselves correct. Every framework — PGS, Self-Debug, Semantic Triangulation — blindly trusts its verification mechanism. We call this the **"Verifier's Dilemma"**: who verifies the verifier?

The recommended thesis direction is **VERTEX (Verified-Property Extraction with Reference Cross-Testing)** — a tri-agent framework that:
- Generates an optimized solution (Agent A)
- Generates verification properties (Agent B)  
- Generates a brute-force reference oracle (Agent C)
- **Validates properties against the reference before using them to verify code**
- Uses Hypothesis (deterministic fuzzing) instead of LLM-generated inputs

This is the first system to empirically measure **Property Hallucination Rates** and to close the verification loop.

---

## Part 1: Honest Overlap Audit — What's Already Taken

### What PGS (Paper 34) Already Implements

| Mechanism | PGS Does This? | Evidence |
|:---|:---|:---|
| Multi-agent generator/tester architecture | ✅ Yes | Generator + Tester agents |
| Property-oriented feedback from specs | ✅ Yes | Their primary contribution |
| Structurally minimal counterexamples | ✅ Yes | Minimal token count selection |
| Latent bug surfacing via assertion injection | ✅ Yes | Transform WA → AssertionError |
| Verification asymmetry (verifying < generating) | ✅ Yes | Their theoretical foundation |
| SOTA on HumanEval, MBPP, LiveCodeBench, CodeContests, SWE-bench | ✅ Yes | Published results |

### What PRISM-MCTS (Paper 35) Already Implements

| Mechanism | PRISM-MCTS Does This? | Evidence |
|:---|:---|:---|
| Heuristics Memory (store successful patterns) | ✅ Yes | MEMH module |
| Fallacies Memory (store failed patterns) | ✅ Yes | MEMF module |
| Metacognitive reflection | ✅ Yes | Their core contribution |
| Process Reward Model for step evaluation | ✅ Yes | Dual-stage PRM |
| Memory Manager for knowledge distillation | ✅ Yes | Filters redundant entries |
| 55% reduction in search breadth | ✅ Yes | Published results on GPQA, MATH |

### What Our Previous "PRISM" Proposal Overlapped

| Our Claim | Already Exists In |
|:---|:---|
| Property-based verification with multi-agent | PGS (Paper 34) — exact same architecture |
| Metacognitive gating | PRISM-MCTS (Paper 35) — same name, same concept |
| Structurally minimal feedback | PGS (Paper 34) — their contribution |
| Spec-derived invariants | PGS (Paper 34) — their "property-oriented" approach |
| Error classification into categories | PRISM-MCTS (Paper 35) — heuristics/fallacies |

> ⚠️ **Our previous PRISM proposal was inadvertently a mashup of PGS + PRISM-MCTS.** Both already published. We cannot claim this as novel. The thesis requires a fundamentally different contribution.

---

## Part 2: The 5 Genuine Gaps No Paper Addresses

### Gap 1: The "Verifier Hallucination" Problem ★★★★★
Every verification framework (PGS, Self-Debug, Semantic Triangulation) **blindly trusts** its verification mechanism. PGS generates properties from specs — but the properties can be wrong.

- PGS claims "verification is easier than generation" but **never measures** property accuracy
- If property P is wrong and code C satisfies P, the system falsely declares C correct
- **Nobody has published a number for "property hallucination rate"**

### Gap 2: Deterministic Fuzzing vs LLM-Generated Inputs ★★★★
PGS uses LLM-generated "probing inputs." But LLM-generated inputs share the **same blind spots** as LLM-generated code.

- If the model doesn't know `[]` is a critical edge case, it won't generate it as a test input
- Hypothesis library generates: empty, single-element, max-size, negative, duplicate, sorted, reverse-sorted inputs **automatically**
- **No paper compares** Hypothesis vs LLM-generated test inputs head-to-head

### Gap 3: Error Type Classification for Repair ★★★★
Every repair system applies the **same strategy** regardless of error type:

- Paper 26 proved feedback quality is THE bottleneck
- **Cognitive error** (model doesn't understand algorithm) → needs full regeneration
- **Translation error** (model understands but miscoded) → needs targeted counterexample
- **No paper implements or evaluates** type-aware repair routing

### Gap 4: Reference Oracle for Validation ★★★★★
No system generates a **brute-force reference implementation** to validate both code AND properties:

- For HumanEval/MBPP problems, brute-force O(n²) solutions are trivially correct
- LLMs are dramatically better at generating simple brute-force than optimized solutions
- Use the easy thing to validate the hard thing — **never systematically attempted**

### Gap 5: Calibrated Abstention for Code ★★★
Paper 22 shows +26% F1 in abstention scenarios — but for NL, not code.

- No code verification system says "I don't know"
- PGS, Self-Debug, Self-Repair all always output a solution
- **Nobody has measured** calibrated abstention for code generation

---

## Part 3: The VERTEX Architecture

### The Core Insight

```
PGS says:    "Verifying code is easier than generating code."
VERTEX asks: "But who verifies the verifier?"

PGS:    Spec → Properties → Test Code → Pass/Fail
                  ↑
                  └── This can be WRONG.
                      Nobody checks.

VERTEX: Spec → Properties → Validate Properties → THEN Test Code
                                  ↑
                                  └── Use a brute-force reference
                                      to check if properties are correct
                                      BEFORE using them
```

### Full Architecture

```
┌──────────────────────────────────────────────────────────┐
│                PHASE 1: Tri-Agent Generation              │
│                                                           │
│  Agent A (Optimizer): Generates optimized solution        │
│    Prompt: "Solve this efficiently"                       │
│                                                           │
│  Agent B (Verifier): Generates properties from spec       │
│    Prompt: "What must ALWAYS be true about correct output?│
│             Express as Python assert statements"          │
│                                                           │
│  Agent C (Oracle): Generates brute-force reference        │
│    Prompt: "Solve this in the SIMPLEST way possible.      │
│             O(n²) or O(n³) is fine. Prioritize clarity    │
│             and correctness over speed."                  │
│                                                           │
│  ★ All 3 agents are INDEPENDENT — decorrelated errors     │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│          PHASE 2: Property Validation (★ NOVEL ★)         │
│                                                           │
│  Step 2a: Execute Agent C's reference on 100+ random      │
│           inputs from Hypothesis fuzzer                   │
│                                                           │
│  Step 2b: Check Agent B's properties against Agent C's    │
│           outputs on those same inputs                    │
│                                                           │
│  For each property:                                       │
│    If reference PASSES property → property VALIDATED ✅    │
│    If reference FAILS property → property HALLUCINATED 🚨 │
│      → Remove it before using it to test Agent A          │
│      → Log: which property type, which model, why        │
│                                                           │
│  Output: Validated Property Set (VPS)                     │
│  Metric: Property Hallucination Rate = |removed|/|total|  │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│           PHASE 3: Dual-Channel Code Verification         │
│                                                           │
│  Channel 1 — Property Testing:                            │
│    Run Agent A's code against Validated Property Set       │
│    using Hypothesis fuzzer (100+ systematic inputs)       │
│    If violation → concrete counterexample                 │
│                                                           │
│  Channel 2 — Differential Testing:                        │
│    Run Agent A AND Agent C on same random inputs           │
│    Compare outputs                                        │
│    If disagreement → Agent C's output is ground truth     │
│    Find MINIMAL disagreeing input (Paper 34's insight)    │
│                                                           │
│  Confidence Score:                                        │
│    Both channels pass       → HIGH (95%+)                 │
│    Properties pass, diff ok → HIGH (90%+)                 │
│    Properties pass, no ref  → MEDIUM (75%)                │
│    Any channel fails        → trigger Phase 4             │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│           PHASE 4: Error-Classified Repair                │
│                                                           │
│  Step 4a: Classify the error (SHADOW's insight)           │
│    Ask Agent A: "What will your code output for input X?" │
│    If Agent A predicts WRONG output:                      │
│      → COGNITIVE ERROR (doesn't understand algorithm)     │
│      → Full regeneration with enhanced spec context       │
│    If Agent A predicts CORRECT but code outputs wrong:    │
│      → TRANSLATION ERROR (understands but miscoded)       │
│      → Surgical repair: "On input X, expected Z, got Y"  │
│                                                           │
│  Step 4b: Repair (max 2 rounds — Paper 26)                │
│    Provide: failing input + expected output (from ref)    │
│    + validated property that was violated                 │
│                                                           │
│  Step 4c: If repair fails → ABSTAIN                       │
│    Output: "Insufficient confidence. Problem flagged."    │
└──────────────────────────────────────────────────────────┘
```

---

## Part 4: Why VERTEX Is Genuinely Novel (vs ALL 35 Papers)

| Dimension | PGS (Paper 34) | PRISM-MCTS (35) | Self-Debug (25) | Sem. Triang. (22) | VERTEX |
|:---|:---|:---|:---|:---|:---|
| Property generation | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Property validation** | ❌ Trusts blindly | ❌ N/A | ❌ | ❌ | **✅ Via reference oracle** |
| Brute-force reference | ❌ | ❌ | ❌ | ❌ | **✅ Agent C** |
| Input generation | LLM-generated | N/A | Unit tests | Problem transform | **Hypothesis (deterministic)** |
| Error type classification | ❌ | ❌ | ❌ | ❌ | **✅ Cognitive vs Translation** |
| Calibrated abstention | ❌ | ❌ | ❌ | ✅ (partial) | **✅ Confidence scoring** |
| **Property halluc. measurement** | ❌ | ❌ | ❌ | ❌ | **✅ First empirical study** |
| Domain | Code | General reasoning | Code | Code | **Code** |

### The 4 Novel Contributions (None Exist in Any Paper)

1. **Empirical Study of Property Hallucination Rates**
   - First-ever measurement of how often LLM-generated properties are wrong
   - Measured across HumanEval (164), MBPP (974), LiveCodeBench
   - Across 3 models (GPT-4, Claude, Gemini)
   - **This alone is a publishable contribution**

2. **Reference-Validated Invariants (Phase 2)**
   - Use a brute-force oracle to validate properties BEFORE using them
   - Remove hallucinated properties from the validation set
   - No paper does this

3. **Hypothesis vs LLM-Generated Inputs (Controlled Experiment)**
   - Head-to-head: does Hypothesis find more bugs than PGS's LLM-generated inputs?
   - Measure: bug detection rate, boundary coverage, edge case discovery
   - No paper compares these approaches

4. **Error-Type-Aware Repair Routing**
   - Cognitive errors → full regeneration
   - Translation errors → counterexample-driven surgical repair
   - First implementation and empirical evaluation

---

## Part 5: Detailed Implementation Plan

### Project Structure

```
vertex/
├── main.py                      # Entry point & pipeline orchestrator
├── agents/
│   ├── optimizer.py             # Agent A — optimized solution generation
│   ├── verifier.py              # Agent B — property extraction from spec
│   └── oracle.py                # Agent C — brute-force reference generation
├── validation/
│   ├── property_validator.py    # Phase 2 — validate properties via reference
│   ├── hypothesis_fuzzer.py     # Hypothesis integration + strategy config
│   └── differential_tester.py   # Compare Agent A vs Agent C outputs
├── repair/
│   ├── error_classifier.py      # Cognitive vs Translation classification
│   └── repairer.py              # Type-aware repair with counterexamples
├── confidence/
│   └── scoring.py               # Confidence computation + abstention gate
├── utils/
│   ├── llm_client.py            # API abstraction (GPT/Claude/Gemini)
│   ├── sandbox.py               # Subprocess-based safe execution
│   └── counterexample.py        # Minimal counterexample selection
├── benchmarks/
│   ├── humaneval_loader.py      # HumanEval benchmark loader
│   ├── mbpp_loader.py           # MBPP benchmark loader
│   └── livecodebench_loader.py  # LiveCodeBench loader
├── evaluation/
│   ├── metrics.py               # Pass@1, hallucination rate, abstention rate
│   ├── property_halluc_study.py # Property hallucination measurement
│   ├── hypothesis_vs_llm.py     # Controlled comparison experiment
│   └── ablation.py              # Component removal experiments
└── results/
    └── figures/                 # Generated plots and tables
```

**Total estimated code: ~1,400 lines of Python**

### Phase-by-Phase Timeline

#### Phase 1: Foundation (Week 1-3)

| Task | Deliverable | LOC |
|:---|:---|:---|
| LLM client abstraction (GPT/Claude/Gemini) | `llm_client.py` | ~80 |
| Sandbox executor | `sandbox.py` | ~100 |
| Agent A — optimized code generation | `optimizer.py` | ~80 |
| Agent B — property extraction | `verifier.py` | ~120 |
| Agent C — brute-force oracle | `oracle.py` | ~80 |
| Benchmark loaders (HumanEval, MBPP) | `benchmarks/` | ~100 |
| **Milestone:** All 3 agents generate output for 10 problems | | |

#### Phase 2: The Novel Core (Week 4-6)

| Task | Deliverable | LOC |
|:---|:---|:---|
| Hypothesis fuzzer integration | `hypothesis_fuzzer.py` | ~150 |
| **Property Validator (★ CORE CONTRIBUTION)** | `property_validator.py` | ~200 |
| Differential tester (Agent A vs Agent C) | `differential_tester.py` | ~100 |
| Counterexample minimization | `counterexample.py` | ~60 |
| **Milestone:** Property hallucination detected on test problems | | |

#### Phase 3: Repair & Confidence (Week 7-8)

| Task | Deliverable | LOC |
|:---|:---|:---|
| Error classifier (cognitive vs translation) | `error_classifier.py` | ~80 |
| Type-aware repairer | `repairer.py` | ~120 |
| Confidence scoring + abstention | `scoring.py` | ~80 |
| Full pipeline orchestrator | `main.py` | ~150 |
| **Milestone:** End-to-end pipeline runs on 50 problems | | |

#### Phase 4: Evaluation & Writing (Week 9-14)

| Task | Deliverable |
|:---|:---|
| **Experiment 1:** Property Hallucination Rate study | Table: rates across models × benchmarks |
| **Experiment 2:** Hypothesis vs LLM inputs | Table: bug detection rate comparison |
| **Experiment 3:** Full benchmark (HumanEval, MBPP) | Pass@1, detection rate, abstention rate |
| **Experiment 4:** Ablation study | Remove each component, measure impact |
| **Experiment 5:** Multi-model evaluation | GPT-4, Claude, Gemini |
| **Experiment 6:** Comparison vs PGS baseline | VERTEX vs PGS on same benchmarks |
| Thesis writing | Chapters 1-6 |

---

## Part 6: Experimental Design

### Experiment 1: Property Hallucination Rate (★ Core Empirical Contribution)

**Question:** How often are LLM-generated properties themselves wrong?

**Method:**
1. For each problem in HumanEval (164 problems):
   - Generate 5-10 properties from the spec using Agent B
   - Execute the KNOWN CORRECT solution (from the benchmark) against each property
   - If correct solution fails a property → that property is hallucinated
2. Repeat across 3 models (GPT-4, Claude, Gemini)
3. Categorize hallucinated properties by type:
   - Overly strict (rejects correct solutions)
   - Logically contradictory
   - Irrelevant (tests something not in the spec)
   - Syntactically invalid

**Expected output:**

| Model | Total Properties | Hallucinated | Rate |
|:---|:---|:---|:---|
| GPT-4 | ~1,200 | ~??? | ???% |
| Claude | ~1,200 | ~??? | ???% |
| Gemini | ~1,200 | ~??? | ???% |

> This table — with real numbers — IS the thesis contribution. Nobody has published these numbers.

### Experiment 2: Hypothesis vs LLM-Generated Inputs

**Question:** Does systematic fuzzing find more bugs than LLM-generated test inputs?

**Method:**
1. Take 100 problems from MBPP
2. For each, generate buggy code (temperature=0.8)
3. Test with:
   - (a) Hypothesis fuzzer (100 random inputs with shrinking)
   - (b) PGS-style LLM-generated inputs (ask LLM for 10 probing inputs)
4. Measure: which approach detects the bug first? On how many problems?

**Expected output:**

| Metric | Hypothesis | LLM Inputs |
|:---|:---|:---|
| Bug detection rate | ???% | ???% |
| Mean inputs to detection | ??? | ??? |
| Edge case coverage | ??? | ??? |
| Empty/boundary detection | ???% | ???% |

### Experiment 3: Full Benchmark Evaluation

**Metrics:**
- **Pass@1:** Percentage of problems solved correctly on first attempt
- **Verified Pass@1:** Pass@1 among problems the system is confident about
- **Abstention Rate:** Percentage of problems where system abstains
- **Property Hallucination Rate:** Properties removed by Phase 2
- **Error Classification Accuracy:** Manual validation on 50 problems

### Experiment 4: Ablation Study

| Configuration | What's Removed | Expected Impact |
|:---|:---|:---|
| Full VERTEX | Nothing | Baseline |
| − Property Validation | Remove Phase 2 | Higher false positive rate |
| − Reference Oracle | Remove Agent C | No property validation, no diff testing |
| − Hypothesis (use LLM inputs) | Replace fuzzer | Lower edge case detection |
| − Error Classification | Same repair for all | Lower repair success on cognitive errors |
| − Abstention | Always output | Lower precision |

---

## Part 7: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---|:---|
| Agent C (brute-force) is itself wrong | Medium | High | Brute-force solutions are dramatically simpler — measure C's accuracy separately. For HumanEval, brute-force Pass@1 should be >90%. |
| Property hallucination rate is very low (<5%) | Medium | High | If properties are rarely wrong, the thesis contribution weakens. Mitigation: test with weaker models (GPT-3.5, open-source) where rates should be higher. Also, the measurement itself is still novel even if rates are low. |
| Hypothesis is slower than LLM inputs | Low | Low | Set timeout (30s). Hypothesis's shrinking ensures minimal counterexamples. Speed is a tradeoff, not a blocker. |
| Error classification is unreliable | Medium | Medium | Manually label 50 problems. If accuracy <75%, simplify to binary (fixable/not-fixable). |
| 3 agents = high API cost | High | Medium | Agent C generates simple code (fewer tokens). Total per problem: ~4-6 API calls. Budget: ~$200 for full HumanEval+MBPP evaluation. |
| PGS publishes a follow-up addressing property validation | Low | High | Move fast. Submit empirical property hallucination study as a short paper while building the full system. |

---

## Part 8: Differentiation Statement (For Thesis Defense)

> **"How is this different from PGS (Paper 34)?"**

"PGS established that property-based verification with multi-agent architectures effectively catches code hallucination. We build directly on this foundation. However, PGS makes a critical assumption: that its generated properties are correct. Our thesis demonstrates empirically that LLM-generated properties are themselves hallucinated X% of the time — a failure mode PGS does not address. VERTEX closes this verification loop by introducing a brute-force reference oracle that validates properties before they are used to verify code, combined with deterministic fuzzing (Hypothesis) for systematic boundary exploration and cognitive/translation error classification for targeted repair."

> **"How is this different from PRISM-MCTS (Paper 35)?"**

"PRISM-MCTS applies metacognitive reflection to general reasoning tasks using Monte Carlo Tree Search. VERTEX operates in a fundamentally different domain (code generation verification) using fundamentally different mechanisms (property validation via reference oracles, deterministic fuzzing). The only conceptual overlap is the high-level notion of 'learning from failures' — but PRISM-MCTS stores reasoning heuristics in memory during tree search, while VERTEX validates generated test properties against a brute-force reference before using them. The mechanisms, domain, and contributions are distinct."

---

## Part 9: Thesis Title & Statement

### Recommended Title:

> **"Who Verifies the Verifier? Mitigating Dual Hallucination in LLM-Generated Code and Test Properties through Reference-Validated Invariants and Deterministic Fuzzing"**

### Subtitle Options:
- "A Tri-Agent Framework for Closing the Verification Loop in LLM Code Generation"
- "Empirical Evidence that LLM-Generated Properties Hallucinate, and a System to Fix It"

### One-Sentence Thesis Statement:

> "We demonstrate that LLM-generated verification properties are themselves hallucinated at a measurable rate, and propose VERTEX — a tri-agent framework that validates properties against a brute-force reference oracle before using them to verify optimized code, achieving higher reliability than existing property-based approaches while providing calibrated confidence for safe abstention."

---

## Part 10: How This Builds on (Not Competes With) Existing Work

```
Foundation Layer:
  Self-Debugging (Paper 25)     → Established that LLMs can use execution feedback
  Self-Repair (Paper 26)        → Proved feedback quality is THE bottleneck
  Semantic Triangulation (22)   → Showed decorrelation catches correlated errors

Direct Predecessor:
  PGS (Paper 34)               → Proved property-based verification works for code
                                   BUT trusts properties blindly

Our Contribution:
  VERTEX                        → "Who verifies the verifier?"
                                → First measurement of property hallucination rates
                                → Brute-force reference validates properties
                                → Hypothesis fuzzing vs LLM inputs comparison
                                → Error-type-aware repair routing
                                → Calibrated abstention
```

The thesis is no longer "here's another verification framework." It's:

**"Here's a fundamental gap in ALL verification frameworks. Here's the first measurement of the problem. And here's a system that fixes it."**

That's a defensible thesis.
