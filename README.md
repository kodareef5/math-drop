# math-drop

Check AI-generated mathematics for useful software changes. Keep the evidence and the smallest next action.

The [full study](imports/README.md) classifies **372 result families / 719 manuscripts** and evaluates **133 opportunities**. [Explore the interactive matrix](https://kodareef5.github.io/math-drop/) or [download the original ZIP](https://github.com/kodareef5/math-drop/raw/refs/heads/main/imports/math-drop-study.zip).

| Data and work | Contents |
| --- | --- |
| [Catalog](imports/2026-10-11-study/catalogue.json) · [Classification](imports/2026-10-11-study/triage_all.json) · [Rubric](imports/2026-10-11-study/RUBRIC.md) | Every family, applicability, scores, evidence, and next steps |
| [Analyses](imports/2026-10-11-study/deep/) · [Verification](imports/2026-10-11-study/verify/) | 12 themes, opportunity assessments, and five verification reports |
| [Experiments](imports/2026-10-11-study/experiments/) | Scripts, patches, inputs, logs, and outputs |

These are the study's assessments as of October 11, 2026. Subsequent checks and decisions are recorded separately.

Start with [the leads](leads.md). Each names an upstream target, what has been checked, and what remains to do. Checks live in [`checks/`](checks/). Completed work gets an upstream link; disproved ideas get a short reason and leave the active list.

```sh
python3 checks/switch_chain.py
python3 checks/study.py
python3 -m unittest discover -s tests -v
```

Public sources are listed in [`watchlist.json`](watchlist.json). Daily jobs check release repositories and discussions. Monday jobs search for new releases, related issues, and existing patches. Results appear in [Actions](https://github.com/kodareef5/math-drop/actions) as summaries and downloadable JSON. These are leads to review, not proof verification.

Discovery covers the configured GitHub queries. A first run establishes a baseline; an unchanged source produces no new entry. Search limits and failed sources appear in the report. Saved baselines use the Actions cache; if it expires, the next run establishes a new baseline.

Run a search locally with Python 3.9+ and an authenticated [GitHub CLI](https://cli.github.com/):

```sh
python3 tools/watch.py watch
python3 tools/watch.py hunt
```

Record a finding in `leads.md` with a dated source or commit, a check, and a next action. Label it **check**, **patch**, **watch**, or **closed**. Use short subject tags such as sampling, number theory, or formalization. Add a script when it makes the result reproducible. Verify the target's current code and contribution rules before preparing a patch.

Original project code uses the [MIT license](LICENSE). Imported material retains its existing notices; see the [study provenance](imports/README.md).
