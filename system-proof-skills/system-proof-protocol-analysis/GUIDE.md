# Protocol analysis for goal-driven system proof

[Simplified Chinese review version](GUIDE.zh-CN.md).

This guide and [SKILL.md](SKILL.md) form a standalone caller-facing bundle. Copy or load this directory when integrating the tool; merely keeping it here does not install it into the main agent. The runtime method remains in the pinned Specula checkout at `skills/protocol_analysis/references/scoped-analysis.md`; the bundle does not replace that method or provide the executable.

`analyze-protocol` performs optional, bounded source analysis across operations and shared-state lifecycles. It produces source-linked candidate contracts, properties and proof obligations. It does not select the campaign's specification, establish proof progress, confirm bugs, or approve an implementation change. Tool choice, scope, interpretation and the next mission remain with the calling agent under the existing campaign contract. FM-Agent is a separate tool, not a mode or prerequisite of this one.

The analysis is performed by an agent, not a deterministic semantic oracle. Observations, hypotheses, candidate obligations and suggested checks are evidence to review, with possible mistakes and incomplete coverage. Their quality depends on the question, supplied context, scope and execution; no particular discovery or improvement is promised, and recommendations do not authorize a decision or action.

## Possible contributions to a system-proof task

The useful output is a source-linked premise or obligation that can be connected to the system goal, not simply a longer list of invariants. The following lessons come from the paired HFS/OpenVMM experiments and their follow-up review; they explain possible uses, not decisions prescribed for a new target.

| Need in the proof task | Historical observation | Possible contribution and evidence limit |
| --- | --- | --- |
| Relate a contract to the actual consumer | HFS protocol analysis made the resolver/validator record relation and selected-slot witness more concrete | Name the relation needed from open to read, its establishing operation and intervening mutators. Much of the gap was already in the supplied frontier; this was refinement, not independent recovery of the specification. |
| Avoid an unnecessary or false global invariant | HFS's whole-map restore frame did not require global identity uniqueness. A protocol recommendation to equate unchanged legacy content with operational bytes was rejected: the gap control gave 512 versus 1024 bytes. | Ask whether a property is needed, needs a restricted domain, or conflicts with evidence. The unnecessary strengthening was already known; the false recommendation shows that the report cannot decide correctness by itself. |
| Find the missing connection from local proofs to the top-level claim | OpenVMM protocol analysis identified different decoder/representation predicates at `InitializedVm::load -> restore_snapshot_state` | Identify a concrete call-site bridge for inventory and VP count. A later runtime check cannot justify an entry precondition. This located a proof obligation; it did not prove it. |
| Turn a lifecycle hypothesis into a discriminating check | Following an FM hypothesis, source review and separate native HFS tests showed that closing a handle against another volume can free a slot while that volume's original handle remains live | Distinguish an origin-volume/client discipline from an unrestricted API guarantee. Neither raw analysis report reproduced this trace; test design and execution were separate follow-up work. The fixtures did not prove mount reachability or all Verus premises. |

The protocol runs took 225.481 seconds for HFS (partial) and 205.861 seconds for OpenVMM (structurally completed). These are single historical observations, excluding intake and follow-up checks, not latency guarantees. The separate HFS native run passed 25 tests, including four new diagnostics, in 13.12 seconds including a fresh build. Some OpenVMM report citations were in range but pointed to the wrong definitions, requiring source review.

These experiments support an optional premise/obligation review, not a unique ability unavailable to FM, superiority at equal scope, autonomous bug confirmation or newly completed proofs. The protocol runs had broader source access than the function baseline; existing findings were supplied as context. Preserve that distinction when assessing novelty.

The host repository retains the evidence in `experiments/protocol-analysis/REPORT.md`, `experiments/protocol-analysis/results.json` and `experiments/protocol-analysis/hfs-lifecycle.tests.rs`. These are historical records, not current-method receipts; they are not bundled with a standalone Specula checkout.

## Request fields and scope

The minimal request and invocation are in [SKILL.md](SKILL.md). The command is provided by the host's `argus-spec` package, not Specula's standalone CLI. Its packaged `argus_spec/analysis_request.json` defines the exact request:

| Field | Requirement and meaning |
| --- | --- |
| `goal` | Required; preserve the exact original campaign goal |
| `target` | Required object with `symbol`, `file`, `line`; use an existing source file and an in-range, one-based line |
| `direct_caller` | Required; the immediate caller needing the result |
| `observation_boundary` | Required; the point or interval at which the promised behavior is evaluated, including relevant failures |
| `assumptions` | Required array; use an empty array if none are supplied |
| `scope` | Required; choose exactly one of `paths` or `call_graph` |
| `context_files` | Optional source-relative files containing the focused question, prior findings, candidate contracts or proof gaps; these are context, not certified premises |
| `history_limit` | Optional nonnegative integer, default zero; captures at most this many scoped commit messages, not full diffs or remote issue history |

All selected paths and anchors must exist. Paths are source-root-relative; explicit files may be untracked, while directory expansion selects Git-tracked files. A file/line anchor does not certify that the named symbol is at that location.

`scope.call_graph` accepts `functions`, `calls`, `unresolved`, `roots`, `direction` and `max_depth`; the first three arrays use `proof_map.navigation` records. Roots are function IDs; direction is `callees`, `callers` or `both`; depth is a nonnegative integer or `null` for unrestricted reachability. It selects whole files containing reached functions and retains unresolved/cross-boundary edges. It neither discovers a complete graph nor proves that all relevant writers are included.

## Execution options and incomplete runs

| Command | Parameters and behavior |
| --- | --- |
| `prepare` | Request file plus required `--source` and `--out`; optional `--specula-root`. Captures input/method identity without calling the model. The output directory must be new. |
| `run` | Prepared directory and required positive-integer `--timeout` in seconds. Optional `--agent` selects `copilot-cli` (default), `codex` or `claude-code`; optional `--model` and `--effort` otherwise retain backend defaults. |
| `status` | Run directory; inspects retained results and freshness without rerunning analysis |

Each new attempt needs a new run directory; the tool does not schedule or retry runs. Timeout terminates the invocation's process group and retains partial artifacts. Preserve the outcome and missing coverage before deciding whether another bounded attempt is useful. A source or method change can leave the historical status as completed while `current` becomes false; inspect both fields.

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
