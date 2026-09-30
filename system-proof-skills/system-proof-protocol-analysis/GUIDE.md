# Protocol analysis for goal-driven system proof

`analyze-protocol` performs optional, bounded source analysis across operations and shared-state lifecycles. It produces source-linked candidate contracts, properties and proof obligations. It does not select the campaign's specification, establish proof progress, confirm bugs, or approve an implementation change. Tool choice, scope, interpretation and the next mission remain with the calling agent under the existing campaign contract.

The analysis is performed by an agent, not a deterministic semantic oracle. Observations, hypotheses, candidate obligations and suggested checks are evidence to review, with possible mistakes and incomplete coverage. Their quality depends on the question, supplied context, scope and execution; no particular discovery or improvement is promised, and recommendations do not authorize a decision or action.

## Choosing between FM function analysis and protocol analysis

Use the narrowest method that matches the blocking question:

| Blocking question | Prefer | Boundary |
| --- | --- | --- |
| What does one function or selected callee promise to its direct caller? | `analyze-function` | One source span, contract variants, frame conditions and a selected child obligation |
| Which operation establishes a shared-state premise, which transitions preserve or invalidate it, and which caller consumes it? | `analyze-protocol` | A bounded set of operations/files and an explicit lifecycle or observation interval |
| Does a proposed global invariant need a narrower domain, phase or object set? | `analyze-protocol` | Candidate scope and counter-scenarios, not an invariant proof |
| Did a protocol report reduce the problem to one callee contract? | Return to `analyze-function` or direct proof | The handoff must name the exact caller fact and remaining authoritative check |

There is no mandatory order and no reason to invoke both tools by default. FM analysis may expose a shared-state premise that deserves protocol review; protocol analysis may localize a gap to one function. Tool transitions are justified by the active proof obligation, not by a fixed pipeline.

## Contributions to specification judgment

Useful protocol output can:

- propose materially different lifecycle or invariant candidates, including a weaker observable relation;
- identify a missing establisher, unexamined writer, cancellation/error transition or caller compensation;
- classify a proposed global property as a candidate, requiring restriction, not required by the goal, or contradicted by bounded source evidence;
- connect a local contract to the operation and caller that establish and consume it;
- give a concrete sequence, source audit, component test, implementation proof or model check that discriminates between candidates.

These are inputs to specification attack and reasoning, not an adequacy oracle. A report may repeat supplied context, cite the wrong definition, omit an out-of-scope writer or recommend a false strengthening. The calling agent must distinguish prior findings from new deductions and use independent evidence before changing authoritative status.

Real-system runs are compatibility and information-value evidence only. Their findings, runtimes and project-specific names must not become default prompt rules or claims of superiority over FM-Agent.

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
| `run` | Prepared directory and required positive-integer `--timeout` in seconds. The native system-proof adapter uses authenticated `copilot-cli`; optional `model` and `effort` overrides otherwise retain the Copilot CLI default. Standalone Specula retains its other adapters. |
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

Execution requires Git, Bash, Python, an authenticated Copilot CLI and a clean, pinned Specula checkout containing the bounded method. The native system-proof adapter resolves its relocated submodule automatically and does not require `SPECULA_ROOT`, an API key, MCP setup or another provider. Standalone invocation may still use `SPECULA_ROOT`, `--specula-root` and the other adapters documented by Specula.

Protocol analysis does not require TLA generation, TLC or Verus. The caller owns background execution; it need not make this optional analysis a synchronous prerequisite for other proof work. Copied sources and no-edit prompt instructions are not an OS sandbox; permissive adapters can access the host. A source or method change can make an old protocol result stale without erasing its historical artifacts.
