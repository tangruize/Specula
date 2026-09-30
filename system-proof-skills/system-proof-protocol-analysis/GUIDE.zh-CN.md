# 面向目标驱动系统证明的协议分析

[英文版](GUIDE.md)。

本指南与 [SKILL.zh-CN.md](SKILL.zh-CN.md) 组成独立的调用者说明包。集成工具时可以复制或加载这个目录；仅将它放在这里，不会把它安装到主 agent 中。运行时方法仍位于固定版本的 Specula checkout 中，路径为 `skills/protocol_analysis/references/scoped-analysis.md`；本说明包不替代该方法，也不提供可执行程序。

`analyze-protocol` 对跨操作和共享状态生命周期进行可选、有明确范围的源码分析，产出关联源码的候选契约、性质和证明义务。它不选定验证任务（campaign）的规格，不确认证明进展，不确认缺陷，也不批准实现变更。工具选择、范围、结果解释和下一项任务，仍由调用 agent 按现有验证任务约定决定。FM-Agent 是独立工具，不是本工具的一种模式或前置要求。

## 输入与调用

保留原始系统目标、需要相关事实的调用者、相关观察边界，以及已知假设或证明缺口。已有注解和报告只是上下文，不会自动成为已获认证的前提。以下示例使用占位路径和符号；请替换为真实的源码定位，并设置适合本次调用的预算。

命令由宿主的 `argus-spec` 包提供，而不是由 Specula 的独立 CLI 提供。该包中的 `argus_spec/analysis_request.json` 定义请求格式。下面是一个按文件限定范围的最小示例：

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

所有选定路径和源码定位都必须存在。上下文文件是可选的。路径相对于源码根目录；显式指定的文件可以未被 Git 跟踪，而目录展开只选择 Git 跟踪的文件。文件／行号定位不能证明所写符号确实位于该位置。

```sh
analyze-protocol prepare request.json --source /path/to/project --out /path/to/new-run \
  --specula-root /path/to/Specula
analyze-protocol run /path/to/new-run --timeout 600
analyze-protocol status /path/to/new-run
```

`prepare` 捕获输入和方法标识，不调用模型。`run` 只执行分析，必须显式设置以秒为单位的超时。`status` 检查保留的结果及其新鲜度，不重新执行分析。每次新的尝试都需要新的运行目录；工具本身不负责任务调度或重试。

也可以使用 `scope.call_graph`，其中包含 `functions`、`calls`、`unresolved`、`roots`、`direction` 和 `max_depth`；前三个数组采用 `proof_map.navigation` 的记录格式。工具会选取包含可达函数的整个文件，并保留未解析的边和跨边界的边。它既不会发现完整调用图，也不证明所有相关写入操作都已纳入范围。

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

命令由 `argus-spec` 安装，需要 Git、Bash、Python 和配置好的 coding-agent 后端。初始化宿主仓库固定版本的 `specula` 子模块，或提供包含限定范围分析方法的干净 `tangruize/Specula` checkout。通过 wheel 安装时，需要设置 `SPECULA_ROOT` 或传入 `--specula-root`。后端／模型配置由显式参数指定或从现有配置继承，不由本文固定。

协议分析不需要完整的 `specula setup`、TLA 生成、TLC 或 Verus 配置。后台执行由调用者负责；不必把这项可选分析作为其他证明工作的同步前置条件。源码副本和提示中的禁止修改指令不是操作系统沙箱；使用宽松权限的适配器可以访问宿主环境。源码或方法变化可能使旧协议分析结果过期，但不会抹去其历史产物。
