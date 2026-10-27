#!/usr/local/bin/python3
"""Independent warm-review tests: no P84/P17 implementation imports.

Uses reviewer B's own earlier occupation-number lift for new original-rail,
coherent cross-response checks. Separate mpmath quadrature checks asymptotics.
"""
from pathlib import Path
import importlib.util
import json
import math
import numpy as np
import mpmath as mp
from scipy.linalg import eigh, eigh_tridiagonal
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_b_lift',ROOT.parent/'independent_checks.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

def new_fock(n,g):
    d=2+2*n; h=np.diag(np.full(d,3.))
    t,s=(1+math.sqrt(2))*g/2,(math.sqrt(2)-1)*g/2
    for i,j,v in [(0,2,t),(1,2+n,t),(0,2+n,s),(1,2,s)]:h[i,j]=h[j,i]=v
    for j in range(n):h[2+j,2+n+j]=h[2+n+j,2+j]=2.
    for a in (2,2+n):
        for j in range(n-1):h[a+j,a+j+1]=h[a+j+1,a+j]=-.5
    basis=[(i,j) for i in range(d) for j in range(i,d) if (i,j) not in ((0,0),(1,1))]
    H=prior.boson_matrix(h,basis)
    vals,U=eigh(H); idx=np.argmax(U[basis.index((0,1))]**2)
    E=vals[idx];psi=U[:,idx]
    vone=np.diag(np.r_[1.,-1.,np.zeros(2*n)])
    wone=np.zeros((d,d));wone[2,2]=1;wone[2+n,2+n]=-1
    V=prior.boson_matrix(vone,basis);W=prior.boson_matrix(wone,basis)
    direct=np.column_stack((V@psi,W@psi))
    specs=[];modes=[]
    for parity in (1,-1):
        x,U1=eigh_tridiagonal(np.r_[3.,np.full(n,5 if parity==1 else 1)],
                             np.r_[math.sqrt(2)*g if parity==1 else g,np.full(n-1,-.5)])
        P=np.zeros((d,n+1));P[0,0]=1/math.sqrt(2);P[1,0]=parity/math.sqrt(2)
        for j in range(n):P[2+j,j+1]=1/math.sqrt(2);P[2+n+j,j+1]=parity/math.sqrt(2)
        modes.append(P@U1);specs.append((x,U1[0],U1[0]**2))
    xp,ap,wp=specs[0];ym,am,wm=specs[1]
    dp=xp[:,None]+xp[None,:]-E;dm=ym[:,None]+ym[None,:]-E
    D=np.sum(wp[:,None]*wp[None,:]/dp**2)+np.sum(wm[:,None]*wm[None,:]/dm**2)
    N=math.sqrt(2/D)
    fp=(xp-3)/(math.sqrt(2)*g);fm=(ym-3)/g
    jp=(wp[None,:]/dp).sum(axis=1);jm=(wm[None,:]/dm).sum(axis=1)
    hp=((wp*fp)[None,:]/dp).sum(axis=1);hm=((wm*fm)[None,:]/dm).sum(axis=1)
    amp=ap[:,None]*am[None,:]
    fv=(N*amp*(jp[:,None]+jm[None,:])).ravel()
    fw=(N*amp*(hp[:,None]*fm[None,:]+fp[:,None]*hm[None,:])).ravel()
    transform=np.column_stack([
        [math.sqrt(2)*vp[a]*vm[a] if a==b else vp[a]*vm[b]+vm[a]*vp[b]
         for a,b in basis] for vp in modes[0].T for vm in modes[1].T])
    reconstructed=transform@np.column_stack((fv,fw))
    # Align the common arbitrary real eigenvector sign once for both controls.
    if np.dot(reconstructed[:,0],direct[:,0])<0:direct=-direct
    q=(ap[:,None]*am[None,:]).ravel();sums=(xp[:,None]+ym[None,:]).ravel()
    modesources=np.column_stack((fv,fw))
    z=E+.073+.041j
    r=1/(sums-z);K=np.dot(q*r,q)
    C=np.einsum('i,ij->j',q*r,modesources)
    matrix=modesources.T@(r[:,None]*modesources)-C[:,None]*C[None,:]/K
    physical=direct.T@np.linalg.solve(H-z*np.eye(len(H)),direct)
    return dict(n=n,g=g,pair_energy=float(E),
                source_pointwise_errors=np.linalg.norm(reconstructed-direct,axis=0).tolist(),
                cross_response_max_error=float(np.max(abs(physical-matrix))),
                first_rung_source_norm_squared=float(np.dot(direct[:,1],direct[:,1])),
                z=str(z))

mp.mp.dps=55
pi=mp.pi
A=4-2*mp.sqrt(3);B=4/mp.sqrt(3)-2
class Ch:
    def __init__(self,c,k):
        self.c=mp.mpf(c);self.k=k;self.coupling=mp.sqrt(k)
        delta=2*k/(2+mp.sqrt(3+4*k))
        self.atom=3-delta if c==5 else 3+delta
        self.mass=1/(1+k*self.bathp(self.atom))
    def bath(self,z):
        u=mp.mpc(z)-self.c
        return -2/(u+mp.sqrt(u-1)*mp.sqrt(u+1))
    def bathp(self,z):
        u=mp.mpc(z)-self.c;root=mp.sqrt(u-1)*mp.sqrt(u+1)
        return 2/(root*(u+root))
    def m(self,z):return 1/(3-z-self.k*self.bath(z))
    def mp(self,z):return (1+self.k*self.bathp(z))*self.m(z)**2
    def H(self,z):return self.coupling*self.bath(z)*self.m(z)
    def density(self,x):
        u=x-self.c
        if abs(u)>=1:return mp.mpf(0)
        v=mp.sqrt(1-u*u)
        return 2*self.k*v/(pi*((3-x+2*self.k*u)**2+4*self.k**2*v*v))
    def I(self,fun,cuts=()):
        ts=[mp.mpf(0),pi]
        for z in cuts:
            if self.c-1<z<self.c+1:ts.append(mp.acos(z-self.c))
        ts=sorted(ts)
        return self.mass*fun(self.atom)+mp.quad(lambda t:self.density(self.c+mp.cos(t))*mp.sin(t)*fun(self.c+mp.cos(t)),ts)
    def L(self,E):return mp.re(self.I(lambda x:self.m(E-x)))

def continuum(gtext):
    g=mp.mpf(gtext);p,m=Ch(5,2*g*g),Ch(1,g*g)
    guess=6-A*g*g
    E=mp.findroot(lambda z:p.L(z)+m.L(z),(guess-g*g/10,guess+g*g/10))
    D=p.I(lambda x:p.mp(E-x))+m.I(lambda y:m.mp(E-y));N=mp.sqrt(2/mp.re(D))
    K=p.I(lambda x:m.m(E-x),(E-2,E))
    Cv=N*(p.I(lambda x:p.m(E-x)*m.m(E-x),(E-2,E))+
          m.I(lambda y:m.m(E-y)*p.m(E-y),(E-6,E-4)))
    Cw=N*(p.I(lambda x:p.H(E-x)*m.H(E-x),(E-2,E))+
          m.I(lambda y:m.H(E-y)*p.H(E-y),(E-6,E-4)))
    av,aw=Cv/K,Cw/K
    lo,hi=max(mp.mpf(4),E-2),min(mp.mpf(6),E)
    def amps(x):
        y=E-x
        v=N*(p.m(E-x)+m.m(E-y))-av
        w=-N*((y-3)/g*p.H(E-x)+(x-3)/(mp.sqrt(2)*g)*m.H(E-y))-aw
        return v,w
    def integral(i,j):
        def f(t):
            x=lo+(hi-lo)*mp.sin(t)**2;y=E-x;a=amps(x)
            return p.density(x)*m.density(y)*mp.re(a[i]*mp.conj(a[j]))*2*(hi-lo)*mp.sin(t)*mp.cos(t)
        return 2*pi*mp.quad(f,[0,pi/2])/g**8
    M=mp.matrix([[integral(0,0),integral(0,1)],[0,integral(1,1)]])
    M[1,0]=M[0,1];ratio=-M[0,1]/M[1,1];res=M[0,0]-M[0,1]**2/M[1,1]
    return dict(g=gtext,Ep=mp.nstr(E,35),matrix_over_g8=[[mp.nstr(M[i,j],28) for j in range(2)] for i in range(2)],
                optimal_ratio=mp.nstr(ratio,28),residual_over_g8=mp.nstr(res,28),
                memory_alpha_over_g2=mp.nstr(av/g**2,28),rung_alpha_over_g2=mp.nstr(aw/g**2,28))

def asymptotic():
    weight=lambda x:(2/pi)**2*(1-(x-5)**2)/(x-3)**4
    mb=lambda x:2/(x-1+mp.sqrt((x-1)**2-1))
    ints=[mp.quad(lambda x,j=j:weight(x)*mb(x)**j,[4,6]) for j in range(3)]
    pref=3*A/mp.sqrt(2)
    M=mp.matrix([[4*pi*B*B*ints[0],4*pi*B*pref*ints[1]],
                 [4*pi*B*pref*ints[1],4*pi*pref*pref*ints[2]]])
    r=-M[0,1]/M[1,1];res=M[0,0]-M[0,1]**2/M[1,1]
    assert abs(ints[0]-16/(27*pi*pi))<mp.mpf('1e-50')
    return dict(matrix=[[mp.nstr(M[i,j],35) for j in range(2)] for i in range(2)],
                ratio=mp.nstr(r,35),residual=mp.nstr(res,35),
                reduction=mp.nstr(M[0,0]/res,35),determinant=mp.nstr(mp.det(M),35),
                coefficient_identity_residual=mp.nstr(M[0,0]-64*B*B/(27*pi),8))

if __name__=='__main__':
    with np.errstate(divide='ignore',over='ignore',invalid='ignore'):
        fock=[new_fock(n,g) for n,g in [(3,.2),(5,.08),(7,.2)]]
    for x in fock:
        assert max(x['source_pointwise_errors'])<1e-10
        assert x['cross_response_max_error']<1e-10
    data=dict(original_rail_coherent_checks=fock,asymptotic=asymptotic(),
              continuum=[continuum(g) for g in ('.2','.08','.03','.01')],
              scope='55-digit ordinary quadrature; no interval enclosure or time-domain theorem')
    def finite(v):
        if isinstance(v,dict):
            for x in v.values():finite(x)
        elif isinstance(v,list):
            for x in v:finite(x)
        elif isinstance(v,float):assert math.isfinite(v)
    finite(data)
    (ROOT/'extension_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
