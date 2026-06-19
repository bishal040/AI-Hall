# User Research Notes: Synthesized Analysis

This document contains the optimized, structured insights extracted from the user's manual research spreadsheet.

## CodeHalu: Investigating Code Hallucinations in LLMs via
Execution-based Verification

**Goal:** Hallucination Classification Method

**Test Case:** 17 LLMs

**Issue:** Code hallucinations in LLMs have not been systematically explored.

**Existing Work:** Hallucination in NLP is explored but code generation domain is largely unexplored

**Improvement:** Execution-based verification and dynamic detection algorithm (CodeHalu) and CodeHaluEval benchmark.

**Pattern:** All Cluster A papers agree: static/text-based methods are insufficient — you need execution or runtime feedback to catch code-specific hallucinations. CodeHalu is the earliest systematic attempt at this in the code domain.

**Lacking:** Only tests whether code runs correctly — does not classify WHY the hallucination occurred (training gap vs. reasoning failure). No cross-model comparison of hallucination rates on the same problem set.

**Framework:** CodeHalu

---

## Beyond Functional Correctness: Exploring
Hallucinations in LLM-Generated Code

**Goal:** Categorize the hallucinations, causes and
impacts

**Test Case:** Thematic analysis of LLM generated codes

**Issue:** Gap in understanding types, causes, and impacts of code hallucinations.

**Existing Work:** Prior studies mostly focus on NLG hallucinations.

**Improvement:** prompt enhanced to mitigate cuase and impacts of code hallucinations

**Pattern:** Shares the taxonomy-building impulse with papers 1, 3, 6. All three independently converge on the need to classify hallucinations before you can fix them — suggesting classification is an unsolved foundation problem.

**Lacking:** Prompt-only mitigation — no training-based fix. Does not test whether the taxonomy holds across different LLMs or problem difficulty levels. Thematic analysis is manual and may not scale.

**Framework:** Taxonomy framework with 3 primary categories.

---

## Hallucination by Code Generation
LLMs: Taxonomy, Benchmarks, Mitigation,
and Challenges

**Goal:** Investigates recent studies and techniques 
relevant to hallucination

**Test Case:** Survey of existing papers

**Issue:** Hallucinated code is challenging to identify and fix.

**Existing Work:** Existing surveys focus on general natural language hallucinations rather than code-specific.

**Improvement:** Structured taxonomy of code hallucinations, consolidation of benchmarks and mitigation strategies.

**Pattern:** This is the meta-paper for Cluster A. It synthesizes papers 1, 2, 6, 14, 15, 16 and shows they each address one part of a larger picture. The pattern it reveals: no single paper covers detection + mitigation + benchmarking together.

**Lacking:** As a survey it proposes no new solution. Does not evaluate which mitigation strategy works best across problem types. Does not address why hallucination rates differ between models.

**Framework:** Taxonomy framework with 4 primary categories.

---

## ASurvey on Hallucination in Large Language 
Models: Principles, Taxonomy, Challenges, and Open Questions

**Goal:** Survey : Detection, Causes, Benchmarks and Mitigation

**Test Case:** Survey of 395 papers

**Notes:** Give a read for good knowledge

**Issue:** LLMs generate plausible but nonfactual content, raising reliability concerns in IR systems.

**Existing Work:** Prior works focused on task-specific models; need an open-ended LLM taxonomy.

**Improvement:** Provides an overview of detection methods, mitigating factors, and RAG limitations.

**Pattern:** This is the broadest paper — covers all LLM hallucination, not just code. The pattern connecting it to papers 1–3: every sub-domain (NLP, code, QA) has had to rebuild the same taxonomy from scratch because general hallucination research did not transfer well to specialized domains.

**Lacking:** Too broad to give actionable guidance for code-specific hallucination. Does not discuss algorithmic problem-solving as a task type. RAG limitations section is relevant to paper 16 but not connected.

**Framework:** Redefined taxonomy: Factuality vs Faithfulness hallucination.

---

## The Illusion of Progress: Re-evaluating 
Hallucination Detection in LLMs

**Goal:** Analyzes hallucination evaluation methods

**Notes:** ROUGE has alarmingly low precision for factual errors. Simple length heuristics can rival complex techniques.

**Issue:** Current detection methods rely on ROUGE which misaligns with human judgments.

**Existing Work:** Prior work relies heavily on ROUGE to evaluate QA hallucination detection.

**Improvement:** highlights the drop in performance of established methods and advocates for LLM-as-Judge

**Pattern:** Critical bridge paper. It implies that results claimed by papers 1, 2, 6, 7 may be overstated if they relied on flawed metrics. The pattern: almost every paper in this set uses a different evaluation metric — there is no standard, and paper 5 explains why that is a serious problem.

**Lacking:** Only addresses evaluation methodology — proposes no new detection or mitigation technique. Does not test LLM-as-Judge on code-specific hallucination tasks, only on QA.

**Framework:** ROUGE vs LLM-as-Judge evaluation framework.

---

## CodeMirage: Hallucinations in Code Generated by Large Language Models

**Goal:** Methodology,  mitigation strategies

**Test Case:** 1,137 hallucinated Python snippets using GPT 3.5

**Notes:** Claims to be the first research paper on code based hallucination

**Issue:** Hallucinations in LLM-generated code (syntax errors, logical errors, security vulnerabilities, memory leaks)

**Existing Work:** No prior benchmark existed specifically for code hallucinations; general text hallucination research didn't cover code

**Improvement:** Introduced the CodeMirage benchmark (1,137 hallucinated Python snippets) and a detection methodology tested on CodeLLaMA, GPT-3.5, and GPT-4

**Pattern:** First benchmark paper for code hallucination — directly enables papers 1 and 3 to do comparative work. Pattern with paper 7: both build benchmarks because the field had none. Benchmark creation is a recurring prerequisite pattern across this paper set.

**Lacking:** Limited to Python only. Only tests GPT-family and one open model. Does not break down hallucination rates by problem type or difficulty. No analysis of why GPT-4 outperforms GPT-3.5 beyond raw accuracy.

**Framework:** CodeMirage

---

## Evaluating Debugging Capability of Large Language Models

**Goal:** Evaluate the debugging capabilities of LLMs

**Test Case:** Debugging bench mark consisting of 4,253 instances

**Issue:** LLMs' debugging capability is underexplored and poorly evaluated

**Existing Work:** Prior debugging evaluations suffered from data leakage, small dataset scale, and limited bug variety

**Improvement:** Introduced DebugBench — 4,253 instances across 4 bug categories and 18 bug types in C++, Java, and Python, with rigorous quality checks

**Pattern:** Mirror image of paper 6 but for debugging. Both papers' core finding is the same: we cannot improve what we cannot measure. The pattern across papers 7, 8, 9, 11: debugging failure is not random — it is systematic and predictable.

**Lacking:** Does not test iterative debugging — only single-shot fix attempts. Does not distinguish between bugs the model can recognise but not fix vs bugs it cannot recognise at all. This distinction maps directly to your "ghost debugging" observation.

**Framework:** DebugBench

---

## The Debugging Decay Index: Rethinking Debugging
Strategies for Code LLMs

**Goal:** Debugging decay index(DDI) : Quantifies when debugging is ineffective and need intervention

**Issue:** LLMs lose 60–80% of their debugging effectiveness within just 2–3 iterative attempts

**Existing Work:** Existing iterative debugging methods use fixed heuristics and cannot adapt based on past outcomes — stuck in exploitation without exploration

**Improvement:** Introduced the Debugging Decay Index (DDI), a mathematical framework that detects when debugging becomes ineffective and triggers a strategic fresh start at optimal intervention points

**Pattern:** This paper is the mathematical formalisation of your personal experience. When you watched an AI keep "fixing" the same wrong thing — that is debugging decay. The pattern with paper 11: both papers attack the same problem (iterative failure) from different angles — DDI detects failure, TGPR prevents it.

**Lacking:** DDI tells you WHEN to stop but not WHY the model got stuck. Does not analyse what type of bug or problem structure triggers faster decay. No comparison across different LLMs — does decay speed differ between models?

**Framework:** DDI (Debugging Decay Index)

---

## ChatDBG: Augmenting Debugging with Large Language
Models

**Goal:** ChatDBG : AI-powered debugging assistant

**Issue:** Traditional debuggers are passive tools — they can't reason about program state or answer high-level questions like "why is x null?"

**Existing Work:** Conventional debuggers (GDB, LLDB, Pdb) only provide tracing, breakpoints, and backtraces — no reasoning capability

**Improvement:** ChatDBG lets the LLM "take the wheel" as an autonomous agent that queries and controls the debugger, performs root cause analysis, and generates fixes — achieving 85% bug fix success rate in Python

**Pattern:** Opposite philosophy to papers 8 and 11. Instead of teaching the LLM to debug better internally, ChatDBG gives the LLM external tools (real debugger access). The pattern: papers 9, 12, 13 all converge on the same insight — LLMs need runtime information, not just source code, to debug effectively.

**Lacking:** 85% success rate is only on Python. Does not test on algorithmic problems with complex logic (your specific use case). Requires integration with external debugger — not usable in a standard chat interface like you use.

**Framework:** ChatDBG

---

## Demystifying Errors in LLM Reasoning Traces: An Empirical
Study of Code Execution Simulation

**Goal:** Systematically uncover and characterize the errors in reasoning traces

**Test Case:** 427                                                                                          12 input values per snippet

**Notes:** **Not any solutions but a diagnonsis

**Issue:** Lack of
systematic evaluation of reasoning traces leaves open fundamental questions

**Existing Work:** Prior studies have focused on output accuracy and performance comparisons

**Improvement:** Instead of focusing on output diagnosis, they worked on trace reasoning level diagnosis

**Pattern:** Most underrated paper in your set. While every other paper asks "did the output work?", paper 10 asks "where exactly did the model's reasoning go wrong?" This maps precisely to your question of why AI gives wrong answers even when shown example I/O — the error happens in the trace, before output.

**Lacking:** Only diagnosis — no mitigation proposed. Small dataset (427 snippets). Does not test across multiple LLMs to see if reasoning trace errors differ by model — which would directly explain your AI-A-vs-AI-B observation.

---

## TGPR: TREE-GUIDED POLICY REFINEMENT FOR ROBUST
SELF-DEBUGGING OF LLMS

**Goal:** Explores both failed and successful refinement paths actively, with denser training
trajectories and more adaptive policies.

**Issue:** LLM iterative refinement for debugging struggles to efficiently search the large space of possible code fixes

**Existing Work:** Existing methods rely on predefined heuristics that can't adapt based on past refinement outcomes — suffer from the exploration–exploitation dilemma

**Improvement:** TGPR combines GRPO with a Thompson-Sampling-based tree search, actively exploring both failed and successful refinement paths to learn more adaptive debugging policies

**Pattern:** Most technically advanced paper in Cluster B. The pattern with paper 8: DDI detects decay reactively, TGPR prevents it proactively. Together they form a complete picture of the iterative debugging failure problem and two complementary solutions.

**Lacking:** Requires training-time modification — not applicable to off-the-shelf LLMs you use in chat. Does not test on university-level algorithmic problems specifically. High technical complexity makes it difficult to replicate for a thesis.

**Framework:** TGPR (Tree-Guided Policy Refinement)

---

## LEVERAGING PRINT DEBUGGING TO IMPROVE CODE
GENERATION IN LARGE LANGUAGE MODELS

**Goal:** Using print statements to trace and
analyse logs for fixing the bug

**Test Case:** Leetcode Dataset: Easy and Medium

**Issue:** LLMs struggle with code generation for complex data structures and algorithms

**Existing Work:** Standard debugging approaches (like rubber duck debugging) don't give LLMs enough intermediate runtime insight to fix complex logic

**Improvement:** Proposed an in-context learning approach using print debugging — inserting print statements to trace and analyze logs — outperforming rubber duck debugging by 1.5% (easy) and 17.9% (medium) on LeetCode

**Pattern:** Most directly relevant paper to your thesis motivation. LeetCode easy vs medium = similar to your university easy vs hard experience. The 17.9% gap on medium problems shows that intermediate runtime information matters significantly more as problem complexity increases.

**Lacking:** Only tests easy and medium LeetCode — no hard problems. Does not explain WHY print debugging works better (is it the variable values? the execution path?). The improvement disappears if the model cannot correctly interpret the print output — not tested.

**Framework:** Print Debugging

---

## Debug like a Human: A Large Language Model Debugger via Verifying
Runtime Execution Step by Step

**Goal:** LDB debugs code block by block using runtime execution information.

**Issue:** LLMs treat generated programs as indivisible entities during debugging, making it hard to locate errors in complex logic flows

**Existing Work:** Existing approaches rely only on post-execution feedback (pass/fail on test cases) without examining intermediate runtime states

**Improvement:** LDB segments programs into basic blocks, tracks intermediate variable values at runtime step by step, and verifies each block against the task description — improving baseline performance by up to 9.8%

**Pattern:** Converges with papers 9 and 12: all three independently reach the same conclusion — the LLM needs step-by-step runtime information. This convergence from three different teams is strong evidence that runtime access is the key missing capability.

**Lacking:** 9.8% improvement is modest. Does not test on problems where the bug is in the algorithm design itself (not execution logic) — which is common in university-level algorithmic problems. No analysis of failure cases.

**Framework:** LDB (Large Language Model Debugger)

---

## Detecting and Correcting Hallucinations in LLM-Generated Code
via Deterministic AST Analysis

**Goal:** Autocorrecting KCH using deterministic, static analysis framework

**Test Case:** 200 Python Snippets

**Notes:** **KCH = Knowledge Conflcting Hallucination

**Issue:** Knowledge Conflicting Hallucination

**Existing Work:** Constrained decoding or non-deterministic LLM
in-the-loop repair does not work because they operate on output form or plausibility

**Improvement:** Deterministic, static-analysis validates generated code using Abstract Syntax Tree(AST) and  dynamically-generated
Knowledge Base (KB) built via library introspection

**Pattern:** Addresses a very specific hallucination subtype (KCH) that the other Cluster A papers do not. The pattern: as papers get more recent, they narrow their focus from "hallucination in general" (paper 4) to "this specific subtype" (paper 14, 15, 16) — showing the field maturing toward targeted solutions.

**Lacking:** Only targets KCH — useless for logical hallucinations or algorithm design errors, which are more common in your university problem scenario. Python only. 200 samples is small. Does not test whether AST correction improves human-judged correctness.

**Framework:** AST + Knowledge Base framework

---

## Eliminating Hallucination-Induced Errors in LLM
Code Generation with Functional Clustering

**Goal:** Functional Clustering : Generates multiple solutions, groups similar I/O behavior, chooses the most reliable group

**Issue:** Hallucinate subtle bugs

**Existing Work:** Existing confidence methods use proxies (token likelihood, embeddings, self-grading) instead of actual code behavior.

**Improvement:** Generates Multiple solution and test them, then groups them according to identical I/O behavior

**Pattern:** Clever workaround to the verification problem. Instead of detecting hallucination directly, it uses statistical consensus across multiple generations. The pattern with your cross-AI observation: if one model generates 10 solutions and 7 agree, that is the same logic as "AI-B gave the right answer when AI-A didn't" — consensus reveals truth.

**Lacking:** Computationally expensive — requires generating and running multiple solutions. Fails when ALL generations share the same hallucination (which happens on harder algorithmic problems). Does not explain which hallucination types the clustering catches vs misses.

**Framework:** Functional Clustering

---

## Towards Mitigating API Hallucination in Code Generated by
LLMs with Hierarchical Dependency Aware

**Goal:** Mitigates hallucination by analyzing dependency of the project and constraining the AI to relevant API usage

**Issue:** API hallucination

**Existing Work:** RAG does not check dependency and validation of a API

**Improvement:** MARIN check dependency and does Dependency Constrained De
coding

**Pattern:** Narrowest-scope paper in Cluster A. Solves one very specific problem (API hallucination in large projects) extremely well. The pattern with paper 14: both use external knowledge (library introspection / dependency graph) to constrain generation — suggesting that grounding LLMs in verifiable external facts is the most reliable mitigation direction.

**Lacking:** Only relevant if you are working with large codebases with complex dependencies — not university-level homework problems. Cannot help with logic errors or algorithmic thinking errors. Requires project-level setup.

**Framework:** MARIN

---

## Large Language Model Powered Symbolic Execution

**Goal:** Break into subparts using paths, LLM does Symbolic execution to analyze each path

**Notes:** Basically this paper proposes how to analyze programs in small LLMs that originally needed large LLMs

**Issue:** Larger  LLMs are expensive and not accessible to general users

**Existing Work:** Traditional static analysis (symbolic execution, theorem provers, SMT solvers) can't reason over code directly

**Improvement:** AUTOBUG breaks down program analysis into smaller path-based subtasks that smaller LLMs can handle, improving accuracy and scale without needing enterprise hardware.

**Pattern:** Infrastructure paper — enables the findings of other papers to run on accessible hardware. The pattern with paper 10: both are about understanding WHY code fails, not just WHETHER it fails. Together they suggest a growing subfield of LLM-powered program analysis that goes deeper than surface-level correctness.

**Lacking:** Very technically complex — symbolic execution is a formal methods topic. Does not address hallucination directly; addresses analysis cost. Least relevant to your thesis unless you want to build a detection tool that runs on local models.

**Framework:** AutoBug

