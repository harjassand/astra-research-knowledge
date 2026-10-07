#!/usr/bin/env python3
"""Own bounded exact checks for regularization and rational pure output."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime,hashlib,json,signal,time


def ldlt(a,allow_last_zero=False):
    d=len(a); l=[[F(int(i==j)) for j in range(d)] for i in range(d)]; p=[]
    for i in range(d):
        pivot=a[i][i]-sum((l[i][k]**2*p[k] for k in range(i)),F(0))
        assert pivot>0 or (allow_last_zero and i==d-1 and pivot==0)
        p.append(pivot)
        for j in range(i+1,d):
            l[j][i]=(a[j][i]-sum((l[j][k]*l[i][k]*p[k]
                                  for k in range(i)),F(0)))/pivot
    return p


def solve(a,b):
    d=len(a); t=[list(row)+[x] for row,x in zip(a,b)]
    for i in range(d):
        if t[i][i]==0:
            j=next(j for j in range(i+1,d) if t[j][i])
            t[i],t[j]=t[j],t[i]
        c=t[i][i]; t[i]=[x/c for x in t[i]]
        for j in range(d):
            if j!=i:
                c=t[j][i]; t[j]=[x-c*y for x,y in zip(t[j],t[i])]
    return [t[i][-1] for i in range(d)]


def minus(a,b):
    return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def sphere(t,s):
    r=sum((x*x for x in t),F(0)); den=1+r
    return [2*t[0]/den,2*t[1]/den,s*(1-r)/den]


def run():
    begin=time.monotonic(); checks=0; gram_cases=0; max_bits=0
    measures=[[(F(0),F(1))],[(F(1),F(1))],[(F(1,2),F(1))],
              [(F(1,5),F(2,7)),(F(3,4),F(5,7))]]
    for n in range(1,13):
        d=n//2+1
        for atoms in measures:
            pi=[sum((w*comb(n,k)*p**k*(1-p)**(n-k) for p,w in atoms),F(0))
                for k in range(n+1)]
            assert sum(pi,F(0))==1
            checks+=1
            for exponent in (3,12,40):
                eta=F(1,2**exponent)
                preg=[(1-eta)*x+eta/F(n+1) for x in pi]
                u=[(1-eta)*sum((w*p**j for p,w in atoms),F(0))+eta/F(j+1)
                   for j in range(n+2)]
                acquired=[sum((F(comb(k,j),comb(n,j))*preg[k]
                                for k in range(j,n+1)),F(0)) for j in range(n+1)]
                assert acquired==u[:n+1]
                checks+=n+1
                h=[[u[i+j] for j in range(d)] for i in range(d)]
                alpha=eta/F(2**(2*d)*(4*d)**(d*d+d))
                for shift in (0,1):
                    g=[[u[i+j+shift] for j in range(d)] for i in range(d)]
                    guarded=[[g[i][j]-(alpha if i==j else 0)
                              for j in range(d)] for i in range(d)]
                    ldlt(guarded)
                    checks+=d
                k=[[u[i+j+1] for j in range(d)] for i in range(d)]
                if n%2==0:
                    a=[row[:d-1] for row in k[:d-1]]
                    v=[k[i][d-1] for i in range(d-1)]
                    solution=solve(a,v)
                    k[d-1][d-1]=sum((x*y for x,y in zip(v,solution)),F(0))
                    assert ldlt(k,True)[-1]==0
                    checks+=d+1
                else:
                    ldlt(k); checks+=d
                ldlt(minus(h,k)); checks+=d
                for matrix in (h,k):
                    for row in matrix:
                        for x in row:
                            max_bits=max(max_bits,x.numerator.bit_length(),x.denominator.bit_length())
                max_bits=max(max_bits,alpha.denominator.bit_length())
                gram_cases+=1
    singular_cases=0
    for b in range(1,65):
        eta=F(1,2**b)
        u1=F(1,2); u2=F(1,4)+eta/12
        assert u2-u1*u1==eta/12
        x=u2/u1; w=u1*u1/u2
        populations=[1-2*u1+u2,2*(u1-u2),u2]
        represented=[1-w+w*(1-x)**2,2*w*x*(1-x),w*x*x]
        assert represented==populations
        assert 0<x<1 and 0<w<1 and 1-w==eta/(3+eta)
        checks+=5; singular_cases+=1
    stereo_cases=0
    for s in (-1,1):
        for t in ([F(0),F(0)],[F(1),F(0)],[F(1,3),-F(4,5)],
                  [F(2),-F(3)]):
            for b in (3,12,40):
                u=[t[0]+F(1,2**b),t[1]-F(1,2**b)]
                bt=sphere(t,s); bu=sphere(u,s)
                for point in (bt,bu):
                    assert sum((x*x for x in point),F(0))==1
                    assert -1<=point[2]<=1
                    d0=(1-point[2])/2; d1=(1+point[2])/2
                    assert d0+d1==1
                    assert d0*d1-(point[0]**2+point[1]**2)/4==0
                    checks+=4
                diff=sum(((x-y)**2 for x,y in zip(bt,bu)),F(0))
                td=sum(((x-y)**2 for x,y in zip(t,u)),F(0))
                den=(1+sum((x*x for x in t),F(0)))*(1+sum((x*x for x in u),F(0)))
                assert diff*den==4*td
                assert diff/4<=td
                checks+=2; stereo_cases+=1
    rounded_cases=0
    for m in range(1,41):
        weights=[F(j+1,m*(m+1)//2) for j in range(m)]
        q=2**(m.bit_length()+12)
        nums=[(x*q).numerator//(x*q).denominator for x in weights[:-1]]
        nums.append(q-sum(nums))
        rounded=[F(x,q) for x in nums]
        assert sum(nums)==q and all(x>=0 for x in nums)
        tv=sum((abs(x-y) for x,y in zip(weights,rounded)),F(0))/2
        assert tv<=F(m-1,q)
        checks+=2; rounded_cases+=1
    return {'status':'PASS','counted_exact_checks':checks,'N_range':[1,12],
            'uniform_component_gram_cases':gram_cases,'singular_N2_cases':singular_cases,
            'stereographic_cases':stereo_cases,'dyadic_weight_cases':rounded_cases,
            'largest_observed_numerator_or_denominator_bits':max_bits,
            'elapsed_seconds':time.monotonic()-begin,
            'scope':'finite exact identities/guards; no peer code, full quadrature backend, or hardware execution'}


if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('30-second cap')))
    signal.alarm(30)
    result=run(); result['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
