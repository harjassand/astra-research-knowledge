"""Independent numerical matrix reconstruction and high-mode cost continuation.

The exact proof and signs are in PROOF.md and certify.py. This file only checks
implementation and records costs. Every passband, including the highest, counts.
"""
from fractions import Fraction as Q
from pathlib import Path
import math
import numpy as np
from mpmath import mp

HERE=Path(__file__).resolve().parent
mp.dps=70

def mpq(x):
    return mp.mpf(x.numerator)/x.denominator if isinstance(x,Q) else mp.mpf(x)

def g(w):
    return (w/mp.sinh(w))**2 if w else mp.mpf(1)

def endpoints(t,A,B):
    t,A,B=map(mpq,(t,A,B));d=mp.sqrt((t+A)**2-4*B*t)
    s2=(t+A+d)/2;p2=B*t/s2
    return [mp.sqrt(p2),mp.sqrt(t),mp.sqrt(s2)]

def Jend(e):
    p,r,s=e
    return mp.quad(g,[0,p])+mp.quad(g,[r,s])

def dfit(e):
    return mp.lu_solve(mp.matrix([[w*w,w**4,1] for w in e]),mp.matrix([-w**3*g(w) for w in e]))

def parts(t,A,B,H,delta):
    t,A,B,H,delta=map(mpq,(t,A,B,H,delta))
    c=(B*t+(t+A)*(H+delta)-t*H)/4;d=B*t*(H+delta)/4
    disc=mp.sqrt(c*c-4*d);s1=(c-disc)/2;s2=(c+disc)/2
    kap=t+H-c
    k1=(t*H-d-kap*s1)/(s2-s1);k2=kap-k1
    return [k1/s1,k2/s2],[k1,k2],[s1,s2]

A=Q(17,5);B=Q(4000,2003);t=Q(28144153,971605);H=Q(400);delta=Q(3,5)
ms,ks,sig=parts(t,A,B,H,delta)
masses=np.array([1.]+list(map(float,ms)))
Hmat=np.zeros((3,3))
for j,k in enumerate(map(float,ks),1):
    Hmat[0,0]+=k;Hmat[j,j]+=k;Hmat[0,j]-=k;Hmat[j,0]-=k
iv=1/np.sqrt(masses);D0=iv[:,None]*Hmat*iv[None,:]
Dpi=D0.copy();Dpi[0,0]+=4
alpha=np.linalg.eigvalsh(D0);beta=np.linalg.eigvalsh(Dpi)
e=endpoints(t,A,B)
expected_alpha=np.array([0,float(t),float(H)])
expected_beta=np.array([float(e[0]**2),float(e[2]**2),float(H+delta)])
assert np.allclose(alpha,expected_alpha,atol=1e-11,rtol=1e-13)
assert np.allclose(beta,expected_beta,atol=1e-11,rtol=1e-13)
z=np.sqrt(masses)/math.sqrt(2);v=np.array([1.,0.,0.]);w=-2*(v-z/math.sqrt(2))
val,vec=np.linalg.eigh(D0);pinv=(vec[:,1:]/val[1:])@vec[:,1:].T
C=float(w@pinv@w)
assert abs(C-.05)<1e-13
for angle in [.01,.1,1.,math.pi]:
    Dq=D0+4*math.sin(angle/2)**2*np.outer(v,v)
    Cq=float(w@np.linalg.solve(Dq,w))
    assert abs(Cq-.05)<2e-10
trace=sum(beta)-sum(alpha)
logprod=float(np.prod(beta)/np.prod(alpha[1:]))
invsum=sum(1/x for x in beta)-sum(1/x for x in alpha[1:])
assert abs(trace-4)<1e-11 and abs(logprod-2)<1e-11 and abs(invsum-.525)<1e-11
J=Jend(e)+mp.quad(g,[mp.sqrt(mpq(H)),mp.sqrt(mpq(H+delta))])
Jp=Jend(endpoints(40,4,2))
Jrig=mp.quad(g,[0,mp.sqrt(2)])
lines=['# Independent floating reconstruction','',
       'This checks implementation; the analytic theorem and exact numerical signs are separate.',
       '',f'masses = {masses.tolist()}',f'springs = {list(map(float,ks))}',
       f'D0 = {D0.tolist()}',f'Dpi = {Dpi.tolist()}',
       f'alpha(D0) = {alpha.tolist()}',f'beta(Dpi) = {beta.tolist()}',
       f'largest endpoint residual = {max(np.max(abs(alpha-expected_alpha)),np.max(abs(beta-expected_beta))):.3g}',
       f'C_CM from pseudoinverse = {C:.17g}',f'trace = {trace:.17g}',f'log-product = {logprod:.17g}',
       f'inverse endpoint sum = {invsum:.17g}',f'J_three_band = {mp.nstr(J,50)}',
       f'J_optimized_pendant = {mp.nstr(Jp,50)}',f'J_rigid = {mp.nstr(Jrig,50)}',
       f'gain relative to pendant = {mp.nstr((Jp-J)/Jp,30)}','',
       '## Stiff-mode continuation at C=1/20','',
       'These are floating examples of the exact moment-preserving sequence in the proof.',
       '| high-band start | internal spring sum | J full spectrum | pendant minus J |',
       '|---:|---:|---:|---:|']
C=mp.mpf(1)/20
rhat=mp.findroot(lambda r:dfit(endpoints(r*r,2+C*r*r,2))[1],(5,6))
Ahat=2+C*rhat*rhat;delta=4-Ahat
for high in [10,20,40,100,200,1000]:
    H=mp.mpf(high)**2;Bl=2*H/(H+delta)
    tt=(Ahat-Bl)/(Bl*((1+C)/2-1/Bl+delta/(H*(H+delta))))
    ee=endpoints(tt,Ahat,Bl)
    assert ee[2]<high
    m,k,sg=parts(tt,Ahat,Bl,H,delta)
    jj=Jend(ee)+mp.quad(g,[high,mp.sqrt(H+delta)])
    assert all(x>0 for x in m+k)
    lines.append('| '+str(high)+' | '+mp.nstr(sum(k),15)+' | '+mp.nstr(jj,22)+' | '+mp.nstr(Jp-jj,15)+' |')
lines+=['',f'limit A = {mp.nstr(Ahat,50)}',f'limit J = {mp.nstr(Jend(endpoints(rhat*rhat,Ahat,2)),50)}',
        '', 'PASS: positive parts, both endpoint matrices, static response at several Bloch numbers,',
        'all exact-resource numerical reconstructions, and high-frequency continuation.','']
out='\n'.join(lines)
(HERE/'NETWORK_CHECK.md').write_text(out)
print(out)
