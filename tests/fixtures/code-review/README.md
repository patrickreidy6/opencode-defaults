# Code review evaluation fixtures

Build six small, dependency-free Git repositories for a paired comparison of the
old and revised `/xm-code-review` prompts. These cases test review precision as
well as bug detection; they are a smoke test, not a model benchmark.

From the repository root, choose a **new** directory in temporary storage:

```powershell
uv run --no-project python tests/fixtures/code-review/build.py "$env:TEMP/code-review-comparison"
```

```sh
python3 tests/fixtures/code-review/build.py "${TMPDIR:-/tmp}/code-review-comparison"
```

The builder refuses existing destinations and destinations inside this source
repository. It creates `case-01` through `case-06`, runs their tests and private
behavior probes, checks Git state, and writes the evaluator's `manifest.json`
**beside**, not inside, the six repositories. Each repository contains its
approved requirements at `docs/specs/change-design.md`. Case names, commit
messages, and repository files do not identify the expected review outcome.
Commit dates are fixed synthetic values, so independently built sets have the
same base and HEAD hashes. The manifest records final source SHA-256 hashes and
the command, Python version, and output of the real test run. An evaluator may
provide those fields as test evidence without exposing the private probe or
expected-finding fields.

| Case | Behavior under evaluation | Expected defects |
|---|---|---|
| 01 | Correct aggregation with repeated and empty inputs | None |
| 02 | Intentionally excluded Unicode/normalization support | None |
| 03 | Empty input handled by the public caller; finite inputs can overflow an intermediate sum | One arithmetic-overflow defect; no empty-input finding |
| 04 | Existing boundary bug unaffected by a receipt-format change | None against this change |
| 05 | Committed and staged defects fixed in the final working tree, using an untracked helper | None |
| 06 | Catalog changes cents to dollars while payment code still expects cents | One unit-conversion regression |

All repository tests pass in the final state. Case 06 deliberately lacks a test
for the broken cross-file path. The private probe demonstrates 750 cents in the
base becoming 7 in the final state; case 04 confirms its boundary defect is
already present in the base. Case 05 confirms that HEAD returns 1480 while the
final tree correctly returns 1200. This distinguishes observed behavior from an
evaluator's assumption about the code.

Live evaluation also identified a legitimate numeric defect in case 03:
`summarize([1e308, 1e308])` returns infinity even though its mathematical mean,
`1e308`, is representable. The input contract permits these finite values. A
private probe verifies that result and the representable mean computed by
dividing before summing. Accept Minor or Important severity for this finding.
The original empty-input check still tests false-positive filtering; rejecting
that false alarm must not suppress the distinct overflow defect. Only private
expectations and probes changed after this discovery: the model-visible source,
tests, requirements, commit dates, and case names remain unchanged.

For each prompt, build a separate fixture set and use fresh reviewer sessions
with the same model, effort and permissions. Install the respective command in
each case's ignored `.opencode` directory. Pass only the spec path and
`base_sha` from the manifest to the command; do not give the reviewer this file,
the builder, manifest, expected categories, or private probe results. Keep
evaluator output outside each case repository, and deny reviewer access outside
that repository when the runtime supports it. Directory separation alone is not
an access-control boundary.

Afterward, compare each report against the private manifest. Record detected
expected defects, missed defects, unsupported material findings, unnecessary
scope additions, verdict, cost, and elapsed time. Count duplicate reports of one
root cause once. A clearly separated historical observation in case 04 is not a
false positive unless treated as a defect introduced/worsened by this change or
used to block it. Unexpected findings require human adjudication against the
code, not automatic rejection because they are absent from the manifest.

Retain both raw reports and the adjudication. Check that reviewer sessions left
the repositories unchanged. Neither keyword matching nor successful installation
establishes review quality; rerun selected cases after material prompt or model
changes, and add cases from real misses or false alarms.

The [2026-11-12 evaluation results](results-2026-11-12.json) retain the original,
first-revision and final-refinement prompts, raw reports, session IDs, timings,
costs and adjudications. The [design record](../../../docs/specs/cross-model-workflow-design.md#code-review-verification-and-scope)
explains the observed false rejections, numerical-boundary refinement and scoped
Surface installation. These results are evaluator material; never copy them
into a repository being reviewed.
