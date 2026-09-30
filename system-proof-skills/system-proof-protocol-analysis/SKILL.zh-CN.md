---
name: system-proof-protocol-analysis
description: "当 system-proof 任务需要审查跨操作前提、不变量的必要范围、缺失的调用者到被调用者证明桥接，或结合限定范围源码调查生命周期缺陷假说时，使用 analyze-protocol。产出建议性证据，不是证明或已确认的缺陷。"
---

# 围绕验证目标的协议分析

[英文版](SKILL.md)。本文供人工审核，描述的是同一个 skill，不是另一个需要注册的 skill。

这是面向调用者的集成 skill，不是分析执行 agent 的运行时方法。复制时应保留整个目录；它不会自动安装到主 agent 中。[GUIDE.zh-CN.md](GUIDE.zh-CN.md) 提供从实验提炼的例子、详细参数、产物和术语说明。

工具自身也是由 agent 执行分析。它的观察、假说和候选义务／检查是供审阅的分析证据，不是决策、已验证事实或必然发现。

## 什么情况下使用

当前系统目标涉及以下问题时，可以考虑这项可选分析：

- 契约依赖跨操作的共享状态：哪个构造过程、所有者或先前调用建立了前提，哪些中间操作保持或使它失效？
- 不变量的作用或范围不清楚：调用者究竟需要什么性质，适用于哪些对象与阶段，哪些证据支持或反驳它？
- 已有局部证明，但尚未连接到顶层主张：具体缺少哪个调用者到被调用者的表示关系或前置条件桥接？
- 疑似违反依赖操作顺序、状态转移或失败处理：哪些有源码依据的操作序列和低成本区分性检查，可以区分真正的违反、允许的效果和调用者补偿？

这些是通用的问题模式，不是特定系统的要求，也不保证一定获得新发现。它不是编译器、证明器或缺陷确认执行器，不要求每轮证明都调用，也不规定与其他分析工具的固定调用顺序。是否值得进行一次有明确范围、可能耗时数分钟的调查，由调用 agent 决定。

## 调用前准备

宿主需要提供 `argus-spec` 中的 `analyze-protocol` 命令、配置好的 coding-agent 后端，以及固定版本的 Specula checkout。保留原始目标、真实的目标符号／文件／行号、直接调用者、观察边界、假设和限定的源码范围。若已有聚焦问题、当前证明进展及缺口、已知发现，将其放入相对源码根目录的 `context_files` 中；不要用更窄的问题替换原始目标。缺少输入或依赖时应明确报告，而不是悄悄扩大范围。

## 基本使用

创建 `request.json`，将占位内容替换为实际目标和源码定位：

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

准备新的运行目录，只在准备成功后执行分析；即使分析返回非零退出码，也应查看结果：

```sh
analyze-protocol prepare request.json --source /path/to/project --out /path/to/new-run \
  --specula-root /path/to/Specula
analyze-protocol run /path/to/new-run --timeout 600
analyze-protocol status /path/to/new-run
```

`prepare` 捕获输入，不调用模型。`run` 只执行分析；示例超时以秒为单位，不是运行时长承诺。`status` 检查保留的证据，不重新执行。每次新的尝试都需要新目录；预算及后台调度由调用者负责。

## 读取与交接结果

同时检查 `status` 和 `current`，不要只看退出码。仍匹配当前输入的 `completed` 报告表示结构完整，不表示已获证明。保留部分完成、失败、超时和过期的结果；不要悄悄重试或将它们标记为成功。

保留运行目录、源码／方法标识、覆盖范围和未解决的边界。如果存在 `report.json`，读取它，并连同前提、源码引用、使用该事实的调用者、依赖、建议检查和剩余证明工作一起交接相关发现。否则保留状态和已有日志／原始输出。建议的测试与证明不是执行证据；任何后续检查都需要单独记录。

是否调用工具、采纳或拒绝候选、修改范围或实现、选择下一项证明义务，都由调用 agent 决定。本 skill 和报告均不选定最终规格，不关闭 proof-map 中的证明义务，不偿还信任／变更债务，也不认证缺陷。
