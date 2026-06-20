# The FLARE System
**(Fault Localization via Anticipatory Reasoning & Execution)**

## A Practical, Buildable Thesis System

No 5-layer architectures. No quantum-inspired metaphors. No model weight access. Just **Python + LLM API calls + a test runner.**

FLARE is built on one dead-simple observation from the 17 research papers:

> Paper 12 showed that just adding print statements improved medium LeetCode problems by 17.9%. Paper 10 showed that reasoning trace errors happen BEFORE code is written. Paper 8 showed that after 2-3 failed fix attempts, the LLM loses 60-80% effectiveness.

**What if we combined all three insights into the simplest possible pipeline?**

---

## The Core Idea: "Trace Before You Run"

Before executing ANY generated code, ask the LLM one extra question:

> *"Trace through your code with this input. What will the output be?"*

That's it. That single question is the entire thesis contribution. Here's why it's powerful:

- If the LLM predicts the **wrong output** → it doesn't even understand the algorithm. Don't run the code. Don't debug. Fix the thinking first.
- If the LLM predicts the **right output** but the code produces the wrong one → it understood the algorithm but made a coding mistake. Show it where the code diverged from its own prediction.
- If the LLM predicts the **right output** and the code matches → the code is correct. Done.

---

## The FLARE Pipeline (6 Steps)

```
┌─────────────────────────────────────────────────────┐
│  Step 1: GENERATE                                   │
│  Input: Problem description + test cases            │
│  Output: Generated code                             │
│                                                     │
│  Step 2: SELF-TRACE (the novel part)                │
│  Prompt: "Trace this code with input X step by      │
│  step. What is the output?"                         │
│  Output: Predicted output + variable trace          │
│                                                     │
│  Step 3: PRE-FLIGHT CHECK                           │
│  Compare: Predicted output vs Expected output       │
│  If MISMATCH → go to Step 4a (Cognitive Repair)     │
│  If MATCH → go to Step 4b (Execute)                 │
│                                                     │
│  Step 4a: COGNITIVE REPAIR                          │
│  Prompt: "You predicted Y but the answer should     │
│  be Z. Your algorithm is wrong. Rethink it."        │
│  → Back to Step 1 (fresh generation)                │
│                                                     │
│  Step 4b: EXECUTE                                   │
│  Run the code against test cases                    │
│  If PASS → Step 6 (Done)                            │
│  If FAIL → Step 5 (Translation Repair)              │
│                                                     │
│  Step 5: TRANSLATION REPAIR                         │
│  Prompt: "You predicted the output would be Z       │
│  (correct), but your code produced Y. Your logic    │
│  is right but your code has a bug. Here is the      │
│  actual execution trace. Fix only the bug."         │
│  → Back to Step 4b (max 2 attempts, then restart)   │
│                                                     │
│  Step 6: DONE ✓                                     │
└─────────────────────────────────────────────────────┘
```

---

## What You Actually Build (The Codebase)

```
flare/
├── main.py              # Entry point — runs FLARE on a dataset
├── generator.py         # Step 1: Sends problem to LLM, gets code back
├── self_tracer.py       # Step 2: Asks LLM to trace its own code
├── preflight.py         # Step 3: Compares predicted vs expected output
├── repairer.py          # Steps 4a/5: Sends targeted repair prompts
├── executor.py          # Step 4b: Sandboxed code execution
├── decay_monitor.py     # Tracks attempts, forces restart after 2 failures
├── benchmarks/
│   ├── humaneval.py     # HumanEval dataset loader
│   ├── leetcode.py      # LeetCode dataset loader (easy/medium/hard)
│   └── mbpp.py          # MBPP dataset loader
└── results/
    └── metrics.py       # Pass@1, hallucination rate, abstention rate
```

**Total implementation: ~500-800 lines of Python.** That's it.

---

## The Experiment You Run For Your Thesis

### Setup
- Models: GPT-4, Claude, Gemini (or whichever you have API access to)
- Benchmarks: HumanEval (164 problems), LeetCode (Easy/Medium/Hard split)
- Baseline: Standard single-pass generation (no FLARE)
- Treatment: FLARE pipeline

### What You Measure

| Metric | What It Tells You |
|:---|:---|
| **Pass@1 improvement** | Does FLARE help LLMs solve more problems? |
| **Pre-flight catch rate** | How often does Step 3 catch a wrong algorithm BEFORE execution? |
| **Cognitive vs Translation error ratio** | What percentage of failures are "didn't understand" vs "understood but miscoded"? |
| **Repair success rate** | When FLARE identifies the error type, how often does the targeted repair work? |
| **Decay avoidance rate** | How often does FLARE's 2-attempt restart prevent ghost debugging? |

### Expected Results (Based on Paper 12's Data)

Paper 12 showed print debugging improved medium problems by 17.9%. FLARE goes further because it catches errors BEFORE execution (something print debugging cannot do). Conservative estimate:

| Difficulty | Baseline Pass@1 | FLARE Pass@1 | Improvement |
|:---|:---|:---|:---|
| Easy | ~85% | ~92% | +7% |
| Medium | ~55% | ~72% | +17% |
| Hard | ~25% | ~40% | +15% |

---

## Why This Is Novel (What You Write in "Related Work")

| Existing Approach | What It Does | What FLARE Does Differently |
|:---|:---|:---|
| Print Debugging (Paper 12) | Adds prints AFTER failure | FLARE catches errors BEFORE execution via self-tracing |
| LDB (Paper 13) | Traces blocks after failure | FLARE forces the LLM to predict the trace BEFORE running code |
| DDI (Paper 8) | Detects decay reactively | FLARE prevents decay by classifying error type and using targeted repair |
| Functional Clustering (Paper 15) | Generates N solutions | FLARE uses 1 solution + 1 self-trace (much cheaper) |
| ChatDBG (Paper 9) | Gives LLM debugger access | FLARE needs zero external tools — just prompt engineering |

**The key novelty:** No existing paper forces the LLM to commit to a predicted execution trace before the code is run, and no existing paper uses the mismatch between the predicted and actual traces to classify the error type (cognitive vs translation) and choose a repair strategy.

---

## Why This Is Practical

1. **Zero infrastructure** — No Docker, no debugger integration, no AST parsing libraries. Just `subprocess.run()` and API calls.
2. **Zero model training** — Works with any off-the-shelf LLM via API.
3. **Fast experiments** — Each problem takes ~3 API calls (generate + trace + repair if needed). You can evaluate 164 HumanEval problems in a few hours.
4. **Clear thesis structure:**
   - Chapter 1: Introduction (the hallucination problem)
   - Chapter 2: Related Work (your 17 papers)
   - Chapter 3: FLARE Architecture (this document)
   - Chapter 4: Experimental Setup (benchmarks, models, metrics)
   - Chapter 5: Results & Analysis
   - Chapter 6: Discussion & Future Work
5. **Publishable** — The cognitive vs translation error classification alone is a publishable finding, even if the overall improvement is modest.

---

## The One-Sentence Thesis Statement

> "We propose FLARE, a lightweight pre-execution self-tracing framework that reduces LLM code hallucination by forcing models to predict their own execution traces before running code, enabling automatic classification of failures as cognitive errors (algorithm misunderstanding) or translation errors (coding mistakes), and applying targeted repair strategies that avoid debugging decay."
