"""Exact stationary-law check on 13 labelled degree-preserving graph states.

This checks the transition model, not a NetworkX installation or a mixing bound.
"""

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product


def realizations(degrees):
    pairs = list(combinations(range(len(degrees)), 2))
    for edges in combinations(pairs, sum(degrees) // 2):
        counts = Counter(v for edge in edges for v in edge)
        if tuple(counts[v] for v in range(len(degrees))) == tuple(degrees):
            yield frozenset(edges)


def proposals(graph):
    directed = [edge for a, b in sorted(graph) for edge in ((a, b), (b, a))]
    counts = Counter()
    for (a, b), (c, d) in product(directed, repeat=2):
        additions = frozenset((tuple(sorted((a, c))), tuple(sorted((b, d)))))
        if len({a, b, c, d}) == 4 and not additions.intersection(graph):
            removals = {tuple(sorted((a, b))), tuple(sorted((c, d)))}
            counts[frozenset(graph.difference(removals).union(additions))] += 1
        else:
            counts[graph] += 1
    return counts


def check():
    degrees = (4, 4, 2, 2, 2, 2)
    states = list(realizations(degrees))
    kernels = {g: proposals(g) for g in states}
    total = (sum(degrees)) ** 2
    assert len(states) == 13
    assert all(sum(row.values()) == total for row in kernels.values())
    assert all(h in kernels for row in kernels.values() for h in row)
    assert all(kernels[g][h] == kernels[h][g] for g in states for h in states)
    successes = {g: total - kernels[g][g] for g in states}
    assert min(successes.values()) > 0
    mass = sum(successes.values())
    jump_stationary = {g: Fraction(successes[g], mass) for g in states}
    # Verify stationarity independently by multiplying the jump transition matrix.
    for h in states:
        incoming = sum(jump_stationary[g] * Fraction(kernels[g][h], successes[g])
                       for g in states if g != h)
        assert incoming == jump_stationary[h]
    tv = sum(abs(p - Fraction(1, len(states))) for p in jump_stationary.values()) / 2
    return {
        "degrees": list(degrees), "states": len(states),
        "count_all_attempts_kernel_symmetric": True,
        "successful_swaps_stationary_max_min": str(Fraction(max(successes.values()), min(successes.values()))),
        "successful_swaps_stationary_tv": str(tv),
        "successful_swaps_stationary_tv_decimal": float(tv),
        "scope": "Stationary distributions of exact finite models. No finite-time uniformity or upstream runtime claim.",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
