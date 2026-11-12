---
description: Write a Superpowers implementation plan with Claude Opus 5.5 (xhigh)
agent: xm-planner
subagent: false
model: anthropic/claude-opus-5-5#xhigh
---

Write an implementation plan for this approved spec: $ARGUMENTS

Invoking this command approves the selected spec for planning, not implementation.
Use the supplied path, treating a quoted path with spaces as one path. If omitted,
prefer the spec explicitly selected in this conversation, otherwise use a
Markdown spec in `docs/superpowers/specs/` only if exactly one candidate exists.
Name the selected file before planning. If the choice is missing or ambiguous, ask for the
exact path; do not guess or silently substitute for a missing explicit path.

Load `writing-plans` with the skill tool and follow it. Read the complete spec,
applicable repository instructions, and the relevant existing code/docs first.
Use the approved spec as the authority; do not reopen brainstorming unless a
material contradiction prevents planning. Surface such a contradiction to the
user rather than silently changing scope.

Save the plan under `docs/superpowers/plans/` using project naming conventions;
link the spec from it. If an existing plan for this spec is selected, revise that
file rather than creating a competing plan. This agent may edit only Markdown
plans in that directory. If project instructions require another destination,
explain the restriction and request a project-local permission override; do not
write elsewhere through another tool. Shell commands and subagent delegation are
disabled. Use read/glob/grep and documentation tools for research.

Include acceptance criteria, exact interfaces and dependencies, meaningful tests,
and runnable verification commands. Carry forward the spec's invariants; where
relevant include actor independence, virtual-time causality, deterministic replay
and hidden-evaluation separation. Keep financial/domain assumptions sourced or
explicitly identified as decisions, not invented facts.

Self-review using `writing-plans`. Link the saved plan and stop for user review.
Suggest `/xm-plan-review <exact-plan-path>` and `/xm-plan-simplify <exact-plan-path>`
against the same unchanged draft; wait for BOTH reports before revising once.
The reports must name the same plan path and content hash. If their hashes differ
or either reports that its input changed, do not combine them as a review of one
revision: rerun the stale review on the current draft first.
The commands are opt-in: do not dispatch them or advance to execution yourself.
Do not run tests, write implementation files, create worktrees, or make commits.
After the user approves the revised plan, execution belongs in a new Build
session on GPT-6 Astra with the plan and spec paths.
