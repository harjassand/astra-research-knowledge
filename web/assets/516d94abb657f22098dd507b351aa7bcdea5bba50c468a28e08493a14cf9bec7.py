"""Sufficient Gaussian-removal bound via conditional PSD of log Hankel.
This is a sufficient criterion, never a separability obstruction.
"""
import math,json,time
from pathlib import Path
import mpmath as mp

def bound(N,shift):
    m=(N-shift)//2
    if m==0: return 'inf'
    A=mp.matrix(m)
    for i in range(m):
        for j in range(m):
            k=i+j+shift
            A[i,j]=mp.log(mp.mpf(k+2)/(k+1)*mp.mpf(N-k)/(N-k-1))
    z=mp.lu_solve(A,mp.matrix([1]*m))
    return str(mp.mpf(N)/(2*sum(z)))

if __name__=='__main__':
    rows=[]
    for N in [2,3,4,6,8,16,32,64,128]:
        mp.mp.dps=2*N+50
        t=time.monotonic()
        row={'N':N,'delta_sufficient_by_CPSD':min(mp.mpf(bound(N,0)),mp.mpf(bound(N,1))),'seconds':time.monotonic()-t}
        row['delta_sufficient_by_CPSD']=str(row['delta_sufficient_by_CPSD'])
        print(json.dumps(row),flush=True);rows.append(row)
    Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2))
