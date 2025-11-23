# Language & Privacy Policy

## Overview
The VIVARIUM ZERO repository adopts **English as the primary language** for all public-facing materials (code comments, issues, pull requests, documentation). A curated **Chinese translation layer** exists for accessibility and is stored strictly under `docs/zh/`.

## Structure
- Primary spec (sanitized): `docs/PRODUCT_SPEC.md`
- Chinese translation: `docs/zh/PRODUCT_SPEC_ZH.md`
- Additional bilingual docs follow the same naming convention: `NAME.md` and `zh/NAME_ZH.md`.
- Private drafts (excluded from Git): place in `private/` (ignored by `.gitignore`).

## Privacy & Sanitization
Removed:
- Personal names and roles
- Home-lab specifics (exact hardware ownership, management tooling names)
- Any sensitive operational details
Generalized references (e.g., "edge server" instead of personal device).

## Contribution Rules
1. Public PRs must use English in descriptions and code.
2. Optional Chinese translation updates: include in same PR, clearly marked.
3. Do not commit personal info (emails, internal hostnames, tokens).
4. If sensitive info is accidentally committed, perform removal immediately and coordinate history rewrite.

## Adding a New Document
1. Create English version under `docs/`.
2. (Optional) Add Chinese translation under `docs/zh/` with `_ZH` suffix.
3. Reference both in README if broadly relevant.

## History Rewrite Guidance (If Needed)
If legacy commits contain sensitive data:
```
# Prepare a replacements file mapping sensitive tokens to ***REMOVED***
git filter-repo --replace-text replacements.txt

# Force push after validation (coordinate with collaborators)
git push --force origin master
```
Always audit a fresh clone before force-pushing.

## Non-Goals
- Automatic machine translation commits
- Maintaining more than two languages

## Review Checklist
- [ ] English primary doc present
- [ ] Chinese translation (if provided) marked and placed correctly
- [ ] No personal identifiers
- [ ] `.gitignore` includes `private/`

---
This policy ensures clarity, privacy, and consistency for the open source community.
