"""Matched finite-period controls for the three-state driven ring."""
from math import exp, log
from pulse_witness import EDGES, eye, matmul, matvec, expm, matscale, generator, phase_transition_and_flux

A,d,B0,tau=4.,.1,.5,.02
Es=[[0.,-A,-A],[-A,0.,-A],[-A,-A,0.]]
Bs=[[B0-d,B0,B0+d],[B0+d,B0-d,B0],[B0,B0+d,B0-d]]

def solve(label, es, bs, order=(0,1,2)):
    pmap=eye(3)
    for r in order:
        Q,_=generator(es[r],bs[r])
        pmap=matmul(expm(matscale(Q,tau)),pmap)
    p=[1/3]*3
    for _ in range(100000):
        pn=matvec(pmap,p); err=sum(abs(a-b) for a,b in zip(pn,p)); p=pn
        if err<2e-15: break
    p0=p[:]; flux=[0.]*3; W=0.
    prev=es[order[-1]]
    for r in order:
        E,B=es[r],bs[r]
        W+=sum(p[i]*(E[i]-prev[i]) for i in range(3))
        p,fl=phase_transition_and_flux(E,B,p,tau)
        flux=[a+b for a,b in zip(flux,fl)]
        prev=E
    print(f'{label}: order={order}, period={len(order)*tau:.4g}s, p0={p0}, '
          f'closure={err:.2g}, edge_flux={flux}, J/cycle={sum(flux)/3:.14g}, '
          f'Jrate={sum(flux)/(3*len(order)*tau):.14g}/s/site, Wwell={W:.14g} kBT/site/cycle')

solve('full forward',Es,Bs)
solve('full time-reversed',Es,Bs,(0,2,1))
solve('same rotating wells, fixed mean barriers',Es,[[B0]*3 for _ in range(3)])
solve('same barrier schedule, fixed flat wells',[[0.]*3 for _ in range(3)]*3,Bs)
Bs_mirror=[[B0+d,B0,B0-d],[B0-d,B0+d,B0],[B0,B0-d,B0+d]]
solve('barrier wave mirrored against rotating wells',Es,Bs_mirror)
# High-frequency averaged rates: physical traffic T and effective unicycle affinity.
c=exp(-B0); q=exp(-A); x=exp(d); y=exp(-d)
u=c/3*(x+q*(1+y)); w=c/3*(y+q*(1+x)); T=u+w; aff=3*log(u/w)
J=(u-w)/3; K=3*(u+w)
print(f'averaged CTMC: u={u:.14g}/s, w={w:.14g}/s, T={T:.14g}/s/site, K={K:.14g}/s, '
      f'Aeff={aff:.14g}, J={J:.14g}/s/site, T/3*tanh(Aeff/6)={T/3*__import__("math").tanh(aff/6):.14g}, '
      f'K/9*tanh(Aeff/6)={K/9*__import__("math").tanh(aff/6):.14g}')

# Exact time-averaged jump traffic of the driven protocol, then a strongest
# equal-traffic, equal-current static unicycle comparator with uniform rates.
def occupancy_integral(E,B,p):
    Q,rates=generator(E,B)
    Aug=[[0.]*6 for _ in range(6)]
    for i in range(3):
        for j in range(3): Aug[i][j]=Q[i][j]
        Aug[i+3][i]=1.
    M=expm(matscale(Aug,tau))
    z=[sum(M[i+3][j]*p[j] for j in range(3)) for i in range(3)]
    traffic=sum(kij*z[i]+kji*z[j] for i,j,kij,kji in rates)
    pnext=matvec([row[:3] for row in M[:3]],p)
    return traffic,pnext

p=None
P=eye(3)
for E,B in zip(Es,Bs):
    Q,_=generator(E,B); P=matmul(expm(matscale(Q,tau)),P)
p=[1/3]*3
for _ in range(100000):
    pn=matvec(P,p); err=sum(abs(a-b) for a,b in zip(pn,p)); p=pn
    if err<2e-15: break
p0=p[:]; total_traffic=0.
for E,B in zip(Es,Bs):
    tr,p=occupancy_integral(E,B,p); total_traffic+=tr
Tdyn=total_traffic/(3*tau)
# Obtain the exact driven cycle current by integrating each phase from p0.
p=p0[:]; edge_flux=[0.]*3
for E,B in zip(Es,Bs):
    p,fl=phase_transition_and_flux(E,B,p,tau)
    edge_flux=[a+b for a,b in zip(edge_flux,fl)]
Jdyn=sum(edge_flux)/(3*3*tau)
ustat=(Tdyn+3*Jdyn)/2; wstat=(Tdyn-3*Jdyn)/2
Astat=3*log(ustat/wstat)
print(f'finite matched static: T={Tdyn:.14g}/s/site, J={Jdyn:.14g}/s/site, '
      f'u={ustat:.14g}/s, w={wstat:.14g}/s, Aeff={Astat:.14g}, '
      f'J* Aeff={Jdyn*Astat:.14g} kBT/s/site; ETP={Tdyn/3*__import__("math").tanh(Astat/6):.14g}/s/site')
