"""Exact polynomial certificate for the m=2 geometric echo.

Ring: Gaussian rational polynomials in q,s, with s^2=1-q^2.
All coefficients used below are Gaussian integers, hence Python complex stores
them exactly at these small magnitudes. The two endpoint sqrt(2) denominators
are omitted: Uscaled=2U. No floating point trigonometry is used.
"""
from collections import defaultdict

def add(a,b):
    c=dict(a)
    for k,v in b.items(): c[k]=c.get(k,0)+v
    return {k:v for k,v in c.items() if v!=0}
def scale(a,z): return {k:v*z for k,v in a.items() if v*z!=0}
def pmul(a,b):
    out={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            if j+l<2: out=add(out,{(i+k,j+l):x*y})
            else: out=add(out,{(i+k,0):x*y,(i+k+2,0):-x*y})
    return out

one={(0,0):1};q={(1,0):1};s={(0,1):1}
def pauli_mul(a,b):
    if a==0:return 1,b
    if b==0:return 1,a
    if a==b:return 1,0
    z={(1,2):(1j,3),(2,3):(1j,1),(3,1):(1j,2),
       (2,1):(-1j,3),(3,2):(-1j,1),(1,3):(-1j,2)}
    return z[a,b]
def omul(A,B):
    out={}
    for (a,b),p in A.items():
        for (c,d),q_ in B.items():
            z,e=pauli_mul(a,c);w,f=pauli_mul(b,d)
            key=(e,f);out[key]=add(out.get(key,{}),scale(pmul(p,q_),z*w))
    return {k:v for k,v in out.items() if v}
def oadd(A,B):
    out=dict(A)
    for k,v in B.items():out[k]=add(out.get(k,{}),v)
    return {k:v for k,v in out.items() if v}
def oscale(A,z): return {k:scale(v,z) for k,v in A.items()}
def dag(A):return {k:{ij:complex(v).conjugate() for ij,v in p.items()} for k,p in A.items()}
def product(xs):
    out={(0,0):one}
    for x in xs:out=omul(out,x)
    return out
def effect(A):
    out={}
    for (a,b),p in A.items():
        if a in [0,3]:out[b]=add(out.get(b,{}),p)
    return {k:v for k,v in out.items() if v}

def main():
    identity={(0,0):one};B={(1,1):one};C={(0,1):q,(0,2):s};O={(3,0):one}
    endpoint=oadd(identity,oscale(B,1j))
    pulses=[endpoint,oscale(C,1j),oscale(B,1j),oscale(C,1j),endpoint]
    U=product(pulses)
    E=effect(product([dag(U),O,U]))
    expected={0:{(0,0):4,(2,0):-32,(4,0):32}}
    assert E==expected,(E,expected)
    for j in range(5):
        H=B if j in [0,2,4] else C
        derivative=omul(oscale(H,-1j),pulses[j])
        ds=pulses.copy();ds[j]=derivative;dU=product(ds)
        dE=effect(oadd(product([dag(dU),O,U]),product([dag(U),O,dU])))
        assert dE=={},(j,dE)
    print('EXACT: effect=(8q^4-8q^2+1) I; all five area derivatives vanish.')

if __name__=='__main__':main()
