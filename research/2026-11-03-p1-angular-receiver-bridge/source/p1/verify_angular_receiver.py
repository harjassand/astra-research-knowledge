"""Exact-rational diagnostics for the six-species angular receiver.
All formulas use falling factorial mass action; checks are finite diagnostics,
not substitutes for the symbolic all-population arguments.
"""
from fractions import Fraction as Q
from itertools import product
from random import Random

def fall(n,k):
    z=1
    for j in range(k): z*=n-j
    return z if n>=k else 0

def work(x,w=20):
    out=0
    for b,c in ((x[1],x[2]),(x[4],x[5])):
        r=b-c; t=min(b,c)
        out+=3*max(r,0)+w*max(-r,0)+2*(t%2)+t//2
    return out

def h(b,c):
    t=min(b,c)
    return abs(b-c)+(3*t+(t%2))//2

def angle(x,w=20):
    a,b,c,d,e,f=x
    s=b+c+e+f; t=a+d; z=max(s-work(x,w),0)
    return Q(s*z,s+t+1)

def ang_sq(x,w=20):
    z=angle(x,w)
    return z*z

def channels(x, rates):
    a,b,c,d,e,f=x
    # integer tuples: state change, rate, source id
    dA=((1,1,0,0,0,0),(1,0,1,0,0,0),(1,1,1,0,0,0),(-3,-2,-2,0,0,0))
    dD=((0,0,0,1,1,0),(0,0,0,1,0,1),(0,0,0,1,1,1),(0,0,0,-3,-2,-2))
    pa=[rates[i]*v for i,v in enumerate((1,a*b,fall(a,2)*b*c,fall(a,3)*fall(b,2)*fall(c,2)))]
    pb=[rates[i+4]*v for i,v in enumerate((1,d*e,fall(d,2)*e*f,fall(d,3)*fall(e,2)*fall(f,2)))]
    core=((0,-2,-2,0,2,2),(0,2,2,0,-2,-2))
    pc=(rates[8]*a*d*fall(b,2)*fall(c,2),rates[9]*a*d*fall(e,2)*fall(f,2))
    for i,(v,z) in enumerate(list(zip(dA,pa))+list(zip(dD,pb))+list(zip(core,pc))):
        if z:
            y=tuple(k+v0 for k,v0 in zip(x,v))
            assert min(y)>=0
            yield i, z,y

def quadratic(x, gamma=Q(1), eta=Q(1),w=20,c0=100):
    a,b,c,d,e,f=x
    p=work(x,w)+c0
    gs=max(a-h(b,c),0)**2+max(d-h(e,f),0)**2
    return eta*gs+gamma*(p*p+ang_sq(x,w)/3)

def check():
    rng=Random(67321)
    cases=0; trans=0; termini=0; cores=0; ready_good=0
    for j in range(28000):
        x=tuple(rng.randrange(0,34) for _ in range(6))
        rates=tuple(rng.randrange(1,29) for _ in range(10))
        s=x[1]+x[2]+x[4]+x[5]
        p=work(x)
        assert Q(p)>=Q(s,4)
        assert Q(p)-Q(s,4)==Q(11,4)*(max(x[1]-x[2],0)+max(x[4]-x[5],0))+ (Q(20)-Q(1,4))*(max(x[2]-x[1],0)+max(x[5]-x[4],0))+Q(3,2)*(min(x[1],x[2])%2+min(x[4],x[5])%2)
        v=ang_sq(x)
        counts=0
        for i,z,y in channels(x,rates):
            trans+=1
            vy=ang_sq(y)
            if i>=8:
                cores+=1
                assert v==vy, ("core not invariant",x,y,i)
            elif i in (3,7):
                termini+=1
                assert vy<=v, ("terminal increased angular",x,y,v,vy)
                assert quadratic(y)-quadratic(x)<=-(2*(work(x)+100)-1), ("terminal full receiver inequality",x,y)
            else:
                assert abs(angle(y)-angle(x))<=25 # w+5
            if min(x[0]-h(x[1],x[2]),x[3]-h(x[4],x[5]))<=-3 and i<10:
                # If both input margins >=3, g=0 at all one-jump endpoints.
                if h(x[1],x[2])>=x[0]+3 and h(x[4],x[5])>=x[3]+3:
                    assert y[0]-h(y[1],y[2])<=0 and y[3]-h(y[4],y[5])<=0
        cases+=1
    for n in [20,100,1000]:
        x=(3,n,n,3,n,n)
        rates=(1,)*10
        a,b,c,d,e,f=x
        t_total=6*fall(b,2)*fall(c,2)*2
        g_total=2*(1+3*n+6*n*n)
        assert t_total>g_total*20
        drift=sum(z*(quadratic(y)-quadratic(x)) for i,z,y in channels(x,rates))
        assert drift<0
        ready_good+=1
    print({"random_states":cases,"actual_transitions":trans,"core_checks":cores,"terminal_monotonicity_checks":termini,"balanced_drift_checks":ready_good,"status":"PASS"})

if __name__=='__main__':check()
