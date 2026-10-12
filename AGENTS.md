# Working on math-drop

Find useful consequences of AI math releases and turn the best ones into reproducible checks or small upstream patches for `kodareef5`.

## Keep the work useful

- Start with the question or defect being resolved. End with evidence, a patch, or a specific reason to stop.
- Keep the presentation terse and publish the supporting work. Preserve the full classification, evidence, and experiments. Avoid duplicate catalogs, elaborate scoring systems, and status reports without new findings.
- Treat `imports/` as a dated source record. Keep original files unchanged; record new checks and decisions separately.
- For each promising idea, name the target repository, relevant function or document, expected benefit, and smallest test that could disprove it.
- Check the current source and existing issues and PRs before preparing a contribution. Preserve links and commit IDs.
- Separate published claims, inherited judgments, and checks run here. A Lean file alone does not establish that the paper's headline was proved.
- Check assumptions, constants, realistic input sizes, and existing implementations. Drop ideas with no practical advantage. Correctness fixes, useful tests, and documentation corrections count as results.
- Keep theorem-dependent changes separate from bugs supported by established mathematics. Do not claim a finite sampler is uniform merely because its stationary distribution is uniform.
- Automate repeatable searches and comparisons. Record changes and failures; skip repetitive no-change write-ups. Jobs may collect leads, but a search hit is not a verified result.
- Update `leads.md` when a finding changes the next action. Close weak or duplicate leads. Run the affected checks before publishing changes.

## Write plainly

- Lead with the finding or change. Use concrete names, short sentences, active verbs, and measured numbers.
- Name sources. Say what was checked and what remains uncertain.
- Cut hype, vague metaphors, stock introductions, flattery, repeated summaries, and decorative formatting. Avoid forced contrasts and lists padded to a fixed length.
- Keep necessary explanations and complete sentences. Brevity must not make the reader decode the text.
- Before finishing, remove any sentence that adds no fact, decision, instruction, or useful context.

Writing guidance abridged from [pstack's unslop](https://github.com/cursor/plugins/blob/1b6d44ff26d4e242f4e8f68c391e6d2f7ca16def/pstack/skills/unslop/SKILL.md). Read as a reference; no skill installation or pstack tooling is required.
