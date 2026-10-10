#!/usr/bin/env python3
"""High-precision gain-2 verification for f=g proportional to |0>+|3>/50."""
import json, math
from pathlib import Path
import mpmath as mp
import sys
sys.path.insert(0,str(Path(__file__).parent))
import probe

mp.mp.dps=80
G=mp.mpf(2); t=mp.mpf(1000)
lam=1/mp.sqrt(2)
root=mp.sqrt(2501)
coeff={0:mp.mpf(50)/root,3:mp.mpf(1)/root}

def amplitude(m,n,j,k):
    a,b=m-j,n-j
    pref=(-1 if j%2 else 1)*mp.power(lam,j+k)*mp.power(G,-mp.mpf(m+n-2*j+1)/2)
    fac=mp.sqrt(mp.factorial(m)*mp.factorial(n)*mp.factorial(a+k)*mp.factorial(b+k))/(mp.factorial(j)*mp.factorial(k)*mp.factorial(a)*mp.factorial(b))
    return pref*fac

def calc(M):
    psi=[[mp.mpf('0') for q in range(M+1)] for p in range(M+1)]
    for m,fm in coeff.items():
      for n,gn in coeff.items():
       for j in range(min(m,n)+1):
        a,b=m-j,n-j
        maxk=(M-a-b)//2
        for k in range(maxk+1):
         p,q=a+k,b+k
         psi[p][q]+=fm*gn*amplitude(m,n,j,k)
    # rho has p-p' divisible by 3 because input number differences are in {-3,0,3};
    # sum logdet of independent residue-class blocks.
    logdet=mp.mpf('0')
    traces=[]
    for residue in range(3):
      inds=list(range(residue,M+1,3)); d=len(inds)
      R=mp.matrix(d,d)
      for i,p in enumerate(inds):
       for j,p2 in enumerate(inds):
        R[i,j]=sum(psi[p][q]*psi[p2][q] for q in range(M+1))
      A=mp.eye(d)+t*R
      L=mp.cholesky(A)
      logdet+=2*sum(mp.log(L[i,i]) for i in range(d))
      traces.append(mp.fsum(R[i,i] for i in range(d)))
    thermal=mp.fsum(mp.log1p(t*mp.power(2,-n-1)) for n in range(1500))
    b=probe.tails([complex(coeff[0]),0,0,complex(coeff[3])],[complex(coeff[0]),0,0,complex(coeff[3])],2.0,M)
    tailerr=2*float(t)*math.sqrt(b['probability_bound'])
    return {"M":M,"logdet_output_mp":str(logdet),"logdet_thermal_mp":str(thermal),"gap_mp":str(logdet-thermal),
            "cut_trace_mp":str(sum(traces)),"tail_probability_bound":b['probability_bound'],"logdet_tail_error_bound":tailerr}

results=[calc(M) for M in (100,120,150,180,220)]
out={"mp_dps":mp.mp.dps,"G":2,"t":1000,"input":"f=g=(50|0>+|3>)/sqrt(2501)","results":results}
path=Path(__file__).with_name('counterexample_mp_results.json')
path.write_text(json.dumps(out,indent=2))
for r in results: print(r)
print('wrote',path)
