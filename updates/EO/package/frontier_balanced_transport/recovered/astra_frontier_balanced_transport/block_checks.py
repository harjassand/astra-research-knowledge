"""Independent matrix-coordinate diagnostics for the variational and noise identities.
Floating arithmetic verifies finite examples, never the infinite-volume theorem.
"""
import numpy as np, json
from scipy.linalg import null_space, eigh
from pathlib import Path
from fractions import Fraction as Q
from pauli_core import *

rng=np.random.default_rng(401012)
records=[]
for trial in range(24):
    no,ne,nz=6,5,2
    wo=np.diag(rng.uniform(.5,2,no))
    we=np.diag(np.r_[np.zeros(nz),rng.uniform(.5,2,ne-nz)])
    C=rng.normal(size=(ne,no))
    j=rng.normal(size=no)
    basis=null_space(C[:nz])
    reducedW=basis.T@wo@basis
    val,vec=eigh(reducedW)
    root_inv=vec@np.diag(val**-.5)@vec.T
    winve=np.diag(np.r_[np.zeros(nz),1/np.diag(we)[nz:]])
    T=root_inv@basis.T@C.T@winve@C@basis@root_inv
    jred=root_inv@basis.T@j
    maxerr=0.
    for d in (.15,.6,2.,10.):
        S=np.block([[d*wo,np.zeros((no,ne))],[np.zeros((ne,no)),d*we]])
        Ablock=np.block([[np.zeros((no,no)),-C.T],[C,np.zeros((ne,ne))]])
        B=S+Ablock
        jj=np.r_[j,np.zeros(ne)]
        direct=jj@np.linalg.solve(B,jj)
        spectral=d*jred@np.linalg.solve(d*d*np.eye(T.shape[0])+T,jred)
        maxerr=max(maxerr,abs(direct-spectral))
        ff=basis@rng.normal(size=basis.shape[1]); gg=rng.normal(size=ne)
        f=np.r_[ff,np.zeros(ne)];g=np.r_[np.zeros(no),gg]
        Sp=np.linalg.pinv(S); af=Ablock@f; ag=Ablock@g
        low=2*jj@f-f@S@f-af@Sp@af
        up=(jj-ag)@Sp@(jj-ag)+g@S@g
        r1=S@f-(jj-ag); r2=S@g+af
        gap=r1@Sp@r1+r2@Sp@r2
        assert low<=direct+1e-9 and direct<=up+1e-9
        assert abs((up-low)-gap)<1e-7
        assert abs(direct-spectral)<1e-9
        # Regularized near-monotonicity used in the thermodynamic limit.
        a=j@j; dgap=d*np.min(np.diag(wo))
        for l1,l2 in ((.001,.01),(.01,.1),(.1,1.)):
            k1=jj@np.linalg.solve(B+l1*np.eye(no+ne),jj)
            k2=jj@np.linalg.solve(B+l2*np.eye(no+ne),jj)
            assert k1<=k2+l2*a/dgap**2+1e-8
    records.append({'trial':trial,'max_noise_spectral_identity_error':maxerr})
# Exact continuity identity in a nontrivial chain.
n=9;H,J,_,edges=model(n)
for i in range(n):
    ni={(0,0):Q(1,2),(0,1<<i):Q(-1,2)}
    def bond(k):
        j=(k+1)%n
        return {string([(k,'X'),(j,'Y')]):Q(1,2),string([(k,'Y'),(j,'X')]):Q(-1,2)}
    assert scale(A(H,ni),-1)==add(bond((i-1)%n),scale(bond(i),-1))
# An exact two-block counterexample to dropping balance.
# B=[[1,1],[-1,0]], J=(1,0): B^-1 J=(0,1), true response=0.
# The inadmissible f=(1,0), with S^+ ignoring populations, gives false lower=1.
out={'random_block_checks':records,'exact_continuity_sites':n,
 'balance_counterexample':{'S':'diag(1,0)','A':'[[0,1],[-1,0]]','J':'[1,0]',
 'true_response':'0','false_unbalanced_lower':'1','diagonal_Af':'[0,-1]'},
 'infinite_volume_claim':'Proof only; not established by these finite diagnostics.'}
Path(__file__).with_name('block_checks.json').write_text(json.dumps(out,indent=2))
print('24 random block models, 96 direct/spectral comparisons, 9 exact continuity equations passed.')
