# October 11, 2026 study

[Interactive matrix](https://kodareef5.github.io/math-drop/) · [Original ZIP](math-drop-study.zip) · [Extracted files](2026-10-11-study/) · [Checksums](2026-10-11-study/MANIFEST.json)

The study examines [`openai/math` at `fd4aeeb`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). All 372 families have a classification, covering 719 manuscripts in 17 subjects.

| File | Contents |
| --- | --- |
| [`catalogue.json`](2026-10-11-study/catalogue.json) | Families, manuscript summaries, source paths, formalization and withdrawal flags |
| [`triage_all.json`](2026-10-11-study/triage_all.json) · [`triage/`](2026-10-11-study/triage/) | Per-family classifications and batch memos |
| [`RUBRIC.md`](2026-10-11-study/RUBRIC.md) | Channels, tiers, scores, and action definitions |
| [`deep/`](2026-10-11-study/deep/) | 12 thematic analyses and 133 opportunities |
| [`verify/`](2026-10-11-study/verify/) | Five verification reports and per-claim verdicts |
| [`calibration.json`](2026-10-11-study/calibration.json) · [`prior.json`](2026-10-11-study/prior.json) | Score adjustments and reassessed earlier suggestions |
| [`experiments/`](2026-10-11-study/experiments/) | Scripts, a proposed patch, inputs, logs, and outputs |
| [`TRIAGE_PROMPT.md`](2026-10-11-study/TRIAGE_PROMPT.md) · [`DEEP_PROMPT.md`](2026-10-11-study/DEEP_PROMPT.md) | Original analysis instructions |

The family classifications are 23 enabling, 68 indirect, and 281 foundational. The opportunity assessments are 38 pursue now, 17 pursue as research, 24 monitor, and 54 do not pursue. These are different units: one family can lead to several opportunities.

The ZIP preserves all 551 original files. The expanded tree preserves their bytes, with five Python bytecode caches kept only in the ZIP. `python3 checks/study.py` checks the archive, extracted files, and classification coverage.

The recorded verification and experiment outputs belong to the original study. Publishing them does not mean they were rerun here. Absolute paths refer to its original environment; some experiments need upstream checkouts or dependencies that were not included. Current follow-up work belongs in [`leads.md`](../leads.md).

Imported material retains its existing attribution and license notices. The instrumented Zstandard sources identify [upstream commit `49cf517`](https://github.com/facebook/zstd/tree/49cf51799ea051457f57243527aa2058f999f005). Its [BSD license](2026-10-11-study/experiments/scratch_optimization/zstd_instr/LICENSE) and [GPLv2 text](2026-10-11-study/experiments/scratch_optimization/zstd_instr/COPYING) have been added alongside the unchanged sources. The root MIT license does not replace third-party terms.
