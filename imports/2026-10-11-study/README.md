# Math drop opportunity study (github.com/openai/math @ fd4aeeb, analysed 2026-10-11)

- `math-drop-matrix.html` — the interactive matrix (same as the published page).
- `catalogue.json` — all 372 families / 719 manuscripts parsed from the repo.
- `triage/` + `triage_all.json` — per-family classification (discipline × channel × tier, 7 scores) and per-batch memos.
- `deep/` — 12 theme write-ups (`.md`) and their scored opportunity rows (`.json`); `lean_confidence.json` = per-family Lean status.
- `verify/` — independent verification reports and per-row verdicts.
- `calibration.json` — cross-theme score overrides with reasons. `prior.json` — the earlier ChatGPT list, re-checked.
- `experiments/` — scripts, logs and small outputs from every experiment (large cloned repos and virtualenvs omitted).
- `RUBRIC.md`, `TRIAGE_PROMPT.md`, `DEEP_PROMPT.md` — the shared method given to every agent.
