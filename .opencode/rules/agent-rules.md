# Agent Orchestration Rules

## ⚠️ 强制流程（收到需求后必须先走此流程，再动手）

**每次收到需求，先回答以下问题：**

```
接收需求
  │
  ├─ 这需要 @plan 先出设计吗？
  │   ├─ 是 → 必须先出设计/架构图，提交 review，等用户批准
  │   │        未批准前绝不动手写代码
  │   └─ 否
  │
  ├─ 设计完成 → 提交审查（用 pipeline）
  │   ├─ av --pipeline "功能名" "描述" \
  │   │     "plan:出设计" "reviewer:审批方案" "build:实现" "test:写测试"
  │   └─ 等用户批准 review 后才能推进到 build 步骤
  │
  ├─ review 通过后 → 开始 build
  │
  ├─ build 完成后 → 派 @test 写测试（--bg spawn，绝不让 build 替 test 干活）
  │
  ├─ 最后 @reviewer 审查代码
  │
  └─ 通过后 /commit
```

**核心原则：@build 只负责 build，不替其他 agent 干活。未经 review 批准不得开始实现。**

## Agent Selection
...

## Workflow
- **Plan first** for anything complex: @plan → review → @build → @test → @reviewer → commit
- **Review gate**: build step blocked until review is approved via `av --review approve`
- **Simple changes**: @build directly (no review needed)
- **After changes**: always run @test to verify (via --bg spawn, never manually)
- **Before commit**: run @review on the diff
