---
name: system-proof-protocol-analysis
description: "Use analyze-protocol when a system-proof task needs a cross-operation premise audit, an invariant's necessary scope, a missing caller-to-callee proof bridge, or a lifecycle bug hypothesis checked against bounded source. Produces advisory evidence, not proofs or confirmed bugs."
---

# Goal-scoped protocol analysis

The tool itself runs an agent. Its observations, hypotheses and candidate obligations/checks are analysis evidence for review, not decisions, verified facts or guaranteed discoveries.

The native system-proof adapter uses the authenticated Copilot CLI and the pinned Specula submodule automatically. It does not require API keys, MCP setup, TLA generation or `specula setup`. Do not enter the full Specula pipeline unless a separate mission explicitly requests modeling or model checking.

Use `analyze-function` instead when one direct caller is blocked on one function or selected callee. Use `analyze-protocol` when the needed premise spans multiple operations, writers, lifecycle phases, callbacks or compensating failure paths. Neither tool is mandatory before the other.

## When to use

Consider this optional analysis when the current system goal raises one of these questions:

- A contract relies on shared state across operations: which constructor, owner or earlier call establishes the premise, and which intervening operations preserve or invalidate it?
- An invariant's role or scope is unclear: what property does the caller need, over which objects and phases, and what evidence supports or challenges it?
- Local proofs exist but the top-level claim remains disconnected: which concrete caller-to-callee representation or precondition bridge is still missing?
- A suspected violation depends on operation ordering, state transitions or failure handling: what source-supported sequence and cheap discriminating check could distinguish a real violation from a permitted effect or caller compensation?

These are general question patterns, not system-specific requirements or a guarantee of a new finding. This is not a compiler, prover or bug-confirmation runner, and it is not required on every proof iteration or in a fixed order with other analysis tools. The calling agent chooses whether the question warrants a bounded, potentially multi-minute investigation.

## Before invoking

The host must provide `analyze-protocol` from `argus-spec`, a configured coding-agent backend and the pinned Specula checkout. Retain the original goal, a real target symbol/file/line, direct caller, observation boundary, assumptions and bounded source scope. Put the focused question, current proof frontier and known findings in source-relative `context_files` when available; do not replace the original goal with a narrower question. Report missing inputs or dependencies instead of silently broadening scope.

## Basic use

Create `request.json`, replacing the placeholders with the actual goal and source anchors:

```json
{
  "goal": "THE EXACT ORIGINAL CAMPAIGN GOAL",
  "target": {"symbol": "Component::apply", "file": "src/component.rs", "line": 42},
  "direct_caller": "Service::execute",
  "observation_boundary": "Entry to apply through return to execute, including errors",
  "assumptions": [],
  "scope": {"paths": ["src/component.rs", "src/service.rs"]}
}
```

Inside a campaign, save the request as a project-relative file and use the native catalog adapter:

```sh
system-proof --root /path/to/project tools run analyze-protocol \
  --request protocol-request.json --backend native
```

For standalone reproduction, prepare a new run directory, run only after preparation succeeds, then inspect the result even if the run exits nonzero:

```sh
analyze-protocol prepare request.json --source /path/to/project --out /path/to/new-run \
  --specula-root /path/to/Specula
analyze-protocol run /path/to/new-run --timeout 600
analyze-protocol status /path/to/new-run
```

`prepare` captures inputs without a model call. `run` performs analysis only; the example timeout is in seconds, not a promised runtime. `status` checks retained evidence without rerunning. Each new attempt needs a new directory; the caller owns the budget and any background scheduling.

## Read and hand off the result

Inspect both `status` and `current`, not just the exit code. A current `completed` report is structurally complete, not proved. Preserve partial, failed, timed-out and stale outcomes; do not silently retry or label them successful.

Retain the run directory, source/method identity, coverage and unresolved boundaries. If available, read `report.json` and hand off relevant findings with their premises, source citations, consuming caller, dependencies, proposed check and remaining proof. Otherwise retain the status and available logs/raw output. Suggested tests and proofs are not execution evidence; any follow-up check needs its own record.

The calling agent decides whether to invoke the tool, adopt or reject a candidate, change scope or implementation, or choose the next obligation. Neither this skill nor the report selects the final specification, closes proof-map obligations, repays trust/change debt, or certifies a bug.

See [GUIDE.md](GUIDE.md) for detailed parameters, output artifacts, terminology and historical evidence.
