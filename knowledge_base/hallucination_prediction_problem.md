# A Different Problem: Hallucination Prediction
## Can We PREDICT Which Problems Will Cause Hallucination Before the LLM Even Tries?

---

## The Paradigm Shift: Stop Fixing, Start Predicting

Every solution proposed so far — by us AND by all 17 research papers — operates on the same assumption:

> "Let the LLM generate code. Then detect/fix the hallucination."

This is like building better ambulances instead of preventing car crashes.

**The different problem:** What if we could predict WHICH coding problems will cause an LLM to hallucinate BEFORE it even attempts them? If we know in advance that "Problem X has a 92% chance of causing hallucination in GPT-4," we can:

- Route easy/safe problems directly to the LLM (fast, cheap)
- Route risky problems through heavy verification (FLARE, SHADOW)
- Route near-impossible problems to human programmers (honest abstention)

This doesn't just fix code hallucination. This creates a **universal methodology** applicable to ANY domain where LLMs hallucinate — medical, legal, scientific, financial — because the fundamental question is the same: "For this specific input, how likely is the model to hallucinate?"

---

## Why This Is the "World Problem"

Hallucination in code is special because we can **objectively verify** outputs (via execution). No other domain has this luxury. Medicine can't "run" a diagnosis. Law can't "compile" legal advice.

But here's the key insight: **the ability to verify lets us BUILD the training data for a hallucination predictor.** We can:

1. Run 10,000 coding problems through an LLM
2. Execute every output and label it: hallucinated or correct
3. Analyze what FEATURES of the problem predicted hallucination
4. Build a classifier that predicts hallucination from problem features alone

Once we understand WHY hallucination happens in code (where we CAN verify), we can transfer those insights to domains where we CAN'T verify.

**Code becomes the laboratory for understanding hallucination universally.**

---

## The Research Questions

### RQ1: What makes a coding problem hallucination-prone?
Is it the algorithm type? The number of edge cases? The reasoning depth? The similarity to training data? We don't know — and no paper has studied this.

### RQ2: Can we build a predictor?
Given only the problem description (before any code is generated), can a classifier predict whether the LLM will hallucinate? With what accuracy?

### RQ3: Does this transfer across models?
If Problem X causes hallucination in GPT-4, does it also cause hallucination in Claude? In Gemini? Are hallucination-prone problems universal or model-specific?

### RQ4: Can we use prediction to optimize verification?
If we apply heavy verification (FLARE) only to predicted-risky problems, do we get the same accuracy improvement at a fraction of the computational cost?

---

## The Experimental Design

### Phase 1: Build the Hallucination Dataset

```
For each problem in [HumanEval, MBPP, LeetCode Easy/Medium/Hard]:
    For each model in [GPT-4, Claude, Gemini]:
        Generate code (5 attempts per problem)
        Execute against test cases
        Label: HALLUCINATED or CORRECT
        Record: problem features (see below)
```

**Problem features to extract:**
| Feature | What It Measures | How to Compute |
|:---|:---|:---|
| Cyclomatic complexity | How many branching paths | Count if/else/for/while in reference solution |
| Algorithm category | DP, Graph, Greedy, etc. | Problem tags from LeetCode |
| Constraint count | How many edge cases | Count constraints in problem statement |
| Reasoning depth | Steps of logic needed | Count operations in reference solution |
| Input space size | How many possible inputs | Derived from constraints |
| NL ambiguity score | How vague is the problem statement | Measured by LLM or readability metric |
| Training overlap score | How similar to common patterns | Embedding similarity to top-100 LeetCode solutions |

### Phase 2: Train the Hallucination Predictor

A simple classifier (Random Forest, XGBoost, or even logistic regression) that takes problem features as input and predicts P(hallucination).

**Evaluation:** Standard ML metrics — precision, recall, F1, AUC-ROC.

**The publishable finding:** "We found that [feature X] is the strongest predictor of hallucination, accounting for Y% of the variance. Problems with [high cyclomatic complexity + DP category + >3 constraints] have a 87% hallucination rate across all models."

### Phase 3: Deploy the Predictor with FLARE

```
New problem arrives
    ↓
Hallucination Predictor: P(hallucination) = ?
    ↓
If P < 0.2: Direct generation (fast, cheap)
If 0.2 ≤ P < 0.7: FLARE pipeline (self-trace + verification)
If P ≥ 0.7: Heavy verification OR honest abstention
```

**The publishable finding:** "By applying FLARE only to problems with P(hallucination) > 0.2, we achieve 95% of FLARE's accuracy improvement while using only 40% of the API calls."

---

## Why This Solves the "World Problem"

### For Code (Direct Application)
The predictor tells you which problems need extra verification. Apply FLARE/SHADOW only where needed. Save compute and time.

### For Medicine (Transfer Learning)
Once you understand that "high reasoning depth + ambiguous specification → hallucination," you can apply the same principle: medical queries with complex reasoning chains and ambiguous symptoms are high-risk. Route them to human doctors.

### For Law (Transfer Learning)  
Legal questions involving multiple interacting statutes (high "cyclomatic complexity" equivalent) are high-risk. Route them to human lawyers.

### For Science (Transfer Learning)
Scientific claims requiring multi-step logical inference from sparse data are high-risk. Flag them for human review.

**The universal principle:** Hallucination risk increases predictably with reasoning complexity, specification ambiguity, and distance from training distribution. This principle, once proven in code, transfers everywhere.

---

## The Thesis Structure

| Chapter | Content |
|:---|:---|
| 1. Introduction | The AI hallucination crisis across domains |
| 2. Related Work | The 17 papers — what they did and what they missed |
| 3. The Hallucination Prediction Problem | Formal problem definition, why prediction > prevention |
| 4. Dataset Construction | How we built and labeled the hallucination dataset |
| 5. Feature Analysis | Which problem features predict hallucination (RQ1) |
| 6. The Predictor | Classifier design, training, evaluation (RQ2) |
| 7. Cross-Model Analysis | Does hallucination transfer across models? (RQ3) |
| 8. Integrated System | Predictor + FLARE = cost-efficient verification (RQ4) |
| 9. Discussion | Transfer to non-code domains |
| 10. Conclusion | The hallucination boundary is predictable and exploitable |

---

## The One-Sentence Thesis Statement

> "We demonstrate that LLM code hallucination is not random but systematically predictable from problem-level features, and show that a lightweight hallucination predictor can route problems to appropriate verification pipelines, achieving near-zero hallucination rates at a fraction of the computational cost of universal verification — with implications for hallucination prediction across all AI domains."

---

## Why This Is a World-Class Contribution

1. **It's a new PROBLEM, not a new solution.** Every paper tries to fix hallucination. Nobody has tried to PREDICT it. Defining a new problem is the highest form of academic contribution.

2. **It produces a DATASET.** A labeled hallucination dataset with problem features is a standalone contribution that other researchers will cite and use.

3. **It produces INSIGHTS.** "Hallucination correlates most strongly with [X]" is a finding that changes how the entire field thinks about the problem.

4. **It's PRACTICAL.** The predictor saves real compute by routing easy problems away from expensive verification.

5. **It TRANSFERS.** The methodology (not the specific classifier) applies to every domain where AI is used.
