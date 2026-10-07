#!/usr/bin/env python3
"""Own exact algebra checks for direct filtered fitting; no peer imports."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime,hashlib,json,signal,time
from independent_exact_checks import (sector,zero,identity,mm,linear,
                                      projector,direct_k,trace_pair)


def run():
    t0=time.monotonic()
    checks=0
    column_cases=0
    floor_cases=0
    for n in range(1,33):
        m=n//2+1
        # Zeros are allowed in acquired global data. Keep the endpoint positive.
        values=[F(0) if t%3==0 else F(1,t+1) for t in range(n+1)]
        values[n]=F(1,2**n)
        prefix=[F(0)]
        for v in values: prefix.append(prefix[-1]+v)
        c=[(prefix[n-b+1]-prefix[b])/F(n-2*b+1) for b in range(m)]
        a=[[sector(n,b,k) for b in range(m)] for k in range(n+1)]
        z=[sum((a[k][b]*c[b] for b in range(m)),F(0)) for k in range(n+1)]
        columns=[[a[k][b]*c[b]/z[k] for b in range(m)] for k in range(n+1)]
        for k in range(n+1):
            assert k+1<=2**k
            assert z[k]>=F(1,2**(2*n))
            assert all(x>=0 for x in columns[k])
            assert sum(columns[k],F(0))==1
            r=n-k
            branch=[F(comb(r,u),(k+1)*2**r)*(prefix[u+k+1]-prefix[u])
                    for u in range(r+1)]
            assert sum(branch,F(0))==z[k]
            assert sum((x/z[k] for x in branch),F(0))==1
            checks+=6
            column_cases+=1
            floor_cases+=1
        w=[F(1,n+1)]*(n+1)
        q=[sum((w[k]*a[k][b] for k in range(n+1)),F(0)) for b in range(m)]
        beta=sum((q[b]*c[b] for b in range(m)),F(0))
        v=[w[k]*z[k]/beta for k in range(n+1)]
        filtered_q=[q[b]*c[b]/beta for b in range(m)]
        mixture_q=[sum((v[k]*columns[k][b] for k in range(n+1)),F(0))
                   for b in range(m)]
        assert sum(v,F(0))==1
        assert mixture_q==filtered_q
        inv=[v[k]/z[k] for k in range(n+1)]
        assert [x/sum(inv,F(0)) for x in inv]==w
        # Target normalizer floor needs only r0=1 and nonnegative other r.
        db=[(n-2*b+1)*(comb(n,b)-(comb(n,b-1) if b else 0)) for b in range(m)]
        losses=[F(1) if b==0 else F(b%2,b+1) for b in range(m)]
        target_norm=sum((db[b]*losses[b]*c[b] for b in range(m)),F(0))
        assert target_norm>=F(1,2**n)
        checks+=4

    dense_entries=0
    metric_cases=0
    for n in range(1,5):
        d=2**n
        m=n//2+1
        p=[projector(n,b) for b in range(m)]
        dims=[sum(pb[i][i] for i in range(d)) for pb in p]
        xs=[F(1,m)]*m
        ys=[F(b+1,m*(m+1)//2) for b in range(m)]
        values=[F(3)**(2*t-n)/F(7)**((2*t-n)**2) for t in range(n+1)]
        c=[sum(values[b:n-b+1],F(0))/F(n-2*b+1) for b in range(m)]
        bx=sum((xs[b]*c[b] for b in range(m)),F(0))
        by=sum((ys[b]*c[b] for b in range(m)),F(0))
        gx=zero(d); gy=zero(d)
        for b in range(m):
            gx=linear(gx,p[b],F(1),xs[b]/dims[b])
            gy=linear(gy,p[b],F(1),ys[b]/dims[b])
        fx=[[values[i.bit_count()]*gx[i][j]/bx for j in range(d)] for i in range(d)]
        fy=[[values[i.bit_count()]*gy[i][j]/by for j in range(d)] for i in range(d)]
        difference=linear(fx,fy,F(1),-F(1))
        spectral=zero(d)
        norm=F(0)
        for b in range(m):
            mult=comb(n,b)-(comb(n,b-1) if b else 0)
            for t in range(n+1):
                e=[[p[b][i][j] if j.bit_count()==t else F(0)
                    for j in range(d)] for i in range(d)]
                tr=sum(e[i][i] for i in range(d))
                assert tr==(mult if b<=t<=n-b else 0)
                assert mm(e,e)==e
                lam=values[t]*(xs[b]/(dims[b]*bx)-ys[b]/(dims[b]*by))
                spectral=linear(spectral,e,F(1),lam)
                norm+=abs(lam)*tr
                checks+=2
        assert spectral==difference
        tv=sum((abs(xs[b]*c[b]/bx-ys[b]*c[b]/by) for b in range(m)),F(0))/2
        assert norm/2==tv
        checks+=d*d+1
        dense_entries+=d*d
        metric_cases+=1
    return {'status':'PASS','counted_exact_checks':checks,
            'combinatorial_N_range':[1,32], 'normalized_column_cases':column_cases,
            'normalizer_floor_cases':floor_cases,'dense_N_range':[1,4],
            'full_spectral_metric_cases':metric_cases,
            'full_difference_matrix_entries_compared':dense_entries,
            'elapsed_seconds':time.monotonic()-t0,
            'scope':'exact finite algebra and boundary data; no exponentials, optimizer, generic iid backend or hardware'}


if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('30-second audit cap')))
    signal.alarm(30)
    result=run()
    result['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
