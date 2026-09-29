# Goal-scoped protocol analysis for proof agents

This fork adds an optional `protocol-analysis` skill. It adapts Specula's pre-TLA source investigation to an existing verification goal. It is not a new phase of `specula run`, does not replace the original `code-analysis` skill, and does not automatically generate TLA+, run verification/tests, or confirm bugs.

The canonical method is [scoped-analysis.md](../skills/protocol_analysis/references/scoped-analysis.md). Consumers must load this file from their pinned checkout, not a machine-local modified copy. The existing `deep-analysis.md`, `concurrent-analysis.md` and `distributed-analysis.md` in `skills/code_analysis/references/` supply analysis patterns; the bounded method takes precedence over their full-pipeline or exhaustive-investigation recommendations.

## Integration boundary

This repository owns the portable method and the existing agent launch adapters. The calling proof framework owns its public CLI, request/report schemas, source/call-graph selection, process timeout, provenance/freshness checking, and proof-map or budget policy. The Argus integration exposes `analyze-protocol prepare/run/status`; that command belongs to `argus-spec`, not the standalone Specula CLI.

For this method, a Git checkout plus the dependencies of the selected launch adapter is sufficient; do not run `specula setup` or recursively initialize research submodules merely to obtain these files. The Copilot adapter needs Bash, Python 3 and an installed/authenticated Copilot CLI. Other adapters retain their own prerequisites. The adapter's permissive execution flags are not an operating-system sandbox: use separate host isolation for untrusted inputs.

Obtain this fork's adaptation without changing its default branch:

```sh
git clone --branch proof-agent-analysis --single-branch \
  https://github.com/tangruize/specula.git
```

For a submodule consumer, record an exact commit in the parent gitlink and the fork URL in `.gitmodules`. The optional `branch = proof-agent-analysis` setting guides explicit remote updates; ordinary `git submodule update --init -- specula` must use the parent's exact commit, not whichever commit happens to be latest on a branch.

## Prepared workspace

The caller creates a fresh workspace with:

| Path | Contract |
| --- | --- |
| `task.json` | Original goal, target symbol/file/line, direct caller, observation boundary, assumptions, selected source files and any supplied graph boundaries |
| `response-schema.json` | The caller's exact output schema, including coverage, advisory findings and limitations |
| `source/` | Read-only-in-intent source and context snapshot, retaining original relative paths and line numbers |
| `history.txt` | Explicitly supplied scoped history, or an explicit statement that none was requested |
| `method/` | Copies of the bounded method and relevant code-analysis references from the pinned checkout |
| `prompt.md` | The bounded method text, with any caller-specific task instructions |

Run one supported adapter with this directory as its working directory and an explicit caller-owned timeout. An adapter can consume `--prompt-file=/absolute/path/to/prompt.md` and `--log=/absolute/path/to/agent.log`; model/effort options remain optional. This document does not introduce a scheduler, retry loop, or mandatory analysis stage.

The agent writes `analysis.json` and optionally `analysis.md`. Require the exact original goal, actual files read, unfinished work and unresolved boundaries, and findings with precise premises, source citations, a consuming caller, compensation analysis, dependencies and a cheapest decisive next check. Schema validity, in-range citations and report completion do not establish semantic truth or prove that citations support their claims.

## What the method changes

The analysis challenges shared-state and lifecycle premises instead of automatically strengthening invariants. A cross-component finding can include a `global_property` record with `state`, `phase`, `established_by`, `preserved_by`, `consumed_by`, `excluded_transitions`, `disposition`, and `remaining_proof`. Its disposition distinguishes `candidate`, `requires_restriction`, `not_required`, and `contradicted`; none is a proof result.

Inspect constructors, writers, callbacks, error/cancellation exits and consumers within the supplied scope. A call graph is navigation, not closure over every shared-state writer. Missing transitions remain explicit unknowns. Prefer the weakest observable relation needed by the caller rather than equality of caches, handles or every representation field.

When supplied with an existing proof frontier, separate known findings from new deductions. Rank next obligations by what they enable at the original caller, not by easy leaf proofs or aggregate verifier counts. A useful candidate names its exact premises, consumer and remaining proof; a useful rejection explains why a stronger global property is unnecessary or contradicted.

Save partial results early. Missing dependencies or unfinished investigation must remain partial rather than become success-shaped output. Stop after the report: source changes, frozen-spec decisions, executable discriminators and proof attempts belong to the caller's separately authorized next step.
