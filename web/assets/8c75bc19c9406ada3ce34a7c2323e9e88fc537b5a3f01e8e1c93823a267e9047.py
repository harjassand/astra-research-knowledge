"""Exact-integer diagnostics for the hard-budget qutrit.

The bounds below are rational Collatz-Wielandt certificates, not floating
eigensolver outputs. mpmath is used only to print logarithms of exact integers
or fractions. The algebraic proof is in REPORT.txt and does not rely on checks.
"""
from math import comb
from fractions import Fraction
import json
from pathlib import Path
import mpmath as mp

mp.mp.dps = 70
OUT = Path(__file__).parent

def score(k, i):
    """Exact reciprocal miss of the explicit row/Dicke probe, cost k+i."""
    s = sum(comb(i, t) * comb(k-i, i-t) * 3**t
            for t in range(max(0, 2*i-k), i+1))
    return (s << (k-i)) if k >= i else Fraction(s, 2**(i-k))

def best_explicit(q):
    vals = [(score(k, q-k), k) for k in range((q+1)//2, q+1)]
    val, k = max(vals)
    return val, k, q-k

def perron_bounds(k, b, iterations=140):
    """Exact rational enclosure for rho(M), M similar to 2^(k+b) A.

    M_ij=2^(b-i) sum_t C(j,t) C(k-j,i-t) 3^t is positive integer.
    Any positive integer vector v certifies min(Mv/v)<=rho<=max(Mv/v).
    Power iteration creates the vector; its convergence is not assumed.
    """
    b = min(k, b)
    mat = [[0]*(b+1) for _ in range(b+1)]
    for i in range(b+1):
        for j in range(b+1):
            s = sum(comb(j,t)*comb(k-j,i-t)*3**t
                    for t in range(max(0,i+j-k),min(i,j)+1))
            mat[i][j] = s << (b-i)
    scale = 1 << max(256,8*k)
    v = [scale]*(b+1)
    for _ in range(iterations):
        mv = [sum(a*x for a,x in zip(row,v)) for row in mat]
        vmax = max(mv)
        v = [max(1, a*scale//vmax) for a in mv]
    mv = [sum(a*x for a,x in zip(row,v)) for row in mat]
    ratios = [Fraction(a,x) for a,x in zip(mv,v)]
    return min(ratios),max(ratios)

def mp_fraction(x):
    return mp.mpf(x.numerator)/x.denominator

def rate_from_rho(k,b,x):
    return ((k-b)*mp.log(2)+mp.log(mp_fraction(x)))/(k+b)

def finite_optimum(q):
    # Ground patterns give k<=Q; full-cutoff sectors k<Q/2 are admissible too.
    rows=[]
    for k in range(1,q+1):
        b=min(k,q-k)
        lo,hi=perron_bounds(k,b)
        # reciprocal miss is rho(M)*2^(k-b), irrespective of unused budget.
        wl=lo*(1 << (k-b))
        wu=hi*(1 << (k-b))
        rows.append((wl,wu,k,b))
    wl=max(x[0] for x in rows)
    wu=max(x[1] for x in rows)
    winner=max(rows,key=lambda x:x[0])
    return {
      'Q':q,'k':winner[2],'b':winner[3],
      'rate_lower':str(mp.log(mp_fraction(wl))/q),
      'rate_upper':str(mp.log(mp_fraction(wu))/q),
      'relative_width':str(mp_fraction(wu/wl-1)),
      'reciprocal_lower_numerator':str(wl.numerator),
      'reciprocal_lower_denominator':str(wl.denominator),
      'reciprocal_upper_numerator':str(wu.numerator),
      'reciprocal_upper_denominator':str(wu.denominator),
    }

def check_generating_coefficients(maxq=24):
    fs=[1,1]
    for q in range(2,maxq+1): fs.append(fs[-1]+4*fs[-2])
    for q in range(maxq+1):
        direct=sum(score(k,q-k) for k in range((q+1)//2,q+1))
        assert direct==sum(fs[:q+1]),(q,direct,sum(fs[:q+1]))

if __name__=='__main__':
    check_generating_coefficients()
    data={
      'hard_rate':str(mp.log((1+mp.sqrt(17))/2)),
      'hard_separable_rate':str(mp.log(2)),
      'expected_entangled_rate':str(mp.mpf(5)/6*mp.log(4)),
      'optimal_high_fraction':str((7-mp.sqrt(17))/10),
      'coefficient_identity_checked_through_Q':24,
      'finite_optimum':[], 'explicit_probe':[]}
    for q in [1,2,3,4,6,8,12,16,24,32,48]:
        row=finite_optimum(q)
        data['finite_optimum'].append(row)
        print('OPT',q,row['k'],row['b'],row['rate_lower'][:20],row['relative_width'][:10],flush=True)
    for q in [3,6,12,24,48,96,192,384,768,1024]:
        val,k,i=best_explicit(q)
        row={'Q':q,'k':k,'b':i,'reciprocal_miss_exact_integer':str(val),
             'rate':str(mp.log(val)/q)}
        data['explicit_probe'].append(row)
        print('ROW',q,k,i,row['rate'][:20],flush=True)
    (OUT/'exact_checks.json').write_text(json.dumps(data,indent=2))
