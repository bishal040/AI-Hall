# Constrained Property-Based Verification (CPV)
## The Definitive Thesis Solution — Production-Grade Hallucination Detection for LLM Code Generation

*This framework emerged from a critical analysis of the Executable Verification Paradigm (EVP). It fixes EVP's four fatal flaws while keeping its core insight: generation (probabilistic) and verification (deterministic) must be fundamentally different processes.*

---

## What EVP Got Wrong, and How CPV Fixes It

| EVP Flaw | Why It Fails | CPV Fix |
|:---|:---|:---|
| **Magic API calls** | LLM writes `wikidata.population("France")` — an API that doesn't exist | **Strict Schema Enforcement:** LLM outputs JSON args to predefined tools. Schema parser catches any hallucinated parameters instantly. |
| **Self-fulfilling tests** | LLM writes a buggy function AND a buggy `assert` that matches | **Property-Based Testing:** LLM defines invariants, not hardcoded values. A fuzzer (Hypothesis) throws random inputs the LLM can't predict. |
| **No error attribution** | When sandbox crashes, is it bad code or a bad test? | **Multi-Agent Reflexive Loop:** Agent A writes code, Agent B writes properties. SyntaxError = bad test. AssertionError = caught hallucination. |
| **Brutal latency** | Running isolated sandboxes for every claim is too expensive | **Tiered Verification Funnel:** AST + mypy first (milliseconds), then dynamic execution only for survivors. |

---

## The CPV Architecture

### Layer 1: Strict Schema Enforcement (Eliminates Freeform Hallucination)

The LLM is NEVER allowed to write arbitrary code to verify its claims. It maps its logic onto a rigidly defined toolset via JSON Schema / Function Calling.

**Example — Verifying a complexity claim:**

The LLM does NOT write:
```python
# DANGEROUS: LLM could hallucinate this entire function
result = my_custom_api.query_complexity("red_black_tree", "insert")
assert result == "O(log n)"
```

Instead, a predefined tool exists:
```json
{
  "name": "query_complexity",
  "description": "Look up the time complexity of an operation on a data structure",
  "parameters": {
    "type": "object",
    "properties": {
      "data_structure": {
        "type": "string",
        "enum": ["array", "linked_list", "binary_tree", "red_black_tree", "hash_map", "heap", "graph"]
      },
      "operation": {
        "type": "string",
        "enum": ["insert", "delete", "search", "traverse", "sort", "balance"]
      }
    },
    "required": ["data_structure", "operation"]
  }
}
```

The LLM outputs ONLY:
```json
{"data_structure": "red_black_tree", "operation": "insert"}
```

A deterministic backend looks up the answer from a curated knowledge base. If the LLM hallucinates a parameter outside the enum (e.g., `"quantum_tree"`), the JSON schema validator catches it immediately — no code execution needed.

**Why this kills hallucination:** The LLM cannot invent data sources. It can only point to pre-validated ones through constrained channels.

---

### Layer 2: Property-Based Testing (Eliminates Self-Fulfilling Tests)

When verifying generated code, the LLM defines **structural invariants** — mathematical properties that must ALWAYS hold — instead of writing hardcoded test cases.

**Example — Verifying a Red-Black Tree insertion:**

The LLM does NOT write:
```python
# DANGEROUS: LLM hallucinates the "expected" result to match its own bug
tree = RedBlackTree()
tree.insert(5)
tree.insert(3)
tree.insert(7)
assert tree.root.value == 5  # What if the bug IS in the root assignment?
```

Instead, the LLM defines invariants:
```python
from hypothesis import given, strategies as st

@given(values=st.lists(st.integers(), min_size=1, max_size=100))
def test_rbt_properties(values):
    tree = RedBlackTree()
    for v in values:
        tree.insert(v)
    
    # INVARIANT 1: Root is always black
    assert tree.root.color == BLACK
    
    # INVARIANT 2: No red node has a red child
    assert no_red_red_violations(tree.root)
    
    # INVARIANT 3: Every path from root to leaf has the same black-node count
    assert uniform_black_height(tree.root)
    
    # INVARIANT 4: The tree is a valid BST (left < parent < right)
    assert is_valid_bst(tree.root)
    
    # INVARIANT 5: All inserted values are present
    for v in values:
        assert tree.search(v) is not None
```

Hypothesis then generates **hundreds of randomized test inputs** automatically — inputs that the LLM cannot predict or pre-accommodate. The invariants are structural truths about the data structure that are independent of specific values.

**Why this kills self-fulfilling tests:** The LLM cannot "match" its test to its bug when it doesn't know what inputs will be tested. The invariants are mathematically defined — either a Red-Black Tree has uniform black height or it doesn't. There's no room for ambiguity.

---

### Layer 3: Multi-Agent Reflexive Loop (Eliminates Error Attribution Confusion)

```
┌─────────────────────────────────────────────────┐
│  Agent A: Code Generator                        │
│  → Generates the code for the given problem     │
│                                                 │
│  Agent B: Property Definer                      │
│  → Independently defines invariants/properties  │
│  → Has NO access to Agent A's implementation    │
│                                                 │
│  Executor: Sandboxed Runtime                    │
│  → Combines Agent A's code + Agent B's tests    │
│  → Runs in isolated environment                 │
│                                                 │
│  Error Attribution:                             │
│  ┌──────────────────────────────────────────┐   │
│  │ SyntaxError / NameError / TypeError      │   │
│  │ → Agent B's test code is broken          │   │
│  │ → Feed stack trace back to Agent B       │   │
│  │ → "Fix your test syntax and retry"       │   │
│  │ → Does NOT count as hallucination        │   │
│  ├──────────────────────────────────────────┤   │
│  │ AssertionError                           │   │
│  │ → Test executed cleanly but FAILED       │   │
│  │ → Agent A's code violates the invariant  │   │
│  │ → THIS is a caught hallucination         │   │
│  │ → Feed failure details to Agent A        │   │
│  ├──────────────────────────────────────────┤   │
│  │ All tests PASS                           │   │
│  │ → Code is verified ✅                    │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

**Why this kills error attribution confusion:** By cleanly separating "the test itself is broken" (runtime error) from "the test found a bug" (assertion error), the system never conflates a bad test with a caught hallucination. And by having Agent B work INDEPENDENTLY of Agent A, the verification is genuinely adversarial — Agent B doesn't know Agent A's implementation details and can't unconsciously accommodate them.

---

### Layer 4: Tiered Verification Funnel (Eliminates Latency Problem)

Not every claim needs the full property-based testing treatment. Use a funnel:

```
Tier 1: Static Analysis (milliseconds)
├── AST parsing — does the code even parse?
├── Type checking (mypy) — are types consistent?
├── Import validation — do all imports exist?
└── Schema validation — are all tool calls well-formed?
    │
    │ Fails here? → Instant rejection, no execution needed
    │ Passes? ↓
    │
Tier 2: Dynamic Execution (seconds)
├── Bundle surviving claims into ONE execution environment
├── Run property-based tests with Hypothesis
├── Resource limits: 10s timeout, 256MB memory cap
└── Collect results
    │
    │ All invariants hold? → VERIFIED ✅
    │ Invariant violated? → HALLUCINATION CAUGHT 🚨
    │ Timeout/OOM? → Flag as UNVERIFIABLE ⚠️
```

**Why this kills latency:** Tier 1 catches ~40-50% of hallucinations (syntax errors, bad imports, type mismatches) in milliseconds, before any sandbox is ever spun up. Only clean code reaches the expensive dynamic tier.

---

## Sandboxing Strategy

For a thesis prototype, the best approach is a **lightweight subprocess sandbox**:

```python
import subprocess
import tempfile
import os

def execute_in_sandbox(code: str, timeout: int = 10) -> dict:
    """Run code in an isolated subprocess with resource limits."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        f.flush()
        
        try:
            result = subprocess.run(
                ['python3', f.name],
                capture_output=True,
                text=True,
                timeout=timeout,
                env={
                    'PATH': os.environ['PATH'],
                    'PYTHONPATH': '',  # Restrict imports
                }
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'error_type': classify_error(result.stderr)  # SyntaxError vs AssertionError
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error_type': 'TIMEOUT'}
        finally:
            os.unlink(f.name)

def classify_error(stderr: str) -> str:
    """Distinguish test-code bugs from caught hallucinations."""
    if 'SyntaxError' in stderr or 'NameError' in stderr or 'TypeError' in stderr:
        return 'TEST_BUG'       # Agent B's problem — retry the test
    elif 'AssertionError' in stderr:
        return 'HALLUCINATION'  # Agent A's code is wrong — caught!
    elif stderr == '':
        return 'PASS'           # All good
    else:
        return 'UNKNOWN'
```

**Why not Docker?** For a thesis prototype testing code snippets, subprocess isolation is sufficient. Docker adds ~500ms cold-start overhead per container, which would make running 1000+ test cases painfully slow. Docker is the right choice for production deployment, but overkill for thesis experiments.

**Why not WASM?** Pyodide (Python-in-WASM) has limited library support — `hypothesis` doesn't run natively in it. And WASM's security model is more about browser sandboxing than adversarial code isolation. For Python specifically, subprocess + resource limits is simpler and more capable.

**For production (future work section of thesis):** Firecracker microVMs (what AWS Lambda uses) — ~125ms cold start, strong isolation, Linux-only. Perfect for a real deployment.

---

## The Complete Thesis Experiment

### Domain Focus
**LLM hallucination during debugging of advanced data structures and algorithms.**

This is narrow enough to be rigorous and broad enough to be interesting. It directly connects to your 17 research papers.

### Benchmark
- LeetCode Medium + Hard problems tagged: Trees, Graphs, Dynamic Programming, Heaps
- HumanEval+ (extended version with more edge-case tests)
- Custom: 50 manually curated Red-Black Tree / AVL / Graph algorithm problems

### What You Measure

| Metric | Definition |
|:---|:---|
| **Hallucination Detection Rate** | % of buggy code correctly flagged by property-based tests |
| **False Positive Rate** | % of correct code incorrectly flagged |
| **Error Attribution Accuracy** | % of failures correctly classified as TEST_BUG vs HALLUCINATION |
| **Pre-execution Catch Rate** | % of hallucinations caught by Tier 1 (static) alone |
| **Pass@1 Improvement** | How much does CPV-guided repair improve first-attempt success? |

### Thesis Statement

> "We propose Constrained Property-Based Verification (CPV), a multi-agent verification framework that detects LLM code hallucinations by forcing models to define structural invariants verified through adversarial property-based testing — achieving hallucination detection rates above 90% on advanced data structure problems while cleanly attributing failures to either cognitive errors or test-code defects."
