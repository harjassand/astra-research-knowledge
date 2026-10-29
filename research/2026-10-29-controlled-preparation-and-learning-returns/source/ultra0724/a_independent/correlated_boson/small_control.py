"""Independent full 36-state interacting transfer vs exact-moment HS sum.

Only this small implementation control constructs a many-body state space.
The M64 consumers do not import its occupation enumeration or matrices.
"""
from pathlib import Path
import itertools,json,math,time
import numpy as np
from scipy.linalg import eigh,expm

HERE=Path(__file__).resolve().parent

def compositions(n,m):
    if m==1:yield (n,);return
    for k in range(n+1):
        for tail in compositions(n-k,m-1):yield (k,)+tail

def main():
    start=time.perf_counter();M=3;K=2;L=2;U=4.;beta=1.;J=.25
    w=np.array([1.,2.,3.]);T=J*np.outer(w,w)/np.dot(w,w)
    occ=list(compositions(K,M));idx={x:i for i,x in enumerate(occ)};D=len(occ)
    one=np.zeros((D,D))
    for a,n in enumerate(occ):
        for j in range(M):
            if n[j]==0:continue
            for i in range(M):
                if i==j:one[a,a]+=T[i,i]*n[i];continue
                q=list(n);q[j]-=1;q[i]+=1
                one[idx[tuple(q)],a]+=T[i,j]*math.sqrt(n[j]*(n[i]+1))
    Hhop=np.kron(one,np.eye(D))+np.kron(np.eye(D),one)
    v=np.array([U*sum((x-y)**2 for x,y in zip(a,b)) for a in occ for b in occ])
    delta=beta/L;A=np.exp(-delta*v/2)[:,None]*expm(-delta*Hhop)*np.exp(-delta*v/2)[None,:]
    ZL=float(np.sum(eigh(A,eigvals_only=True)**L))
    Zcontinuous=float(np.sum(np.exp(-beta*eigh(Hhop+np.diag(v),eigvals_only=True))))
    c=math.exp(-delta*U);x=(1+c+c*c+c**3)/2-1;p=(1-c)/(2*(1-x))
    atoms=np.array([1.,x+1j*math.sqrt(1-x*x),x-1j*math.sqrt(1-x*x)])
    probs=np.array([1-2*p,p,p]);E=expm(-delta*T)
    hs=0.;minimum=1e9;maximum=0.
    for labels in itertools.product(range(3),repeat=M*L):
        a=np.array(labels).reshape(L,M);B=np.eye(M,dtype=complex)
        for l in range(L):B=E@(atoms[a[l]][:,None]*B)
        h=((np.trace(B))**2+np.trace(B@B))/2
        value=abs(h)**2;weight=float(np.prod(probs[np.array(labels)]))
        hs+=weight*value;minimum=min(minimum,value);maximum=max(maximum,value)
    out={'M':M,'K_each':K,'L':L,'U':U,'beta':beta,'J':J,'w':w.tolist(),
      'full_sector_states':D*D,'deterministic_phase_histories':3**(M*L),
      'Z_finite_slice_full_sector':ZL,'Z_finite_slice_HS_moment_sum':hs,
      'absolute_disagreement':abs(hs-ZL),'Z_continuous_full_sector':Zcontinuous,
      'actual_finite_slice_difference':ZL-Zcontinuous,
      'min_nonnegative_canonical_weight':minimum,'max_weight':maximum,
      'phase_moment1_residual':float(abs(np.sum(probs*atoms)-c)),
      'phase_moment2_residual':float(abs(np.sum(probs*atoms**2)-c**4)),
      'seconds_after_imports':time.perf_counter()-start,
      'scope':'Binary64 full-sector/quadrature implementation control; not an interval arithmetic or continuum qualification of either M64 run.'}
    assert abs(hs-ZL)<1e-11
    (HERE/'SMALL_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
