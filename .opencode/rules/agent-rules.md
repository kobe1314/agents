# ⚠️ SYSTEM-LEVEL MANDATORY PROCESS — YOU MUST FOLLOW THIS

**These rules are injected into your system prompt every session. You CANNOT skip them.**

---

## YOU MUST follow this process for EVERY feature request, without exception:

### Step 1: STOP. Do NOT write any code yet.
Read this entire file before proceeding.

### Step 2: Create a pipeline with review gate
```
av --pipeline "功能名" "描述" \
  "plan:出设计方案" \
  "reviewer:审批方案" \
  "build:实现" \
  "test:写测试"
```

### Step 3: Pipeline creates a review. YOU WAIT.
- Pipeline will pause at "reviewer" step
- A review is created automatically
- Tell the user: `av --review approve <review_id>`

### Step 4: DO NOTHING until user approves.
- No design changes
- No code writing
- No testing
- The `"build"` step waits for user approval

### Step 5: After approval, implement.
- Pipeline continues automatically
- Build step spawns as background task

### Step 6: Delegate testing.
- `av --bg spawn "test-xxx" "pytest ..."` — do NOT write tests yourself

### Step 7: Review before commit.
- Run `@reviewer` on the diff

---

## STRICT RULES

| Rule | Description |
|------|-------------|
| YOU MUST | Create pipeline with reviewer step for every feature |
| YOU MUST NOT | Write implementation code before review is approved |
| YOU MUST NOT | Write tests — delegate to @test via --bg spawn |
| YOU MUST | Wait for user to run `av --review approve` before starting build |
| YOU MUST | Run @reviewer before /commit |

## Violation consequence

If you write implementation code before review approval, you are violating the project's mandatory process. The user will notice because there will be no review record in the pipeline.
