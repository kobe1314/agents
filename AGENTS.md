# Auto-load opencode.json

At the start of every session, automatically load configuration:

1. Read `opencode.json` from the current working directory
2. If not found, fall back to `~/.config/opencode/opencode.json`
3. Apply the `agent`, `model`, `permission`, and other settings from the config

# Auto-load skills

At the start of every session, load all available skills from `.agents/skills/`:

1. Run `npx skills list` to detect installed skills
2. Read the SKILL.md of each installed skill to understand its capabilities
3. Retain skill context throughout the session for on-demand use
4. Skills available in this project:
   - `agent-browser` — Headless browser automation (navigate, click, type, snapshot)
   - `agent-memory` — Persistent memory across sessions (facts, lessons, entities)
   - `ce-commit-push-pr` — Commit, push, and open PRs
   - `excalidraw-diagram-generator` — Generate Excalidraw architecture diagrams
   - `find-skills` — Discover and install skills from the ecosystem
   - `handoff` — Create handoff docs and propose permanent knowledge updates
   - `react-best-practices` — React/Next.js performance optimization guidelines
   - `self-improving-agent` — Log learnings, errors, and corrections
   - `trigger-cost-savings` — Token/cost optimization strategies

# Memory Protocol (agent-memory)

**CLI shortcuts** (agent-memory database: `~/.agent-memory/memory.db`):

```bash
# Facts
python3 .agents/skills/agent-memory/cli/fact.py add "<fact>" --tags tag1 tag2
python3 .agents/skills/agent-memory/cli/fact.py recall "<query>"
python3 .agents/skills/agent-memory/cli/fact.py list

# Lessons
python3 .agents/skills/agent-memory/cli/learn.py add "<action>" "<context>" positive|negative|neutral "<insight>"
python3 .agents/skills/agent-memory/cli/learn.py list

# Entities
python3 .agents/skills/agent-memory/cli/entity.py track "<name>" person|project --attr key value
python3 .agents/skills/agent-memory/cli/entity.py get "<name>"
python3 .agents/skills/agent-memory/cli/entity.py list
```

**On session start:**
1. Load recent lessons: `python3 .agents/skills/agent-memory/cli/learn.py list --limit 5`
2. Check entity context for current task
3. Recall relevant facts: `python3 .agents/skills/agent-memory/cli/fact.py recall "<topic>"`

**On session end:**
1. Extract durable facts from conversation and store: `python3 .agents/skills/agent-memory/cli/fact.py add`
2. Record any lessons learned
3. Update entity information

**During conversation:**
- When user expresses a clear preference → auto-save as fact
- When something fails → record as negative lesson
- When meeting new people/projects → track as entity

# Skill installation convention

All skills MUST be installed to `.agents/skills/` as the single canonical directory:

- **npx skills**: Run `npx skills add <skill> -y` (without `-g`) — it installs to `.agents/skills/` by default.
- **skillhub**: Run `skillhub install <skill> --dir .agents/skills` to target `.agents/skills/` instead of the default `skills/`.
- **No `skills/` directory** should be created at project root. If a tool creates it automatically, move the skill to `.agents/skills/` and remove `skills/`.

# Multi-Agent Orchestration

This project uses a multi-agent orchestration system. Choose the right agent for each task:

## Available Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| `@plan` | deepseek-reasoner | read-only | Architecture design, task breakdown, risk analysis |
| `@build` | deepseek-v4-flash | read+write+bash | Default: implementation, features, bug fixes |
| `@reviewer` | deepseek-reasoner | read-only | Code review, security audit, quality assessment |
| `@debugger` | deepseek-v4-flash | read+write+bash | Runtime errors, crashes, troubleshooting |
| `@test` | deepseek-v4-flash | read+write+bash | Write/run tests, fix failures |
| `@docs` | deepseek-v4-pro | read+write | Documentation, README, API docs |
| `@refactor` | deepseek-v4-flash | read+write+bash | Code cleanup, optimization, restructuring |
| `@architect` | deepseek-reasoner | read-only | System design, technical decisions |

## Standard Workflows

### Complex feature
```
@plan → review plan → @build → @test → @reviewer → commit
```

### Bug fix
```
@debugger → identify root cause → @build → fix → @test → commit
```

### Code improvement
```
@refactor → make changes → @test → @reviewer → commit
```

## Custom Slash Commands

| Command | Agent | Description |
|---------|-------|-------------|
| `/test` | @test | Run tests and fix failures |
| `/commit` | @build | Commit changes with conventional message |
| `/docs` | @docs | Generate/update documentation |
| `/fix` | @build | Auto-fix lint/style/type issues |
| `/review` | @reviewer | Review current changes |
| `/plan` | @plan | Create implementation plan |
| `/deploy` | @architect | Create deployment plan
