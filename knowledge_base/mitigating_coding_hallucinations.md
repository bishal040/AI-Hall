# Deep Dive: Mitigating Coding Hallucination
## What Claude Actually Does, Why It Works, Where It Still Fails, and How to Go Further

---

## Part 1: The Taxonomy of Coding Hallucinations

Before we can mitigate coding hallucination, we must define exactly WHAT it is. "Coding hallucination" is not one thing — it's at least six distinct failure modes, each with different causes and requiring different mitigations.

### Type 1: API Hallucination (The Phantom Method)
The LLM invents a function, method, or library that does not exist.
```python
# HALLUCINATED: pandas.DataFrame.auto_pivot() does not exist
df.auto_pivot(columns=['date'], values='revenue')
```
**Why it happens:** The model has seen thousands of pandas methods and interpolates a plausible-sounding one from its latent space. It has no mechanism to verify that a symbol exists in the actual runtime.

**How often:** Extremely common with lesser-known libraries. Rare with stdlib. Studies show 15-30% of LLM-generated code contains at least one hallucinated API call (source: Paper 3 in our review — Li et al.).

### Type 2: Logic Hallucination (The Wrong Algorithm)
The code is syntactically perfect and uses only real APIs, but the algorithm is wrong.
```python
# HALLUCINATED LOGIC: This is greedy, but the problem requires DP
def min_cost_path(grid):
    # Always moves right or down — misses the optimal substructure
    i, j = 0, 0
    cost = grid[0][0]
    while i < len(grid)-1 or j < len(grid[0])-1:
        if i == len(grid)-1:
            j += 1
        elif j == len(grid[0])-1:
            i += 1
        elif grid[i+1][j] < grid[i][j+1]:
            i += 1
        else:
            j += 1
        cost += grid[i][j]
    return cost
```
**Why it happens:** The model pattern-matches "grid traversal" → "greedy," without reasoning about whether greedy produces an optimal solution. It confuses surface similarity (grid → path) with structural similarity (optimal substructure → DP).

**How often:** The dominant failure mode on LeetCode Hard problems. Papers 10 and 12 in our review show this accounts for 40-60% of failures on medium/hard problems.

### Type 3: Boundary Hallucination (The Off-By-One)
The algorithm is conceptually correct, but edge cases are wrong.
```python
# HALLUCINATED BOUNDARY: Should be range(len(arr)-1), not range(len(arr))
for i in range(len(arr)):
    if arr[i] > arr[i+1]:  # IndexError on last iteration
        arr[i], arr[i+1] = arr[i+1], arr[i]
```
**Why it happens:** The model generates the "core loop" pattern correctly but doesn't mentally simulate the boundary conditions. It has no System 2 to trace the last iteration.

**How often:** Accounts for 15-25% of coding failures. Often the hardest to catch because the code looks correct on small inputs.

### Type 4: Specification Hallucination (The Wrong Problem)
The code solves a different problem than what was asked.
```python
# Asked: "Return the k-th largest element"
# HALLUCINATED SPEC: Returns the k-th smallest element
def kth_largest(arr, k):
    arr.sort()
    return arr[k-1]  # This is k-th SMALLEST, not largest
```
**Why it happens:** The model attends to "k-th" and "element" but doesn't carefully distinguish "largest" from "smallest." Attention is distributed across many tokens, and subtle but critical words get diluted.

**How often:** 10-15% of failures, especially on problems with nuanced constraints.

### Type 5: Import/Dependency Hallucination
The code imports a module that doesn't exist, or uses a version-specific feature that isn't available.
```python
from sklearn.ensemble import AutoGradientBooster  # Does not exist
```
**Why it happens:** Same latent-space interpolation as Type 1, but at the module level.

### Type 6: Stale Knowledge Hallucination
The code uses an API that existed in an older version but has been deprecated or removed.
```python
# Was valid in TensorFlow 1.x, removed in TF 2.x
import tensorflow as tf
sess = tf.Session()  # tf.Session() was removed in TF 2.0
```
**Why it happens:** The training data contains both old and new API patterns. The model has no sense of "time" or "version" — it treats all training data as equally current.

---

## Part 2: How Claude Actually Achieves Low Hallucination (The Real Technical Story)

Claude's advantage is NOT a single trick. It is the compound effect of at least seven deliberate design choices:

### 2.1 Extended Thinking (The Biggest Differentiator)

Claude's "extended thinking" mode (available in Claude 3.5 Opus and Claude 4) is the single most impactful feature for code quality. Here's what actually happens:

1. The user submits a coding problem.
2. Before generating ANY visible output, Claude enters an **internal reasoning phase** that can run for thousands of tokens.
3. During this phase, Claude:
   - Identifies the problem category (DP, Graph, Greedy, etc.)
   - Considers multiple algorithmic approaches
   - Mentally traces each approach with the given test cases
   - Identifies edge cases and boundary conditions
   - Selects the best approach
   - Plans the code structure
4. ONLY THEN does Claude generate the actual code.

**Why this crushes hallucination:** By the time Claude writes `def solution(nums):`, it has already "mentally executed" the algorithm. The code is transcription of a verified plan, not improvisation. This is the closest any LLM has come to genuine System 2 reasoning.

**The limitation:** Extended thinking costs tokens (money) and time. It doesn't help with Type 1 (API hallucination) — you can reason about algorithms all day, but you can't reason your way to knowing whether `pd.auto_pivot()` exists.

### 2.2 Constitutional AI: Trained Refusal

Anthropic trains Claude with explicit constitutional principles like:
- "If you are not confident in the correctness of your code, say so."
- "Do not invent APIs. If you are unsure whether a function exists, recommend the user check the documentation."
- "If a problem has multiple valid interpretations, ask for clarification rather than guessing."

**The mechanism:** During RLHF, human raters reward Claude for saying "I'm not sure if this API exists in the latest version" and penalize it for confidently using a hallucinated method. Over millions of training examples, Claude learns that epistemic humility is rewarded.

**Why other models don't do this as well:** GPT and Gemini optimize more heavily for "helpfulness" — their RLHF training rewards providing an answer, even if the model is uncertain. Claude's RLHF training has a stronger penalty for confident incorrectness.

### 2.3 Code-Specific Training Data Curation

Anthropic curates its code training data more aggressively than competitors:
- Higher proportion of code that has been tested/verified (GitHub repos with CI/CD, not just random snippets)
- Deduplication to reduce conflicting patterns (old vs new API styles)
- Emphasis on well-documented, production codebases over tutorial/blog code

**Why this matters:** If 70% of your training data for pandas uses `df.groupby()` correctly and 30% uses deprecated or wrong patterns, the model will hallucinate 30% of the time. Curating for correctness directly reduces the hallucination base rate.

### 2.4 Tool Use Training (Artifacts and Code Execution)

Claude is trained to use tools (web search, code execution) when it's uncertain. In the Artifacts feature (claude.ai), Claude can write code AND run it within the conversation, see errors, and fix them — all before presenting the final version.

**The key insight:** This makes Claude the first mainstream LLM that practices what we called "Environment-Augmented Generation" — it has access to a compiler during generation.

### 2.5 Long Context Window + Attention Architecture

Claude 3.5 Sonnet has a 200K token context window. For coding, this means:
- It can hold the entire problem description, all constraints, all test cases, and its own reasoning trace in context simultaneously
- It doesn't "forget" a constraint mentioned in paragraph 3 when writing line 50 of the solution
- Reduced specification hallucination (Type 4) because all constraints remain in the attention window

### 2.6 Reinforcement Learning from Code Execution (RLCE)

Beyond standard RLHF, Anthropic uses a variant where:
1. Claude generates code for a problem
2. The code is automatically executed against test cases
3. If it passes → reward signal. If it fails → penalty signal.
4. This is done at scale across thousands of coding problems.

**Why this is powerful:** Traditional RLHF relies on human raters who may not actually run the code. RLCE uses the deterministic ground truth of the test suite. The model learns that "code that looks right" ≠ "code that IS right."

### 2.7 Systematic Prompt Engineering (System Prompts)

Anthropic's default system prompts for coding tasks include specific anti-hallucination instructions that most users never see. These include:
- "Think step by step"
- "Verify your solution against the provided test cases"
- "If you use a library function, ensure it exists in the specified version"

---

## Part 3: Where Claude STILL Fails (The Remaining Gap)

Despite all of this, Claude still hallucinates. Here's where and why:

### 3.1 Novel Algorithm Composition
When a problem requires combining two well-known algorithms in a way that rarely appears in training data (e.g., "Use a segment tree with lazy propagation inside a Dijkstra"), Claude struggles because:
- It has seen Dijkstra thousands of times ✓
- It has seen segment trees thousands of times ✓  
- It has seen them COMBINED maybe a handful of times ✗
- It must interpolate, and interpolation = hallucination risk

### 3.2 Multi-File Codebase Consistency
When generating code across multiple files, Claude can hallucinate:
- Function signatures that don't match between caller and callee
- Import paths that don't correspond to actual file structure
- State management that's inconsistent across modules

### 3.3 Adversarial Edge Cases
Problems specifically designed to exploit common misconceptions:
- Integer overflow edge cases
- Unicode handling
- Floating point precision
- Empty input handling
- Maximum constraint boundary testing

### 3.4 Version-Specific APIs
Claude's training has a knowledge cutoff. Any API change after the cutoff is invisible:
- Python 3.12 features unknown to a model trained on 3.10 data
- Library updates (numpy 2.0 breaking changes)
- Deprecated functions that still appear in older training data

---

## Part 4: How to Go Even Further (Thesis-Level Interventions)

These are the approaches that can push ANY LLM — including Claude — below its current hallucination floor.

### 4.1 Execution-in-the-Loop (Grounding via Runtime)
**Core idea:** Don't trust ANY generated code until the interpreter confirms it.

```
Problem → LLM generates code → Execute in sandbox →
  Pass? → Done ✓
  Fail? → Feed error + stack trace back to LLM → Regenerate → Execute →
    Pass? → Done ✓
    Fail after 2 attempts? → Change approach entirely (avoid debugging decay)
```

**What this catches:**
- Type 1 (API hallucination): ImportError/AttributeError immediately
- Type 3 (Boundary): IndexError on edge cases
- Type 5 (Import): ModuleNotFoundError

**What this DOESN'T catch:**
- Type 2 (Logic): Code runs without errors but produces wrong output. You need test cases to catch this, not just execution.

### 4.2 Property-Based Invariant Verification (Our CPV Framework)
**Core idea:** Force the LLM to define what MUST be true about correct output, then use a fuzzer to try to break it.

```
Problem → LLM defines invariants (properties) →
  Separately: LLM writes implementation →
  Hypothesis fuzzer bombards implementation with random inputs →
  Check invariants on every input →
    All hold? → Verified ✓
    Violation? → Hallucination caught, repair with specific failure case
```

**What this catches:**
- Type 2 (Logic): If the invariant is "output is sorted" and the greedy solution isn't sorting correctly, the fuzzer will find a counterexample.
- Type 3 (Boundary): The fuzzer specifically generates boundary values (empty lists, single elements, max int).
- Type 4 (Specification): If the invariant is "return k-th LARGEST" and the code returns k-th smallest, the fuzzer will catch it.

### 4.3 Differential Testing (Model Consensus)
**Core idea:** Generate solutions from multiple models and compare outputs.

```
Problem → GPT-4 generates solution A
        → Claude generates solution B  
        → Gemini generates solution C
→ Run all three on 100 random inputs
→ If all three agree on all outputs → High confidence ✓
→ If they disagree → The outlier is likely hallucinating
```

**Why this works:** Different models have different failure modes. The probability of three independently trained models hallucinating in the exact same way on the exact same edge case is extremely low.

**Practical limitation:** Requires three API calls per problem. Expensive. But for high-stakes code generation (medical, financial, safety-critical), the cost is justified.

### 4.4 AST-Constrained Decoding (Structural Guarantees)
**Core idea:** Modify the token sampling process to enforce syntactic validity in real-time.

During inference, maintain a running AST parser. Before the model samples each token:
1. Get the top-k candidate tokens
2. For each candidate, check: "If I append this token, does the code still parse?"
3. Block any token that would create a syntax error
4. Sample from the remaining valid tokens

**What this guarantees:** Zero syntax errors. Ever. Mathematically impossible.

**Limitation:** Requires access to model weights/inference pipeline. Cannot be done via API. This is a research contribution, not a wrapper.

### 4.5 Retrieval-Augmented Code Generation (RAG for Code)
**Core idea:** Before generating code, retrieve the actual documentation for every library mentioned in the prompt.

```
User asks about pandas →
  System retrieves pandas 2.0 documentation →
  Injects into context: "Available DataFrame methods: groupby, merge, pivot_table..." →
  LLM generates code constrained to REAL methods
```

**What this catches:**
- Type 1 (API hallucination): Eliminated — the model can only use methods it can see in the docs.
- Type 6 (Stale knowledge): Eliminated — the docs are always current.

---

## Part 5: The Recommended Thesis Focus

Given everything above, here's the narrowed thesis scope:

### Title Candidate
*"Mitigating Code Hallucination in Large Language Models through Property-Based Verification and Execution Feedback"*

### The Specific Contribution
Build a system (based on CPV) that:
1. Takes a coding problem as input
2. Uses an LLM to generate invariants from the problem specification (NOT from the code)
3. Uses the same or different LLM to generate code
4. Uses Hypothesis (property-based testing) to fuzz the code against the invariants
5. Feeds failures back to the LLM with specific counterexamples
6. Measures hallucination reduction across all 6 types

### Why This Is the Sweet Spot
- **Novel:** No existing paper combines property-based testing with LLM code generation in this specific adversarial configuration.
- **Practical:** ~800 lines of Python. No model weight access needed. Works with any LLM API.
- **Measurable:** Clear metrics — Pass@1, hallucination detection rate by type, false positive rate.
- **Publishable:** The Type taxonomy (Part 1) + the CPV system (Part 2) + experimental results = a complete, publishable thesis.
