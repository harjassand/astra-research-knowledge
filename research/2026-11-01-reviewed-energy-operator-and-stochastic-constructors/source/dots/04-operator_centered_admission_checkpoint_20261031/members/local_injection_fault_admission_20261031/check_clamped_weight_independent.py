"""Independent finite diagnostics for the clamped creation inequalities.
No diagnostic replaces the operator proof or certifies floating expm errors.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(20261031)
mins={'real_creation':1.,'selected_creation':1.}
for _ in range(100):
    C=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)); C/=np.linalg.norm(C,2)
    D=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));D=(D+D.conj().T)/2;D/=np.linalg.norm(D,2)
    K=np.block([[np.zeros((3,3)),C.conj().T],[C,D]])
    u=rng.uniform();lam=256.;R=8.;z=R*np.exp(2j*np.pi*rng.uniform())
    V=np.diag([1.]*3+[1+u]*3);Q=np.diag([0.]*3+[1.]*3)
    real=4/lam*u*V+lam/4*u*Q-1j*(K@V-V@K)
    mins['real_creation']=min(mins['real_creation'],float(np.linalg.eigvalsh(real).min()))
    V=np.diag([1.]*3+[2.]*3)
    selected=36*R*R/lam*V+lam/2*Q-(1j*z.conjugate()*K@V-1j*V*z*K)
    mins['selected_creation']=min(mins['selected_creation'],float(np.linalg.eigvalsh(selected).min()))
assert min(mins.values())>=-1e-10
I=np.eye(2);L=np.array([[0,1],[0,0]],complex);N=L.conj().T@L
X=L+L.conj().T;Z=np.diag([1.,-1.]);Y=np.array([[0,-1j],[1j,0]])
def kron(*xs):
    out=np.ones((1,1))
    for x in xs:out=np.kron(out,x)
    return out
K0=(kron(X,I,X)+.5*kron(N,I,Z))/2
K1=(kron(I,X,Y)+.5*kron(I,N,X))/2
c=max(np.linalg.norm(K0,2),np.linalg.norm(K1,2))
Hsys=.3*kron(I,I,Z); beta=.1; a=.2;T=.2;tau=.04;g=1;k=2
# Selected source0 windows separated by an actual interval with both real
# source-creating interactions ON. No resetting or classical-path reduction.
segments=[(.04,0),(.12,None),(.04,1)]
rows=[]
for lam in (256.,1024.,4096.):
    Hbase=Hsys+lam*beta*(kron(L.conj().T,L,I)+kron(L,L.conj().T,I))+K1
    jumps=[np.sqrt(lam)*kron(L,I,I),np.sqrt(lam)*kron(I,L,I),
           np.sqrt(a)*kron(L.conj().T,I,I),np.sqrt(a)*kron(I,L.conj().T,I)]
    Csum=sum(J.conj().T@J for J in jumps);d=8;Id=np.eye(d)
    dissip=sum(np.kron(J.T,J.conj().T) for J in jumps)-.5*(np.kron(Id,Csum)+np.kron(Csum.T,Id))
    def dual(Ha,Hb):return 1j*np.kron(Id,Ha.conj().T)-1j*np.kron(Hb.T,Id)+dissip
    Gram=np.zeros((d,d),complex)
    for av in range(4):
        for bv in range(4):
            v=Id.reshape(-1,order='F')
            for dt,sel in reversed(segments):
                ca=1 if sel is None else (av>>sel)&1
                cb=1 if sel is None else (bv>>sel)&1
                v=expm(dt*dual(Hbase+ca*K0,Hbase+cb*K0))@v
            sign=(-1)**(av.bit_count()+bv.bit_count())
            Gram+=sign*v.reshape((d,d),order='F')
    Gram=(Gram+Gram.conj().T)/2
    amplitude=np.sqrt(max(0.,np.linalg.eigvalsh(Gram).max()))
    gamma=.75-2*beta;aeff=a+4*c*c/lam
    C0=g*(1+3/(4*gamma))+aeff*g*(1/(lam*gamma)+3*tau/(4*gamma))
    R=min(lam/(16*c),np.sqrt(lam)/(np.sqrt(72)*c*np.sqrt(g*tau)))
    eta=np.exp(C0/2+18*R*R*c*c*g*tau/lam)/(R-1)
    assert amplitude<=eta**k+1e-8
    rows.append({'lambda':lam,'c':c,'R':R,'selected_k':k,'actual_amplitude_float':amplitude,'bound_eta_power':eta**k,
                 'Gram_min_eigenvalue_float':float(np.linalg.eigvalsh(Gram).min())})
out={'kind':'independent floating diagnostic, not a numerical certificate','operator_schur_checks':100,
     'minimum_slacks':mins,'common_dilation_cross_Gram_cases':rows}
print(json.dumps(out,indent=2))
if __name__=='__main__':Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
