# Protocol analysis for goal-driven system proof

[Simplified Chinese review version](GUIDE.zh-CN.md).

This guide and [SKILL.md](SKILL.md) form a standalone caller-facing bundle. Copy or load this directory when integrating the tool; merely keeping it here does not install it into the main agent. The runtime method remains in the pinned Specula checkout at `skills/protocol_analysis/references/scoped-analysis.md`; the bundle does not replace that method or provide the executable.

`analyze-protocol` performs optional, bounded source analysis across operations and shared-state lifecycles. It produces source-linked candidate contracts, properties and proof obligations. It does not select the campaign's specification, establish proof progress, confirm bugs, or approve an implementation change. Tool choice, scope, interpretation and the next mission remain with the calling agent under the existing campaign contract. FM-Agent is a separate tool, not a mode or prerequisite of this one.

## Inputs and invocation

Retain the original system goal, the caller needing the fact, the relevant observation boundary, and known assumptions or proof gaps. Existing annotations and reports are context, not automatically certified premises. Examples below use placeholder paths/symbols; substitute real source anchors and a budget appropriate to the invocation.

The command is provided by the host's `argus-spec` package, not by Specula's standalone CLI. Its packaged `argus_spec/analysis_request.json` defines the request. A minimal file-scoped example is:

```json
{
  "goal": "THE EXACT ORIGINAL CAMPAIGN GOAL",
  "target": {"symbol": "Registry::restore", "file": "src/registry.rs", "line": 42},
  "direct_caller": "Service::load",
  "observation_boundary": "Entry to restore through return to load, including errors",
  "assumptions": [],
  "scope": {"paths": ["src/registry.rs", "src/service.rs"]},
  "context_files": ["research/current-frontier.md"]
}
```

All selected paths and anchors must exist. Context files are optional. Paths are source-root-relative; explicit files may be untracked, while directory expansion selects Git-tracked files. A file/line anchor does not certify that the named symbol is at that location.

```sh
analyze-protocol prepare request.json --source /path/to/project --out /path/to/new-run \
  --specula-root /path/to/Specula
analyze-protocol run /path/to/new-run --timeout 600
analyze-protocol status /path/to/new-run
```

`prepare` captures inputs and method identity without calling the model. `run` performs analysis only, with an explicit seconds-based timeout. `status` checks retained results and freshness without rerunning analysis. Each new attempt needs a new run directory; the tool does not schedule or retry runs.

Alternatively, `scope.call_graph` accepts `functions`, `calls`, `unresolved`, `roots`, `direction` and `max_depth`; the first three arrays use `proof_map.navigation` records. It selects whole files containing reached functions and retains unresolved/cross-boundary edges. It neither discovers a complete graph nor proves that all relevant writers are included.

Native campaign integration is owned by the host framework: it must bind the exact original goal, authorize source roots, apply action/time budgets and register advisory receipts. Standalone invocations do not automatically register campaign receipts. A host's catalog or dummy response is not evidence that analysis ran; retain the actual backend outcome and artifacts when integrating.

## Evidence produced

| Artifact | What it records |
| --- | --- |
| Protocol `request.json`, `manifest.json`, `work/` | Captured goal, scope, source/method revisions, copied source, actual `prompt.md`, `task.json` and output schema |
| Protocol `report.json` | Structurally accepted complete **or partial** report: findings, citations, premises, consumers, dependencies, suggested checks, coverage and limitations |
| Protocol `status.json` and logs | Execution outcome, elapsed time and raw work; timeout/invalid output may leave only `work/analysis.json` and logs rather than an accepted report |
| Native `analysis` receipt | Campaign linkage, hashes and currentness; exposed through `review-packet.analysis_evidence` |

Protocol output follows the host package's `argus_spec/analysis_response.json`. Its optional `global_property` records state, phase, establishers, preserving operations, consumers, excluded transitions and remaining proof. `candidate`, `requires_restriction`, `not_required` and `contradicted` are the analyst's proposed classifications, not machine-proved judgments.

`run` exits zero only for a current `completed` report. `partial`, `failed`, `invalid`, `timed_out`, `interrupted` and `stale` are non-success outcomes. `prepare` and nonstale prepared/running `status` can also exit zero: exit zero alone does not mean an analysis completed. A native `outcome: passed` means a complete advisory report, not a proved property; this receipt cannot close proof-map edges, repay trust/change debt or count as a core proof attempt.

Coverage and citations are structurally checked, but whether a cited line supports a claim is not. `source_supported` is an analysis label. Report generation does not provide execution evidence for a proposed test or proof. Consuming a finding therefore retains its source identity, premises, scope gaps and proposed check; any later test or verifier result is separate evidence with its own coverage.

## Terms

| Term | Meaning |
| --- | --- |
| Protocol / lifecycle phase | Relations between operations and shared state during a stated interval; not necessarily a network protocol or concurrent execution |
| Direct caller / consumer | Code or a system claim that needs a fact as a premise; not merely another function mentioned in the report |
| Observation boundary | The point or interval at which the promised behavior is evaluated, such as return to the caller rather than internal callback completion |
| Call cone | Nodes reached from chosen graph roots under a direction/depth bound; other shared-state writers may lie outside it |
| Establish / preserve / consume | Create a property, maintain it across a transition, and use it to establish another obligation, respectively |
| Frame | Which relevant observations stay unchanged across an operation; it need not mean equality of every cache or representation field |
| Compensation | A caller's rollback, rejection, discard or other handling that can change the system significance of a local failure |
| Freshness / `current` | Captured inputs and method still match the checked identities; it does not certify semantic truth |

## Runtime boundary

The command is installed by `argus-spec`. It needs Git, Bash, Python and a configured coding-agent backend. Initialize the host repository's pinned `specula` submodule, or supply a clean checkout of `tangruize/Specula` containing the bounded method. Installed wheels need `SPECULA_ROOT` or `--specula-root`. Backend/model configuration remains explicit or inherited, not fixed by this document.

Protocol analysis needs no full `specula setup`, TLA generation, TLC or Verus setup. The caller owns background execution; it need not make this optional analysis a synchronous prerequisite for other proof work. Copied sources and no-edit prompt instructions are not an OS sandbox; permissive adapters can access the host. A source or method change can make an old protocol result stale without erasing its historical artifacts.
