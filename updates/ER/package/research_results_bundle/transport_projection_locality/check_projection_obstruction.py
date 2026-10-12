#!/usr/bin/env python3
"""Exact, finite symbolic checks for the exclusion-projection locality obstruction.
Requires SymPy. No downloads, experiment, or transport-value extrapolation.
"""
import sympy as s

a,b=s.symbols('a b', integer=True)
h=(a-b)*(2*a+b-2)*(a+2*b-2)
def at(x,y): return s.expand(h.subs({a:x,b:y}, simultaneous=True))
jumps=[(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]
assert s.expand(sum(h-at(a+x,b+y) for x,y in jumps)) == 0
assert s.expand(at(0,b)+at(0,b+1)-2*at(1,b)) == 0
assert s.expand(at(a,0)+at(a+1,0)-2*at(a,1)) == 0
assert at(2,1)+at(1,2)-2*at(1,1) == 0
assert at(2,1)-at(1,1) == 6
assert at(1,2)-at(2,1) == -12
print('Exact gap-graph harmonic identities and moments: PASS')

n=7
I=s.I
single={('X','Y'):('Z',I),('Y','Z'):('X',I),('Z','X'):('Y',I),
        ('Y','X'):('Z',-I),('Z','Y'):('X',-I),('X','Z'):('Y',-I)}
def word(dic):
    q=['I']*n
    for i,x in dic.items(): q[i%n]=x
    return tuple(q)
def clean(p): return {w:s.expand(c) for w,c in p.items() if s.expand(c)!=0}
def add(*ps):
    q={}
    for p in ps:
        for w,c in p.items():q[w]=q.get(w,0)+c
    return clean(q)
def scale(p,x):return clean({w:c*x for w,c in p.items()})
def mul(p,q):
    out={}
    for u,c in p.items():
        for v,d in q.items():
            phase=1; w=[]
            for x,y in zip(u,v):
                if x=='I':w.append(y)
                elif y=='I':w.append(x)
                elif x==y:w.append('I')
                else:
                    z,f=single[x,y];w.append(z);phase*=f
            w=tuple(w);out[w]=out.get(w,0)+c*d*phase
    return clean(out)
def A(H,p):return scale(add(mul(H,p),scale(mul(p,H),-1)),-I)
def P(p):return {w:c for w,c in p.items() if all(x in 'IZ' for x in w)}
def j(i):return {word({i:'X',i+1:'Y'}):s.Rational(1,2),word({i:'Y',i+1:'X'}):-s.Rational(1,2)}
J=add(*(j(i) for i in range(n)))
Hhop=add(*({word({i:'X',i+1:'X'}):-s.Rational(1,2),word({i:'Y',i+1:'Y'}):-s.Rational(1,2)} for i in range(n)))
Hdiag=add(*({word({i:'Z',i+1:'Z'}):s.Integer(1)} for i in range(n)))
def V(a,b):return add(*({word({x:'Z',x+a:'Z',x+a+b:'Z'}):s.Integer(1)} for x in range(n)))
F=add(*(mul(j(i),{word({i+2:'Z',i+3:'Z'}):1}) for i in range(n)))
Fmid=add(*(mul(j(i),{word({i-1:'Z',i+2:'Z'}):1}) for i in range(n)))
assert add(P(A(Hhop,F)),scale(add(V(2,1),scale(V(1,1),-1)),-1)) == {}
assert add(P(A(Hhop,Fmid)),scale(add(V(1,2),scale(V(2,1),-1)),-1)) == {}
assert add(A(Hdiag,A(Hdiag,J)),scale(add(J,scale(Fmid,-1)),8)) == {}
cross=A(Hhop,A(Hdiag,J))
assert P(A(Hhop,cross)) == {}
assert A(Hhop,J) == {}
print('Exact n=7 Pauli identities (t=U=1): PASS')
print('All checks passed. These verify finite algebra, not an infinite-volume decay theorem.')
