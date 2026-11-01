"""Explicit local divergence-free cycle improvement of the Thomson competitor.

The reference flow has exactly the prescribed divergence. Each correction is a
circulation around a square of two adjacent spin flips. Its coefficient depends
only on the two exterior spins. All energies are exact 5-spin marginal sums.
The target dynamics itself is never truncated. This is an ordinary flow/potential
variational construction, independent of the degree-three reference solve.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import time


def pair_conditional(t, L, x, y, R):
    return (1+t*L*x)*(1+t*x*y)*(1+t*y*R)/(4*(1+t**3*L*R))


def solve(n):
    start = time.perf_counter()
    assert n >= 6
    t = F(n-1, n+1); gamma = F(n*n-1, n*n+1); gap = 1-gamma
    tn = t**n
    V = n*(1+t)/(1-t)*(1-tn)/(1+tn)
    C2 = (t*t+t**(n-2))/(1+tn)
    U0 = F(0); cross = [F(0), F(0)]; gram = [[F(0),F(0)],[F(0),F(0)]]
    hMM = F(0); hMT = F(0); hTT = F(0); total_probability = F(0)
    for s in product([-1,1], repeat=5):
        a,L,x,R,b = s
        p = F(1,32)*(1+t**(n-4)*a*b)/(1+tn)
        for j in range(4): p *= 1+t*s[j]*s[j+1]
        total_probability += p
        w0 = (1-F(1,2)*gamma*x*(L+R))/2
        w = w0*(1 if L==R else 2)
        ref = 2*w0*x/gap
        # h(L,R)=L or R spans all spin-reversal-odd two-exterior-spin functions.
        qs=[]
        p_right = pair_conditional(t,L,x,R,b)
        p_left = pair_conditional(t,a,L,x,R)
        for k in range(2):
            hr = L if k==0 else b
            hl = a if k==0 else R
            qs.append(x*R*hr/p_right - L*x*hl/p_left)
        U0 += F(n,2)*p*ref*ref/w
        for j in range(2):
            cross[j] += F(n,2)*p*ref*qs[j]/w
            for k in range(2): gram[j][k] += F(n,2)*p*qs[j]*qs[k]/w
        S=a*L+L*R+R*b
        hMM += 2*n*p*w
        hMT += 2*n*p*w*S
        hTT += 2*n*p*w*S*S
    assert total_probability == 1
    det = gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]
    assert det > 0
    opt = [(-gram[1][1]*cross[0]+gram[0][1]*cross[1])/det,
           (gram[1][0]*cross[0]-gram[0][0]*cross[1])/det]
    upper = U0+sum(c*k for c,k in zip(cross,opt))
    bM=V; bT=V-n*(1-C2)
    lower = V*V/hMM
    detH = hMM*hTT-hMT*hMT
    lower2 = (hTT*bM*bM-2*hMT*bM*bT+hMM*bT*bT)/detH
    assert lower <= lower2 <= upper <= U0
    result = {
        "n":n,"linear_lower":float(lower),"local_MT_lower":float(lower2),
        "reference_flow_upper":float(U0),"local_square_flow_upper":float(upper),
        "linear_to_square_relative_width":float((upper-lower)/lower),
        "local_primal_dual_relative_width":float((upper-lower2)/lower2),
        "relative_upper_improvement":float((U0-upper)/U0),
        "cycle_coefficients":[float(k) for k in opt],
        "local_patterns":32,"seconds":time.perf_counter()-start,
        "arithmetic":"Exact Fraction local transfer sums, current divergence proved algebraically; decimals are summaries"
    }
    return result


if __name__ == "__main__":
    out=[]
    for n in [6,8,10,12,16,32,64,128,256,1024]:
        r=solve(n);out.append(r);print(json.dumps(r),flush=True)
    Path(__file__).with_name("critical_cycle_flow_results.json").write_text(json.dumps(out,indent=2)+"\n")
