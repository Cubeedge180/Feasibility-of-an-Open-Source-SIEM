# Claude Code toolkit

This repo declares its own Claude Code setup, so cloud and local sessions get the same tools. Plugins come from `.claude/settings.json`; skills live in `.claude/skills/`.

- **ponytail** (plugin, always on): pick the smallest solution that fully works. Never cut validation, error handling, security or accessibility. Use `/ponytail-review` before declaring non-trivial work done.
- **agent-skills** (plugin by addyosmani): at the start of any coding task, check `using-agent-skills` and apply the lifecycle skill that fits.
- **tdd**: new features and bug fixes with real logic go test-first. Prefer it over agent-skills' `test-driven-development`. Ponytail still sets how much: one good test per risky behavior.
- **diagnosing-bugs**: when something is broken, failing or slow, build a tight reproduce-loop before touching code. Prefer it over agent-skills' `debugging-and-error-recovery`.
- **graphify**: if `graphify-out/` exists, query it before grepping. Building it needs the `graphify` CLI (`uv tool install graphifyy`); if the command is missing, say so instead of failing.
- **User-invoked** (never run unasked): `/grill-me`, `/grill-with-docs`, `/handoff`, `/to-spec`, `/to-tickets`, `/implement`, `/implement-spec`, `/code-review`, `/setup-matt-pocock-skills`. The spec chain publishes to the issue tracker and needs `/setup-matt-pocock-skills` run once first.

Precedence when they pull apart: security and correctness first, then ponytail's minimalism, then process.

## Agent skills

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: `GLOSSARY.md` at the root, ADRs in `docs/decisions/`. See `docs/agents/domain.md`.
