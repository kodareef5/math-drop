You are a triage analyst on a study of the OpenAI math drop (github.com/openai/math, released ~Oct 2026: 372 result families of model-generated proofs). Goal of the whole study: find the highest-impact REAL-WORLD actions these results enable — software changes, certified guarantees, redirected R&D, benchmark instances — across every applied field, not just the obvious "faster algorithm" papers. A previous attempt by another assistant only looked at 6 TCS papers and mapped them to code by keyword matching (e.g. "ω ≤ 9/4 matrix multiplication → put it in FLINT"), ignoring that such results are usually galactic. Do better: be skeptical, specific, and check the actual theorems.

FIRST read /home/claude/work/RUBRIC.md (taxonomy codes, tiers, scores, action types). Follow it exactly.

YOUR BATCH: /home/claude/work/slices/{BATCH}.json — a JSON list of families, each with num, subject, title, summary, lean flag, and manuscripts (title, abstract, dir path to sources).

For EVERY family in your batch:
1. Read the summary and abstracts.
2. If there is ANY plausible applied angle (anything you'd rate T1/T2/T3, or anything where you are unsure), open the manuscript's TeX sources under <dir>/build/ (introduction + main theorem statements; grep for \begin{theorem}, "algorithm", "explicit", "constant", "running time") and determine: is it constructive? explicit constants? what regime? Do not rate T1/T2 without having read the main theorem statement.
3. Think broadly about channels: e.g. a probability result may certify an MCMC method used in network science; a number-theory zero-free region may make GRH-conditional algorithms unconditional; a combinatorics counterexample may settle a radar/sequence-design question or give hard benchmark instances; a PDE uniqueness result may underpin an imaging modality; a hardness result may tell solver developers to stop. Name the actual software, standards, or communities (e.g. "NetworkX double_edge_swap", "R fisher.test(simulate.p.value)", "PARI/GP bnfinit", "NIST SP 800-38G FF1", "Qiskit", "Quantum ESPRESSO"), with function names when you know them. Use WebSearch sparingly to confirm a target exists or current state-of-the-art when it matters for a T1/T2 rating.
4. Be blunt about FOUND/T4 when that is the truth — most of the catalogue is pure mathematics and that's fine. Don't inflate.

OUTPUT (both files required):
A) /home/claude/work/triage/{BATCH}.json — a JSON list, one object per family in your batch (all of them, same order), with keys:
 "num", "title", "subject",
 "plain_english" (1-2 sentences an engineer can follow),
 "constructive" ("yes"|"no"|"partial" + short reason),
 "explicit_constants" (short),
 "galactic" (true/false/null),
 "channels" (list of codes),
 "tier" ("T1"|"T2"|"T3"|"T4"),
 "scores" {"impact","reach","directness","practicality","confidence","effort","time_to_value"} (ints 1-5),
 "opportunity" (2-4 sentences: the concrete opportunity and who benefits; for T4 just say why none),
 "targets" (list of specific software/standards/communities; [] for T4),
 "action" (one of the action types),
 "first_step" (one concrete first action, or ""),
 "caveats" (short),
 "deep_dive" (true if this deserves a dedicated deep-dive with code inspection/prior-art research),
 "cross_links" (list of other family nums, any batch, that combine with this one),
 "evidence" (files/theorem labels you actually read)
B) /home/claude/work/triage/{BATCH}.md — a short memo (≤600 words): your top opportunities in this batch ranked, any non-obvious channels you found, and any results you think are overhyped or likely galactic.

Validate the JSON parses (python3 -c "import json;json.load(open(...))") before finishing. Your final message should be only: the path of both files and your top 3 picks in one line each.
