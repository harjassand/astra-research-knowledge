"""Exact finite-replica formula, with floating-point diagnostic evaluation.

The replica transfer is exponential in k.  This executable intentionally
limits construction to k<=2.  It does not infer a spectral density from two
moments.  JSON is overwritten at the explicit --output path.
"""
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from singular_gap_profile import local_transfer, channel


def transfer(k,theta):
    if k not in (1,2):
        raise ValueError('This diagnostic deliberately permits only k=1,2.')
    g=local_transfer(theta).reshape(4,4,4,4)
    blocks={(q,p):g[:,q,:,p] for q in range(4) for p in range(4)}
    m=np.zeros((4**(2*k),4**(2*k)))
    for xs in itertools.product(range(4),repeat=2*k):
        z=np.ones((1,1))
        for r in range(2*k):
            a,b=xs[r],xs[(r+1)%(2*k)]
            z=np.kron(z,blocks[(a,b) if r%2==0 else (b,a)])
        m+=z
    return m


def dense_moment(n,theta,k):
    t=channel(n,theta); eye=np.eye(4**n)
    a=np.column_stack([t(eye[:,j]) for j in range(4**n)])
    return float(np.trace(np.linalg.matrix_power(a@a.T,k)))


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    rows=[]
    for theta in (.1,.3,.6):
        mats={k:transfer(k,theta)/4 for k in (1,2)}
        for n in (1,2,3,4,10,100,1000,10000):
            row={'n':n,'theta':theta}
            for k,m in mats.items():
                normalized=float(np.linalg.matrix_power(m,n)[0,0])
                row[f'mu{k}_over_4n']=normalized
                if n<=4:
                    direct=dense_moment(n,theta,k)/(4**n)
                    row[f'mu{k}_dense_difference']=normalized-direct
            row['mu1_exact_difference']=row['mu1_over_4n']-(1+3*np.cos(theta)**(4*n))/4
            c,s=np.cos(theta),np.sin(theta)
            u=c**(2*n); v=(1-s**4)**n
            w=(c*c*(c*c-s*s))**n; h=n*c**(2*n-1)*s**3
            closed=(12*h*h+9*u*u+4*v*v-6*v+5*w*w+4)/16
            row['mu2_closed_difference']=row['mu2_over_4n']-closed
            rows.append(row); print(json.dumps(row),flush=True)
    args.output.write_text(json.dumps(rows,indent=2)+'\n')
