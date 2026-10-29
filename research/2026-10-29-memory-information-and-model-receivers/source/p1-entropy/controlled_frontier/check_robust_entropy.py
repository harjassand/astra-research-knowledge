#!/usr/bin/env python3
"""Independent exact finite-generator controls for the positive-slack bound.

All algebra is Fraction. Transcendental inequalities use explicit rational
outward log/sqrt intervals, not floating optimizer or comparison status.
No sampling or source observation occurs.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib, json, math, time

ROOT=Path(__file__).resolve().parent
BITS=96

def zeros(n,m=None): return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def tr(a): return list(map(list,zip(*a)))
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def add(a,b,sign=1): return [[x+sign*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sub(a,rr,cc): return [[a[i][j] for j in cc] for i in rr]
def mv(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]
def inv(a):
    n=len(a); z=[row[:]+ident for row,ident in zip(a,eye(n))]
    for j in range(n):
        pivot=next(i for i in range(j,n) if z[i][j])
        z[j],z[pivot]=z[pivot],z[j]
        q=z[j][j]; z[j]=[x/q for x in z[j]]
        for i in range(n):
            if i!=j:
                q=z[i][j]; z[i]=[x-q*y for x,y in zip(z[i],z[j])]
    return [row[n:] for row in z]

def dyadic(lo,hi,bits=BITS):
    d=1<<bits
    l=(lo.numerator*d)//lo.denominator
    h=-((-hi.numerator*d)//hi.denominator)
    return F(l,d),F(h,d)

def log_between_1_2(y,terms=40):
    assert 1<=y<=2
    z=(y-1)/(y+1); p=z; ss=F(0)
    for k in range(terms):
        ss+=2*p/F(2*k+1); p*=z*z
    tail=2*p/(F(2*terms+1)*(1-z*z))
    return ss,ss+tail

@lru_cache(None)
def log_bounds(x):
    assert x>0
    if x==1: return F(0),F(0)
    if x<1:
        l,h=log_bounds(1/x); return -h,-l
    exponent=0; y=x
    while y>=2: y/=2; exponent+=1
    lo,hi=log_between_1_2(y)
    l2,h2=log_between_1_2(F(2))
    return dyadic(lo+exponent*l2,hi+exponent*h2)

def sqrt_bounds(x):
    assert x>=0
    d=1<<BITS
    integer=math.isqrt((x.numerator*d*d)//x.denominator)
    low=F(integer,d)
    high=low if low*low==x else F(integer+1,d)
    assert low*low<=x<=high*high
    return low,high

def g_bounds(r):
    assert r>=0
    if r>=F(1,2): return F(0),F(0)
    if r==0: raise ValueError('Infinite g endpoint is handled separately')
    lo,hi=sqrt_bounds(1-2*r)
    assert hi<1
    llog,_=log_bounds((1+lo)/(1-lo))
    _,hlog=log_bounds((1+hi)/(1-hi))
    return dyadic(2*lo*llog,2*hi*hlog)

def entropy_bounds(flow):
    lo=hi=F(0); n=len(flow)
    for i in range(n):
        for j in range(i):
            x,y=flow[i][j],flow[j][i]
            if x==y: continue
            assert x>0 and y>0
            big,small=max(x,y),min(x,y)
            a,b=log_bounds(big/small)
            lo+=(big-small)*a; hi+=(big-small)*b
    return dyadic(lo,hi)

def jeffreys_bounds(a,b):
    lo=hi=F(0)
    for x,y in zip(a,b):
        if x==y: continue
        assert x>0 and y>0
        big,small=max(x,y),min(x,y)
        l,h=log_bounds(big/small)
        lo+=(big-small)*l; hi+=(big-small)*h
    return dyadic(lo,hi)

def laplacian(flow):
    L=[[-x for x in row] for row in flow]
    for i in range(len(flow)): L[i][i]=sum(flow[i])
    assert all(sum(row)==0 for row in L)
    assert all(sum(col)==0 for col in zip(*L))
    return L

def record(flow,w,m):
    L=laplacian(flow); bi=list(range(m)); ii=list(range(m,len(w)))
    G=sub(L,ii,ii); Gi=inv(G)
    B_I=sub(L,bi,ii); I_B=sub(L,ii,bi)
    S=add(sub(L,bi,bi),mm(mm(B_I,Gi),I_B),-1)
    wi=[w[i] for i in ii]; wb=w[:m]
    br=[x-y for x,y in zip(wb,mv(mm(B_I,Gi),wi))]
    bl=[x-y for x,y in zip(wb,mv(tr(mm(Gi,I_B)),wi))]
    c=sum(x*y for x,y in zip(wi,mv(Gi,wi)))
    rates=[sum(row)/weight for row,weight in zip(flow,w)]
    trace=[[-S[i][j] if i!=j else F(0) for j in bi] for i in bi]
    spare=[w[i]*rates[i]-sum(trace[i]) for i in bi]
    assert all(x>=0 for x in spare)
    return dict(S=S,bR=br,bL=bl,c=c,V=sum(wi),rates=rates,trace=trace,spare=spare)

def four_state(kappa,beta,e):
    p=1-beta; flow=zeros(4)
    cycle=[0,2,1,3]
    for j,i in enumerate(cycle):
        nxt=cycle[(j+1)%4]
        flow[i][nxt]=kappa*p; flow[nxt][i]=kappa*beta
    flow[2][3]=flow[3][2]=e
    current=record(flow,[F(1)]*4,2)
    direct=1-current['trace'][0][1]
    assert direct>=0
    flow[0][1]=flow[1][0]=direct
    return flow,[F(1)]*4

def split_port(flow,w,z):
    # New ports 0,1,2: old port 1 is split with equal weight/edge shares.
    # New hidden states 3,4 correspond to old hidden states 2,3.
    groups=[[(0,F(1))],[(1,F(1,2)),(2,F(1,2))],[(3,F(1))],[(4,F(1))]]
    out=zeros(5); ww=[F(0)]*5
    for i in range(4):
        for ni,si in groups[i]: ww[ni]+=w[i]*si
        for j in range(4):
            for ni,si in groups[i]:
                for nj,sj in groups[j]: out[ni][nj]+=flow[i][j]*si*sj
    out[1][2]+=z; out[2][1]+=z
    return out,ww

def check_case(flow,w,m,kappa,beta,e,within=F(0)):
    r=record(flow,w,m); V=r['V']; c=r['c']; Lambda=F(1)
    assert V==2 and c==2/kappa and c>V
    assert all(rate<=Lambda for rate in r['rates'][m:])
    assert r['bR']==r['bL']
    if m==2: assert r['S']==[[F(1),F(-1)],[F(-1),F(1)]]
    E=entropy_bounds(flow)
    analytic=log_bounds((1-beta)/beta)
    coeff=4*kappa*(1-2*beta)
    assert E[0]<=coeff*analytic[1] and E[1]>=coeff*analytic[0]
    h1=F(0); return1=F(0); group_return1=F(0); e1lo=e1hi=F(0)
    # Group cut is {0} versus every other port.
    for x in range(m,len(w)):
        aa=[flow[i][x] for i in range(m)]; bb=[flow[x][i] for i in range(m)]
        ax=sum(aa); bx=sum(bb)
        if not ax*bx: continue
        h=ax*bx/(Lambda*w[x]); h1+=h
        alpha=[v/ax for v in aa]; beta_law=[v/bx for v in bb]
        return1+=h*sum(a*b for a,b in zip(alpha,beta_law))
        group_return1+=h*(alpha[0]*beta_law[0]+(1-alpha[0])*(1-beta_law[0]))
        el,eh=jeffreys_bounds(alpha,beta_law)
        e1lo+=h*el; e1hi+=h*eh
    assert h1==2*kappa*kappa
    delta=Lambda*c-V; h0=max(Lambda*(V-2*delta),F(0))
    assert h1>=h0
    A=sum(r['spare'])
    assert return1<=A
    cut_budget=A+sum(r['trace'][i][j] for i in range(1,m) for j in range(1,m) if i!=j)
    assert group_return1<=cut_budget
    if m==2: assert cut_budget==A
    assert e1lo<=kappa*E[1] and e1hi>=kappa*E[0]
    assert E[0]>=e1hi or E[1]==e1lo==0
    if h0>0 and cut_budget/h0<F(1,2):
        gl,gh=g_bounds(cut_budget/h0)
        bound=dyadic(h0*gl,h0*gh)
        assert E[0]>bound[1]
    else: bound=(F(0),F(0))
    return {"ports":m,"kappa":kappa,"beta":beta,"hidden_symmetric_rate":e,
            "within_group_symmetric_flow":within,"weights":w,"flows":flow,
            "record":r,"h1":h1,"h0":h0,"delta":delta,"one_tick_self_return":return1,
            "one_tick_same_group_flux":group_return1,"A":A,"cut_budget":cut_budget,
            "E_interval":E,"one_tick_entropy_interval":dyadic(e1lo,e1hi),
            "robust_lower_bound_interval":bound,"strictly_positive_lower_bound":bool(bound[0]>0),
            "exact_and_interval_checks":"PASS"}

def ser(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:ser(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [ser(v) for v in x]
    return x

def main():
    start=time.perf_counter(); cases=[]
    for kappa in [F(9,10),F(4,5),F(7,10),F(1,2)]:
        for e in [F(0),1-kappa]:
            for beta in [F(1,2),F(1,4),F(1,10),F(1,100),F(1,10000)]:
                flow,w=four_state(kappa,beta,e)
                cases.append(check_case(flow,w,2,kappa,beta,e))
                for z in [F(0),F(1,100)]:
                    ff,ww=split_port(flow,w,z)
                    cases.append(check_case(ff,ww,3,kappa,beta,e,z))
    result={"scope":"Independent positive-clock-slack bound and multiport cut; exact finite supplied generators",
            "cases":cases,"case_count":len(cases),"positive_lower_bounds":sum(x['strictly_positive_lower_bound'] for x in cases),
            "binary_cases":sum(x['ports']==2 for x in cases),"three_port_cut_cases":sum(x['ports']==3 for x in cases),
            "hidden_native_rate_saturating_cases":sum(x['kappa']+x['hidden_symmetric_rate']==1 for x in cases),
            "zero_h0_controls":sum(x['h0']==0 for x in cases),"source_observations":0,"resets":0,
            "transcendental_certificate":"Rational Taylor log intervals, integer-square-root dyadic brackets, outward rational rounding",
            "wall_seconds":time.perf_counter()-start,"code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'ROBUST_ENTROPY_CHECKS.json').write_text(json.dumps(ser(result),indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))

if __name__=='__main__': main()
