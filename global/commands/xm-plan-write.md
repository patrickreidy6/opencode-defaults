---
description: Write a focused Superpowers plan with Claude Opus 5.5 (xhigh)
agent: xm-planner
subagent: false
model: anthropic/claude-opus-5-5#xhigh
---

Write the simplest reliable implementation plan for this approved spec: $ARGUMENTS

Invoking this command approves the selected spec for planning, not implementation.
Use the supplied path, treating a quoted path with spaces as one path. If omitted,
prefer the spec most recently explicitly selected in this conversation, otherwise use a
Markdown spec in `docs/superpowers/specs/` only if exactly one candidate exists.
Name the selected file before planning. If the choice is missing or ambiguous,
ask for the exact path; do not guess or substitute for a missing explicit path.

Load `writing-plans` for its structure and coverage checks. The scope, detail and
handoff instructions below take precedence over its generic template and workflow.
Read the complete spec, applicable repository instructions and relevant code/docs.
Look for existing capabilities to reuse before proposing new components.

The approved spec is the authority, including its non-goals, exclusions and
deferrals. It supersedes earlier conversation where choices were rejected or
changed. Preserve that scope. Any new component, dependency, stored field,
configuration option or abstraction needs a concrete implementation necessity
tied to an approved requirement; explain consequential additions briefly.

Make ordinary technical choices yourself. Ask a focused question with a
recommendation only when an unresolved decision or contradiction materially
changes behavior, scope or a significant tradeoff. Continue independent planning
where possible, and mark anything dependent on the answer as unresolved. Do not
restart brainstorming or silently change the spec. Distinguish supported facts,
user-approved domain decisions, your implementation choices and open questions.

Write for a capable Astra executor starting in a fresh session:
- Carry forward the approved acceptance criteria, domain constraints and invariants.
- Use cohesive tasks with clear outcomes, affected files and task dependencies.
  Group supporting setup, documentation and verification with the work they serve.
- Specify existing integration points and shared contracts precisely enough for
  separate tasks to agree. Leave routine internal structure, helper names and
  function bodies to the executor unless a particular choice is essential.
- Plan checks for required behavior and consequential failure cases, using the
  project's existing tools. State expected results and runnable commands; these
  are planned checks, not evidence that tests have passed.
- Include code only where it resolves material ambiguity. Do not require full test
  implementations, a fixed number of review-focus cases, or a repeated
  test/implementation/commit sequence for every small step. Keep detail and testing
  proportional to the work and failure impact.

Save the plan under `docs/superpowers/plans/` using project naming conventions;
link the spec from it. If an existing plan for this spec is selected, revise that
file rather than creating a competing plan. This agent may edit only Markdown
plans in that directory. If project instructions require another destination,
explain the restriction and request a project-local permission override; do not
write elsewhere through another tool. Shell commands and subagent delegation are
disabled. Use read/glob/grep and documentation tools for research. Do not run tests,
write implementation files, create worktrees or make commits.

Do one focused self-review for spec coverage, contract consistency and proportion;
correct any issues found. Link the saved plan, summarize its approach, major tasks
and consequential choices, and stop for user review.

Suggest `/xm-plan-review` and `/xm-plan-simplify` with the exact saved plan path.
These reviews are opt-in. If both are requested, keep the plan and linked spec
unchanged until both reports arrive. Confirm matching plan AND spec paths and
content hashes before reconciling them together. If the inputs differ or a report
says they changed, ask the user to rerun the stale review on the current draft.
If only one review is requested, do not wait for an unrequested companion.
Do not dispatch reviews or advance to execution yourself. After the user approves
the plan, execution belongs in a new Build session on GPT-6 Astra with both the
plan and spec paths. Use this handoff instead of the skill's execution-method menu.
