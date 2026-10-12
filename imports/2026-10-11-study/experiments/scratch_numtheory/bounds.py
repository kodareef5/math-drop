"""
Q3 / Q2 quick calculations for the numtheory deep dive.

(1) Least quadratic non-residue n(p): compare the unconditional bound that 003
    yields, C (log p)^A with C uncomputed (we set C = 1, which is optimistic),
    against:
      - Bach's GRH bound 2 (log p)^2 and Lamzouri-Li-Soundararajan's (log p)^2
      - Norton / Trevino explicit Burgess-type bounds 4.7 p^{1/4} log p and
        0.9 p^{1/4} log p (as cited in Trevino, arXiv:1412.3062)
      - the (non-explicit) Burgess-Vinogradov exponent p^{1/(4 sqrt e)}
    A = 32 is the paper's own corollary (via BIMS Thm 6.7: exponent 4/(1-2eps),
    eps = 7/16). A = 8 is what a smoothed explicit-formula argument gives from
    Re s <= 7/8 (1/(1-7/8)); A = 16 is the triage's estimate.
(2) Empirical n(p) for random primes at cryptographic sizes.
(3) 029 -> class groups: the Bach-type generator bound (log|d|)^{1/delta}
    with delta = 1e-6, versus the trivial Minkowski bound (2/pi) sqrt|d|.
"""
import math, random, sys

LN2 = math.log(2)
LOG10_2 = math.log10(2)


def log10_bounds(bits):
    lnp = bits * LN2
    out = {}
    out['Bach GRH 2(ln p)^2'] = math.log10(2 * lnp ** 2)
    out['LLS GRH (ln p)^2'] = math.log10(lnp ** 2)
    for A in (8, 16, 32):
        out['003 C=1 (ln p)^%d' % A] = A * math.log10(lnp)
    out['Norton 4.7 p^1/4 ln p'] = math.log10(4.7) + bits / 4 * LOG10_2 + math.log10(lnp)
    out['Trevino 0.9 p^1/4 ln p'] = math.log10(0.9) + bits / 4 * LOG10_2 + math.log10(lnp)
    out['Burgess-Vinogradov p^(1/4sqrt e)'] = bits / (4 * math.sqrt(math.e)) * LOG10_2
    return out


def crossover(A, which):
    """smallest bit size where (ln p)^A < competitor bound"""
    for bits in range(16, 2_000_000, 1):
        b = log10_bounds(bits)
        if A * math.log10(bits * LN2) < b[which]:
            return bits
    return None


def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def is_probable_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def random_prime(bits, rng):
    while True:
        n = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(n):
            return n


def least_nonresidue(p):
    a = 2
    while legendre(a, p) != p - 1:
        a += 1
    return a


def main():
    print('=== (1) log10 of n(p) bounds by bit size ===')
    names = list(log10_bounds(64).keys())
    print('bits'.ljust(8) + ''.join(n[:22].rjust(24) for n in names))
    for bits in (64, 128, 256, 512, 1024, 2048, 3072, 4096, 8192, 16384):
        b = log10_bounds(bits)
        print(str(bits).ljust(8) + ''.join(('%.1f' % b[n]).rjust(24) for n in names))
    print()
    print('=== crossover bit sizes (003 with C=1 beats competitor) ===')
    for A in (8, 16, 32):
        for comp in ('Trevino 0.9 p^1/4 ln p', 'Burgess-Vinogradov p^(1/4sqrt e)'):
            print('A=%2d vs %-34s : %s bits' % (A, comp, crossover(A, comp)))
    for A in (8, 16, 32):
        # never beats Bach: ratio grows
        print('A=%2d vs Bach GRH at 2048 bits: 10^%.1f times larger' % (
            A, log10_bounds(2048)['003 C=1 (ln p)^%d' % A] - log10_bounds(2048)['Bach GRH 2(ln p)^2']))
    print()

    print('=== (2) empirical least non-residue for random primes ===')
    rng = random.Random(20261011)
    for bits, cnt in ((256, 400), (1024, 120), (2048, 40)):
        vals = [least_nonresidue(random_prime(bits, rng)) for _ in range(cnt)]
        print('%5d-bit primes: n=%d, mean n(p)=%.2f, max n(p)=%d' % (bits, cnt, sum(vals) / cnt, max(vals)))
    print()

    print('=== (3) 029-derived Bach-type bound vs Minkowski for imaginary quadratic d ===')
    delta = 1e-6
    for bits in (512, 1024, 2048, 10**4, 10**6, 10**7):
        lnd = bits * LN2
        l10_bach_type = (1 / delta) * math.log10(lnd)
        l10_mink = math.log10(2 / math.pi) + 0.5 * bits * LOG10_2
        l10_grh_bach = math.log10(6 * lnd ** 2)
        print('|d| ~ 2^%-8d  (log|d|)^1e6 = 10^%.3g   Minkowski = 10^%.3g   GRH 6 log^2 = 10^%.2f' % (
            bits, l10_bach_type, l10_mink, l10_grh_bach))
    # crossover where (ln d)^{1/delta} < sqrt(d)
    lo, hi = 1.0, 1e12
    f = lambda L: (1 / delta) * math.log(L) - 0.5 * L
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    print('crossover: (ln|d|)^1e6 < sqrt|d| once ln|d| > %.3g, i.e. |d| has > %.3g bits' % (hi, hi / LN2))


if __name__ == '__main__':
    main()
