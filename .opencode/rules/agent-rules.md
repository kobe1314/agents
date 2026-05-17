# ⚠️ SYSTEM-LEVEL MANDATORY PROCESS — YOU MUST FOLLOW THIS

**These rules are injected into your system prompt every session. You CANNOT skip them.**

---

## THE COMPLETE WORKFLOW

### Phase 0: 接收需求

```
收到需求
  → 检查有没有对应 skill（excalidraw? react? memory?）
  → 有 skill 先加载 skill
```

### Phase 1: 需求分析

```
  → 分析需求
  → 输出 .md 文档
  → 记录拆分后的需求点
```

### Phase 2: 架构设计

```
  → @architect 生成架构图（excalidraw / mermaid）
  → 交给用户 review
  → 用户给 feedback
  → 修改架构图
  → 用户给 approval
```

**🚫 在 approval 之前，不允许开始任何实现代码**

### Phase 3: 并行开发

```
  approval 后，同时开始：
  ├── @build → 开始实现功能代码
  └── @test  → 开始写测试（并行！）
```

### Phase 4: 审查

```
  build + test 都完成后：
  → @reviewer 审查代码
  → 如果是页面 → 打开浏览器验证
  → 验证通过 → 交给用户验收
```

### Phase 5: 上线

```
  用户验收通过后：
  → 调用 GitHub MCP 上传代码（不可用原始 git 命令）
```

---

## 执行任何步骤前，先问：有没有对应的 skill？

| 步骤 | 可能有的 skill |
|------|---------------|
| 画架构图 | excalidraw-diagram-generator |
| 写前端 | react-best-practices |
| 提交代码 | ce-commit-push-pr |
| 找技能 | find-skills |
| 记教训 | self-improving-agent, agent-memory |

---

## STRICT RULES

| Rule | Description |
|------|-------------|
| YOU MUST | Check for relevant skill before every major step |
| YOU MUST | Write .md requirement doc before any design |
| YOU MUST | Use @architect for architecture diagrams |
| YOU MUST NOT | Start coding before user approves the architecture |
| YOU MUST | Run @test IN PARALLEL with @build (use --bg spawn) |
| YOU MUST | Open browser to verify if it's a page |
| YOU MUST | Use GitHub MCP for git operations, never raw git |
| YOU MUST | Wait for user acceptance before uploading |

## MCP Priority

Before any operation, check in this order:
1. Is there a skill for this? → Load it
2. Is there an MCP tool? → Use it
3. Only if neither → Use shell tools
