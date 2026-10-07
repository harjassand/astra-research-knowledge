#!/usr/bin/env python3
"""Bounded checks of the restricted lifting derivation; not a gate proof."""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(60501)

def signs(n):
    k=(n-1).bit_length()
    return [[1 if (i&t).bit_count()%2==0 else -1 for i in range(n)] for t in range(1<<k)]

# Exact normalized weighted trace identity in two central matrix blocks.
exact=[]
for blocks,weights in [([2],[F(1)]),([3],[F(1)]),([2,3],[F(1,7),F(6,7)]),([1,2,4],[F(1,9),F(2,9),F(6,9)])]:
    n=sum(blocks)
    diagonal_weights=[]
    allowed=[]
    start=0
    for b,w in zip(blocks,weights):
        diagonal_weights.extend([w/b]*b)
        allowed.extend([(i,j) for i in range(start,start+b) for j in range(start,start+b)])
        start+=b
    X={(i,j):F((3*i-2*j+5)%11-5) for i,j in allowed}
    ss=signs(n)
    off=sum(diagonal_weights[i]*x*x for (i,j),x in X.items() if i!=j)
    avg_comm=sum(sum(diagonal_weights[i]*x*x*(s[i]-s[j])**2 for (i,j),x in X.items()) for s in ss)/len(ss)
    pinching_ok=all(sum(s[i]*s[j] for s in ss)==(len(ss) if i==j else 0) for i,j in allowed)
    assert avg_comm==2*off and pinching_ok
    exact.append({'blocks':blocks,'weights':[str(w) for w in weights],'signs':len(ss),'off_L2_squared':str(off),'commutator_average_squared':str(avg_comm),'identity_exact':True})

def vec(x): return x.reshape(-1,order='F')
def unvec(v,d): return v.reshape((d,d),order='F')
def superop(f,d):
    out=np.empty((d*d,d*d),complex)
    for j in range(d):
        for i in range(d):
            E=np.zeros((d,d),complex);E[i,j]=1
            out[:,i+j*d]=vec(f(E))
    return out

def choi(S,d):
    J=np.zeros((d*d,d*d),complex)
    for i in range(d):
        for j in range(d):
            E=np.zeros((d,d),complex);E[i,j]=1
            J+=np.kron(E,unvec(S@vec(E),d))
    return (J+J.conj().T)/2

def unitary(d):
    z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    q,r=np.linalg.qr(z)
    return q@np.diag(np.exp(-1j*np.angle(np.diag(r))))

def hcontraction(d):
    z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));z=(z+z.conj().T)/2
    return z/max(1,np.linalg.norm(z,2))

numerical=[]
for d in range(2,6):
  for a in [.001,.05,.3,.8]:
    U=unitary(d)
    P=[np.diag(np.eye(d)[i]) for i in range(d)]
    K=[np.sqrt(1-a)*p for p in P]+[np.sqrt(a)*U]
    M=[k.conj().T@k for k in K]
    def L(x):return sum(k@x@k.conj().T for k in K)
    def psi(x):return sum(np.trace(m@x)*m/np.trace(m) for m in M)
    C=superop(lambda x:(L(x)+psi(x))/2,d)
    Phi=C.conj().T@C
    apply=lambda x:unvec(Phi@vec(x),d)
    eta=float(1-sum(np.trace(p@apply(p)).real/d for p in P))
    ss=signs(d)
    avloss=0.;avdisp=0.
    for s in ss:
        u=np.diag(s);fu=apply(u)
        avloss+=1-np.trace(fu.conj().T@fu).real/d
        avdisp+=np.trace((fu-u).conj().T@(fu-u)).real/d
    avloss/=len(ss);avdisp/=len(ss)
    assert avloss<=2*eta+1e-10 and avdisp<=eta+1e-10
    E=superop(lambda x:np.diag(np.diag(x)),d)
    EB=E@Phi
    min_eb_choi=float(np.linalg.eigvalsh(choi(EB,d)).min())
    assert min_eb_choi>=-1e-10
    bound=2*np.sqrt(2)*np.sqrt(max(0,eta))
    maxerr=0.;max_off2=0.;identityerr=0.
    for _ in range(40):
        A=hcontraction(d);Y=apply(A);off=Y-np.diag(np.diag(Y))
        err=np.linalg.svd(off,compute_uv=False).sum()/d
        off2=np.linalg.norm(off,'fro')/np.sqrt(d)
        avgc=sum(np.linalg.norm(Y@np.diag(s)-np.diag(s)@Y,'fro')**2/d for s in ss)/len(ss)
        identityerr=max(identityerr,abs(avgc-2*off2**2))
        assert err<=bound+1e-9
        maxerr=max(maxerr,float(err));max_off2=max(max_off2,float(off2))
    numerical.append({'dimension':d,'instrument_mixture_a':a,'eta':eta,'average_schwarz_loss':avloss,'average_displacement_squared':avdisp,'theorem_bound':float(bound),'sample_max_normalized_L1_error':maxerr,'sample_max_off_L2':max_off2,'pinching_identity_error':identityerr,'EB_choi_min_eigenvalue':min_eb_choi})

out={'seed':60501,'exact_weighted_pinching_checks':exact,'numerical_instrument_checks':numerical,'scope':'Exact Fraction checks certify displayed sign/pinching identities for the finite fixtures. NumPy tests are bounded transcription diagnostics only; they do not establish the universal theorem, optimize EB distance, or acquire anchors.'}
(ROOT/'restricted_lifting_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'exact_fixtures':len(exact),'instrument_fixtures':len(numerical),'contraction_probes_per_fixture':40,'max_pinching_identity_error':max(x['pinching_identity_error'] for x in numerical),'min_EB_choi_eigenvalue':min(x['EB_choi_min_eigenvalue'] for x in numerical)},indent=2))
