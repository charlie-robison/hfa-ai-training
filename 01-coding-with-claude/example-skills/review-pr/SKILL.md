---
name: review-pr
description: Review a pull request for code quality, bugs, and adherence to project conventions. Use when asked to review a PR or when a PR number is mentioned.
context: fork
agent: Explore
allowed-tools: Bash(gh *), Read, Grep, Glob
---

# Review Pull Request

Review PR `$ARGUMENTS` thoroughly.

## Gather Context

Fetch the PR details:
```bash
gh pr view $ARGUMENTS
gh pr diff $ARGUMENTS
gh pr view $ARGUMENTS --comments
```

## Review Checklist

For each changed file, evaluate:

1. **Correctness** — Does the code do what the PR description says?
2. **Edge cases** — Are error paths, empty inputs, and boundary conditions handled?
3. **Security** — Any hardcoded secrets, SQL injection, XSS, or auth bypasses?
4. **Performance** — Any N+1 queries, unbounded loops, or missing pagination?
5. **Testing** — Are new behaviors covered by tests? Are tests meaningful (not just asserting True)?
6. **Style** — Does it follow the project's coding conventions?
7. **Naming** — Are variables, functions, and files named clearly?

## Output Format

Respond with:

### Summary
One paragraph: what this PR does and whether it's ready to merge.

### Issues Found
List each issue with:
- **File and line number**
- **Severity** (blocker / warning / nit)
- **What's wrong and how to fix it**

### What Looks Good
Briefly note well-written code worth highlighting.
