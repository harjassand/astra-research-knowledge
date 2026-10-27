#!/usr/local/bin/python3
"""Independent arbitrary-precision evaluation of the continuum formula.
Not an interval enclosure; analytical finiteness/positivity is in PROOF.md.
"""
from pathlib import Path
import json
import mpmath as mp

mp.mp.dps=40
pi=mp.pi
g=mp.mpf(1)/5

class Measure:
    def __init__(self,c,a):
        self.c=mp.mpf(c)
        self.a=a
        d=3-self.c
        self.e=3+2*a*(d-mp.sign(d)*mp.sqrt(d*d-1+4*a))/(1-4*a)
        self.Z=1/(1-a*self.mp(self.e))
    def m(self,z):
        t=z-self.c
        root=mp.sqrt(t-1)*mp.sqrt(t+1)
        return 2/(t+root)
    def mp(self,z):
        t=z-self.c
        root=mp.sqrt(t-1)*mp.sqrt(t+1)
        return -2/(root*(t+root))
    def r(self,z):return 1/(3-z+self.a*self.m(z))
    def rp(self,z):return (1-self.a*self.mp(z))*self.r(z)**2
    def tw(self,th):
        u=mp.cos(th); x=self.c+u; v=mp.sin(th)
        return 2*self.a*v*v/(pi*((3-x+2*self.a*u)**2+4*self.a**2*v*v))
    def integral(self,f,breaks=()):
        p=[mp.mpf(0),pi]
        for x in breaks:
            t=x-self.c
            if -1<t<1:p.append(mp.acos(t))
        p=sorted(set(p))
        return self.Z*f(self.e)+mp.quad(lambda th:self.tw(th)*f(self.c+mp.cos(th)),p)
    def L(self,E):return mp.re(self.integral(lambda x:self.r(E-x)))
    def Lp(self,E):return mp.re(self.integral(lambda x:self.rp(E-x)))
    def w(self,x):
        u=x-self.c
        if abs(u)>=1:return mp.mpf(0)
        v=mp.sqrt(1-u*u)
        return 2*self.a*v/(pi*((3-x+2*self.a*u)**2+4*self.a**2*v*v))

p=Measure(5,2*g*g);m=Measure(1,g*g)
E=mp.findroot(lambda x:p.L(x)+m.L(x),(mp.mpf('5.977'),mp.mpf('5.980')))
D=p.Lp(E)+m.Lp(E);C=mp.sqrt(2/D)
Ap=lambda x:mp.re(p.r(E-x)); Am=lambda y:mp.re(m.r(E-y))
K=p.integral(lambda x:m.r(E-x),(E-2,E))
J=C*(p.integral(lambda x:Ap(x)*m.r(E-x),(E-2,E))+m.integral(lambda y:Am(y)*p.r(E-y),(E-6,E-4)))
c=J/K
lo=max(mp.mpf(4),E-2);hi=min(mp.mpf(6),E)
def integrand(th):
    x=lo+(hi-lo)*mp.sin(th)**2
    return p.w(x)*m.w(E-x)*abs(C*(Ap(x)+Am(E-x))-c)**2*2*(hi-lo)*mp.sin(th)*mp.cos(th)
rho=mp.quad(integrand,[0,pi/2])
obj={name:mp.nstr(value,35) for name,value in [('g',g),('Ep',E),('D',D),('K',K),('J',J),('c',c),('rho',rho),('pair_root_residual',p.L(E)+m.L(E))]}
Path(__file__).with_name('high_precision_results.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps(obj,indent=2))
