"""Independent exact generator checks; no sampling or source observations."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json
import time


def mul(a,b):
    return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]


def tr(a):
    return [list(r) for r in zip(*a)]


def inv(a):
    n=len(a)
    z=[[F(x) for x in r]+[F(i==j) for j in range(n)] for i,r in enumerate(a)]
    for j in range(n):
        i=next(i for i in range(j,n) if z[i][j])
        z[j],z[i]=z[i],z[j]
        s=z[j][j]; z[j]=[x/s for x in z[j]]
        for i in range(n):
            if i!=j:
                s=z[i][j]; z[i]=[x-s*y for x,y in zip(z[i],z[j])]
    return [r[n:] for r in z]


def block(a,rows,cols):
    return [[a[i][j] for j in cols] for i in rows]


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def cycle(a,v,p,q):
    for i,j in zip(v,v[1:]+v[:1]):
        a[i][j]+=p; a[j][i]+=q


def gen(a,w):
    n=len(w)
    assert all(wi>0 for wi in w)
    assert all(a[i][j]>=0 for i in range(n) for j in range(n))
    assert all(sum(a[i])==sum(r[i] for r in a) for i in range(n))
    q=[[a[i][j]/w[i] for j in range(n)] for i in range(n)]
    for i in range(n): q[i][i]=-sum(q[i])
    return q


def record(q,w):
    B=[0,1]; I=list(range(2,len(w)))
    L=[[-w[i]*q[i][j] for j in range(len(w))] for i in range(len(w))]
    G=inv(block(L,I,I)); A=block(L,B,I); C=block(L,I,B)
    product=mul(mul(A,G),C)
    S=[[L[i][j]-product[i][j] for j in B] for i in B]
    wi=[[w[i]] for i in I]
    br=[w[i]-x[0] for i,x in enumerate(mul(mul(A,G),wi))]
    bl=[w[i]-x[0] for i,x in enumerate(mul(mul(tr(C),tr(G)),wi))]
    c=mul(mul(tr(wi),G),wi)[0][0]
    return dict(S=S,w_B=w[:2],b_R=br,b_L=bl,c=c)


def dec(x):
    return Decimal(x.numerator)/Decimal(x.denominator)


def entropy(a):
    E=Decimal(0)
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            p,q=a[i][j],a[j][i]
            if bool(p)!=bool(q): return 'infinite'
            if p and p!=q: E+=dec(p-q)*dec(p/q).ln()
    return E


def four(beta):
    p=1-beta; a=zero(4); w=[F(1)]*4
    cycle(a,[0,2,1,3],p,beta)
    a[0][1]=a[1][0]=2*p*beta
    q=gen(a,w); r=record(q,w); E=entropy(a)
    assert r['S']==[[1,-1],[-1,1]]
    assert r['b_R']==r['b_L']==[2,2] and r['c']==2
    rates=[-q[i][i] for i in range(4)]
    assert rates==[1+2*p*beta,1+2*p*beta,1,1]
    A=4*p*beta
    if beta:
        target=4*dec(p-beta)*dec(p/beta).ln()
        assert abs(E-target)<Decimal('1e-70')
        floor=4*dec(1/A).ln() if A<1 else Decimal(0)
        assert E>=floor
    else:
        assert E=='infinite'; target=floor='infinite'
    return dict(beta=beta,record=r,rates=rates,total_spare=A,
                entropy=E,frontier=target,robust_lower=floor)


def triangle(beta):
    a=zero(3); w=[F(1)]*3; cycle(a,[0,2,1],F(1),beta)
    q=gen(a,w); r=record(q,w); E=entropy(a)
    assert r['S'][0][1]==r['S'][1][0]
    d=[x-y for x,y in zip(r['b_R'],r['b_L'])]
    lb=sum(map(abs,d))**2/(4*r['c'])
    assert E>dec(lb)>0
    return dict(beta=beta,record=r,entropy=E,asymmetry_lower=lb)


def invisible(beta):
    a=zero(5); w=[F(1),F(1),F(1,3),F(1,3),F(1,3)]
    a[0][1]=a[1][0]=F(1,2)
    for i in [2,3,4]: a[0][i]=a[i][0]=F(1,3)
    cycle(a,[2,3,4],F(1,6),beta/3)
    q=gen(a,w); r=record(q,w); E=entropy(a)
    assert r['S']==[[F(1,2),F(-1,2)],[F(-1,2),F(1,2)]]
    assert r['b_R']==r['b_L']==[2,1] and r['c']==1
    rates=[-q[i][i] for i in range(5)]
    assert rates[:2]==[F(3,2),F(1,2)] and max(rates)<=2
    transforms=[]
    for s in [F(0),F(1,3),F(1),F(3),F(11)]:
        K=[[(s if i==j else 0)-q[i][j] for j in [2,3,4]] for i in [2,3,4]]
        f=mul(inv(K),[[F(1)]]*3)
        assert f==[[1/(1+s)]]*3
        transforms.append(dict(s=s,values=[z[0] for z in f]))
    target=dec(F(1,2)-beta)*dec(F(1,2)/beta).ln()
    assert abs(E-target)<Decimal('1e-70')
    return dict(beta=beta,record=r,rates=rates,entropy=E,transform_controls=transforms)


def binary_grid():
    count=0
    for i in range(1,40):
        for j in range(1,40):
            p=F(i,40); q=F(j,40); r=p*q+(1-p)*(1-q)
            J=dec(p-q)*dec(p*(1-q)/(q*(1-p))).ln()
            if r<F(1,2):
                d=dec(1-2*r).sqrt()
                g=2*d*((1+d)/(1-d)).ln()
            else: g=Decimal(0)
            assert J+Decimal('1e-70')>=g
            count+=1
    return count


def convert(x):
    if isinstance(x,(F,Decimal)): return str(x)
    if isinstance(x,list): return [convert(y) for y in x]
    if isinstance(x,dict): return {k:convert(y) for k,y in x.items()}
    return x


def main():
    start=time.perf_counter()
    with localcontext() as ctx:
        ctx.prec=85
        fixed=[four(F(1,2**k)) for k in [1,2,4,8,16,32,64]]
        edge=four(F(0))
        invisible_models=[invisible(F(1,2**k)) for k in [1,2,4,8,16,32,64]]
        asymmetric=[triangle(F(1,2**k)) for k in [1,2,4,8,16]]
        grid=binary_grid()
    data=dict(status='PASS',scope='supplied exact rational generators and decimal scalar checks',
              source_observations=0,source_preparations=0,random_draws=0,
              finite_generators=19,infinite_boundary_controls=1,binary_grid_pairs=grid,
              fixed_record_frontier=fixed,zero_return_boundary=edge,
              identical_complete_boundary_law=invisible_models,
              asymmetric_residence=asymmetric,seconds=time.perf_counter()-start,
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(__file__).with_name('THERMODYNAMIC_COMPLETION_CHECKS.json').write_text(json.dumps(convert(data),indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ['status','finite_generators','infinite_boundary_controls','binary_grid_pairs','source_observations','seconds']},indent=2))


if __name__=='__main__': main()
