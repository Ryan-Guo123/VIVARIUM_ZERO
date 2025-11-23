# AGENTS.md

A dedicated guide for AI coding agents working on VIVARIUM ZERO. Keep actions precise, reversible, and privacy-safe.

## Project Overview
- Domain: Artificial life simulation with a stack-based VM for genetic programming.
- Backend: Python + FastAPI. Optional Docker; local venv fallback.
- Frontend: Vanilla JS + p5.js, WebSocket live visualization.
- CI: GitHub Actions runs pytest.
- Primary language: English. Secondary: curated Chinese under `docs/zh/`.

## Repository Layout (essentials)
- `backend/app/` — FastAPI app, core engine, VM, evolution
- `frontend/` — Static assets (index.html, js, css) served by backend
- `scripts/` — `start.sh`, `stop.sh`
- `docs/` — Public docs (English)
- `docs/zh/` — Chinese translations (secondary language)
- `private/` — Ignored area for internal drafts (do not commit)

## Setup & Run
Prefer local venv unless Docker is required.

```
# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start server (smart: Docker if available else local venv)
./start.sh
# Server binds 0.0.0.0; open http://localhost:8000
```

Docker (optional):
```
# If Docker is available, the start script may use it
# Otherwise to run manually (if a Dockerfile exists later):
# docker build -t vivarium_zero .
# docker run -p 8000:8000 vivarium_zero
```

## Testing
```
# From repo root (with venv active)
pip install -r requirements-dev.txt  # if present; else skip
pytest -q
```
- CI config: `.github/workflows/ci.yml` (Python 3.11 + pytest)
- Run focused tests near changed modules first.

## Code Style & Conventions
- Python: PEP 8, descriptive names, no one-letter vars.
- Keep changes minimal and focused; avoid drive-by refactors.
- Do not add license headers to files.
- Public docs in English; add Chinese only under `docs/zh/` with `_ZH` suffix.
- Avoid adding heavy dependencies; prefer standard libs.

## Agent Workflow
1. Read `AGENTS.md`, `README.md`, and relevant `docs/`.
2. Plan steps with the todo tool; work in small, verifiable patches.
3. When editing code, prefer `apply_patch`; keep diffs minimal.
4. Run tests relevant to your changes; then broader tests.
5. Update docs if behavior or public interfaces change.
6. Respect privacy and language policy (below).

## Privacy & Language Policy
- No personal identifiers in public files (names, emails, home-lab specifics).
- Primary language: English. Chinese translations live in `docs/zh/` and are clearly labeled.
- Place internal drafts under `private/` (ignored by git).
- If sensitive info is discovered in history, propose a filtered rewrite.

## Performance Notes
- Spatial grid reduces collision complexity; keep it enabled.
- VM has a gas limit per tick; avoid unbounded loops.
- Phase 2+ may add JIT (Numba) under Python 3.11 or container images.

## Tools & Commands Cheatsheet
```
# Start (auto Docker or venv)
./start.sh

# Stop (if implemented)
./stop.sh

# Backend health
curl http://localhost:8000/api/health

# Tests
pytest -q
```

## PR & Commit Guidelines
- Follow existing PR template. Keep titles concise.
- Include rationale, constraints, and tests.
- Do not commit contents of `private/`.

## Non-Goals for Agents
- Introducing new languages/frameworks without necessity.
- Drastic redesigns or unrelated refactors.
- Publishing personal information.
