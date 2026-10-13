"""Exact source-flow compilation from guarded coordinate-permutation programs.

A cylinder is represented by disjoint integer masks (forced zero, forced one).
No full configuration space is enumerated by the compiler or moment evaluator.
"""
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

Cylinder = tuple[int, int]
Bond = tuple[int, int]


def swap_mask(mask: int, i: int, j: int) -> int:
    if ((mask >> i) ^ (mask >> j)) & 1:
        return mask ^ (1 << i) ^ (1 << j)
    return mask


def swap_cylinder(c: Cylinder, bond: Bond) -> Cylinder:
    i, j = bond
    return swap_mask(c[0], i, j), swap_mask(c[1], i, j)


def intersection(c: Cylinder, d: Cylinder) -> Cylinder | None:
    if c[0] & d[1] or c[1] & d[0]:
        return None
    return c[0] | d[0], c[1] | d[1]


def probability(c: Cylinder, p: Fraction) -> Fraction:
    return (1-p)**c[0].bit_count()*p**c[1].bit_count()


def combine(terms: Iterable[tuple[Cylinder, int]]) -> dict[Cylinder, int]:
    out: dict[Cylinder,int] = defaultdict(int)
    for c,k in terms:
        out[c] += k
    return {c:k for c,k in out.items() if k}


@dataclass
class CylinderFlow:
    nsites: int
    terms: dict[Bond, dict[Cylinder,int]]
    initial: dict[Cylinder,int]
    final: dict[Cylinder,int]
    nsteps: int
    nhistories: int

    def current(self, state: int, bond: Bond) -> int:
        bond=tuple(sorted(bond))
        return sum(k for (z,o),k in self.terms.get(bond,{}).items()
                   if not (state&z) and state&o==o)

    def energy_polynomial(self, weights: dict[Bond,int]|None=None) -> dict[tuple[int,int],int]:
        """Return E[sum_b w_b H_b^2] as sum c_(ones,zeros) p^ones q^zeros."""
        result: dict[tuple[int,int],int] = defaultdict(int)
        for bond,ts in self.terms.items():
            w=1 if weights is None else weights[bond]
            items=list(ts.items())
            for i,(c,k) in enumerate(items):
                for j in range(i+1):
                    d,l=items[j]
                    merged=intersection(c,d)
                    if merged is not None:
                        result[(merged[1].bit_count(),merged[0].bit_count())] += w*k*l*(1 if i==j else 2)
        return {key:v for key,v in result.items() if v}

    def energy(self, p: Fraction, weights: dict[Bond,int]|None=None) -> Fraction:
        return sum((c*p**a*(1-p)**b for (a,b),c in self.energy_polynomial(weights).items()),Fraction())


def line_exchange(m: int, all_pivots: bool=False) -> CylinderFlow:
    """Exchange an empty length-m column A with adjacent B containing a vacancy.

    Source: 1{A empty, B not full} - 1{B empty, A not full}.
    Original hard two-vacancy KA legality is checked with occupied exterior.
    Every branch has exactly 3*(m-1) swap instructions, including possible noops.
    """
    if m<2:
        raise ValueError('m must be at least two')
    A=list(range(m)); B=list(range(m,2*m))
    neighbors={}
    for x,col in enumerate((A,B)):
        for y,s in enumerate(col):
            neighbors[s]=[s2 for y2,s2 in enumerate(col) if abs(y2-y)==1]+[(B if x==0 else A)[y]]
    allterms: dict[Bond,list[tuple[Cylinder,int]]]=defaultdict(list)
    initial=[];final=[]
    for r in range(m):
        c=(sum(1<<s for s in A)|(1<<B[r]),(0 if all_pivots else sum(1<<B[y] for y in range(r))))
        c0=c
        initial.append((c,1))
        moves=[]
        for y in range(r,0,-1):moves.append((B[y],B[y-1]))
        for y in range(1,m):moves.extend(((B[y],B[y-1]),(B[y-1],A[y-1])))
        for y in range(m-1,r,-1):moves.append((A[y],A[y-1]))
        assert len(moves)==3*(m-1)
        for i,j in moves:
            # A known-zero witness at each endpoint, excluding its partner.
            assert any((c[0]>>s)&1 for s in neighbors[i] if s!=j), (m,r,i,j,c)
            assert any((c[0]>>s)&1 for s in neighbors[j] if s!=i), (m,r,i,j,c)
            b=tuple(sorted((i,j)))
            d=swap_cylinder(c,b)
            allterms[b].extend(((c,1),(d,-1)))
            c=d
        expected=(sum(1<<s for s in B)|(1<<A[r]),(0 if all_pivots else sum(1<<A[y] for y in range(r))))
        assert c==expected
        final.append((c,1))
    return CylinderFlow(2*m,{b:combine(ts) for b,ts in allterms.items()},combine(initial),combine(final),3*(m-1),m)

if __name__=='__main__':
    import sys,time,json
    for m in map(int,sys.argv[1:] or ['4','8','16','32']):
        t=time.perf_counter();flow=line_exchange(m);t1=time.perf_counter();poly=flow.energy_polynomial();t2=time.perf_counter()
        p=Fraction(4,5);energy=sum((v*p**a*(1-p)**b for (a,b),v in poly.items()),Fraction())
        scale=energy/(2*(1-p)**m*(1-p**m))
        print(json.dumps(dict(m=m,states_avoided=f'2^{2*m}',terms=sum(map(len,flow.terms.values())),monomials=len(poly),compile_seconds=t1-t,contract_seconds=t2-t1,energy=float(energy),normalized_energy=float(scale),energy_numerator=str(energy.numerator),energy_denominator=str(energy.denominator))),flush=True)
