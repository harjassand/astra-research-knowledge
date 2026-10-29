"""Independent actual finite guard on correlated inputs; steering and late-key counterexamples."""
import importlib.util,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own_guard_check',HERE/'check_guard.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Reuse our independently generated NONUNITAL physical+memory source, not author fixture.
m=g.m;D=g.D;C=g.C;K=2;source=g.source;P=g.P;Ss=g.Ss;Bs=g.Bs
s=.12;a=1-s;cap=8;R=C*s/a;nb=R/(1+R)
def superop(fun):
    cols=[]
    for i in range(m):
        for j in range(m):
            sig=np.zeros((m,m),complex);sig[i,j]=1;cols.append(fun(sig).reshape(-1))
    return np.stack(cols,axis=1)
def testpass(sig):
    out=np.zeros((m,m),complex)
    for S in Ss:
        for sign in [-1,1]:
            Pi=(np.eye(D)+sign*S)/2;rho=Pi@P/2
            y=sum(z@np.kron(rho,sig)@z.conj().T for z in source)
            pr=np.kron(Pi,np.eye(m));y=pr@y@pr
            # Trace physical carrier explicitly.
            out+=sum(y[x*m:(x+1)*m,x*m:(x+1)*m] for x in range(D))/len(Ss)
    return out
T=superop(testpass)
phis=[sum(np.kron(b,b.conj()) for b in bs) for bs in Bs]
# J=1,t=0,b=0: accepted histories consist of r passing tests then service.
# No outer correction is asserted; this is the valid trivial outer-code domain.
memsupers=[np.zeros((m*m,m*m),complex) for _ in range(4)]
power=np.eye(m*m)
for r in range(cap):
    for p in range(4): memsupers[p]+=s*phis[p]@power
    power=a*T@power

def kraus(S):
    J=S.reshape(m,m,m,m).transpose(0,2,1,3).reshape(m*m,m*m)
    vals,vec=eigh((J+J.conj().T)/2)
    assert vals.min()>-1e-12
    return [np.sqrt(w)*v.reshape(m,m) for w,v in zip(vals,vec.T) if w>1e-14]
accepted=[kraus(S) for S in memsupers]
ebad=sum(b.conj().T@b for bs in accepted[1:] for b in bs)
eacc=sum(b.conj().T@b for bs in accepted for b in bs)
eps=float(eigh(ebad,eigvals_only=True).max())
assert eps<=nb+1e-12 and eigh(eacc,eigvals_only=True).max()<=1+1e-12
rng=np.random.default_rng(440013);maxdist=0
for _ in range(100):
    v=rng.normal(size=K*m*2)+1j*rng.normal(size=K*m*2);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
    real=np.zeros_like(rho);ideal=np.zeros_like(rho)
    for p,bs in zip(g.P1,accepted):
        for b in bs:
            A=np.kron(np.kron(p,b),np.eye(2));B=np.kron(np.kron(np.eye(K),b),np.eye(2))
            real+=A@rho@A.conj().T;ideal+=B@rho@B.conj().T
    dist=float(np.abs(eigh(real-ideal,eigvals_only=True)).sum()/2);maxdist=max(maxdist,dist)
    assert dist<=eps+1e-11 and abs(np.trace(real-ideal))<1e-12
# Sharp aggregate-effect example: branchwise norms sum to d*epsilon, true bound epsilon.
d=4;eta=.03;projectors=[np.diag([int(i==j) for i in range(d)]) for j in range(d)]
beffect=sum(eta*p for p in projectors);assert np.allclose(beffect,eta*np.eye(d))
# |0> payload is flipped in every bad branch, orthogonal to its ideal, attaining eta.
rhoM=np.eye(d)/d;real=np.kron(np.diag([0,1]),eta*rhoM);ideal=np.kron(np.diag([1,0]),eta*rhoM)
tight=float(np.abs(eigh(real-ideal,eigvals_only=True)).sum()/2);assert abs(tight-eta)<1e-12
# Memory-only acceptance can steer initially entangled user: diag(1,1/4) effect.
phi=np.array([1,0,0,1])/np.sqrt(2);B=np.diag([1,.5]);psi=np.kron(np.eye(2),B)@phi
filtered=np.outer(psi,psi.conj());prob=np.trace(filtered).real
marg=np.array([[sum(filtered[2*i+j,2*k+j] for j in range(2)) for k in range(2)] for i in range(2)])/prob
assert np.allclose(np.diag(marg),[.8,.2])
# Late release of conjugating pad key destroys linear infidelity joint-output bound.
theta=.07;U=np.diag([np.exp(1j*theta),np.exp(-1j*theta)]);plus=np.ones(2)/np.sqrt(2);rho=np.outer(plus,plus)
actual=np.zeros((8,8),complex);idealcq=np.zeros_like(actual);reduced=np.zeros((2,2),complex)
for j,p in enumerate(g.P1):
    W=p.conj().T@U@p;out=W@rho@W.conj().T
    actual[2*j:2*j+2,2*j:2*j+2]=out/4;idealcq[2*j:2*j+2,2*j:2*j+2]=rho/4;reduced+=out/4
cqdist=float(np.abs(eigh(actual-idealcq,eigvals_only=True)).sum()/2)
reddist=float(np.abs(eigh(reduced-rho,eigvals_only=True)).sum()/2)
assert abs(cqdist-abs(np.sin(theta)))<1e-12 and abs(reddist-np.sin(theta)**2)<1e-12
out={'all_assertions_passed':True,'actual_finite_guard':{'n':4,'memory_dimension':m,'source_kraus_count':3,'J':1,'t':0,'b':0,'cap':cap,'s':s,'bad_effect_norm':eps,'NB_bound':nb,'accepted_effect_eigenvalues':eigh(eacc,eigvals_only=True).tolist(),'max_joint_trace_distance_100_correlated_reference_inputs':maxdist},'aggregate_effect_tightness':{'memory_dimension':d,'epsilon':eta,'sum_separate_branch_norms':d*eta,'actual_joint_distance':tight},'ideal_filter_steering':{'acceptance':float(prob),'original_user_marginal':[.5,.5],'normalized_accepted_user_marginal':np.diag(marg).real.tolist()},'late_key_release_counterexample':{'theta':theta,'retired_key_reduced_error':reddist,'late_disclosed_key_joint_error':cqdist,'square_root_scaling':True}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
