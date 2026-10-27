#!/usr/bin/env python3
"""Independent mpmath arbitrary-precision quadrature of the infinite measure."""
import json
import mpmath as mp
mp.mp.dps = 42

def make(sign):
    c=mp.mpf(5 if sign==1 else 1)
    lam=mp.mpf(2 if sign==1 else 1)/25
    def q(d): return 2/(2+d+mp.sqrt((2+d)**2-1))
    d=mp.findroot(lambda d:d-lam*q(d),(.015,.06))
    e=3-d if sign==1 else 3+d
    w=1/(1+d/mp.sqrt((2+d)**2-1))
    def mb(z):
        u=z-c
        if u>1: return 2/(u+mp.sqrt(u*u-1))
        if u< -1: return 2/(u-mp.sqrt(u*u-1))
        return 2*(u-1j*mp.sqrt(max(mp.mpf('0'),1-u*u)))
    def s(z): return -1/(z-3-lam*mb(z))
    def sp(z):
        u=z-c
        bath=mb(z)
        return (1+lam*abs(bath)/mp.sqrt(u*u-1))/(z-3-lam*bath)**2
    def density(x):
        u=x-c
        if abs(u)>=1:return mp.mpf(0)
        t=mp.sqrt(1-u*u)
        return (2*lam*t/mp.pi)/((x-3-2*lam*u)**2+(2*lam*t)**2)
    def integrate(fn,breaks=()):
        pts=[mp.mpf(0),mp.pi]
        for b in breaks:
            if c-1<b<c+1: pts.append(mp.acos(b-c))
        pts.sort()
        return w*fn(e)+mp.quad(lambda t:density(c+mp.cos(t))*mp.sin(t)*fn(c+mp.cos(t)),pts)
    return dict(c=c,e=e,w=w,s=s,sp=sp,r=density,I=integrate)

p,m=make(1),make(-1)
def L(a,E): return a['I'](lambda x:a['s'](E-x))
E=mp.findroot(lambda e:L(p,e)+L(m,e),(mp.mpf('5.9785'),mp.mpf('5.9786')))
D=p['I'](lambda x:p['sp'](E-x))+m['I'](lambda x:m['sp'](E-x))
A=lambda x:p['s'](E-x)
C=lambda y:m['s'](E-y)
bp=[E-2,E]
bm=[E-6,E-4]
G=p['I'](lambda x:m['s'](E-x),bp)
J=p['I'](lambda x:A(x)*m['s'](E-x),bp)+m['I'](lambda y:C(y)*p['s'](E-y),bm)
Q=J/G
lo=max(mp.mpf(4),E-2);hi=min(mp.mpf(6),E)
def f(t):
    sn,cs=mp.sin(t),mp.cos(t)
    x=lo+(hi-lo)*sn*sn;y=E-x
    return p['r'](x)*m['r'](y)*abs(A(x)+C(y)-Q)**2 *2*(hi-lo)*sn*cs
rho=2/D*mp.quad(f,[0,mp.pi/2])
out={k:mp.nstr(v,34) for k,v in dict(E_pair=E,D=D,G_real=G.real,G_imag=G.imag,J_real=J.real,J_imag=J.imag,q_real=Q.real,q_imag=Q.imag,rho=rho).items()}
print(json.dumps(out,indent=2))
