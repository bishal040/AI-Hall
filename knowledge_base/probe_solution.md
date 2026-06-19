# The PROBE Architecture
**(Programmatic Runtime Observation & Belief Elicitation)**

*A highly novel, practically implementable framework for your thesis that stops LLMs from guessing and forces them to use the Scientific Method.*

If TRACE was too common (standard debugging) and T.I.M.E. was too theoretical (quantum-level execution), the **PROBE Architecture** hits the exact sweet spot for a Master's Thesis. It is entirely novel, completely solves the gaps in the 17 papers, and can actually be built using Python, AST parsing, and standard LLMs.

---

## The Core Philosophy: Stop Guessing, Start Probing
The fundamental flaw causing "Debugging Decay" (Paper 8) and logic hallucination (Papers 2, 6) is that **LLMs are forced to guess the fix**. When a program fails, the LLM says, *"Maybe if I change `x + 1` to `x - 1` it will work."* 

The PROBE Architecture forbids the LLM from writing a fix until it proves *why* the bug exists. It forces the AI to use the Scientific Method.

## The 4 Stages of PROBE

### Stage 1: The Observation (AST Contextualization)
* **What happens:** The code fails a test case. Instead of feeding the whole raw code back to the LLM, the framework uses Deterministic AST Analysis (Paper 14) to map out the structure of the program. 
* **The Shift:** The LLM is provided the AST map and the exact test case mismatch. It is NOT asked to fix the code.

### Stage 2: Belief Elicitation (Hypothesis Generation)
* **What happens:** Based on the failure, the LLM must generate **3 competing hypotheses** about what went wrong in the reasoning trace (Paper 10). 
  * *Hypothesis A:* The loop condition terminates one step too early.
  * *Hypothesis B:* The API returns a string instead of an int (Paper 16).
  * *Hypothesis C:* Variable `y` becomes negative during iteration 3.
* **The Shift:** This prevents the LLM from getting tunnel vision. By forcing multiple hypotheses, we use the logic of Functional Clustering (Paper 15) at the *idea* level rather than the *code* level.

### Stage 3: The Experiment (Micro-Probing)
* **What happens:** This is the magic step. The LLM is asked to write **"Micro-Probes"** to test its hypotheses. A micro-probe is a simple `print()` or `assert` statement injected into the original code.
* **The Execution:** The framework injects these probes dynamically into the AST (Leveraging Print Debugging - Paper 12) and executes the code block by block (LDB - Paper 13). 
* **The Shift:** The LLM isn't changing the logic; it is setting up sensors. When the code runs, the sensors report back: *"Probe A is false, Probe B is false, Probe C is TRUE."*

### Stage 4: Targeted Remediation (The Proven Fix)
* **What happens:** The LLM now has absolute mathematical proof that Hypothesis C is the actual bug. Only now is it allowed to write the code fix.
* **The Shift:** Because the fix is based on a proven runtime anomaly, the "Ghost Debugging" loop is destroyed. If the fix fails, the Debugging Decay Index (DDI - Paper 8) triggers, wiping the slate clean and forcing the LLM to generate 3 *new* hypotheses.

---

## Why PROBE is the Perfect Thesis Solution

| Why it works | The Research It Builds On |
| :--- | :--- |
| **It is Highly Buildable** | You don't need access to LLM weights or massive compute. You just need Python's `ast` module and prompt engineering. |
| **It Solves the "Black Box" Problem** | It extracts intermediate runtime states naturally via micro-probes (Papers 9, 12, 13). |
| **It Eradicates Ghost Debugging** | LLMs get stuck in loops because they guess blindly. PROBE removes guessing entirely (Papers 8, 11). |
| **It Scales to Hard Algorithms** | Complex university algorithms can't be fixed by guessing. They require isolating the mathematical flaw (Paper 10, 17). PROBE isolates the flaw via hypothesis testing. |

### Conclusion
The **PROBE Architecture** shifts the paradigm from "LLM as a Coder" to **"LLM as a Scientist."** It is a highly robust, deeply intelligent framework that perfectly encapsulates the warnings and discoveries of all 17 research papers, while remaining entirely feasible for you to code and evaluate for your thesis defense.
