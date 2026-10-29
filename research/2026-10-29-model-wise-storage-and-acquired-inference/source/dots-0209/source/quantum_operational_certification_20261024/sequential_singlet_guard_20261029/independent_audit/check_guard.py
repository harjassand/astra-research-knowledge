"""Independent joint nonunital Pauli instrument and adversarial finite-horizon DP."""
import numpy as np,json,math
from scipy.linalg import eigh
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
rng=np.random.default_rng(3391007)
P1=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def swap(n,i,j):
    S=np.zeros((2**n,2**n))
    for x in range(2**n):
        y=x^((1<<i)|(1<<j)) if ((x>>i)&1)!=((x>>j)&1) else x; S[y,x]=1
    return S
n=4;D=16;Ss=[swap(n,i,j) for i in range(n) for j in range(i)];w,V=eigh(sum(Ss));E=V[:,abs(w)<1e-8];d0=K=2;P=E@E.T
Q=V[:,abs(w)>=1e-8];dec=[E.T]+[np.outer([1,0],q) for q in Q.T];C=3
results=[]
for m in [2,3]:
    Z=rng.normal(size=(3,D*m,D*m))+1j*rng.normal(size=(3,D*m,D*m));w,v=eigh(sum(z.conj().T@z for z in Z));inv=(v/np.sqrt(w))@v.conj().T;source=[z@inv for z in Z]
    A=[np.kron(d,np.eye(m))@z@np.kron(E,np.eye(m)) for d in dec for z in source]
    Bs=[]
    for p in P1:
        bp=[]
        for a in A:
            B=np.zeros((m,m),complex)
            for i in range(K):
                for j in range(K): B+=p[j,i].conjugate()*a[j*m:(j+1)*m,i*m:(i+1)*m]/K
            bp.append(B)
        Bs.append(bp)
    W=sum(b.conj().T@b for bs in Bs[1:] for b in bs)
    Ieff=sum(b.conj().T@b for bs in Bs for b in bs)
    def failprob(sig):
        q=0j
        for s in [-1,1]:
            for S in Ss:
                rho=(np.eye(D)+s*S)@P/(2*d0)
                out=sum(z@np.kron(rho,sig)@z.conj().T for z in source)
                q+=np.trace(np.kron((np.eye(D)-s*S)/2,np.eye(m))@out)/len(Ss)
        return q
    Feff=np.zeros((m,m),complex)
    for i in range(m):
        for j in range(m):
            sig=np.zeros((m,m));sig[i,j]=1;Feff[j,i]=failprob(sig)
    min_eig=float(eigh(C*Feff-W,eigvals_only=True).min())
    # Arbitrarily correlated logical-memory density; equality is full joint-map identity.
    z=rng.normal(size=(K*m,K*m))+1j*rng.normal(size=(K*m,K*m));rho=z@z.conj().T;rho/=np.trace(rho)
    actual=np.zeros_like(rho)
    for p in P1:
        pad=np.kron(p,np.eye(m))
        actual+=sum(pad@a@pad@rho@pad.conj().T@a.conj().T@pad.conj().T for a in A)/4
    instr=sum(np.kron(p,b)@rho@np.kron(p,b).conj().T for p,bs in zip(P1,Bs) for b in bs)
    residual=float(np.linalg.norm(actual-instr))
    assert min_eig>-1e-10 and np.linalg.norm(Ieff-np.eye(m))<1e-11 and residual<1e-11
    results.append({'memory_dimension':m,'joint_nonunital_kraus_count':3,'operator_hazard_min_eigenvalue':min_eig,'full_joint_twirl_residual':residual,'instrument_TP_residual':float(np.linalg.norm(Ieff-np.eye(m)))})
# Exact rational maximization over every history-dependent scalar hazard policy.
# At a state, probabilities are f,s-f,g,a-g with f<=C*s/a*g.
# Linear objective maxima occur at the listed polygon vertices, including idle hazards.
dps=[]
for s,C,b,t,J,L in [(F(1,10),3,0,1,5,35),(F(1,5),3,1,1,5,35),(F(1,8),7,1,2,10,50)]:
    a=1-s;R=C*s/a;u=R/(1+R);p=1/(1+R)
    vertices=[(F(0),F(0)),(F(0),a),(s,a),(s,s/R)]
    @lru_cache(None)
    def value(left,j,f,bad):
        if bad>b:return F(0)
        if j==J:return F(int(f>t))
        if not left:return F(0)
        ans=[]
        for pf,pg in vertices:
            v=pf*value(left-1,j+1,min(t+1,f+1),bad)+(s-pf)*value(left-1,j+1,f,bad)+pg*value(left-1,j,f,bad+1)+(a-pg)*value(left-1,j,f,bad)
            ans.append(v)
        return max(ans)
    worst=value(L,0,0,0)
    nb=sum(F(math.comb(t+j,j))*u**(t+1)*p**j for j in range(b+1))
    assert worst<=nb
    dps.append({'s':str(s),'C':C,'b':b,'t':t,'J':J,'L':L,'worst_adaptive_accepted_bad_probability':float(worst),'NB_upper_bound':float(nb),'exact_rational_inequality_passed':True,'states':value.cache_info().currsize})
out={'all_assertions_passed':True,'joint_instrument':results,'fully_adaptive_scalar_DP':dps}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
