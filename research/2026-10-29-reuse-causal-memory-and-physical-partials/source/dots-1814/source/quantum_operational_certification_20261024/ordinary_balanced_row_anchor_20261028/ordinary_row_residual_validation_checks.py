from pathlib import Path
from fractions import Fraction as F
import numpy as np, itertools, math, json, hashlib
from scipy.stats import binom

rng=np.random.default_rng(635824)
he=lambda A:(A+A.conj().T)/2
root=lambda A:(lambda e,v:(v*np.sqrt(np.maximum(e,0)))@v.conj().T)(*np.linalg.eigh(he(A)))
# Explicit Hadamard; no randomized construction is used for its rows.
H=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float)/2
U=np.zeros((8,8),complex)
for s,t,l in itertools.product(range(4),range(4),range(2)):
    U[2*s+l,2*t+l]=(np.eye(4) if l==0 else H)[s,t]
ps=[np.array([1,0]),np.array([0,1]),np.array([1,1])/np.sqrt(2),
    np.array([1,-1])/np.sqrt(2),np.array([1,1j])/np.sqrt(2),np.array([1,-1j])/np.sqrt(2)]
def Z(kraus,x):
    V=np.kron(x.reshape(4,1),np.eye(2));cols=[]
    for psi in ps:
        tag=np.array([-psi[1],psi[0]])
        for K in kraus:cols.append(np.kron(K@V@psi,tag)/np.sqrt(6))
    return np.column_stack(cols)
def rational_stereo(t):
    ss=sum(z*z for z in t);den=1+ss
    return [2*z/den for z in t]+[(1-ss)/den]

householder_exact=0
for t in itertools.product([F(-1),F(0),F(1,3)],repeat=3):
    v=rational_stereo(t);sgn=1 if v[0]>=0 else -1
    w=[F(i==0)+sgn*v[i] for i in range(4)];ww=sum(a*a for a in w)
    hh=[[F(i==j)-2*w[i]*w[j]/ww for j in range(4)] for i in range(4)]
    assert ww>=2
    for j in range(1,4): assert sum(v[i]*hh[i][j] for i in range(4))==0
    for j,l in itertools.product(range(4),repeat=2):
        assert sum(hh[i][j]*hh[i][l] for i in range(4))==F(j==l)
    householder_exact+=1

errs={key:0. for key in ['normalization','discard_probability_identity','kernel_probability_identity',
    'physical_common_factor_identity','row_residual_purification_bound_excess',
    'full_task_root_bound_excess','decoder_partial_trace']}
models=probes=kernel_probes=0;summary=[]
x0=np.array([1,2,2,4],float)/5
for rotation in [0.,1e-4,.01,.2]:
    for trial in range(6):
        aa=he(rng.normal(size=(8,8))+1j*rng.normal(size=(8,8)))
        ev,vec=np.linalg.eigh(aa);rot=(vec*np.exp(1j*rotation*ev))@vec.conj().T
        splits=np.array([1-1e-6-1e-12,1e-6,1e-12]);W=np.vstack([np.sqrt(s)*np.eye(8) for s in splits])
        probs=rng.dirichlet(np.ones(3));kraus=[np.sqrt(p)*W@rot@np.diag(np.exp(1j*rng.uniform(-math.pi,math.pi,8)))@U for p in probs]
        zz=[Z(kraus,np.eye(4)[s]) for s in range(4)]
        d=zz[0].shape[0];gs=[np.column_stack([z[i] for z in zz]) for i in range(d)]
        bs=[he(g.conj().T@g).real for g in gs]
        assert np.linalg.norm(sum(bs)-np.eye(4))<1e-12
        vv=np.array([np.linalg.eigh(b)[1][:,-1] for b in bs])
        # Arbitrary learned perturbations, with no rank-one correctness premise.
        vv+=.003*rng.normal(size=vv.shape);vv/=np.linalg.norm(vv,axis=1)[:,None]
        keep=np.arange(d)<16
        if trial%2:keep[5]=False
        kap=min(.25,float(np.min((vv[keep]@x0)**2)))
        assert kap>0 and np.all((vv[keep]@x0)**2>=9*kap/16)
        Lambda=sum(np.trace(b) for i,b in enumerate(bs) if not keep[i])
        S=sum(np.trace(b)-v@b@v for i,(b,v) in enumerate(zip(bs,vv)) if keep[i])
        pd=0.
        for e in np.eye(4):
            z=Z(kraus,e);T=z@z.conj().T;pd+=sum(np.diag(T).real[~keep])/4
        errs['discard_probability_identity']=max(errs['discard_probability_identity'],abs(pd-Lambda/4))
        pk=0.
        for i,v in enumerate(vv):
            if not keep[i]:continue
            sg=1 if v[0]>=0 else -1;ww=np.eye(4)[0]+sg*v
            hh=np.eye(4)-2*np.outer(ww,ww)/(ww@ww)
            for j in range(1,4):
                z=Z(kraus,hh[:,j]);pk+=np.vdot(z[i],z[i]).real/(3*d);kernel_probes+=1
        errs['kernel_probability_identity']=max(errs['kernel_probability_identity'],abs(pk-S/(3*d)))
        z0=Z(kraus,x0);T0=z0@z0.conj().T
        mix=1e-5;tau=(1-mix)*T0+mix*np.eye(d)/d
        m=max(0,1-float(np.trace(root(root(T0)@tau@root(T0))).real))
        sh=np.zeros_like(vv);sh[keep]=vv[keep]/(vv[keep]@x0)[:,None]
        V,_=np.linalg.qr(rng.normal(size=(d,d//2))+1j*rng.normal(size=(d,d//2)))
        ks=[V[2*j:2*j+2] for j in range(d//2)]
        C=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj()) for K in ks)
        tr=np.trace(C.reshape(d//2,2,d//2,2),axis1=1,axis2=3)
        errs['decoder_partial_trace']=max(errs['decoder_partial_trace'],np.linalg.norm(tr-np.eye(d//2)))
        for _ in range(5):
            x=rng.normal(size=4);x/=np.linalg.norm(x);z=Z(kraus,x);T=z@z.conj().T
            linear=sum(x[s]*zz[s] for s in range(4))
            errs['physical_common_factor_identity']=max(errs['physical_common_factor_identity'],np.linalg.norm(z-linear))
            errs['normalization']=max(errs['normalization'],abs(np.trace(T).real-1))
            rr=sh@x;predz=rr[:,None]*z0
            bound=math.sqrt(Lambda)+3*math.sqrt(S/kap)
            errs['row_residual_purification_bound_excess']=max(errs['row_residual_purification_bound_excess'],np.linalg.norm(z-predz)-bound)
            pred=rr[:,None]*tau*rr[None,:]
            ell=float(1.5*np.trace(C.T@T).real);eh=float(1.5*np.trace(C.T@pred).real)
            rb=math.sqrt(3*Lambda)+math.sqrt(27*S/kap)+math.sqrt(24*m/kap)
            errs['full_task_root_bound_excess']=max(errs['full_task_root_bound_excess'],abs(math.sqrt(ell)-math.sqrt(max(eh,0)))-rb)
            probes+=1
        summary.append({'rotation':rotation,'retained':int(sum(keep)),'Lambda':float(Lambda),'S':float(S),'kappa':kap,'kernel_probability':float(pk)})
        models+=1

tests=0;max_false_accept=max_false_reject=0.
for u,beta in itertools.product([.01,.05,.2,.8],[.01,.1,.25]):
    n=math.ceil(64/u*math.log(1/beta));cut=math.floor(n*u/2)
    fa=float(binom.cdf(cut,n,u));fr=float(binom.sf(cut,n,u/4))
    assert fa<=beta and fr<=beta
    max_false_accept=max(max_false_accept,fa);max_false_reject=max(max_false_reject,fr);tests+=1
exact=0
for kap,ga,ep,d,L in itertools.product([F(1,4),F(1,100)],[F(1),F(1,7)],
    [F(1),F(1,19)],[4,16,48],[1,12,64]):
    lm=ga*ep/2**20;sm=kap*ga*ep/2**24;m=sm
    assert 9*lm+81*sm/kap+72*m/kap<ga*ep/32768
    assert F(27,32768)<F(1,1024)
    assert F(1,512)+2*F(1,2048)+F(1,512)==F(5,1024)
    assert 2*F(5,1024)+F(1,2)<1
    N=F(2**44*d*L,1)/(kap*ga*ep)
    assert F(2**22*d*L,1)/(kap*N)<=lm/4
    assert F(4096*d*L,1)/N<=sm/256
    exact+=1
assert max(errs.values())<1e-10,errs
src=Path(__file__).with_name('ORDINARY_ROW_RESIDUAL_VALIDATION_AND_FALLBACK.md')
out={'status':'PASS author diagnostics; independent receiving pending',
    'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
    'exact_rational_householder_cases':householder_exact,'physical_non_rank_one_models':models,
    'encoder_task_probes':probes,'actual_kernel_setting_expectations':kernel_probes,
    'finite_binomial_tail_cases':tests,'maximum_test_tail_probabilities':{'false_accept':max_false_accept,'false_reject':max_false_reject},
    'exact_budget_cases':exact,'max_residuals':errs,'models':summary,'actual_source_calls':0,'sampled_source_trial_outcomes':0,
    'evidence_class':'Source-disabled physical expectation diagnostics and numerical binomial-tail evaluations; no multinomial or Bernoulli draws',
    'scope':'Distinct actual-source linear purification and ordinary coordinate-probe mean checks, including rotated non-rank-one diagonals and rare discarded coordinates. Exact rational selector controls and finite statistical inequalities checked. No quantum acquisition, full pilot/optimizer implementation or hardware execution.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='models'},indent=2))
