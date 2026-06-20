# Detecting Hallucination in the Self-Trace
## The "Who Watches the Watchman?" Problem — And Its Solution

---

## The Vulnerability You Found

In FLARE, we ask the LLM: *"Trace your code with input X. What's the output?"*

But what if the LLM **doesn't actually trace the code?** What if it just looks at the code, guesses what the output "should" be, and writes a convincing-looking trace that's completely fabricated?

This is a real risk. LLMs are trained to produce plausible text, not to faithfully simulate a CPU. The trace could be a hallucination itself.

---

## The 4 Failure Modes of Self-Tracing

| Mode | What Happens | Is It Dangerous? |
|:---|:---|:---|
| **A: Correct trace, correct code** | LLM traces accurately, code works | ✅ No problem |
| **B: Wrong trace, wrong code (different outputs)** | LLM traces wrong, code produces a different wrong answer | ✅ Caught by FLARE — mismatch between predicted and actual |
| **C: Wrong trace, right code** | LLM traces wrong but code happens to work anyway | ⚠️ Mild risk — code passes, but LLM got lucky. May fail on other inputs |
| **D: Fabricated trace matches wrong code** | LLM doesn't really trace — just guesses "output = 7", code also happens to produce 7, but 7 is wrong | 🚨 **DANGEROUS** — FLARE thinks it's correct because predicted = actual, but both are wrong |

**Mode D is the killer.** The LLM hallucinates both the code AND the trace consistently. They agree with each other, but both are wrong.

---

## The Solution: Don't Trust the Trace — Execute It

The answer is almost embarrassingly simple: **turn the LLM's trace into executable assertions and let Python verify them.**

The LLM's trace contains concrete, checkable claims like:
```
Step 1: i=0, nums[0]=2, complement=7, hashmap={}
Step 2: i=1, nums[1]=7, complement=2, hashmap={2: 0}
Step 3: Found! Return [0, 1]
```

Each of these is a testable statement. We extract them and inject them as `assert` statements directly into the code:

```python
def two_sum(nums, target):
    hashmap = {}
    for i, num in enumerate(nums):
        complement = target - num
        
        # === INJECTED TRACE ASSERTIONS ===
        if i == 0:
            assert num == 2, f"Trace claimed nums[0]=2 but got {num}"
            assert complement == 7, f"Trace claimed complement=7 but got {complement}"
            assert hashmap == {}, f"Trace claimed hashmap empty but got {hashmap}"
        if i == 1:
            assert num == 7, f"Trace claimed nums[1]=7 but got {num}"
            assert complement == 2, f"Trace claimed complement=2 but got {complement}"
            assert hashmap == {2: 0}, f"Trace claimed hashmap={{2:0}} but got {hashmap}"
        # === END ASSERTIONS ===
        
        if complement in hashmap:
            return [hashmap[complement], i]
        hashmap[num] = i
```

Now when we run the code:
- If the assertions **pass** → the trace was genuine, the LLM really did trace the code accurately
- If any assertion **fails** → the trace was fabricated, and the assertion error message tells us EXACTLY which step was hallucinated

**The Python interpreter becomes the lie detector.** The LLM can hallucinate all it wants in text, but `assert x == 5` will crash if x is not 5. You cannot hallucinate past the interpreter.

---

## The Refined FLARE Pipeline (With Trace Verification)

```
Step 1: GENERATE code
Step 2: SELF-TRACE (LLM predicts step-by-step variable values)
Step 3: PRE-FLIGHT CHECK (predicted output vs expected output)
        If mismatch → cognitive repair (same as before)
        If match → continue

Step 3.5: TRACE VERIFICATION (NEW STEP)
        Extract variable claims from the trace
        Inject as assert statements into the code
        Execute the instrumented code
        
        If all assertions PASS → trace is genuine → proceed
        If assertion FAILS → trace was hallucinated
            → Tell LLM: "You claimed x=5 at step 3 but x was actually 12.
               Your trace was wrong. Re-examine your code."
            → Back to Step 2

Step 4: EXECUTE against remaining test cases
Step 5: REPAIR if needed (same as before)
Step 6: DONE ✓
```

---

## What This Catches That Raw FLARE Doesn't

### Mode D (The Dangerous One): Solved

LLM writes wrong code. LLM fabricates a trace that "predicts" the wrong output. Both agree. But when we inject the trace claims as assertions, the assertions either:
- **Fail** (because the fabricated intermediate values don't match reality) → caught
- **Pass** (meaning the trace is actually accurate, and the code really does produce that output) → then the bug is in the algorithm, not the trace, and we catch it by comparing against the expected test case output

Either way, it's caught.

### Mode C (The Lucky One): Solved

LLM traces wrongly but code happens to work. When we inject trace assertions, they fail because the trace doesn't match the actual execution. Even though the code produces the right output, the assertion failure reveals that the LLM didn't understand WHY the code works — which means it can't fix it if a harder test case breaks it later.

---

## The Practical Implementation

The trace verification step requires one simple function:

```python
def extract_and_inject_assertions(code: str, trace: str) -> str:
    """
    Parse the LLM's trace for variable value claims.
    Inject assert statements at the corresponding points in the code.
    Return the instrumented code.
    """
    # Use LLM to extract structured claims from the trace:
    # [{"step": 1, "line": 5, "variable": "x", "value": 2}, ...]
    # Then inject: assert x == 2, f"Trace mismatch at step 1"
    ...
```

You can even use the LLM itself to do the extraction — ask it to convert its own trace into a JSON list of `{variable, expected_value, line_number}` claims. Then programmatically inject the assertions.

**Total additional code: ~50 lines of Python.**

---

## The Layered Defense (Summary)

```
Layer 1: Test Cases          → Catches wrong final output
Layer 2: Self-Trace          → Catches wrong algorithm understanding
Layer 3: Trace Assertions    → Catches fabricated/hallucinated traces
```

A hallucination can only survive if it:
1. Produces the correct final output (passes test cases), AND
2. The LLM predicts that correct output (passes pre-flight), AND
3. Every intermediate value the LLM claimed is verified by the interpreter (passes assertions)

At that point, if all three layers agree, the code is almost certainly correct — because the LLM has demonstrated step-by-step understanding that has been independently verified by the Python runtime.
