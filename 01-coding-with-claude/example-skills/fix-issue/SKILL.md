---
name: fix-issue
description: Fix a GitHub issue by number. Reads the issue, implements the fix, writes tests, and creates a commit.
disable-model-invocation: true
argument-hint: "<issue-number>"
---

# Fix GitHub Issue

Fix issue #$ARGUMENTS.

## Step 1 — Understand the Issue

```bash
gh issue view $ARGUMENTS
```

Read the issue title, description, labels, and any comments. Identify:
- What is broken or missing?
- What is the expected behavior?
- Are there reproduction steps?

## Step 2 — Find Relevant Code

Search the codebase for files related to the issue. Use Grep and Glob to locate
the relevant modules, tests, and configuration.

## Step 3 — Implement the Fix

- Make the minimum change needed to resolve the issue
- Follow the project's coding conventions
- Do not refactor unrelated code

## Step 4 — Write or Update Tests

- Add a test that would have caught this issue
- Verify existing tests still pass:
  ```bash
  pytest --tb=short -q
  ```

## Step 5 — Commit

Create a commit with a message that references the issue:

```
fix: <short description>

Closes #$ARGUMENTS
```

## Important
- If the issue is unclear, stop and ask for clarification instead of guessing
- If the fix requires changes to multiple services, explain the full scope before proceeding
