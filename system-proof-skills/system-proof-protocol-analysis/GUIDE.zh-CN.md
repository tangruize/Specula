# 面向目标驱动系统证明的协议分析

`analyze-protocol` 对跨操作和共享状态生命周期进行可选、有明确范围的源码分析，产出关联源码的候选契约、性质和证明义务。它不选定验证任务（campaign）的规格，不确认证明进展，不确认缺陷，也不批准实现变更。工具选择、范围、结果解释和下一项任务，仍由调用 agent 按现有验证任务约定决定。

分析由 agent 完成，不是确定性的语义判定器。观察、假说、候选义务和建议检查都是待审阅的证据，可能有误，也可能覆盖不全。质量取决于问题、提供的上下文、范围和实际执行；不承诺必然发现某个问题或带来改进，建议也不构成作出决策或执行操作的授权。

## 在 FM function analysis 与 protocol analysis 之间选择

使用与 blocking question 匹配的最窄方法：

| Blocking question | 优先使用 | 边界 |
| --- | --- | --- |
| 一个 function 或选定 callee 对 direct caller 到底承诺什么？ | `analyze-function` | 一个 source span、contract variant、frame condition 和选定 child obligation |
| 哪个 operation 建立 shared-state premise，哪些 transition 保持或破坏它，哪个 caller 使用它？ | `analyze-protocol` | 有界 operation/file 集合，以及明确 lifecycle 或 observation interval |
| proposed global invariant 是否需要缩小 domain、phase 或 object set？ | `analyze-protocol` | candidate scope 和 counter-scenario，不是 invariant proof |
| protocol report 是否已把问题缩小到一个 callee contract？ | 返回 `analyze-function` 或 direct proof | handoff 必须给出精确 caller fact 和剩余 authoritative check |

不存在强制顺序，也不应默认两个工具都调用。FM analysis 可能暴露值得 protocol review 的 shared-state premise；protocol analysis 也可能把缺口定位到一个 function。工具切换由 active proof obligation 决定，而不是固定 pipeline。

## 对 Action 1 的贡献

有用的 protocol output 可以：

- 提出语义上真正不同的 lifecycle/invariant candidate，包括更弱的 observable relation；
- 识别缺失的 establisher、未检查 writer、cancellation/error transition 或 caller compensation；
- 把 proposed global property 分类为 candidate、需要限制、goal 不需要，或被 bounded source evidence 挑战；
- 把 local contract 连接到建立和消费它的 operation/caller；
- 给出能够区分 candidate 的具体 sequence、source audit、component test、implementation proof 或 model check。

这些只是 specification attack 和 reasoning 的输入，不是 adequacy oracle。report 可能重复输入 context、引用错误 definition、遗漏 scope 外 writer，或建议错误加强。调用 agent 必须区分 prior finding 与 new deduction，并在改变 authoritative status 前取得独立 evidence。

真实系统运行只提供 compatibility 和 information-value evidence。其 finding、runtime 和项目专有名称不得变成默认 prompt rule，也不能证明它优于 FM-Agent。

## 请求字段与范围

最小请求和调用示例见 [SKILL.zh-CN.md](SKILL.zh-CN.md)。命令由宿主的 `argus-spec` 包提供，而不是由 Specula 的独立 CLI 提供。该包中的 `argus_spec/analysis_request.json` 定义准确的请求格式：

| 字段 | 要求与含义 |
| --- | --- |
| `goal` | 必填；保留完全一致的原始验证任务目标 |
| `target` | 必填对象，包含 `symbol`、`file`、`line`；使用真实源码文件及范围内、从一开始计数的行号 |
| `direct_caller` | 必填；需要该结果的直接调用者 |
| `observation_boundary` | 必填；评价承诺行为的时点或区间，包括相关失败情况 |
| `assumptions` | 必填数组；没有提供假设时使用空数组 |
| `scope` | 必填；在 `paths` 和 `call_graph` 中恰好选择一种 |
| `context_files` | 可选的相对源码根目录的文件，可包含聚焦问题、已有发现、候选契约或证明缺口；它们是上下文，不是已认证前提 |
| `history_limit` | 可选非负整数，默认零；最多捕获该数量的范围内提交消息，不含完整 diff 或远程 issue 历史 |

所有选定路径和源码定位都必须存在。路径相对于源码根目录；显式指定的文件可以未被 Git 跟踪，而目录展开只选择 Git 跟踪的文件。文件／行号定位不能证明所写符号确实位于该位置。

`scope.call_graph` 包含 `functions`、`calls`、`unresolved`、`roots`、`direction` 和 `max_depth`；前三个数组采用 `proof_map.navigation` 的记录格式。根节点使用函数 ID；方向为 `callees`、`callers` 或 `both`；深度为非负整数，或用 `null` 表示不限制可达深度。工具会选取包含可达函数的整个文件，并保留未解析的边和跨边界的边。它既不会发现完整调用图，也不证明所有相关写入操作都已纳入范围。

## 执行参数与未完成的运行

| 命令 | 参数与行为 |
| --- | --- |
| `prepare` | 请求文件，以及必填的 `--source` 和 `--out`；可选 `--specula-root`。捕获输入／方法标识，不调用模型。输出目录必须是新目录。 |
| `run` | 已准备的目录，以及必填的正整数 `--timeout`，单位为秒。native system-proof adapter 使用已认证的 `copilot-cli`；可选 `model` 和 `effort` override，未指定时保留 Copilot CLI default。standalone Specula 仍保留其他 adapter。 |
| `status` | 运行目录；检查保留的结果及其新鲜度，不重新执行分析 |

每次新的尝试都需要新的运行目录；工具本身不负责任务调度或重试。超时会终止本次调用的进程组，并保留部分产物。先保留执行结果和覆盖缺口，再判断是否值得进行另一次限定范围的尝试。源码或方法变化后，历史状态可能仍显示完成，但 `current` 会变为 false；应同时检查两个字段。

原生验证任务集成由宿主框架负责：必须绑定完全一致的原始目标，授权源码根目录，应用操作次数／时间预算，并注册建议性执行记录。独立调用不会自动注册验证任务的执行记录。宿主的工具目录条目或占位响应（dummy）不是分析已经运行的证据；集成时应保留实际后端的执行结果和产物。

## 产出的证据

| 产物 | 记录内容 |
| --- | --- |
| 协议分析的 `request.json`、`manifest.json`、`work/` | 捕获的目标、范围、源码／方法版本、源码副本、实际使用的 `prompt.md`、`task.json` 和输出 schema |
| 协议分析的 `report.json` | 结构检查通过的完整**或部分完成**报告：发现、引用、前提、使用方、依赖、建议检查、覆盖范围和局限 |
| 协议分析的 `status.json` 及日志 | 执行结果、耗时和原始工作产物；超时或输出无效时，可能只留下 `work/analysis.json` 和日志，而没有被接受的报告 |
| 原生 `analysis` 执行记录（receipt） | 与验证任务的关联、哈希及是否仍匹配当前输入；通过 `review-packet.analysis_evidence` 提供 |

协议分析输出遵循宿主包中的 `argus_spec/analysis_response.json`。其中可选的 `global_property` 记录状态、阶段、建立该性质的操作、保持该性质的操作、使用方、排除的状态转移和剩余证明工作。`candidate`、`requires_restriction`、`not_required` 和 `contradicted` 是分析者提出的分类，不是机器证明的判定。

`run` 仅在报告为 `completed` 且仍匹配当前输入时返回零退出码。`partial`、`failed`、`invalid`、`timed_out`、`interrupted` 和 `stale` 都是非成功结果。`prepare`，以及尚未过期且处于 prepared/running 状态的 `status`，也可以返回零退出码：仅凭退出码为零，不能认定分析已完成。原生 `outcome: passed` 表示获得完整的建议性报告，不表示某个性质已被证明；该执行记录不能关闭 proof-map 的边、偿还信任／变更债务，或计作核心证明尝试。

工具会对覆盖信息和引用进行结构检查，但不检查被引用的源码行是否真正支持某个主张。`source_supported` 是分析标签。生成报告不会为建议的测试或证明提供执行证据。因此，使用某项发现时仍应保留其源码标识、前提、范围缺口和建议检查；后续测试或验证器结果是独立证据，各有自己的覆盖范围。

## 术语

| 术语 | 含义 |
| --- | --- |
| 协议／生命周期阶段（Protocol / lifecycle phase） | 指定时间区间内操作与共享状态之间的关系；不一定是网络协议，也不要求并发执行 |
| 直接调用者／使用方（Direct caller / consumer） | 将某个事实作为前提使用的代码或系统主张；不只是报告里提到的另一个函数 |
| 观察边界（Observation boundary） | 评价承诺行为的时点或区间，例如返回调用者时，而非内部回调完成时 |
| 调用锥（Call cone） | 从选定图根节点出发，在方向／深度限制内可达的节点；其他共享状态写入者可能在范围外 |
| 建立／保持／使用（Establish / preserve / consume） | 分别指使某性质成立、在状态转移中维持该性质，以及使用该性质建立另一项证明义务 |
| 帧性质（Frame） | 某次操作前后哪些相关观察保持不变；不一定要求所有缓存或表示字段完全相等 |
| 补偿（Compensation） | 调用者的回滚、拒绝、丢弃或其他处理，这些行为可能改变局部失败对系统的意义 |
| 新鲜度（Freshness）／`current` | 捕获的输入和方法仍与检查的标识一致；不认证语义真实性 |

## 运行边界

执行需要 Git、Bash、Python、已认证的 Copilot CLI，以及包含 bounded method 的干净、固定版本 Specula checkout。native system-proof adapter 自动解析 relocated submodule，不要求 `SPECULA_ROOT`、API key、MCP setup 或其他 provider。standalone invocation 仍可使用 `SPECULA_ROOT`、`--specula-root` 和 Specula 文档记录的其他 adapter。

协议分析不需要 TLA 生成、TLC 或 Verus。后台执行由调用者负责；不必把这项可选分析作为其他证明工作的同步前置条件。源码副本和提示中的禁止修改指令不是操作系统沙箱；使用宽松权限的适配器可以访问宿主环境。源码或方法变化可能使旧协议分析结果过期，但不会抹去其历史产物。
