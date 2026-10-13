"""Exact even-Majorana algebra for the graded translation-covariance argument.

A word I denotes i^(|I|(|I|-1)/2) prod_{a in I} c_a, in ascending order.
Site i carries Majoranas 2*i and 2*i+1. Coefficients are Fractions.
This is an algebra/checking module, not the complete worst-case predictor.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from typing import Iterable

Word = tuple[int, ...]
Poly = dict[Word, Fraction]
I_POW = (1, 1j, -1, -1j)


def canonical(word: Word) -> Word:
    if not word:
        return word
    shift = 2 * (min(word) // 2)
    return tuple(a - shift for a in word)


def phase_product(a: Word, b: Word) -> tuple[complex, Word]:
    """M_a M_b = phase M_(a xor b); only the four Gaussian units occur."""
    if tuple(sorted(set(a))) != a or tuple(sorted(set(b))) != b:
        raise ValueError('Majorana indices must be sorted and distinct.')
    inversions = sum(x > y for x in a for y in b)
    out = tuple(sorted(set(a).symmetric_difference(b)))
    power = ((len(a)*(len(a)-1) + len(b)*(len(b)-1)
              - len(out)*(len(out)-1)) // 2 + 2*inversions) % 4
    return I_POW[power], out


def a_commutator(hword: Word, word: Word) -> tuple[int, Word]:
    """Coefficient for -i[M_hword,M_word] in the Hermitian basis."""
    p, out = phase_product(hword, word)
    q, out2 = phase_product(word, hword)
    assert out == out2
    c = -1j * (p-q)
    assert c.imag == 0 and c.real == int(c.real)
    return int(c.real), out


def clean(p: dict[Word, Fraction]) -> Poly:
    return {w: Fraction(c) for w, c in p.items() if c}


def add_scaled(out: dict[Word, Fraction], p: Poly, scale: Fraction) -> None:
    for w, c in p.items():
        out[w] += scale*c


def unpaired(word: Word) -> int:
    sites: dict[int, int] = defaultdict(int)
    for a in word:
        sites[a//2] += 1
    return sum(k == 1 for k in sites.values())


def is_population(word: Word) -> bool:
    return unpaired(word) == 0


def degree(word: Word) -> int:
    if len(word) % 2:
        raise ValueError('Only even Majorana words are used here.')
    return len(word)//2


def radius(word: Word) -> int:
    s = sorted({a//2 for a in word})
    return max((b-a-1 for a,b in zip(s,s[1:])), default=0)


def z_word(sites: Iterable[int]) -> tuple[Word, int]:
    s = tuple(sorted(set(sites)))
    return tuple(a for i in s for a in (2*i,2*i+1)), (-1)**len(s)


def column(word: Word, t: Fraction = Fraction(1),
           densities: tuple[tuple[tuple[int, ...], Fraction], ...] = (),
           *, part: str = 'all') -> Poly:
    """Infinite translation-quotient column, including all nonzero outputs.

    densities stores Z-product templates with their Hamiltonian coefficients.
    Candidate translates are generated near endpoints, never across a long
    Jordan-Wigner interior. Long gaps therefore do not add hidden loop work.
    """
    if part not in {'all','hop','diag'}:
        raise ValueError('part must be all, hop or diag')
    out: dict[Word, Fraction] = defaultdict(Fraction)
    sites = {a//2 for a in word}
    if part in {'all','hop'}:
        starts = {i+j for i in sites for j in (-1,0)}
        for i in starts:
            terms = (((2*i+1,2*i+2), t/2),
                     ((2*i,2*i+3), -t/2))
            for h, hc in terms:
                c, w = a_commutator(h,word)
                if c:
                    out[canonical(w)] += hc*c
    if part in {'all','diag'}:
        single_sites = {i for i in sites if sum(a//2 == i for a in word) == 1}
        for template, hc in densities:
            starts = {i-x for i in single_sites for x in template}
            for sh in starts:
                h, sign = z_word(x+sh for x in template)
                c, w = a_commutator(h,word)
                if c:
                    out[canonical(w)] += hc*sign*c
    return clean(out)


def apply(p: Poly, t: Fraction=Fraction(1),
          densities: tuple[tuple[tuple[int,...],Fraction], ...] = (),
          *, part: str='all') -> Poly:
    out: dict[Word,Fraction] = defaultdict(Fraction)
    for w,c in p.items():
        add_scaled(out,column(w,t,densities,part=part),c)
    return clean(out)


def current(t: Fraction=Fraction(1)) -> Poly:
    return {(0,2):-t/2, (1,3):-t/2}


def normalize_sites(sites: Iterable[int]) -> tuple[int,...]:
    s=tuple(sorted(sites))
    return tuple(x-s[0] for x in s)


def exclusion_column(sites: tuple[int,...], t: Fraction, d: Fraction) -> Poly:
    """(2 t^2/d) exclusion Laplacian on translated k-subsets, in M basis."""
    cset=set(sites)
    starts={i+j for i in cset for j in (-1,0)}
    out: dict[Word,Fraction]=defaultdict(Fraction)
    w, sign=z_word(sites)
    w=canonical(w)
    scale=2*t*t/d
    for i in starts:
        if (i in cset) != (i+1 in cset):
            target=cset.symmetric_difference({i,i+1})
            v,sign2=z_word(target)
            assert sign == sign2
            out[w] += scale*sign
            out[canonical(v)] -= scale*sign
    return clean(out)
