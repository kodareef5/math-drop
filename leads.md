# Leads

Checked 2026-10-12. No upstream patch submitted from this repo yet.

| State | Subject | Target | Next action |
| --- | --- | --- | --- |
| check | sampling | NetworkX edge swaps | Compare the exact model below with a pinned runtime. |
| watch | number theory | Sage `prove_BSD` | Check regressions against the existing rewrite. |
| check | computer algebra | HAP Artin-group example | Run the documented command and prepare a small correction if needed. |

## NetworkX edge swaps

[`double_edge_swap`](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/networkx/algorithms/swap.py#L202-L228) stops after successful swaps. That differs from counting every proposal, including rejections.

Run `python3 checks/switch_chain.py`. For degree sequence `(4,4,2,2,2,2)`, it enumerates all 13 labelled graphs and every ordered pair of oriented edges. The per-proposal transition matrix is symmetric. The successful-swap chain has stationary total variation distance `6/91` from uniform, with a largest-to-smallest probability ratio of `2`.

This is an exact model check. It does not test a NetworkX installation, establish a mixing time, or promise uniform samples after finitely many steps. The result follows from the transition probabilities and does not depend on accepting the new [switch-chain claim](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/SwitchChain.lean).

Next: test the current runtime against this model and decide whether documentation or a separate proposal-counting option is useful. The existing API promises successful swaps, so changing its default would change its contract. Read the [contribution policy](https://github.com/networkx/networkx/blob/6da4704cbf32ba6f50f6d9c46cc0a071e3a87985/CONTRIBUTING.rst) before preparing a contribution. Related [PR #8721](https://github.com/networkx/networkx/pull/8721) changes rich-club averaging; inspect its interaction with any sampling change.

## Sage BSD crash paths

At [`0835358`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/BSD.py#L805), the source assigns through a tuple element in the Kato branch. It also passes `secs_dc` to [`heegner_index_bound`](https://github.com/sagemath/sage/blob/0835358cba62dc19fccdff54f32e52fded9f22b0/src/sage/schemes/elliptic_curves/heegner.py#L6815), whose signature has no such keyword. These paths were inspected here but have not been exercised in a Sage runtime.

The issue search found [PR #42397](https://github.com/sagemath/sage/pull/42397), which already addresses the keyword crash, and its open replacement [PR #42884](https://github.com/sagemath/sage/pull/42884). A separate patch may duplicate that work.

Next: run curves `1014e1` and `1058d1` against the replacement branch and check its regression coverage. Any uncovered crash can be addressed independently of new mathematical claims.

## HAP Artin-group example

At [`415d365`](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/www/SideLinks/About/aboutArtinGroups.html#L304), the page names `ResolutionArtin(D)`. The [manual entry](https://github.com/gap-packages/hap/blob/415d3655c99f1e0aa95e042b20b80b8eb404b4e1/doc/newResolutions.xml#L18) names `ResolutionArtinGroup`.

Next: verify the example's intended arguments in GAP and correct that call if needed. Keep any change to the mathematical guarantee separate. Searches for `Artin` and `ResolutionArtin` found no matching issue or PR on this date; that search is not exhaustive.
