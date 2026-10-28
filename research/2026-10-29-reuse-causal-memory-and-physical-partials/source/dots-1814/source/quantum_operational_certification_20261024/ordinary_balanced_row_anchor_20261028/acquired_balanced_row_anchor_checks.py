from pathlib import Path
from fractions import Fraction as F
import numpy as np, itertools, math, json, hashlib

rng=np.random.default_rng(635823)
he=lambda A:(A+A.conj().T)/2
root=lambda A:(lambda e,v:(v*np.sqrt(np.maximum(e,0)))@v.conj().T)(*np.linalg.eigh(he(A)))
X=[];w=[]
for j in range(4): X.append(np.eye(4)[j]);w.append(1/12)
for sig in itertools.product([-1,1],repeat=4): X.append(np.array(sig)/2);w.append(1/24)
X=np.array(X);w=np.array(w)
H=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float)/2
U=np.zeros((8,8),complex)
for s,t,l in itertools.product(range(4),range(4),range(2)):
    U[2*s+l,2*t+l]=(np.eye(4) if l==0 else H)[s,t]
u0=np.array([(np.eye(4) if l==0 else H)[s] for s in range(4) for l in range(2) for a in range(2)])
lam0=np.array([(1-.5*(a==l))/3 for s in range(4) for l in range(2) for a in range(2)])
xstar=np.array([1,2,2,4],float)/5
assert np.min((u0@xstar)**2)>=.01-1e-15

def gridpoint_near(x, kap):
    # Exact rational point in the manuscript's full grid. This tests its covering
    # proof using a known witness; it does not execute the exhaustive search.
    M=1
    while M*M*kap<4096: M*=2
    j=int(np.argmax(np.abs(x)));sgn=1 if x[j]>=0 else -1
    y=x.copy();y[j]*=sgn
    inds=[i for i in range(4) if i!=j]
    ts=[F(int(round(float(y[i]/(1+y[j]))*M)),M) for i in inds]
    norm=sum(t*t for t in ts);den=1+norm
    q=[F(0)]*4
    for i,t in zip(inds,ts):q[i]=2*t/den
    q[j]=sgn*(1-norm)/den
    assert sum(t*t for t in q)==1
    return np.array(q,float),q,M

coverage=0;coverage_max=0.
for kap in [F(1,4),F(1,100),F(1,10000)]:
    for _ in range(60):
        x=rng.normal(size=4);x/=np.linalg.norm(x)
        q,qq,M=gridpoint_near(x,kap)
        distance=np.linalg.norm(q-x)
        assert distance<=math.sqrt(float(kap))/16+1e-15
        coverage_max=max(coverage_max,distance/math.sqrt(float(kap)))
        coverage+=1

def lossstate(kraus,x):
    V=np.kron(x.reshape(4,1),np.eye(2));aa=[K@V for K in kraus]
    J=sum(np.outer(a.reshape(-1),a.reshape(-1).conj()) for a in aa)/2
    rho=sum(a@a.conj().T for a in aa)/2
    return (2*np.kron(rho,np.eye(2))-J)/3

errs={key:0. for key in ['pilot_direction_bound_excess','discarded_mass_bound_excess',
    'anchor_true_balance_deficit','weighted_ratio_bound_excess','projected_factorization',
    'discarded_root_bound_excess','full_task_root_bound_excess','decoder_partial_trace']}
pilot_models=physical_models=probes=retained_rows=missing_rows=0
summary=[]
for rare in [1e-3,1e-6,1e-10,1e-15]:
    for trial in range(6):
        splits=np.array([1-rare-rare/100,rare,rare/100])
        lam=np.concatenate([s*lam0 for s in splits]);us=np.tile(u0,(3,1));d=len(lam)
        kap=.01;L=12;N=10**12;threshold=math.ceil(2**18*L/kap)
        labels=rng.multinomial(N,lam/4)
        vv=np.zeros((d,4));e=np.ones(d);keep=np.zeros(d,dtype=bool)
        # Aggregate conditional multinomial simulation represents N classical
        # records without generating or claiming actual source calls.
        for i,(u,n) in enumerate(zip(us,labels)):
            if n<=256*L: continue
            probabilities=4*w*(X@u)**2
            probabilities/=probabilities.sum()
            counts=rng.multinomial(int(n),probabilities)
            mean=np.einsum('a,ai,aj->ij',counts,X,X)/n
            ev,vec=np.linalg.eigh(mean);v=vec[:,-1]
            vv[i]=v;e[i]=max(0,1-(u@v)**2)
            errs['pilot_direction_bound_excess']=max(errs['pilot_direction_bound_excess'],e[i]-256*L/n)
            if n>=threshold and ev[-1]-ev[-2]>=1/12: keep[i]=True
        assert np.all(labels[ N*lam/4>=8*L ]>=N*lam[N*lam/4>=8*L]/8)
        assert sum(lam*e)<=4096*d*L/N
        discarded=float(sum(lam[~keep]))
        errs['discarded_mass_bound_excess']=max(errs['discarded_mass_bound_excess'],discarded-2**22*d*L/(kap*N))
        anchor,exact_anchor,mesh=gridpoint_near(xstar,F(1,100))
        assert np.all((vv[keep]@anchor)**2>=9*kap/16)
        errs['anchor_true_balance_deficit']=max(errs['anchor_true_balance_deficit'],kap/4-np.min((us[keep]@anchor)**2))
        sh=np.zeros((d,4));sh[keep]=vv[keep]/(vv[keep]@anchor)[:,None]
        true=np.zeros((d,4));true[keep]=us[keep]/(us[keep]@anchor)[:,None]
        wi=lam*(us@anchor)**2
        Er=float(sum(wi*np.sum((sh-true)**2,axis=1)))
        errs['weighted_ratio_bound_excess']=max(errs['weighted_ratio_bound_excess'],Er-16*sum(lam*e)/kap)
        retained_rows+=int(sum(keep));missing_rows+=int(sum((lam>0)&(labels==0)));pilot_models+=1
        # A genuine physical source with coherent branch splitting and mixed
        # unrecorded output dephasing. Rare coordinates are not source flags.
        W=np.vstack([np.sqrt(s)*np.eye(8) for s in splits])
        probs=rng.dirichlet(np.ones(3))
        kraus=[np.sqrt(p)*W@np.diag(np.exp(1j*rng.uniform(-math.pi,math.pi,8)))@U for p in probs]
        assert np.linalg.norm(sum(K.conj().T@K for K in kraus)-np.eye(8))<1e-12
        T0=lossstate(kraus,anchor)
        assert np.linalg.norm(np.diag(T0).real-wi)<1e-12
        # A normalized acquired-bank surrogate with an explicitly evaluated
        # Bures error, not an assumed PSD completion of diagonal measurements.
        mix=.0001;tau=(1-mix)*T0+mix*np.eye(d)/d
        fidelity=float(np.trace(root(root(T0)@tau@root(T0))).real)
        m=max(0,1-fidelity)
        V,_=np.linalg.qr(rng.normal(size=(d,d//2))+1j*rng.normal(size=(d,d//2)))
        ks=[V[2*j:2*j+2] for j in range(d//2)]
        C=sum(np.outer(K.T.reshape(-1),K.T.reshape(-1).conj()) for K in ks)
        tr=np.trace(C.reshape(d//2,2,d//2,2),axis1=1,axis2=3)
        errs['decoder_partial_trace']=max(errs['decoder_partial_trace'],np.linalg.norm(tr-np.eye(d//2)))
        for _ in range(5):
            x=rng.normal(size=4);x/=np.linalg.norm(x)
            T=lossstate(kraus,x);PTP=keep[:,None]*T*keep[None,:]
            rr=true@x;reconstructed=rr[:,None]*T0*rr[None,:]
            errs['projected_factorization']=max(errs['projected_factorization'],np.linalg.norm(PTP-reconstructed))
            ell=float(1.5*np.trace(C.T@T).real);ellP=float(1.5*np.trace(C.T@PTP).real)
            errs['discarded_root_bound_excess']=max(errs['discarded_root_bound_excess'],abs(math.sqrt(ell)-math.sqrt(max(0,ellP)))-math.sqrt(3*discarded))
            rh=sh@x;pred=rh[:,None]*tau*rh[None,:]
            ellhat=float(1.5*np.trace(C.T@pred).real)
            bound=math.sqrt(3*discarded)+math.sqrt(3*Er)+math.sqrt(24*m/kap)
            errs['full_task_root_bound_excess']=max(errs['full_task_root_bound_excess'],abs(math.sqrt(ell)-math.sqrt(max(0,ellhat)))-bound)
            probes+=1
        physical_models+=1
        summary.append({'rare_split':rare,'retained':int(sum(keep)),'missing':int(sum(labels==0)),
            'discarded_selector_mass':discarded,'row_error':Er,'mesh_denominator':mesh})

exact=0
for kap,ga,ep,d,L in itertools.product([F(1,4),F(1,100)],[F(1),F(1,7)],
    [F(1),F(1,19)],[4,16,48],[1,12,64]):
    z=F(2**18*L,1)/kap;threshold=(z.numerator+z.denominator-1)//z.denominator
    zN=F(2**43*d*L,1)/(kap*ga*ep);N=(zN.numerator+zN.denominator-1)//zN.denominator
    assert threshold<=F(2**19*L,1)/kap
    Lambda=F(8*d*threshold,N);E=F(2**16*d*L,1)/(kap*N);m=kap*ga*ep/2**22
    assert Lambda<=F(2**22*d*L,1)/(kap*N)
    assert 9*Lambda+9*E+72*m/kap<=ga*ep/32768
    assert F(27,32768)<F(1,512)
    assert F(27,32768)+F(1,128)<F(1,64)
    assert F(2,64)+F(1,2)<1
    exact+=1
assert max(errs.values())<1e-10,errs
src=Path(__file__).with_name('ACQUIRED_BALANCED_ROW_ANCHOR_EXTENSION.md')
out={'status':'PASS author diagnostics; independent receiving pending',
    'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
    'exact_rational_net_cover_cases':coverage,'largest_chord_over_sqrt_kappa':coverage_max,
    'aggregate_conditional_pilot_models':pilot_models,'represented_classical_records_per_model':10**12,
    'total_represented_classical_source_trials':pilot_models*10**12,
    'individual_classical_trial_records_materialized':False,
    'evidence_class':'Aggregated multinomial count simulation plus source-disabled algebraic physical-model diagnostics',
    'retained_rows':retained_rows,'missing_nonzero_rows':missing_rows,
    'actual_physical_source_models':physical_models,'encoder_probes':probes,
    'exact_budget_cases':exact,'max_residuals':errs,'model_summary':summary,
    'actual_source_calls':0,
    'scope':'Known physical fixture diagnostics plus aggregated classical multinomial simulation. Net covering checked by exact rational witness-near grid points; exhaustive anchor search, production SDP, receiver circuit and hardware not executed. No structural promise inferred from data.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='model_summary'},indent=2))
