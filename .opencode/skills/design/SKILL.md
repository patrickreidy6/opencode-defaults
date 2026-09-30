---
name: design
description: Collaboratively clarify requirements and produce proportionate plans for project kickoff, feature design, or smaller tasks, especially in OpenCode Plan mode. Use when the user wants a planning conversation; not for purely informational requests or implementation-only work with an agreed plan.
license: MIT
---

# Design

Help me plan this project or task. Ask questions whose answers materially affect scope, design, or success criteria, and give your recommendation with each question. Ask dependent questions sequentially and use your judgment for routine details. Once we agree, produce a plan proportional to the task, including acceptance criteria and verification.

## 1. Ground the conversation

- Read relevant project instructions, existing briefs and plans, and enough code to understand the current state. Investigate facts the environment can answer before asking the user.
- Inherit settled project decisions. Reopen one only when the request changes it or evidence reveals a conflict; explain the reason.
- Identify the intended outcome, who benefits, the scope, and what success means. Separate confirmed facts and choices from assumptions and unresolved decisions.
- Match the planning depth to the work. A feature within an existing project should start from that project's context rather than repeat its kickoff interview.

## 2. Resolve consequential decisions

- Ask the highest-impact unresolved question whose prerequisites are known. Use OpenCode's `question` tool when available.
- Give a recommended answer and brief rationale with each question. Offer alternatives when they represent meaningful tradeoffs and leave room for the user's own answer.
- Wait for answers before asking dependent questions. Group a few independent questions only when that makes responding easier.
- Use judgment for routine, reversible details. Honor "you decide" by choosing and briefly recording the recommendation; ask only if a necessary constraint remains missing.
- Investigate technical unknowns directly. If one cannot be resolved yet, make it an explicit assumption or a scoped discovery step with a decision criterion.
- Stop interviewing when remaining uncertainty can be handled by stated assumptions or discovery steps and the goal, scope, consequential choices, and acceptance criteria are clear. Aim for enough agreement to plan, rather than exhaustive questioning.

## 3. Agree on the approach

- Summarize the intended outcome, scope and non-goals, key constraints, and proposed approach concisely. Compare alternatives only where the choice matters.
- Invite correction on unresolved choices. Treat a clear "sounds good" or equivalent as agreement to what was presented; use agreement already given rather than asking for it again.
- Carry the agreed decisions into the plan. Scale up if new complexity materially changes scope, explaining what needs another decision.

## 4. Produce a proportionate plan

| Scope | Example request | Output |
| --- | --- | --- |
| Project kickoff | "Help me plan a new hotel research tool." | Project brief, key architecture decisions, phased plan, and concise `AGENTS.md` draft. Combine the brief and plan when separate documents add little value. |
| Feature or subsystem | "Plan price alerts within the existing tool." | Focused implementation plan referencing the project's settled decisions and relevant parent plan. |
| Small task | "Plan adding a sort option to this table." | Short in-chat plan with acceptance criteria and verification. |

Include only the detail needed to make the work actionable:
- Goal, scope, relevant constraints, and important decisions with their rationale.
- Ordered steps or independently verifiable slices; dependencies and likely files or interfaces when useful and grounded in the repo.
- Observable acceptance criteria and appropriate verification for the change: focused tests, output inspection, or a manual check.
- Open questions, consequential assumptions, or discovery steps that could change the plan.

Use existing documentation conventions. Otherwise propose `docs/plans/<topic>.md` for a durable plan. Preserve existing work: revise the same plan when requested, and keep unrelated or incomplete plans intact. Small tasks can stay in chat unless persistence is requested.

## 5. Draft durable project instructions

At kickoff, draft a concise `AGENTS.md`; for later tasks, propose updates only when durable project guidance changes.
- Capture established commands, conventions, architectural constraints, setup quirks, and operational gotchas that future sessions need.
- Ground commands and paths in the repository. In an empty project, distinguish agreed future structure from existing tooling and mark proposed commands as unverified.
- Keep temporary task lists and progress in the plan. Link to project briefs or detailed guidance with a clear condition for reading them.
- Preserve existing instructions and resolve material conflicts with the user. OpenCode's `/init` can help populate or refresh repository-specific facts when writing is permitted.

## 6. Respect mode and handoff

- In Plan mode, investigate and present drafts in chat, or use a designated plan artifact only when the harness explicitly permits it. A skill never grants additional write permissions.
- Once documents are approved, save them only when requested or authorized and the active mode permits it. Otherwise identify the Build-mode handoff needed to save them.
- Finish with the plan, any intended artifacts, and the next step. Plan approval alone does not authorize implementation or commits; follow the user's explicit execution request separately.

## Completion check

Before handing off, confirm that the plan reflects the agreed intent, reuses relevant project decisions, orders dependencies sensibly, and includes observable acceptance criteria and verification. Surface unresolved consequential assumptions, distinguish draft artifacts from saved files, and keep the output proportional to the task.

## Attribution

Question sequencing and the distinction between investigating facts and asking for decisions are adapted from Matt Pocock's [grilling skill](https://github.com/mattpocock/skills/blob/85f83d3fde1d3a90d5c9a657f6998c79a6c37308/skills/productivity/grilling/SKILL.md). This adaptation adds proportional planning, project instructions, and OpenCode mode-aware handoffs. Upstream copyright and MIT terms are preserved in [LICENSE](LICENSE).
