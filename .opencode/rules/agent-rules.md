# Agent Orchestration Rules

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
- **After changes**: always run @test to verify
- **Before commit**: run @review on the diff

## Communication
- Use Chinese (中文) for conversation with the user
- Use English for code, comments, and commit messages
- Always explain the "why" before showing the "what"
