"""Independent deterministic checks; no RNG draws or source-trial samples."""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, math, itertools
import numpy as np
from scipy.stats import binom

HERE=Path(__file__).resolve().parent
Q=HERE.parent
def mm(A,B): return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def tr(A): return [list(z) for z in zip(*A)]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def stereo(t):
    s=sum(a*a for a in t)
    return [2*a/(1+s) for a in t]+[(1-s)/(1+s)]
def hh(v):
    sign=1 if v[0]>=0 else -1
    w=[F(i==0)+sign*v[i] for i in range(4)];n=sum(a*a for a in w)
    assert n>=2
    return [[F(i==j)-2*w[i]*w[j]/n for j in range(4)] for i in range(4)]

control_cases=0
for tt in itertools.product([F(-1,3),F(0),F(2,5)],repeat=3):
    v=stereo(tt);H=hh(v)
    assert sum(a*a for a in v)==1 and mm(tr(H),H)==eye(4)
    assert all(sum(v[i]*H[i][a] for i in range(4))==0 for a in [1,2,3])
    # The three projectors sum to I-vv^T exactly, including v_1=0 cases.
    for i,j in itertools.product(range(4),repeat=2):
        assert sum(H[i][a]*H[j][a] for a in [1,2,3])==F(i==j)-v[i]*v[j]
    control_cases+=1

net_cases=0
for tt in itertools.product([F(-3,5),F(-1,7),F(2,9)],repeat=3):
    x=stereo(tt)
    for kap in [F(1,4),F(1,100),F(1,100000)]:
        M=1
        while M*M*kap<4096:M*=2
        j=max(range(4),key=lambda j:abs(x[j]));sign=1 if x[j]>=0 else -1
        assert abs(x[j])>=F(1,2)
        ids=[i for i in range(4) if i!=j]
        t=[x[i]/(1+abs(x[j])) for i in ids]
        assert max(map(abs,t))<=F(2,3)
        rounded=[F(round(a*M),M) for a in t];v=stereo(rounded)
        z=[F(0)]*4
        for a,i in enumerate(ids):z[i]=v[a]
        z[j]=sign*v[3]
        assert sum(a*a for a in z)==1
        assert sum((a-b)**2 for a,b in zip(x,z))<=F(3,M*M)<kap/256
        net_cases+=1

constant_cases=0
for kap,gam,eps,d,L in itertools.product([F(1,4),F(1,73),F(1,100000)],
    [F(1),F(2,7)],[F(1),F(1,31)],[4,10,32],[1,19]):
    ceil=lambda f:(f.numerator+f.denominator-1)//f.denominator
    T=ceil(F(2**18*L)/kap)
    N=ceil(F(2**43*d*L)/(kap*gam*eps))
    assert T<=F(2**19*L)/kap
    lam=F(8*d*T,N);er=F(2**16*d*L)/(kap*N);m=kap*gam*eps/2**22
    assert lam<=F(2**22*d*L)/(kap*N)
    assert 9*lam+9*er+72*m/kap<=gam*eps/32768
    # Retained eigenvector error and anchor thresholds, squared rational bounds.
    e=F(256*L,T);assert e<=kap/1024 and 2*e<kap/256
    assert F(128,9)<16
    # Validation residual and fast-subclass count cap, including ceilings.
    LM=gam*eps/2**20;SM=kap*gam*eps/2**24
    assert 9*LM+81*SM/kap+72*SM/kap==F(297,2**24)*gam*eps
    assert F(297,2**24)<F(1,32768)
    NP=ceil(F(2**44*d*L)/(kap*gam*eps))
    assert F(2**22*d*L)/(kap*NP)<=LM/4
    assert F(4096*d*L,NP)<=SM/256
    assert F(27,32768)<F(1,1024)
    assert F(1,512)+2*F(1,2048)+F(1,512)==F(5,1024)
    constant_cases+=1

# Physical channels use two rational-amplitude unitary Kraus branches, not the
# author's diagonal-noise/source fixture. The branches move selector rows
# differently and introduce complex phases. A common six-state purification is
# retained across encoder probes, so no independent-purification alignment occurs.
states=[np.array([1,0]),np.array([0,1]),np.array([1,1])/np.sqrt(2),
    np.array([1,-1])/np.sqrt(2),np.array([1,1j])/np.sqrt(2),np.array([1,-1j])/np.sqrt(2)]
def purif(Ks,x):
    V=np.kron(np.asarray(x).reshape(4,1),np.eye(2))
    return np.column_stack([np.kron(K@V@p,np.array([-p[1],p[0]]))/np.sqrt(6)
        for p in states for K in Ks])
def choi_decoder(k,shift):
    # Actual CPTP decoder: relabel each pair of physical basis states to qubit,
    # retaining the pair index in a discarded environment. Shift is a unitary.
    P=np.roll(np.eye(k),shift,axis=1)
    Ds=[P[2*j:2*j+2] for j in range(k//2)]
    return sum(np.outer(D.T.reshape(-1),D.T.reshape(-1).conj()) for D in Ds)
errors={k:0. for k in ['source_TP','norm','common_purification','discard_mean',
    'kernel_mean','projection_residual_excess','same_decoder_root_excess','decoder_TP']}
physical_cases=probe_cases=kernel_cases=0
ts=[(F(1,5),F(-1,7),F(1,9)),(F(-1,6),F(2,7),F(1,8)),(F(0),F(1,9),F(-1,5))]
for shift,phase_mode,mask_mode in itertools.product([1,3,5],[0,1],[0,1]):
    P=np.roll(np.eye(8),shift,axis=0)
    phases=np.array([1j**((j*(phase_mode+1))%4) for j in range(8)])
    W=np.diag(phases)@P
    Ks=[.6*np.eye(8),.8*W]
    errors['source_TP']=max(errors['source_TP'],np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(8)))
    Zs=[purif(Ks,e) for e in np.eye(4)]
    G=[np.column_stack([Z[i] for Z in Zs]) for i in range(16)]
    B=[(g.conj().T@g).real for g in G]
    assert np.linalg.norm(sum(B)-np.eye(4))<1e-12
    vv=np.array([stereo(ts[i%3]) for i in range(16)],float)
    retained=np.array([i%4!=mask_mode for i in range(16)])
    x0=np.array([0,0,0,1.]);kap=.25
    assert min((vv[retained]@x0)**2)>=9*kap/16
    Lambda=float(sum(np.trace(b) for i,b in enumerate(B) if not retained[i]))
    S=float(sum(np.trace(b)-v@b@v for i,(b,v) in enumerate(zip(B,vv)) if retained[i]))
    pd=sum(sum(np.linalg.norm(purif(Ks,e),axis=1)[~retained]**2) for e in np.eye(4))/4
    errors['discard_mean']=max(errors['discard_mean'],abs(pd-Lambda/4))
    pk=0.
    for i in np.flatnonzero(retained):
        H=np.array(hh(stereo(ts[i%3])),float)
        for a in [1,2,3]:
            z=purif(Ks,H[:,a]);pk+=np.vdot(z[i],z[i]).real/48;kernel_cases+=1
    errors['kernel_mean']=max(errors['kernel_mean'],abs(pk-S/48))
    Z0=purif(Ks,x0);ratio=np.zeros((16,4));ratio[retained]=vv[retained]/(vv[retained]@x0)[:,None]
    C=choi_decoder(8,shift)
    errors['decoder_TP']=max(errors['decoder_TP'],np.linalg.norm(np.trace(C.reshape(8,2,8,2),axis1=1,axis2=3)-np.eye(8)))
    for t in ts+[(F(0),F(0),F(0))]:
        x=np.array(stereo(t),float);Z=purif(Ks,x);T=Z@Z.conj().T
        errors['norm']=max(errors['norm'],abs(np.trace(T).real-1))
        errors['common_purification']=max(errors['common_purification'],np.linalg.norm(Z-sum(x[j]*Zs[j] for j in range(4))))
        Zpred=(ratio@x)[:,None]*Z0
        b=math.sqrt(Lambda)+3*math.sqrt(S/kap)
        errors['projection_residual_excess']=max(errors['projection_residual_excess'],np.linalg.norm(Z-Zpred)-b)
        ell=1.5*np.trace(C.T@T).real
        pred=1.5*np.trace(C.T@(Zpred@Zpred.conj().T)).real
        errors['same_decoder_root_excess']=max(errors['same_decoder_root_excess'],abs(math.sqrt(max(0,ell))-math.sqrt(max(0,pred)))-math.sqrt(3)*b)
        probe_cases+=1
    physical_cases+=1
assert max(errors.values())<1e-12,errors

tail_cases=0;tail_max=0.
for u,beta in itertools.product([F(1,1000),F(1,17),F(1,3),F(4,5)],
    [F(1,2048),F(1,128),F(1,10)]):
    n=math.ceil(64/float(u)*math.log(1/float(beta)));cut=(n*u/2).numerator//(n*u/2).denominator
    fa=binom.cdf(cut,n,float(u));fr=binom.sf(cut,n,float(u/4))
    assert fa<=float(beta) and fr<=float(beta)
    assert math.exp(-n*float(u)/8)<=float(beta)
    assert math.exp(-n*float(u)/12)<=float(beta)
    tail_max=max(tail_max,float(fa),float(fr));tail_cases+=1

# Branch-risk and high-probability resource accounting are exact rational checks.
mixtures=0
for acc,pbad,fbad,star,gam,eps in itertools.product(
    [F(0),F(1,10000),F(1,3),F(1)],[F(0),F(1,2)],
    [F(0),F(1)],[F(0),F(2,5)],[F(1),F(1,7)],[F(1),F(1,19)]):
    base=(1+gam/2)*star
    bad=min(acc,2*eps/2048*pbad+eps/512*fbad)
    accepted_good=acc-bad
    worst=(1-acc)*(base+eps/512)+accepted_good*(base+eps/1024)+bad
    assert worst<=base+5*eps/1024
    mixtures+=1

binding_counts={}
for rel,key in [('ordinary_balanced_row_anchor_20261028/balanced_row_anchor_independent_receipt.json','sha256_relative_to_programme_root'),
    ('ordinary_generic_matrix_gls_sylvester_clipping_20261028_independent_receipt.json','sha256')]:
    receipt=json.loads((Q/rel).read_text())
    for name,digest in receipt[key].items():
        assert hashlib.sha256((Q/name).read_bytes()).hexdigest()==digest,(rel,name)
    binding_counts[rel]=len(receipt[key])
sources=['ACQUIRED_BALANCED_ROW_ANCHOR_EXTENSION.md','ORDINARY_ROW_RESIDUAL_VALIDATION_AND_FALLBACK.md']
out={'status':'PASS independent deterministic mathematical diagnostics',
    'source_sha256':{s:hashlib.sha256((HERE/s).read_bytes()).hexdigest() for s in sources},
    'exact_rational_control_cases':control_cases,'exact_rational_net_cases':net_cases,
    'exact_budget_and_count_cases':constant_cases,'physical_channels':physical_cases,
    'encoder_probes':probe_cases,'ordinary_kernel_expectation_cases':kernel_cases,
    'binomial_tail_cases':tail_cases,'maximum_tail_probability':tail_max,
    'exact_acceptance_fallback_mixture_cases':mixtures,'max_residuals':errors,
    'verified_import_binding_counts':binding_counts,
    'actual_source_calls':0,'sampled_source_outcomes':0,'rng_draws':0,
    'evidence_class':'Deterministic exact rational algebra, source-disabled physical channel expectation calculations, and numerical binomial CDF evaluations. No aggregate or individual source-trial sampling, acquisition circuit, production SDP, or hardware execution.'}
(HERE/'row_anchor_validation_independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
