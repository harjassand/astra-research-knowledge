#!/usr/bin/env python3
"""Independent one-dimensional mpmath calculation (diagnostic, not interval)."""
import json
import os
import mpmath as mp

mp.mp.dps=int(os.environ.get('DPS','45'))
g=mp.mpf(1)/5

class Ch:
    def __init__(self,c,k):
        self.c=mp.mpf(c); self.k=k
        guess=mp.mpf('2.958') if c==5 else mp.mpf('3.021')
        self.atom=mp.findroot(lambda z:3-z-self.k*self.surface(z),guess)
        self.mass=1/(1+self.k*self.sp(self.atom))
    def surface(self,z):
        w=z-self.c
        return 2*(-w+mp.sign(w)*mp.sqrt(w*w-1))
    def sp(self,z):
        w=z-self.c
        return 2*(-1+abs(w)/mp.sqrt(w*w-1))
    def m(self,z): return 1/(3-z-self.k*self.surface(z))
    def mp(self,z): return (1+self.k*self.sp(z))*self.m(z)**2
    def boundary(self,z):
        w=z-self.c
        if abs(w)>=1: return self.m(z)
        s=2*(-w+1j*mp.sqrt(1-w*w))
        return 1/(3-z-self.k*s)
    def density(self,x):
        w=x-self.c
        if abs(w)>=1: return mp.mpf(0)
        q=mp.sqrt(1-w*w)
        a=3-x-2*self.k*(self.c-x)
        return 2*self.k*q/(mp.pi*(a*a+4*self.k*self.k*q*q))
    def band(self,f,cuts=()):
        ts=[mp.mpf(0),mp.pi]
        for x in cuts:
            if self.c-1 < x < self.c+1: ts.append(mp.acos(x-self.c))
        ts.sort()
        return sum(mp.quad(lambda t:self.density(self.c+mp.cos(t))*mp.sin(t)
                           *f(self.c+mp.cos(t)),[a,b])
                   for a,b in zip(ts[:-1],ts[1:]))
    def integral(self,f,cuts=()): return self.mass*f(self.atom)+self.band(f,cuts)

p=Ch(5,2*g*g);m=Ch(1,g*g)
def L(ch,e): return ch.integral(lambda x:ch.m(e-x))
E=mp.findroot(lambda e:L(p,e)+L(m,e),(mp.mpf('5.9785'),mp.mpf('5.9787')))
D=p.integral(lambda x:p.mp(E-x))+m.integral(lambda x:m.mp(E-x))
def a(x): return p.m(E-x)
def b(y): return m.m(E-y)
M=p.integral(lambda x:m.boundary(E-x),(E-2,E))
J=p.integral(lambda x:a(x)*m.boundary(E-x),(E-2,E))
J+=m.integral(lambda y:b(y)*p.boundary(E-y),(E-6,E-4))
alpha=J/M
lo=max(mp.mpf(4),E-2);hi=min(mp.mpf(6),E)
def f(x):
    y=E-x
    u=a(x)+b(y)
    return p.density(x)*m.density(y)*abs(u-alpha)**2
rho=2/D*mp.quad(f,[lo,hi])
print(json.dumps({k:mp.nstr(v,30) for k,v in dict(
    E_plus=p.atom,E_minus=m.atom,mass_plus=p.mass,mass_minus=m.mass,
    E=E,D=D,M_real=M.real,M_imag=M.imag,J_real=J.real,J_imag=J.imag,
    alpha_real=alpha.real,alpha_imag=alpha.imag,rho=rho,
    formal_2pi_rho=2*mp.pi*rho).items()},indent=2))
