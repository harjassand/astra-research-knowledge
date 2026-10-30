"""Exact native degree-five countercheck; standard library only.

Derivative series use alpha=d/2. All internal coefficients are Gaussian
integers; only final reported Taylor coefficients are rationalized.
"""
from fractions import Fraction
from math import comb, factorial
import json
from pathlib import Path

D = Path(__file__).resolve().parent
P = {('X','Y'):('Z',(0,1)),('Y','Z'):('X',(0,1)),('Z','X'):('Y',(0,1)),
     ('Y','X'):('Z',(0,-1)),('Z','Y'):('X',(0,-1)),('X','Z'):('Y',(0,-1))}
HANDLES={'A':'XIX','B':'IXY','C':'YIZ'}

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def pmul(a,b):
    out=''; z=(1,0)
    for x,y in zip(a,b):
        if x=='I': q,w=y,(1,0)
        elif y=='I': q,w=x,(1,0)
        elif x==y: q,w='I',(1,0)
        else: q,w=P[x,y]
        out+=q; z=mul(z,w)
    return out,z

def poly(p,q):
    out={}
    for a,x in p.items():
        for b,y in q.items():
            c,w=pmul(a,b); z=mul(mul(x,y),w)
            out[c]=add(out.get(c,(0,0)),z)
    return {p:z for p,z in out.items() if z!=(0,0)}

def smul(p,q,k):
    out=[]
    for n in range(k+1):
        term={}
        for j in range(n+1):
            for x,z in poly(p[j],q[n-j]).items():
                z=tuple(comb(n,j)*a for a in z)
                term[x]=add(term.get(x,(0,0)),z)
        out.append({x:z for x,z in term.items() if z!=(0,0)})
    return out

def exp_series(gen,k):
    s=[{'III':(1,0)}]
    for _ in range(k): s.append(poly(gen,s[-1]))
    return s

def inverse(w): return [(h,-s) for h,s in w[::-1]]
def comm(u,v): return inverse(v)+inverse(u)+v+u
A=[('A',1)]; B=[('B',1)]; C=[('C',1)]
W3=comm(A,comm(B,C)); W5=comm(A,comm(A,W3))

def unitary(word,sa,sb,k,drift=True,drift_profile=None):
    signs={'A':sa,'B':sb,'C':sa*sb}
    u=[{'III':(1,0)}]+[{} for _ in range(k)]
    for j,(h,o) in enumerate(word):
        g={HANDLES[h]:(0,-2*o*signs[h])}
        if drift: g['IIZ']=(0,-1 if drift_profile is None else -drift_profile[j])
        u=smul(exp_series(g,k),u,k)
    if drift:
        net=len(word) if drift_profile is None else sum(drift_profile)
        u=smul(exp_series({'IIZ':(0,net)},k),u,k)
    return u

def coeff(term,k,den=1):
    div=den*2**k*factorial(k)
    return {p:[str(Fraction(z[0],div)),str(Fraction(z[1],div))] for p,z in term.items()}

def main():
    k=5; sums=[{} for _ in range(k+1)]; rows=[]
    assert len(W5)==46
    first_moments={h:sum(s*(2*j+1) for j,(a,s) in enumerate(W5) if a==h)//2 for h in HANDLES}
    assert first_moments=={'A':65,'B':16,'C':16}
    for sa in (-1,1):
        for sb in (-1,1):
            frozen=unitary(W5,sa,sb,k,False)
            assert all(not frozen[j] for j in range(1,5))
            assert coeff(frozen[5],5)=={'ZXI':['0','16']}
            u=unitary(W5,sa,sb,k,True)
            assert not u[1]
            assert coeff(u[2],2)=={'XIY':['0',str(65*sa)],'IXX':['0',str(-16*sb)]}
            rows.append({'signs':[sa,sb,sa*sb],'U2':coeff(u[2],2)})
            for n,term in enumerate(u):
                for p,z in term.items(): sums[n][p]=add(sums[n].get(p,(0,0)),z)
    means={str(n):coeff({p:z for p,z in term.items() if z!=(0,0)},n,4) for n,term in enumerate(sums)}
    result={'word':W5,'segments':len(W5),'first_moments':first_moments,
            'individual':rows,'mean_unitary_coefficients':means,
            'frozen_degree5':{'ZXI':['0','16']},
            'leading_variance_weights':{'XIY':4225,'IXX':256}}
    pal=W5+W5[::-1]
    pal_sums=[{} for _ in range(k+1)]
    for sa in (-1,1):
        for sb in (-1,1):
            u=unitary(pal,sa,sb,k,True,[1]*46+[-1]*46)
            assert coeff(u[2],2)=={'XIY':['0',str(130*sa)],'IXX':['0',str(-32*sb)]}
            for n,term in enumerate(u):
                for p,z in term.items(): pal_sums[n][p]=add(pal_sums[n].get(p,(0,0)),z)
    pal_means={str(n):coeff({p:z for p,z in term.items() if z!=(0,0)},n,4) for n,term in enumerate(pal_sums)}
    assert pal_means['1']==pal_means['2']==pal_means['3']=={}
    assert pal_means['4']=={'III':['-8962','0']}
    assert pal_means['5']=={'ZXI':['0','-4896']}
    for sa in (-1,1):
        for sb in (-1,1):
            frozen=unitary(pal,sa,sb,k,False)
            assert all(not frozen[j] for j in range(1,5))
            assert coeff(frozen[5],5)=={'ZXI':['0','32']}
    result['palindrome_triangular_bath']={'segments':92,'mean_coefficients':pal_means,'variance_weights':{'XIY':16900,'IXX':1024}}
    print(json.dumps(result,indent=2))
    (D/'degree5_certificate.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
