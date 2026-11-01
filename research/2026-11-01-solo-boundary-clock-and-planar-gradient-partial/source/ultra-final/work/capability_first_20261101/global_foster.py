"""Exact actual-generator receiving for the completed directed cubic prototype."""
from fractions import Fraction as F
from math import isqrt, prod
from pathlib import Path
import json

# Raw reaction vectors and rates are reconstructed here; no numerical solver
# or generator evaluator from the resolvent implementation is imported.
FOUR_CYCLE=[((2,1,0),(0,2,1),1),((0,2,1),(1,0,2),2),
            ((1,0,2),(1,1,1),3),((1,1,1),(2,1,0),5)]


TILT=F(33,32)


def parts(x):
    a,b,c=x
    u,v=a+3*c+6,3*a+b+6
    zb,zc=F(1,u),F(1,v)
    hb=3 if a==c==0 else 2 if a==1 and c==0 else 0
    hc=int(a==0 and b<=1)
    h=1+(zb+zc)/726+F(hb+hc,16)
    return zb+zc,hb,hc,h


def transitions(x):
    a,b,c=x
    yield (a+1,b,c),1,1
    if a:yield (a-1,b,c),a,-1
    for src,dst,coefficient in FOUR_CYCLE:
        if all(xx>=yy for xx,yy in zip(x,src)):
            rate=coefficient*prod(prod(range(xx-yy+1,xx+1)) for xx,yy in zip(x,src))
            target=tuple(xx-yy+zz for xx,yy,zz in zip(x,src,dst))
            yield target,rate,0


def check_state(x):
    a,b,c=x;n=sum(x);zp,hb,hc,h=parts(x)
    lz=F(0);lhb=F(0);lhc=F(0);tilted=F(0)
    for y,rate,dn in transitions(x):
        zpy,hby,hcy,hy=parts(y)
        lz+=rate*(zpy-zp);lhb+=rate*(hby-hb);lhc+=rate*(hcy-hc)
        tilted+=rate*(TILT**dn*hy-h)
    r1=a*(a-1)*b;r2=2*b*(b-1)*c;r3=3*a*c*(c-1);r4=5*a*b*c
    u,v=a+3*c+6,3*a+b+6
    service=F(r1,2*u*u)+F(r2,u*u)+F(r2+r3,2*v*v)+F(2*r4,v*v)
    ib=int(a<=1 and c==0);ic=int(a==0 and b<=1)
    sb=int(a==2 and c==0);sc=int(a==1 and b<=1)
    assert lz<=11*a-service
    assert lhb==-ib+4*sb and lhc==-ic+sc
    assert 1<=h<=F(3,2)
    upper=-F(a,66)-service/726-F(ib+ic,16)+F(sb,4)+F(sc,16)+F(3,64)
    assert tilted<=upper
    if a<=3 and n>=6 and not (ib or ic):assert service>=F(n-3,289)
    if n>=74000:assert tilted<=upper<=-F(1,128)
    return tilted


def main():
    # The rational analytic inequalities used in the universal proof, not
    # only the finite pointwise checks below.
    assert F(677,144)<5
    assert F(4,66)-F(3,64)>=F(1,128)
    assert F(256,726)-F(19,64)>=F(1,128)
    assert F(74000-3,289)>=256
    assert 1+F(1,2178)+F(1,4)<=F(3,2)
    small=0
    for a in range(16):
        for b in range(16):
            for c in range(16):check_state((a,b,c));small+=1
    cases=[]
    for n in [74000,74001,100000,10**10,2**100,10**100]:
        states={(0,n,0),(1,n-1,0),(2,n-2,0),(3,n-3,0),(4,n-4,0),
                (0,0,n),(0,1,n-1),(1,0,n-1),(1,1,n-2),(1,2,n-3),
                (0,2,n-2),(0,n-1,1),(n,0,0),(n-2,1,1),(3,1,n-4),
                (n//3,n//3,n-2*(n//3)),(2,n//2,n-n//2-2),
                (isqrt(n),n-isqrt(n)-1,1),(1,isqrt(n),n-isqrt(n)-1)}
        worst=None;worst_x=None
        for x in states:
            value=check_state(x)
            if worst is None or value>worst:worst,worst_x=value,x
        cases.append(dict(total_count=str(n),states=len(states),
                          largest_exact_tilted_drift=str(worst),
                          state_with_largest_drift=[str(z) for z in worst_x]))
    result=dict(theorem='Actual generator global Foster inequality for the stated four-complex cycle.',
                tilt='33/32',head=74000,drift_bound='-1/128',
                W_multiplicative_drift='-1/192',
                small_count_checks=small,large_count_checks=sum(c['states'] for c in cases),
                cases=cases,
                scope='Finite exact checks supplement the uniform analytic proof; no universal weak-reversibility theorem or novelty verdict.')
    Path('outputs/capability_first_20261101/global_foster.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
