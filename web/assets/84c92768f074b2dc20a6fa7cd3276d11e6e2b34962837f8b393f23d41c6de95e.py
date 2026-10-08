"""Independent direct RK4 cross-check for sharp_ring.py at one-period high frequency."""
from math import exp
from sharp_ring import protocol
from pulse_witness import EDGES, generator

A,d,B0,tau=4.,.1,.5,.02
z=protocol(A,d,B0,tau)
Es=[[0.,-A,-A],[-A,0.,-A],[-A,-A,0.]]
Bs=[[B0-d,B0,B0+d],[B0+d,B0-d,B0],[B0,B0+d,B0-d]]

def rhs(y, E, B):
    p=y[:3]; out=[0.]*6
    _,rates=generator(E,B)
    for e,(i,j,kij,kji) in enumerate(rates):
        je=kij*p[i]-kji*p[j]
        out[i]-=je; out[j]+=je; out[3+e]=je
    return out

def add(y,k,scale): return [v+scale*w for v,w in zip(y,k)]
def rk4step(y,E,B,h):
    k1=rhs(y,E,B)
    k2=rhs(add(y,k1,h/2),E,B)
    k3=rhs(add(y,k2,h/2),E,B)
    k4=rhs(add(y,k3,h),E,B)
    return [y[i]+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6 for i in range(6)]

for nsteps in [200,500,1000,2000]:
    p=z['p0'][:]; flux=[0.]*3; W=0.; Eprev=Es[-1]
    for E,B in zip(Es,Bs):
        W+=sum(p[i]*(E[i]-Eprev[i]) for i in range(3))
        y=p+[0.]*3; h=tau/nsteps
        for _ in range(nsteps): y=rk4step(y,E,B,h)
        p=y[:3]
        flux=[flux[i]+y[3+i] for i in range(3)]
        Eprev=E
    J=sum(flux)/3
    print(f'n={nsteps} dt={tau/nsteps:.3g} closureL1={sum(abs(p[i]-z["p0"][i]) for i in range(3)):.3g} '
          f'J={J:.13g} dJ={J-z["J"]:.3g} W={W:.13g} dW={W-z["Wwell"]:.3g} '
          f'flux={flux}')
