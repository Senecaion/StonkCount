# 🧭 Collaboration Guide

This document explains the standard **collaborator workflow** for contributing features and fixes to this project.

---

## 1. Overview

We use a **branch + pull request** workflow:

- Everyone is a **collaborator** on this repo.
- Direct pushes to `main` are **prohibited**.
- All changes land via **feature branches** + **Pull Requests (PRs)**.
- Each feature or fix starts with an **Issue**.

---

## 2. Workflow Summary

1. Create an Issue for each new feature or fix.
   - Use clear titles and acceptance criteria.
   - Label appropriately (`enhancement`, `bug`, `chore`, etc.).
   - Assign yourself if you plan to work on it.

2. Branch from an up-to-date main

      git checkout main
      git pull origin main
      git checkout -b feat/short-description-123

   - Include the Issue number (123) in your branch name if possible.
   - Common prefixes:
       * feat/ – new features
       * fix/ – bug fixes
       * chore/ – housekeeping
       * docs/ – documentation changes

3. Make your changes
   - Keep commits small and focused.
   - Follow Conventional Commits style:

       feat: add dotenv support
       fix: handle 429 rate limit backoff

4. Commit and push

      git add .
      git commit -m "feat: add dotenv loading (closes #123)"
      git push -u origin feat/short-description-123

5. Open a Pull Request
   - Go to GitHub → “Compare & pull request”.
   - Base branch: main
   - Compare branch: your feature branch.
   - Link the issue: Closes #123
   - Add reviewers (teammates).
   - Use the PR template if available.

6. Code review
   - Wait for approval.
   - Address comments via new commits.
   - Keep branch fresh:

      git fetch origin
      git rebase origin/main
      git push --force-with-lease

7. Merge
   - Use **Squash & Merge** to keep history clean.
   - Delete your branch after merge.
   - The linked Issue auto-closes via “Closes #123”.

---

## 3. Branch Protection

`main` branch rules:
- No direct pushes.
- Require 1+ approving review.
- Require checks/tests to pass.

---

## 4. Helpful Commands

Task | Command
---- | --------
Update local main | git checkout main && git pull origin main
Create feature branch | git checkout -b feat/thing-123
Push new branch | git push -u origin feat/thing-123
Switch branches | git checkout main / git checkout feat/...
Sync with main | git fetch origin && git rebase origin/main
Undo last commit (soft) | git reset --soft HEAD~1
View branches | git branch -vv
Delete local branch | git branch -d feat/...
Delete remote branch | git push origin --delete feat/...

---

## 5. Naming Conventions

Type | Example | Notes
---- | -------- | -----
Feature | feat/handles-whitelist-123 | new capability
Fix | fix/postgres-connection | bug fix
Chore | chore/update-readme | housekeeping
Docs | docs/collaboration-guide | documentation

---

## 6. Pull Request Checklist

- [ ] PR title follows Conventional Commit style
- [ ] Linked to an Issue (Closes #123)
- [ ] Lint/tests pass
- [ ] Reviewed by another collaborator
- [ ] Contains descriptive summary and testing steps
- [ ] No .env, data, or secrets committed

---

## 7. Good Practices

- Keep PRs small and self-contained.
- Write clear commit messages; avoid “update file”.
- Use draft PRs for early feedback.
- Add or update documentation for new features.
- Use labels (enhancement, bug, help wanted, etc.) to keep project boards organized.

---

## 8. Example Full Cycle

      # create branch
      git checkout main
      git pull origin main
      git checkout -b feat/add-postgres-storage-201

      # code...
      git add .
      git commit -m "feat: integrate Postgres persistence (closes #201)"
      git push -u origin feat/add-postgres-storage-201

      # open PR on GitHub -> request review -> squash merge

---

## 9. References

- GitHub Flow: https://guides.github.com/introduction/flow/
- Conventional Commits: https://www.conventionalcommits.org/
- Git rebase vs merge: https://www.atlassian.com/git/tutorials/merging-vs-rebasing

---

**Remember:** main is always deployable; branches are for experimentation.
