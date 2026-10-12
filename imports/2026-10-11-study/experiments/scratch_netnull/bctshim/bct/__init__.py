import numpy as np
class BCTParamError(Exception): pass
def get_rng(seed):
    if seed is None or seed == np.random: return np.random.mtrand._rand
    if isinstance(seed, np.random.RandomState): return seed
    return np.random.RandomState(seed)
def randmio_und(R, itr, seed=None):
    '''
    This function randomizes an undirected network, while preserving the
    degree distribution. The function does not preserve the strength
    distribution in weighted networks.

    Parameters
    ----------
    W : NxN np.ndarray
        undirected binary/weighted connection matrix
    itr : int
        rewiring parameter. Each edge is rewired approximately itr times.
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    R : NxN np.ndarray
        randomized network
    eff : int
        number of actual rewirings carried out
    '''
    if not np.allclose(R, R.T):
        raise BCTParamError("Input must be undirected")
    rng = get_rng(seed)
    R = R.copy()
    n = len(R)
    i, j = np.where(np.tril(R))
    k = len(i)
    itr *= k

    # maximum number of rewiring attempts per iteration
    max_attempts = np.round(n * k / (n * (n - 1)))
    # actual number of successful rewirings
    eff = 0

    for it in range(int(itr)):
        att = 0
        while att <= max_attempts:  # while not rewired
            while True:
                e1, e2 = rng.randint(k, size=(2,))
                while e1 == e2:
                    e2 = rng.randint(k)
                a = i[e1]
                b = j[e1]
                c = i[e2]
                d = j[e2]

                if a != c and a != d and b != c and b != d:
                    break  # all 4 vertices must be different

            if rng.random_sample() > .5:
                i.setflags(write=True)
                j.setflags(write=True)
                i[e2] = d
                j[e2] = c  # flip edge c-d with 50% probability
                c = i[e2]
                d = j[e2]  # to explore all potential rewirings

            # rewiring condition
            if not (R[a, d] or R[c, b]):
                R[a, d] = R[a, b]
                R[a, b] = 0
                R[d, a] = R[b, a]
                R[b, a] = 0
                R[c, b] = R[c, d]
                R[c, d] = 0
                R[b, c] = R[d, c]
                R[d, c] = 0

                j.setflags(write=True)
                j[e1] = d
                j[e2] = b  # reassign edge indices
                eff += 1
                break
            att += 1

    return R, eff


