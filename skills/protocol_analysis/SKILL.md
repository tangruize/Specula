---
name: protocol-analysis
description: "Bounded, advisory analysis for specification and proof work. Use when a caller's needed property depends on shared-state writers, ownership, lifecycle transitions, error compensation, or a supplied call graph. Does not run the TLA+ or bug-confirmation pipeline."
---

Use this skill only with a prepared analysis workspace containing `task.json`, `response-schema.json`, `source/`, and `history.txt`. If the packet is missing, report the missing inputs instead of starting the full Specula pipeline.

Read [references/scoped-analysis.md](references/scoped-analysis.md) for the method and [../../docs/ProtocolAnalysis.md](../../docs/ProtocolAnalysis.md) for the workspace contract. The caller prepares the source snapshot, copies the referenced methods into `method/`, owns execution time limits, and validates the resulting advisory report.
