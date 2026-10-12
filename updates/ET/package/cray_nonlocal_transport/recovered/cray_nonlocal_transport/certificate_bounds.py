"""Exact rational evaluation of the completed-current lower certificate.

The mathematical completion theorem is in REPORT.md.  This file neither
estimates a mixing time nor uses a stochastic confidence interval.
"""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT = Path(__file__).parent
GATE_COUNTS = (1, 8, 28, 52, 49, 16, 0, 0, 0)

def gate_probability(p: F) -> F:
    if not F(0) < p < F(1):
        raise ValueError('Particle density must lie strictly between zero and one.')
    q = 1-p
    return sum((F(c)*p**n*q**(8-n) for n,c in enumerate(GATE_COUNTS)), F(0))

def radius_second_moment(b: F) -> F:
    determinant = 1-4*b-b*b
    if b < 0 or determinant <= 0:
        raise ValueError('The chordless-path certificate requires 1-4*b-b**2 > 0.')
    return 4*b + 32*b*b*(3-4*b+b*b)/determinant**2

def coarse_energy_majorant(b: F) -> F:
    return 1+8*radius_second_moment(b)

def mmul(a,b):
    return ((a[0][0]*b[0][0]+a[0][1]*b[1][0],a[0][0]*b[0][1]+a[0][1]*b[1][1]),
            (a[1][0]*b[0][0]+a[1][1]*b[1][0],a[1][0]*b[0][1]+a[1][1]*b[1][1]))

def mpow(a,n):
    out=((F(1),F(0)),(F(0),F(1)))
    while n:
        if n&1:out=mmul(out,a)
        a=mmul(a,a);n//=2
    return out

def radius_tail_energy(b: F, cutoff: int) -> F:
    """Bound E[R_z**2 1{R_z>cutoff}] using a rational two-state path automaton."""
    if not isinstance(cutoff,int) or cutoff<0:
        raise ValueError('cutoff must be a nonnegative integer')
    moment=radius_second_moment(b)  # validates the subcriticality inequality
    if cutoff==0:return moment
    det=1-4*b-b*b
    A=((b,2*b),(2*b,3*b))
    S=(((1-3*b)/det,2*b/det),(2*b/det,(1-b)/det))
    AS=mmul(A,S);A2S2=mmul(AS,AS)
    H=tuple(tuple(F((cutoff+1)**2 if i==j else 0)+(2*cutoff+3)*AS[i][j]+2*A2S2[i][j]
                  for j in range(2))for i in range(2))
    result=mmul(mpow(A,cutoff-1),H)
    return 16*b*b*sum(result[i][j]for i in range(2)for j in range(2))

def module_cost(p: F, meta: dict) -> F:
    D = int(meta['denominator'])
    E = [int(s) for s in meta['weighted_energy_squares_by_particle_count']]
    q = 1-p
    g = gate_probability(p)
    # Each unoriented configuration edge contributes twice to the equilibrium
    # energy.  The same factor two occurs in 2*chi*g**2 and cancels.
    return sum((F(e,D*D)*p**n*q**(18-n) for n,e in enumerate(E)),F(0))/(p*q*g*g)

def lower_certificate(p: F, meta: dict) -> dict:
    g = gate_probability(p); b = 1-g
    C = module_cost(p,meta); K = coarse_energy_majorant(b)
    lower = 1/(C*K)
    upper = (1-p**3)**2
    normalized_tail_target = F(1,10**12)
    lo,hi=0,1
    while 16*p*(1-p)*C*radius_tail_energy(b,hi)>normalized_tail_target:hi*=2
    while hi-lo>1:
        mid=(hi+lo)//2
        if 16*p*(1-p)*C*radius_tail_energy(b,mid)<=normalized_tail_target:hi=mid
        else:lo=mid
    R=hi
    return {'p':str(p),'gate_probability':str(g),'bad_probability':str(b),
            'module_cost':str(C),'coarse_energy_bound':str(K),
            'lower_exact':str(lower),'upper_exact':str(upper),
            'lower_decimal':float(lower),'upper_decimal':float(upper),
            'module_cost_decimal':float(C),'coarse_energy_bound_decimal':float(K),
            'cutoff_for_normalized_current_L2_error_1e_minus_6':R}

if __name__ == '__main__':
    meta=json.loads((ROOT/'module_metadata.json').read_text())
    rows=[lower_certificate(p,meta) for p in [F(1,10),F(1,5),F(1,4),F(3,10),F(1,3),F(7,20),F(2,5)]]
    (ROOT/'certified_bounds.json').write_text(json.dumps(rows,indent=2)+'\n')
    for row in rows:
        print('p=',row['p'],'g=',float(F(row['gate_probability'])),
              'C=',row['module_cost_decimal'],'K=',row['coarse_energy_bound_decimal'],
              'lower=',row['lower_decimal'],'upper=',row['upper_decimal'],
              'R=',row['cutoff_for_normalized_current_L2_error_1e_minus_6'])
