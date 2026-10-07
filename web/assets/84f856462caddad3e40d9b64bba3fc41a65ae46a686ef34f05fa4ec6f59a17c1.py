"""Bounded high precision moment diagnostics; no universal proof claimed."""
from pathlib import Path
import json
import time
import mpmath as mp

mp.mp.dps=100


def moments(N, delta):
    return [mp.exp(-delta*(mp.mpf(k)-mp.mpf(N)/2)**2/N)/mp.binomial(N,k)
            for k in range(N+1)]


def matrix(N,delta,offset):
    q=moments(N,delta)
    size=(N-offset)//2+1
    return mp.matrix([[q[i+j+offset]/mp.sqrt(q[2*i+offset]*q[2*j+offset])
                       for j in range(size)] for i in range(size)])


def ldl(A):
    n=A.rows
    L=mp.eye(n)
    D=[]
    for i in range(n):
        d=A[i,i]-sum(L[i,k]**2*D[k] for k in range(i))
        D.append(d)
        if abs(d)<mp.mpf('1e-80'):
            return D, 'NUMERIC_SINGULAR'
        if d<0:
            return D, 'NEGATIVE_PIVOT'
        for j in range(i+1,n):
            L[j,i]=(A[j,i]-sum(L[j,k]*L[i,k]*D[k] for k in range(i)))/d
    return D,'POSITIVE_NUMERIC'


def main():
    start=time.perf_counter()
    rows=[]
    delta=2*mp.log(2)
    for N in list(range(2,33))+[40,48,64]:
        record={'N':N,'delta':str(delta),'matrices':[]}
        for offset in [0,1]:
            D,status=ldl(matrix(N,delta,offset))
            record['matrices'].append({'offset':offset,'status':status,
                                      'min_pivot':mp.nstr(min(D),20),
                                      'pivots_completed':len(D)})
        rows.append(record)
    out={'scope':'High-precision finite diagnostics only. No all-N theorem, interval certificate, or SDP inference.',
         'precision_digits':mp.mp.dps,'rows':rows,'runtime_seconds':time.perf_counter()-start}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'runtime_seconds':out['runtime_seconds'],'rows':rows},indent=2))


if __name__=='__main__':
    main()
