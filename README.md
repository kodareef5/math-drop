# math-drop

Check AI-generated mathematics for useful software changes. Keep the evidence and the smallest next action.

Start with [the leads](leads.md). Each names an upstream target, what has been checked, and what remains to do. Checks live in [`checks/`](checks/). Completed work gets an upstream link; disproved ideas get a short reason and leave the active list.

```sh
python3 checks/switch_chain.py
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
