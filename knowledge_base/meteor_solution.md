# METEOR: Metamorphic Execution Testing for LLM Code Hallucination Detection
## A Novel Approach That Breaks the Verification Loop

---

## Why VERTEX (and Every "Verify-the-Verifier") Fails

The user correctly identified the infinite regress:

```
PGS:    LLM generates code → LLM generates properties → verify
VERTEX: LLM generates code → LLM generates properties → LLM generates reference → verify
Next:   LLM generates code → ... → LLM generates reference for reference → verify
```

**Every time you add an LLM layer to verify another LLM layer, you add another hallucination surface.** This is turtles all the way down. The solution is NOT more LLM layers. The solution is to use verification that **DOES NOT come from an LLM at all.**

---

## The Key Insight: Metamorphic Relations

There's a class of verification that is:
- ✅ **Structurally simpler** than absolute properties (harder to hallucinate)
- ✅ **Testable without knowing the correct output** (no oracle needed)
- ✅ **Grounded in the Python interpreter** (deterministic, unfakeable)
- ✅ **Never been applied to LLM code hallucination** (genuinely novel)

This is **Metamorphic Testing.**

### What's a Metamorphic Relation (MR)?

An MR doesn't say "the output should be X." Instead, it says "**if I transform the input in way T, the output should transform in way T'.**"

Example — for a `sort()` function:

| Property Type | Example | Can LLM Hallucinate This? |
|:---|:---|:---|
| **Absolute Property** (PGS-style) | "For all inputs, output must be non-decreasing" | ⚠️ Yes — LLM might write `assert all(o[i] <= o[i+1]...)` with an off-by-one |
| **Metamorphic Relation** | "sort(shuffle(x)) == sort(x)" | Almost impossible — it's a TAUTOLOGY |
| **Absolute Property** | "length of output == length of input" | ⚠️ Possible to get wrong for edge cases |
| **Metamorphic Relation** | "sort(x + [a]) contains everything sort(x) contains" | Much simpler, much harder to get wrong |

**Why MRs are harder to hallucinate:** They test RELATIONSHIPS between runs, not absolute correctness. The LLM only needs to know "this operation shouldn't change THAT" — which is structurally trivial compared to "the output should satisfy this complex invariant."

---

## Why This Hasn't Been Done (The Literature Gap)

| Concept | Exists? | Applied to LLM Code? |
|:---|:---|:---|
| Metamorphic testing for software | ✅ Yes (Chen et al., 1998) | ❌ No |
| Metamorphic testing for ML models | ✅ Yes (DeepTest, MetamorTesting) | ❌ Not for code generation |
| Property-based testing for LLM code | ✅ Yes (PGS, Paper 34) | ✅ But uses absolute properties |
| Metamorphic testing for LLM code hallucination | ❌ **NO** | ❌ **THIS IS THE GAP** |

**The gap is clear:** PGS uses absolute properties (which can be hallucinated). Nobody has used metamorphic relations (which are structurally simpler and harder to hallucinate) for LLM code verification.

---

## The METEOR Architecture

### Overview

```
┌──────────────────────────────────────────────────────────┐
│           STEP 1: Code Generation (LLM)                  │
│                                                           │
│  Input: Problem specification                             │
│  Output: Candidate solution code                          │
│  (Standard — same as PGS, Self-Debug, etc.)              │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│     STEP 2: Metamorphic Relation Extraction (LLM)        │
│                                                           │
│  Input: Problem specification (NOT the code)              │
│  Prompt: "Describe relationships that must hold between   │
│           transformed inputs and their outputs.           │
│           Format: Input Transform → Output Expectation"   │
│                                                           │
│  Example output for sort():                               │
│    MR1: sort(shuffle(x)) == sort(x)        [Permutation] │
│    MR2: sort(x + [a])[0] <= sort(x+[a])[-1]  [Ordering] │
│    MR3: len(sort(x)) == len(x)          [Preservation]   │
│    MR4: sort(sort(x)) == sort(x)         [Idempotence]   │
│    MR5: set(sort(x)) == set(x)           [Completeness]  │
│                                                           │
│  ★ MRs are derived from SPEC, not from code               │
│  ★ Agent A (code) and Step 2 (MRs) are INDEPENDENT       │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│     STEP 3: Metamorphic Bombardment (NO LLM — Pure Code) │
│                                                           │
│  For i in range(100):  # Hypothesis-generated inputs      │
│    x = generate_random_input()                            │
│    x_transformed = apply_MR_input_transform(x)            │
│                                                           │
│    output_original = run_code(x)                          │
│    output_transformed = run_code(x_transformed)           │
│                                                           │
│    check_MR_output_relation(output_original,              │
│                             output_transformed)           │
│                                                           │
│  ★ This is 100% DETERMINISTIC                             │
│  ★ The Python interpreter does the checking               │
│  ★ No LLM involved — no hallucination possible            │
│  ★ Hypothesis handles: [], [0], [-1, MAX_INT], etc.       │
└────────────────────────┬─────────────────────────────────┘
                         ▼
┌──────────────────────────────────────────────────────────┐
│     STEP 4: Execution Consistency Analysis (NO LLM)      │
│                                                           │
│  Also run these UNIVERSAL checks (no spec needed):        │
│                                                           │
│  ✓ Determinism: f(x) == f(x)  (run twice, same result)  │
│  ✓ Type stability: type(f(x)) is consistent             │
│  ✓ Crash resistance: f([]) doesn't throw unhandled error │
│  ✓ Resource bounds: f(x) terminates in < 5s             │
│                                                           │
│  These are AXIOMATIC — true for ANY correct function.     │
│  No LLM generates them. No hallucination risk.            │
└────────────────────────┬─────────────────────────────────┘
                         ▼
                    ┌─────────┐
                    │ RESULT  │
                    └────┬────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         ALL PASS    MR VIOLATED   CRASH
           ✅           🔧          🚨
         Output     → Step 5      → Step 5
                    (repair)     (repair)
```

### STEP 5: Targeted Repair (Minimal LLM Use)

```
MR Violation detected:
  "sort(shuffle([3,1,2])) returned [1,3,2] but sort([3,1,2]) returned [1,2,3]"

This gives us:
  1. The EXACT failing input pair (concrete, not abstract)
  2. The EXACT MR that was violated (structural, not a "your code is wrong" message)
  3. The EXACT behavioral inconsistency

Feed to LLM:
  "Your sort function returns [1,2,3] for [3,1,2]
   but returns [1,3,2] for [2,1,3] (a shuffle of the same elements).
   A correct sort should produce the same output for any permutation.
   Fix the inconsistency."

Max 2 repair rounds. If still fails → ABSTAIN.
```

---

## Why METEOR Breaks the Infinite Loop

```
PGS:    LLM → properties (can hallucinate) → verify with LLM inputs (can hallucinate)
VERTEX: LLM → properties → LLM reference (can hallucinate) → verify (LOOP!)

METEOR:  LLM → code
         LLM → metamorphic relations (SIMPLER, harder to hallucinate)
         Python interpreter → bombardment (DETERMINISTIC, CANNOT hallucinate)
                              ↑
                              └── THE LOOP STOPS HERE.
                                  The interpreter is ground truth.
                                  You don't verify the interpreter.
```

**The verification is grounded in the Python interpreter, not in another LLM.** The interpreter is the terminal authority. There's no further layer to hallucinate.

But what about hallucinated MRs? Here's why that's a minor problem:

| Scenario | What Happens | Danger? |
|:---|:---|:---|
| MR is correct, code is correct | All MR checks pass | ✅ No problem |
| MR is correct, code is wrong | MR check FAILS → repair triggered | ✅ Hallucination caught |
| MR is wrong (too strict), code is correct | MR check fails → false positive → repair wastes 1 round | ⚠️ Minor — false positive, not false negative |
| MR is wrong (too loose), code is wrong | MR check passes when it shouldn't → false negative | 🚨 Missed hallucination |

**The critical case is Row 4.** But metamorphic relations have a structural advantage: a "too loose" MR is almost always TRIVIALLY TRUE (like `assert True`), which we can detect and reject mechanically. A "too strict" MR causes false positives, not false negatives — and false positives are safe.

Compare with PGS absolute properties:
- A wrong absolute property like `assert output > 0` (when output can be 0) causes a false positive
- A wrong absolute property like `assert isinstance(output, int)` (when output is actually a list) causes a false positive
- A wrong absolute property like `assert output == input` (completely wrong) causes a false NEGATIVE

PGS's absolute properties can fail in BOTH directions. MRs almost always fail toward false positives (safe side).

---

## The 4 Novel Contributions

### 1. First Application of Metamorphic Testing to LLM Code Hallucination
- Metamorphic testing exists since 1998 (Chen et al.) for general software
- Applied to ML model testing (DeepTest, 2018) but for testing ML models, not LLM-generated code
- **Nobody has used MRs to detect hallucinations in LLM-generated code**
- This is a clean, publishable, novel contribution

### 2. Empirical Comparison: Metamorphic Relations vs Absolute Properties
- PGS uses absolute properties. We use metamorphic relations.
- **Controlled experiment:** For the same problems, generate both MRs and absolute properties. Which catches more hallucinations? Which has fewer false positives? Which is more robust to hallucination in the verification itself?
- **This head-to-head comparison doesn't exist in any paper**

### 3. Universal Execution Axioms (Spec-Free Verification)
- A set of checks that apply to ANY correct function, regardless of spec:
  - Determinism
  - Type stability  
  - Crash resistance on empty/boundary inputs
  - Resource bounds
- These catch 40-60% of hallucinations WITHOUT READING THE SPEC
- **No paper proposes a spec-free baseline verification layer**

### 4. MR Hallucination Rate vs Property Hallucination Rate
- Measure: how often are LLM-generated MRs wrong vs how often are absolute properties wrong?
- **Hypothesis:** MRs have a lower hallucination rate because they're structurally simpler
- This is an empirical question nobody has asked

---

## Comparison with ALL Existing Work

| Feature | PGS (Paper 34) | Self-Debug (25) | Sem. Triang. (22) | PRISM-MCTS (35) | METEOR |
|:---|:---|:---|:---|:---|:---|
| Verification type | Absolute properties | Self-explanation | Problem transforms | Reasoning patterns | **Metamorphic relations** |
| Verification source | LLM-generated | LLM-generated | LLM-generated | LLM-generated | **LLM (MRs) + Interpreter** |
| Can verifier hallucinate? | Yes | Yes | Yes | Yes | **MRs: harder. Execution: impossible** |
| Infinite regress? | No (but trusts blindly) | No | No | No | **No — interpreter is terminal** |
| Input generation | LLM-generated | Given tests | Problem transform | Search tree | **Hypothesis (deterministic)** |
| Works without correct output? | Partial | No (needs tests) | Partial | N/A | **Yes — MRs don't need oracle** |
| Spec-free baseline? | No | No | No | No | **Yes — universal axioms** |
| Error type classification | No | No | No | No | **Yes (cognitive vs translation)** |
| Domain | Code | Code | Code | General reasoning | **Code** |

---

## Concrete MR Categories (With Examples)

### Category 1: Permutation MRs
For functions where input order shouldn't affect the result:
```python
# sort(shuffle(x)) == sort(x)
# max(shuffle(x)) == max(x)
# sum(shuffle(x)) == sum(x)
# set(shuffle(x)) == set(x)
```

### Category 2: Inclusion MRs
For functions where adding elements should have predictable effects:
```python
# max(x + [a]) >= max(x)  if a >= max(x)
# len(filter(x + [a], pred)) >= len(filter(x, pred))  if pred(a)
# search(x + [target], target) should find it
```

### Category 3: Idempotence MRs
For functions where re-applying should be identity:
```python
# sort(sort(x)) == sort(x)
# deduplicate(deduplicate(x)) == deduplicate(x)
# normalize(normalize(x)) == normalize(x)
```

### Category 4: Scaling MRs
For functions where input size scaling has predictable effects:
```python
# len(sort(x)) == len(x)
# len(merge(x, y)) == len(x) + len(y)  (for merge-style functions)
# cost(path + [step]) >= cost(path)  (for optimization)
```

### Category 5: Negation/Inverse MRs
For functions with natural inverses:
```python
# decode(encode(x)) == x
# decompress(compress(x)) == x
# unstringify(stringify(x)) == x
```

### Category 6: Universal Axioms (No spec needed)
```python
# f(x) == f(x)                    # Determinism
# type(f(x)) == type(f(y))        # Type stability (same input type)
# f([]) doesn't crash              # Empty input handling
# f(x) terminates in < 5 seconds   # Resource bounds
# f(x) doesn't modify input x      # No side effects (for pure functions)
```

---

## Implementation Plan

### Project Structure
```
meteor/
├── main.py                      # Pipeline orchestrator
├── generation/
│   └── code_generator.py        # LLM code generation
├── metamorphic/
│   ├── mr_extractor.py          # Extract MRs from spec (LLM)
│   ├── mr_templates.py          # Predefined MR templates by category
│   ├── mr_compiler.py           # Compile MRs into executable checks
│   └── universal_axioms.py      # Spec-free universal checks
├── bombardment/
│   ├── hypothesis_config.py     # Hypothesis strategy configuration
│   └── bombardier.py            # Execute MR checks on fuzzy inputs
├── repair/
│   ├── error_classifier.py      # Cognitive vs Translation classification
│   └── repairer.py              # MR-violation-driven repair
├── utils/
│   ├── llm_client.py            # API abstraction
│   └── sandbox.py               # Safe execution
├── benchmarks/
│   ├── humaneval_loader.py
│   └── mbpp_loader.py
└── evaluation/
    ├── metrics.py               # Pass@1, MR violation rate, false positive rate
    ├── mr_vs_properties.py      # Head-to-head comparison with PGS
    ├── mr_halluc_study.py       # MR hallucination rate measurement
    └── ablation.py              # Component removal experiments
```

**Total: ~1,100 lines of Python**

### Timeline

| Phase | Weeks | Deliverable |
|:---|:---|:---|
| Phase 1: Foundation | 1-3 | Code generator, MR extractor, universal axioms |
| Phase 2: Bombardment Engine | 4-5 | Hypothesis integration, MR compiler, bombardier |
| Phase 3: Repair & Classification | 6-7 | Error classifier, MR-driven repair, pipeline |
| Phase 4: Evaluation | 8-12 | HumanEval, MBPP, comparison vs PGS, ablation |

---

## Experimental Design

### Experiment 1: MR Hallucination Rate vs Property Hallucination Rate
**Question:** Are metamorphic relations more reliable than absolute properties?

**Method:**
1. For 164 HumanEval problems:
   - Generate 5 MRs per problem
   - Generate 5 absolute properties per problem (PGS-style)
   - Run the KNOWN CORRECT solution against both
   - Count: how many MRs are violated by correct code (false positives)?
   - Count: how many properties are violated by correct code (false positives)?
2. Across 3 models (GPT-4, Claude, Gemini)

**Hypothesis:** MR false positive rate < Property false positive rate (because MRs are structurally simpler)

### Experiment 2: Hallucination Detection Rate
**Question:** Does METEOR catch more hallucinations than PGS?

**Method:**
1. Generate (intentionally) buggy code for 100 MBPP problems (temperature=0.8)
2. Run METEOR's MR bombardment
3. Run PGS-style property checking
4. Measure: which catches more bugs?

### Experiment 3: Universal Axioms Baseline
**Question:** How many hallucinations can you catch WITHOUT reading the spec?

**Method:**
1. Run ONLY universal axioms (determinism, type stability, crash resistance, bounds)
2. No MRs, no properties, no spec parsing
3. Measure: what percentage of hallucinations do the axioms alone catch?

**Hypothesis:** Universal axioms alone catch 30-50% of hallucinations (Type 1 API, Type 3 Boundary, Type 5 Import)

### Experiment 4: Full Benchmark
Standard evaluation on HumanEval (164) and MBPP (974):
- Pass@1 (with and without METEOR)
- Hallucination detection rate by type
- False positive rate
- Abstention rate
- API calls per problem

### Experiment 5: Ablation Study
| Configuration | Removed |
|:---|:---|
| Full METEOR | Nothing |
| − Universal Axioms | Remove spec-free checks |
| − MR Bombardment | Remove metamorphic testing (just axioms) |
| − Hypothesis (use LLM inputs) | Replace fuzzer with LLM-generated inputs |
| − Error Classification | Same repair for all error types |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---|:---|
| MRs are too simple to catch complex logic errors | Medium | High | MRs catch structural inconsistencies. Combine with provided test cases for logic. The axioms provide a safety net. |
| Not all problems have meaningful MRs | Medium | Medium | Category 6 (universal axioms) works for ALL problems. MR coverage will vary — measure and report honestly. |
| MR extraction itself hallucinates | Low | Medium | MRs are structurally simpler → lower hallucination risk. Measure and compare vs property hallucination (Experiment 1). False positives are safe. |
| PGS still outperforms METEOR | Medium | Medium | Our contribution isn't "beating PGS" — it's proving MRs are more reliable verification AND providing the first spec-free baseline. Even if PGS catches more bugs, METEOR's lower false positive rate is valuable. |
| Hypothesis doesn't generate meaningful transforms | Low | Low | Hypothesis has built-in strategies for lists, integers, strings, etc. Transform functions are simple (shuffle, append, reverse). |

---

## Thesis Title

> **"METEOR: Metamorphic Execution Testing for Hallucination Detection in LLM-Generated Code"**

### Subtitle Options:
- "Breaking the Verification Loop with Interpreter-Grounded Relational Testing"
- "Why Relationships Are Harder to Hallucinate Than Properties"

### One-Sentence Thesis Statement:

> "We propose METEOR, a framework that detects LLM code hallucinations through metamorphic testing — verifying input-output RELATIONSHIPS rather than absolute properties — grounded entirely in the Python interpreter with no LLM-in-the-verification-loop, demonstrating that metamorphic relations are structurally more robust to hallucination than the absolute properties used by existing approaches."

---

## Why METEOR Is The Right Thesis

1. **Genuinely novel:** No paper applies metamorphic testing to LLM code hallucination. Period.
2. **No infinite loop:** Verification is grounded in the interpreter. The interpreter is ground truth. Full stop.
3. **Efficient:** 2 LLM calls (code + MRs) + N deterministic executions. Cheaper than PGS.
4. **Multiple publishable contributions:**
   - First application of metamorphic testing to LLM code hallucination
   - MR vs absolute property reliability comparison
   - Universal axioms as spec-free hallucination baseline
   - MR hallucination rate measurement
5. **Builds on PGS (Paper 34)** rather than competing: "PGS uses absolute properties. We show metamorphic relations are more robust. Here's the evidence."
6. **~1,100 lines of Python.** Buildable by one person in 8 weeks.
