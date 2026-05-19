# Execution Playbook

## Blocker Diagnosis

Ask:

1. What were you trying to produce?
2. What did you observe instead?
3. What have you already tried?
4. What hidden assumption would explain all failed attempts?
5. Who has seen this exact failure before?

## Prescriptions by Blocker

### Tool or Environment

- Create a minimal reproducible case.
- Record exact versions, paths, inputs, commands, and outputs.
- Set a hard solo-debugging limit. If no progress in 1-2 days, ask a senior student, maintainer, or collaborator.
- Produce an artifact: error log, minimal script, hardware checklist, data sanity report.

### Wrong Assumption

Symptoms: every parameter change fails; results are unstable; "it should work" is the only evidence.

Actions:

- List 5 assumptions.
- For each, write what you would observe if it were false.
- Test the cheapest assumption first.
- Return to first principles before adding complexity.

### Vague Success Criterion

Symptoms: the user says "finish the experiment" or "write related work" but cannot say how completion will be judged.

Actions:

- Define success in three lines.
- Pick one visible artifact: one plot, one table, one paragraph, one clean run, one decision memo.
- Stop when the artifact answers the intended question.

### Psychological Resistance

Symptoms: the user knows what to do but avoids starting.

Actions:

- Shrink the first step until it requires almost no courage.
- Start with file opening, one command, or one sentence.
- Separate fear of result from difficulty of task.
- If distress is high, use the internal `resilience` module first.

### Collaboration Constraint

Actions:

- Write the dependency explicitly: "I need X from Y by Z to continue."
- Offer a fallback path.
- Put tasks, deadlines, and owners in writing.
- Avoid making the project's critical path depend on an uncontrolled collaborator.

## Weekly Research Loop

Use this at the start of a week:

```text
Main uncertainty this week:
Artifact that will reduce it:
First 4-hour task:
Person to ask if blocked:
Deadline for stop/continue decision:
```

Use this at the end of a day:

```text
Done today:
First task tomorrow:
Blocker / question:
```

## Stop-Loss Rule

Adapted from Pang Tianyu's doctoral reflection:

1. Is the obstacle solvable with the resources available?
2. Is the idea still novel or promising enough to justify more time?
3. What deadline forces a decision?

If the deadline passes without evidence of progress, switch task, subproblem, or direction deliberately rather than drifting.

## Supervisor Update Template

```text
Subject: Weekly update on [project]

Progress:
- [artifact/result]

Issue:
- [specific blocker, not vague frustration]

Options:
- A: [path, cost, risk]
- B: [path, cost, risk]

My recommendation:
- [choice + reason]

Question for you:
- [one decision needed]
```
