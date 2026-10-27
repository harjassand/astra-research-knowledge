"""Independent matrix reconstruction of the jointly charged global optimum.

Floating residuals instantiate JOINT_PROOF.md; they do not provide its global
certificate. Source parameters are exact roots specified and enclosed there.
"""
from pathlib import Path
import math
import numpy as np
from mpmath import mp
from joint_explore import design,fit,objective,C,KAP

mp.dps=80

def main():
    delta,H=mp.findroot(lambda de,h:(design(de,h)[1]-KAP,fit(design(de,h)[0])[0]),('.00577','73.34'))
    e,kap=design(delta,H);res,coeff=fit(e)
    A=4-delta;B=2*H/(H+delta);t=e[1]**2
    cc=(B*t+(t+A)*(H+delta)-t*H)/4;dd=B*t*(H+delta)/4
    disc=mp.sqrt(cc*cc-4*dd);sg1=(cc-disc)/2;sg2=(cc+disc)/2
    k1=(H*t-dd-kap*sg1)/(sg2-sg1);k2=kap-k1
    m1=k1/sg1;m2=k2/sg2
    assert all(v>0 for v in [m1,m2,k1,k2])
    assert abs(m1+m2-1)<mp.mpf('1e-70')
    assert abs(k1+k2-KAP)<mp.mpf('1e-70')
    masses=np.array([1,float(m1),float(m2)]);kk=[float(k1),float(k2)]
    H0=np.zeros((3,3))
    for j,k in enumerate(kk,1):
        H0[0,0]+=k;H0[j,j]+=k;H0[0,j]-=k;H0[j,0]-=k
    iv=1/np.sqrt(masses);D0=iv[:,None]*H0*iv[None,:]
    Dpi=D0.copy();Dpi[0,0]+=4
    aa=np.linalg.eigvalsh(D0);bb=np.linalg.eigvalsh(Dpi)
    ea=np.array([0,float(t),float(H)]);eb=np.array([float(e[0]**2),float(e[2]**2),float(H+delta)])
    assert np.allclose(aa,ea,atol=1e-12,rtol=1e-13)
    assert np.allclose(bb,eb,atol=1e-12,rtol=1e-13)
    z=np.sqrt(masses)/math.sqrt(2);v=np.array([1.,0.,0.]);w=-2*(v-z/math.sqrt(2))
    val,vec=np.linalg.eigh(D0);pinv=(vec[:,1:]/val[1:])@vec[:,1:].T
    cmat=float(w@pinv@w)
    assert abs(cmat-.05)<1e-13
    for q in [.01,.1,.5,1,math.pi]:
        dq=D0+4*math.sin(q/2)**2*np.outer(v,v)
        assert abs(float(w@np.linalg.solve(dq,w))-.05)<1e-9
    J=objective(e)
    rp=mp.sqrt(40);d=mp.sqrt((40+4)**2-8*40);sp=mp.sqrt((44+d)/2);pp=mp.sqrt(80)/sp
    gp=lambda w:(w/mp.sinh(w))**2 if w else mp.mpf(1)
    jp=mp.quad(gp,[0,pp])+mp.quad(gp,[rp,sp])
    lines=['# Joint finite-budget network reconstruction','',
           'Independent floating matrix check; the all-frequency proof uses exact intervals.',
           '',f'delta = {mp.nstr(delta,65)}',f'H = {mp.nstr(H,65)}',
           f'masses = {masses.tolist()}',f'springs = {kk}',
           f'exact-root spring sum = {mp.nstr(k1+k2,65)}',f'CM from pseudoinverse = {cmat:.17g}',
           f'D0 = {D0.tolist()}',f'Dpi = {Dpi.tolist()}',f'D0 eigenvalues = {aa.tolist()}',
           f'Dpi eigenvalues = {bb.tolist()}',
           f'largest endpoint residual = {max(np.max(abs(aa-ea)),np.max(abs(bb-eb))):.3g}',
           f'full bands = {[mp.nstr(w,35) for w in e]}',
           f'full objective = {mp.nstr(J,65)}',f'optimized pendant objective = {mp.nstr(jp,65)}',
           f'gain = {mp.nstr(jp-J,55)}',f'relative gain = {mp.nstr((jp-J)/jp,40)}',
           f'fifth-edge residual = {mp.nstr(res,20)}',
           f'dual nu,lambda,a,b = {[mp.nstr(w,40) for w in coeff]}','',
           'PASS: positive parts, total mass, both endpoint matrices, compliance, both budgets,',
           'fifth-edge stationarity and full three-band Bose objective.','']
    out='\n'.join(lines);Path(__file__).with_name('JOINT_NETWORK_CHECK.md').write_text(out);print(out)

if __name__=='__main__':main()
