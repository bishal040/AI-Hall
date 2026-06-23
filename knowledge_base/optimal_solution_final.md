# 🎯 OPTIMAL THESIS SOLUTION
## Constrained Property-Based Verification (CPV) — Evidence-Grounded Final Architecture

> **Every design decision below is traced back to a specific published paper. Nothing is hand-waved.**

---

## 1. Problem Statement

Large Language Models generate code that compiles, runs, and *looks correct* but contains **semantic hallucinations** — logical errors, boundary failures, and requirement violations that are invisible to surface-level analysis.

### Evidence for the Problem
| Claim | Source |
|:---|:---|
| Requirement Conflicting is the #1 hallucination type across ALL LLMs | Paper 18 (Liu et al., 2026) |
| 94% of compilation errors are type errors, not syntax errors | Paper 24 (Mündler et al., 2025) |
| LLMs make correlated errors — plurality voting amplifies mistakes | Paper 22 (Dai et al., 2026) |
| Self-repair gains are modest when compute cost is accounted for | Paper 26 (Olausson et al., ICLR 2024) |
| Up to 30% of LLM-generated summaries contain factual inconsistencies | Paper 30 (Lin et al., 2026) |
| Code hallucinations span 5 categories: dead code, syntax, logic, robustness, security | Paper 19 (Agarwal et al., 2025) |

---

## 2. Why Existing Solutions Are Insufficient

### 2.1 Self-Repair / Self-Debugging
**What it does:** LLM generates code → executes → explains errors → repairs.
**Why it's insufficient:**
- **"Self-repair is bottlenecked by the model's ability to provide feedback on its own code"** — Paper 26
- Human feedback improves repair success by **+58%** (33.3% → 52.6%) — Paper 26
- Without external signal, the LLM generates **correlated errors** in both code and tests — Paper 22

### 2.2 Plurality Voting / Sampling
**What it does:** Generate N solutions, pick the most common one.
**Why it's insufficient:**
- LLMs produce **correlated errors** — the dominant error has higher probability than the correct solution (0.23 vs 0.07 in Paper 22's example)
- Voting **amplifies** shared mistakes rather than catching them — Paper 22

### 2.3 RAG / Prompt Enhancement
**What it does:** Retrieve relevant code examples, enhance prompts.
**Why it's insufficient:**
- Reduces but does not eliminate hallucination — Paper 18
- Effective for Knowledge Conflicting hallucinations, NOT for Logic hallucinations — Paper 18
- Cannot verify correctness — only influences generation probability

### 2.4 Type-Constrained Decoding
**What it does:** Rejects type-violating tokens during generation.
**Why it's insufficient:**
- Prevents **compilation** errors (reduces by 50%) — Paper 24
- Does NOT catch **logic errors** — a well-typed program can still be semantically wrong
- Only 3.5-5.5% improvement in functional correctness — Paper 24

### 2.5 Semantic Triangulation
**What it does:** Transforms problem into dissociative variant, checks cross-solution consistency.
**Why it's insufficient:**
- Requires the problem to have a meaningful "inverse" or decomposition — Paper 22
- Not all problems are invertible or decomposable
- Catches correlated errors but doesn't verify **structural invariants**

---

## 3. The CPV Solution

### 3.1 Core Thesis Statement

> **Constrained Property-Based Verification (CPV) mitigates code hallucination by replacing self-generated tests with specification-derived structural invariants, using property-based fuzzing to produce high-quality counterexample feedback that enables targeted error attribution and repair.**

### 3.2 Architecture: 6-Layer Verification Funnel

```
  NATURAL LANGUAGE SPECIFICATION
            │
            ▼
  ┌──────────────────────────┐
  │  LAYER 0: SPEC REFINEMENT│  ← Paper 18: reduces #1 hallucination type
  │  • Ambiguity detection   │
  │  • CoT expansion         │
  │  • Paraphrase check      │  ← Paper 30: consistency detection
  └──────────┬───────────────┘
             ▼
  ┌──────────────────────────┐
  │  LAYER 1: DUAL-AGENT     │  ← Paper 26: separate feedback model > self
  │  GENERATION              │
  │  • Agent A: Code Gen     │
  │  • Agent B: Invariant    │     Agent B never sees Agent A's code
  │    Extraction (from spec)│     → decorrelates errors (Paper 22)
  └──────────┬───────────────┘
             ▼
  ┌──────────────────────────┐
  │  LAYER 2: STATIC         │
  │  ANALYSIS (DETERMINISTIC)│
  │  • AST parsing           │  ← Paper 14, 16: deterministic validation
  │  • Import resolution     │
  │  • Type checking         │  ← Paper 24: 94% of comp errors are type errors
  │  • Syntax validation     │
  └──────────┬───────────────┘
             ▼
  ┌──────────────────────────┐
  │  LAYER 3: SANDBOXED      │
  │  EXECUTION               │
  │  • Run code in container │  ← Paper 25: execution feedback is essential
  │  • Catch RuntimeError,   │
  │    ImportError, etc.     │
  │  • Collect stdout/stderr │
  └──────────┬───────────────┘
             ▼
  ┌──────────────────────────┐
  │  LAYER 4: PROPERTY-BASED │  ← OUR KEY CONTRIBUTION
  │  FUZZING                 │
  │  • Hypothesis generates  │
  │    100s of random inputs │
  │  • Check invariants from │
  │    Layer 1 on EVERY input│
  │  • Concrete counter-     │     Paper 26: "feedback quality is the bottleneck"
  │    examples as feedback  │     → counterexamples ARE high-quality feedback
  └──────────┬───────────────┘
             ▼
  ┌──────────────────────────┐
  │  LAYER 5: ERROR-ATTRIBUTED│
  │  REPAIR (MAX 2 ROUNDS)   │  ← Paper 26: diminishing returns after 2-3 rounds
  │  • Classify error type   │  ← Paper 8: Debugging Decay Index
  │  • Select STRUCTURALLY   │  ← Paper 34 (PGS): min token count counterexample
  │    MINIMAL counterexample│
  │  • If fail → ABSTAIN     │  ← Paper 22: abstention > wrong answer
  └──────────────────────────┘
```

### 3.3 Key Design Decisions (Evidence-Grounded)

#### Decision 1: Separate Agent A (Code) and Agent B (Invariants)
**Why:** Paper 26 proves that using a *different* model for feedback dramatically improves repair success. By having Agent B extract invariants from the spec (not from the code), we get **decorrelated** verification — Agent B can't hallucinate the same errors as Agent A because it never sees Agent A's output.

**Evidence:** Paper 22 shows that LLMs make correlated errors, so asking the same model to verify its own code is like "interrogating suspects who have already colluded on the same fake alibi."

#### Decision 2: Invariants from SPEC, Not from Code
**Why:** Paper 18 identifies Requirement Conflicting as the #1 hallucination type. If we extract invariants from the code itself (as test generation does), we inherit the code's hallucinations. Extracting from the spec grounds our verification in the original requirements.

**Evidence:** Paper 22's auto-formalized Hoare-style specifications fail precisely because they're derived from the same model that generated the code.

#### Decision 3: Property-Based Fuzzing (Hypothesis) Instead of Fixed Tests
**Why:** Fixed unit tests cover a finite number of cases. Property-based testing via Hypothesis generates 100s of random inputs across the type space, catching boundary/edge-case hallucinations that fixed tests miss.

**Evidence:** Paper 19 identifies "Robustness issues" (fails on edge cases) as a distinct hallucination category. Hypothesis directly addresses this by fuzzing boundaries.

#### Decision 4: Maximum 2 Repair Rounds
**Why:** Paper 26 shows that repair has diminishing returns — "drawing 10 samples up front and then 1 repair candidate each leads to a pass rate 1.05× higher... drawing 2 samples up front and then 10 repair candidates each leads to a pass rate which is lower than the baseline."

**Evidence:** Paper 8's Debugging Decay Index shows 60-80% capability loss after 2-3 debugging attempts.

#### Decision 5: Abstain on Persistent Failure
**Why:** Paper 22 shows that in "selection-or-abstention" scenarios, the ability to abstain (say "I don't know") achieves +26% higher F1 than forcing an answer. Outputting a wrong solution with high confidence is worse than refusing.

**Evidence:** Paper 4 identifies the inability to say "I don't know" as a fundamental hallucination driver.

#### Decision 6: Concrete Counterexamples as Feedback
**Why:** Paper 26 proves that feedback quality is THE bottleneck of self-repair. Natural language explanations are vague and potentially wrong. A concrete counterexample (e.g., "sort([3, 1, 2]) returned [1, 3, 2]") is:
- **Unambiguous** — no room for misinterpretation
- **Verifiable** — the model can re-execute to confirm
- **Attributable** — points to exactly which property was violated

---

## 4. What Makes CPV Novel (Differentiation Matrix)

| Dimension | Self-Debug (Paper 25) | Semantic Tri. (Paper 22) | Type-Constrained (Paper 24) | **CPV (Ours)** |
|:---|:---|:---|:---|:---|
| Verification source | Self-explanation | Problem transformation | Type system | **Spec-derived invariants** |
| Error signal | Natural language | Consistency check | Type error | **Concrete counterexample** |
| Feedback decorrelation | None (same model) | Dissociative transform | N/A (during generation) | **Separate agent + separate task** |
| Problem scope | All problems | Only invertible/decomposable | Only typed languages | **All problems with definable invariants** |
| Catches logic errors | Only if unit tests available | Yes (via consistency) | No | **Yes (via property fuzzing)** |
| Catches boundary errors | Only if tests cover edges | Partial | No | **Yes (Hypothesis fuzzes boundaries)** |
| Catches type errors | Via execution | Indirectly | Yes (during gen) | **Yes (via static analysis layer)** |
| Repair guidance | Vague NL feedback | None (detection only) | None (prevention only) | **Concrete counterexample + error type** |

---

## 5. Invariant Categories (What Agent B Extracts)

Based on the hallucination taxonomy from Papers 18 and 19:

### Category 1: Type Invariants
```python
# "Given a list of integers, return the sum"
@given(st.lists(st.integers()))
def test_returns_integer(xs):
    result = solution(xs)
    assert isinstance(result, int)
```

### Category 2: Structural Invariants
```python
# "Sort a list"
@given(st.lists(st.integers()))
def test_same_length(xs):
    result = solution(xs)
    assert len(result) == len(xs)

@given(st.lists(st.integers()))
def test_same_elements(xs):
    result = solution(xs)
    assert sorted(result) == sorted(xs)  # permutation check
```

### Category 3: Boundary Invariants
```python
# "Find maximum in a list"
@given(st.lists(st.integers(), min_size=1))
def test_max_in_list(xs):
    result = solution(xs)
    assert result in xs
    assert all(x <= result for x in xs)
```

### Category 4: Relationship Invariants
```python
# "Reverse a string"
@given(st.text())
def test_double_reverse(s):
    assert solution(solution(s)) == s  # involution property
```

### Category 5: Algebraic Invariants
```python
# "Matrix multiply"
@given(matrix_strategy, identity_strategy)
def test_identity(A, I):
    assert solution(A, I) == A  # identity element
```

---

## 6. Evaluation Plan

### 6.1 Benchmarks
| Benchmark | Size | What It Tests | Source |
|:---|:---|:---|:---|
| HumanEval | 164 problems | Functional correctness | OpenAI |
| MBPP | 974 problems | Basic Python programming | Google |
| CodeMirage | 1,137 hallucinated snippets | Hallucination detection | Paper 19 |
| LiveCodeBench | Continuously updated | Competition-level problems | Paper 22 |
| APPS | 10,000 problems | Intro → Competition difficulty | Hendrycks et al. |

### 6.2 Metrics
| Metric | What It Measures | Baseline |
|:---|:---|:---|
| Pass@1 | First-attempt correctness | Self-Debugging (Paper 25) |
| Hallucination Detection Rate | % of hallucinations caught by Layer 4 | CodeMirage detection (Paper 19) |
| Repair Success Rate | % of detected hallucinations successfully repaired | Self-Repair (Paper 26) |
| Abstention Accuracy | Quality of "I don't know" decisions | Semantic Triangulation (Paper 22) |
| Property Coverage | % of spec properties captured by Agent B | Manual annotation |
| Compute Efficiency | Total LLM calls per problem | Paper 26's repair tree analysis |

### 6.3 Baselines
1. **Vanilla generation** — Direct LLM code generation
2. **Self-Debugging** (Paper 25) — LLM self-debug with rubber duck explanation
3. **Self-Repair** (Paper 26) — With natural language feedback
4. **Semantic Triangulation** (Paper 22) — Cross-problem consistency
5. **Type-Constrained Decoding** (Paper 24) — If model access available
6. **pass@k sampling** — Generate k solutions, pick best

### 6.4 Expected Results
Based on Paper 26's findings (human feedback improves repair by +58%):
- **Property violations** provide feedback quality between "LLM self-feedback" and "human expert feedback"
- Expected improvement: **+25-40% repair success rate** over self-repair baseline
- Expected improvement: **+15-25% pass@1** over vanilla generation

---

## 7. Implementation Roadmap

### Phase 1: Prototype (Month 1-2)
- [ ] Implement Agent B invariant extraction for HumanEval-Easy (50 problems)
- [ ] Implement Hypothesis-based fuzzing engine
- [ ] Build sandboxed execution environment
- [ ] Basic pipeline: Spec → Agent B → Agent A → Fuzz → Report

### Phase 2: Core System (Month 3-4)
- [ ] Add error attribution module
- [ ] Implement 2-round repair loop with counterexample feedback
- [ ] Evaluate on full HumanEval (164 problems)
- [ ] Compare against Self-Debugging baseline

### Phase 3: Full Evaluation (Month 5-6)
- [ ] Extend to MBPP (974 problems)
- [ ] Evaluate on CodeMirage hallucination detection
- [ ] Ablation study: remove each layer, measure impact
- [ ] Multi-model evaluation (GPT-4, Claude, DeepSeek, Gemini)

### Phase 4: Thesis Write-up (Month 7-8)
- [ ] Write Related Work using Paper 20's survey structure
- [ ] Document all results with statistical significance
- [ ] Generate figures and tables
- [ ] Submit

---

## 8. Citation Map

```
Our CPV Framework
├── Problem Definition
│   ├── Paper 18 (Liu et al.) — Hallucination taxonomy
│   ├── Paper 19 (Agarwal et al.) — CodeMirage benchmark
│   └── Paper 20 (Gao et al.) — Systematic literature review
├── Design Decisions
│   ├── Paper 22 (Dai et al.) — Correlated errors, decorrelation
│   ├── Paper 24 (Mündler et al.) — Type errors dominate
│   ├── Paper 25 (Chen et al.) — Self-debugging foundation
│   ├── Paper 26 (Olausson et al.) — Feedback quality bottleneck
│   └── Paper 30 (Lin et al.) — Consistency checking
├── Mitigation Strategy
│   ├── Paper 18 — Prompt refinement reduces hallucination
│   ├── Paper 26 — Max 2 repair rounds
│   ├── Paper 22 — Abstention > wrong answer
│   ├── Paper 31 (Kollias et al.) — Constraint geometry
│   └── Paper 34 (PGS) — Structurally minimal counterexample feedback
├── Evaluation
│   ├── Paper 19 — CodeMirage dataset
│   ├── Paper 22 — LiveCodeBench benchmark
│   └── Paper 25 — Self-debugging as baseline
└── Missing (Must Acquire)
    ├── LLMLOOP — Multi-loop self-debug
    └── PropertyEval — PBT evaluation toolkit
```

---

## 9. Recommended Thesis Title

> **"Constrained Property-Based Verification: Mitigating Code Hallucination through Specification-Derived Invariants and Error-Attributed Repair"**

### Subtitle Options:
- "A Multi-Layer Framework for Near-Zero Logic Hallucination in LLM-Generated Code"
- "From Self-Repair to Evidence-Based Repair: Using Counterexamples to Fix What LLMs Get Wrong"

---

## 10. Action Items

### Immediate (Before Starting Implementation)
1. ⚠️ **Download the remaining correct papers:** LLMLOOP, PropertyEval, CodeHaluEval
2. Finalize invariant extraction prompts for Agent B
3. Set up Hypothesis fuzzing environment

### Short-term (During Implementation)
5. Build proof-of-concept on 10 HumanEval problems
6. Validate that Agent B invariants are meaningful (not trivial)
7. Measure counterexample quality vs. natural language feedback
8. Compare repair success rates

### Medium-term (During Evaluation)
9. Run full benchmark evaluation
10. Write ablation study
11. Statistical significance testing
12. Multi-model evaluation
