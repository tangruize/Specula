---
name: system-proof-protocol-analysis
description: "Use the optional analyze-protocol tool for goal-scoped specification and proof investigations across shared-state operations, lifecycle phases or a supplied call graph. Retain source-linked advisory evidence without treating it as proof or a confirmed bug."
---

# Goal-scoped protocol analysis

This is a caller-facing integration skill, not the analysis worker's runtime method. Read [GUIDE.md](GUIDE.md) for request examples, artifacts, status meanings, prerequisites and terminology. Keep both files together when copying this bundle; it is not automatically installed into the main agent.

## Invocation

Retain the original verification goal, target source anchor, direct caller, observation boundary, assumptions and selected source paths or supplied call graph. Supply existing proof findings as context so repeated observations are distinguishable from new deductions. Report missing inputs or dependencies rather than silently broadening the scope.

Use `analyze-protocol prepare` to capture a fresh input packet, `run` with an explicit timeout for the investigation, and `status` to inspect retained evidence and currentness. These commands are provided by the host's `argus-spec` package. The caller owns the execution budget and any asynchronous scheduling; no FM analysis, TLA generation, tests or proof run is implied.

## Evidence handoff

Retain the run directory, execution outcome, currentness, source/method identity, coverage and unresolved boundaries. For a finding being handed off, retain its premises, source citations, consuming caller, dependencies, proposed discriminating check and remaining proof. A proposed global property can identify its establishing and preserving operations, excluded transitions and lifecycle phase; missing operations remain unknown.

`completed` means a structurally complete advisory report, not verified semantics. Preserve partial, failed, timed-out and stale outcomes explicitly. A source citation or analyst label is not execution evidence; later tests and verifier results need separate records.

The calling agent decides whether to invoke the tool, adopt or reject a candidate, change scope or implementation, or choose the next obligation. Neither this skill nor the report selects the final specification, closes proof-map obligations, repays trust/change debt, or certifies a bug.
