# Coding With Claude

Claude Code uses three mechanisms to carry context and extend its capabilities:

| Feature | What it is | Who writes it | Where it lives |
|---------|-----------|---------------|----------------|
| **CLAUDE.md** | Persistent project instructions loaded every session | You | Project root or `~/.claude/` |
| **Rules** | Modular, file-scoped instructions | You | `.claude/rules/*.md` |
| **Skills** | Reusable slash commands Claude can invoke | You | `.claude/skills/<name>/SKILL.md` |

---

## CLAUDE.md

A markdown file that gives Claude persistent context about your project. Think of it as the agent's onboarding doc. It's loaded into the context window at the start of every conversation.

**Where it goes:**

| Scope | Location | Shared with |
|-------|----------|-------------|
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team (via git) |
| Personal | `~/.claude/CLAUDE.md` | Just you |
| Org-wide | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | All users |

**Best practices:**
- Keep it under 200 lines — longer files waste context and reduce adherence
- Be specific: "Use 2-space indentation" > "Format code properly"
- Use `@path/to/file` to import other files instead of inlining everything
- Run `/init` to auto-generate a starting CLAUDE.md from your codebase

See `example-claude-md.md` in this directory for a complete example.

---

## Rules

Rules are modular instruction files in `.claude/rules/`. They let you split a large CLAUDE.md into focused, maintainable pieces. Rules can also be **scoped to specific file paths** so they only load when Claude works with matching files.

**Where they go:**

```
your-project/
├── .claude/
│   └── rules/
│       ├── code-style.md       # Always loaded
│       ├── testing.md          # Always loaded
│       └── api-endpoints.md    # Only loaded for src/api/**/*.ts files
```

**Path-scoped rules** use YAML frontmatter:

```yaml
---
paths:
  - "src/api/**/*.ts"
---

All API endpoints must include input validation...
```

Rules without a `paths` field load unconditionally. Path-scoped rules only load when Claude reads matching files, saving context space.

See the `example-rules/` directory for examples.

---

## Skills

Skills are custom slash commands. Create a `SKILL.md` file with instructions, and Claude adds it as an invocable `/command`. Claude can also load skills automatically when they're relevant to your conversation.

**Where they go:**

| Scope | Location |
|-------|----------|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` |
| Project | `.claude/skills/<skill-name>/SKILL.md` |

**Key frontmatter fields:**

| Field | Purpose |
|-------|---------|
| `name` | The `/slash-command` name |
| `description` | Tells Claude when to use the skill |
| `disable-model-invocation` | Set `true` to make it manual-only (user must type `/name`) |
| `user-invocable` | Set `false` to hide from menu (Claude-only background knowledge) |
| `context` | Set `fork` to run in an isolated subagent |
| `allowed-tools` | Restrict which tools the skill can use |

**String substitutions in skills:**

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed after `/skill-name` |
| `$0`, `$1`, `$2` | Individual arguments by position |
| `${CLAUDE_SKILL_DIR}` | Path to the skill's directory |

See the `example-skills/` directory for examples.

---

## Files in This Directory

| File / Directory | Description |
|-----------------|-------------|
| `example-claude-md.md` | A complete CLAUDE.md for a Python analytics project |
| `example-rules/code-style.md` | Rule: Python code style conventions |
| `example-rules/testing.md` | Rule: Testing standards and commands |
| `example-rules/api-endpoints.md` | Rule: API conventions, scoped to `src/api/**/*.py` |
| `example-skills/deploy/SKILL.md` | Skill: Manual deploy command (`/deploy`) |
| `example-skills/review-pr/SKILL.md` | Skill: PR review with auto-invocation (`/review-pr`) |
| `example-skills/fix-issue/SKILL.md` | Skill: Fix a GitHub issue by number (`/fix-issue`) |

---

## Further Reading

- [Claude Code Memory Docs](https://code.claude.com/docs/en/memory)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
