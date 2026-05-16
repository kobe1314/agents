# Agent Orchestration Rules

## ⚠️ 强制流程（收到需求后必须先走此流程，再动手）

**每次收到需求，先回答以下问题：**

```
接收需求
  │
  ├─ 这需要 @plan 先出设计吗？
  │   ├─ 是 → 调用 @plan，等产出后再继续
  │   └─ 否
  │
  ├─ 这需要 @build 实现吗？
  │   ├─ 是 → 我只负责 build 部分的实现
  │   └─ 否 → 是不是应该让其他 agent 主导？
  │
  ├─ 这需要 @test 参与吗？
  │   ├─ 是 → 必须用 --bg spawn 或 task 派发给 @test
  │   │        绝不让 @build 替 @test 写测试
  │   └─ 否
  │
  ├─ 这需要 @reviewer 审查吗？
  │   ├─ 是 → /review 或 @reviewer
  │   └─ 否
  │
  └─ 这需要 @docs 更新文档吗？
      ├─ 是 → @docs
      └─ 否
```

**核心原则：@build 只负责 build，不替其他 agent 干活。**

## Agent Selection
When starting a task, choose the most appropriate agent:

1. **@plan** — Complex tasks requiring architecture design, task breakdown, or risk analysis
2. **@build** — Default agent for implementation, feature development, and bug fixes
3. **@reviewer** — Code review, security audit, and quality assessment (read-only)
4. **@debugger** — Runtime errors, crashes, and unexpected behavior
5. **@test** — Writing tests, running test suites, fixing test failures
6. **@docs** — Documentation, README, API docs, inline comments
7. **@refactor** — Code cleanup, optimization, restructuring (no behavior change)
8. **@architect** — System design, technical decision-making, architecture review

## Workflow
- **Plan first** for anything complex: @plan → review → @build → @reviewer
- **Simple changes**: @build directly
- **After changes**: always run @test to verify (via --bg spawn, never manually)
- **Before commit**: run @review on the diff

## Communication
- Use Chinese (中文) for conversation with the user
- Use English for code, comments, and commit messages
- Always explain the "why" before showing the "what"
