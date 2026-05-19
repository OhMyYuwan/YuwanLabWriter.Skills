# Ideation Framework

## Problem Types

- **Topic**: a domain, method, dataset, or task. Example: "LLM agents", "graph neural networks", "medical image segmentation".
- **Practical problem**: a real-world failure or need. Example: "the system is too slow", "diagnosis is inaccurate".
- **Scientific problem**: a specific unknown mechanism, boundary, contradiction, or principle. Example: "why does method X fail under condition Y even when benchmark accuracy is high?"
- **Technical route**: how one might solve a problem. Example: "use deep learning", "build a simulation".
- **False problem**: background, significance, method fashion, or engineering route disguised as the research question.

Hu Xiaofeng's five common false problems:

1. Treating research significance as the problem.
2. Treating broad background as the problem.
3. Confusing practical problems with scientific problems.
4. Treating "how to do it" as the problem itself.
5. Starting from a method and searching for a target.

## Six Idea Routes

### 1. Fill a Blank

Build a table of objects, assumptions, methods, datasets, constraints, and evidence types. Blank cells are possible ideas. The table is useful only when the dimensions come from real papers, not imagination.

Prompt: "What dimensions do the last 10 papers vary on, and which combination has not been studied?"

### 2. Extend a Boundary

Start from a known result and relax one assumption: new data regime, system condition, metric, user group, threat model, or causal setting.

Prompt: "What condition did the original paper quietly assume, and what happens when that condition breaks?"

### 3. Follow a Surprising Phenomenon

A small anomaly becomes research-worthy when it is surprising, reproducible, and points to a broader mechanism. Zhiyun Qian's Android ION example follows this pattern: a local observation led to a deeper memory-management exposure.

Prompt: "What did you observe that current theory or common practice does not predict?"

### 4. Use a Rare Tool Responsibly

Tool-first ideas are weak when the tool is fashionable but strong when the tool opens a problem space others cannot access: unusual data, instrumentation, program analysis infrastructure, long-term measurement, or a hard-won experimental setup.

Prompt: "What can this tool reveal that was previously unobservable?"

### 5. Re-derive From First Principles

Huo Qiang's useful order is why -> problem -> method. Ask what the field is actually trying to understand, then use the Passion / Excellence / Impact overlap to decide whether it is a long-term agenda.

Prompt: "If we forgot the dominant method for one hour, what would the question become?"

### 6. Recover Negative Results

Failed replication, weaker-than-expected effects, and contradictory baselines can become ideas if the gap is systematic and explainable.

Prompt: "What did not work, and what does that failure teach about the problem space?"

## Four-Lens Pressure Test

| Lens | Question | Warning sign |
|---|---|---|
| Importance | Who will care if this is answered? | Only your current implementation changes. |
| Feasibility | Can you obtain evidence in 3 months? | Requires resources you do not control. |
| Differentiation | What is new relative to the last 12 months? | You need more than 3 sentences to explain the difference. |
| Publishability | Which venue/community would understand and value it? | No clear audience or evaluation norm. |

## Output Formats

Use one of these when helping the user:

```text
Problem statement:
Known:
Unknown:
Hypothesis:
Evidence needed in 3 months:
Closest related work:
Risk:
```

```text
Dimension table:
Rows = object/scenario/data/assumption
Columns = method/evidence/metric/constraint
Blank or contradictory cells = candidate ideas
```

