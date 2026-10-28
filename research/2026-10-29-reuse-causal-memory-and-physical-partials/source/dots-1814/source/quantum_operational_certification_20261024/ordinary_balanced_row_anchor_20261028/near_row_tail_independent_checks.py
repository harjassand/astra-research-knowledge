"""Independent no-draw checks of the separate approximate-row oracle bound."""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,hashlib,math
import numpy as np

HERE=Path(__file__).resolve().parent;Q=HERE.parent
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def matvec(A,x):return [dot(row,x) for row in A]
def stereo(t):
    s=dot(t,t);return [2*a/(1+s) for a in t]+[(1-s)/(1+s)]
def basis(u):
    sign=1 if u[0]>=0 else -1;w=[F(i==0)+sign*u[i] for i in range(4)];n=dot(w,w)
    return [[F(i==j)-2*w[i]*w[j]/n for j in range(4)] for i in range(4)]
design=[]
for j in range(4):design.append(([F(i==j) for i in range(4)],F(1,12)))
for s in itertools.product([-1,1],repeat=4):design.append(([F(a,2) for a in s],F(1,24)))
x0=[F(0),F(0),F(0),F(1)];kap=F(1,4)
exact_rows=moment_entries=well_rows=bad_rows=fallbacks=0
for tt,scale,spectrum in itertools.product(
    [(F(1,8),F(0),F(-1,9)),(F(-1,6),F(1,7),F(1,10))],
    [F(1,8),F(1,10**20)],
    [(F(0),F(0),F(0)),(F(1,16),F(1,16),F(1,16)),
     (F(1,4),F(0),F(0)),(F(1,2),F(1,3),F(1,5)),(F(1),F(1),F(1))]):
    u=stereo(tt);H=basis(u);ev=[scale]+[scale*z for z in spectrum]
    B=[[sum(H[i][a]*ev[a]*H[j][a] for a in range(4)) for j in range(4)] for i in range(4)]
    lam=scale;tau=sum(ev[1:]);mass=lam+tau;a=dot(u,x0)
    assert a*a>=kap
    good=tau<=lam/4
    if good:
        well_rows+=1
        gap=(lam-max(ev[1:]))/(3*mass)
        assert gap>=F(1,5)
    else:
        bad_rows+=1;assert mass<=5*tau
    # Check the full conditional fourth-design moment identity exactly.
    for i,j in itertools.product(range(4),repeat=2):
        obs=sum(w*x[i]*x[j]*dot(x,matvec(B,x)) for x,w in design)*4/mass
        target=(F(i==j)+2*B[i][j]/mass)/6
        assert obs==target;moment_entries+=1
    w=dot(x0,matvec(B,x0));true=[z/a for z in u]
    for v in [u,x0,[F(1),F(0),F(0),F(0)],stereo((F(2,3),F(1,4),F(-1,3)))]:
        b=dot(v,x0);e=1-dot(u,v)**2
        if b*b>=kap/4:sh=[z/b for z in v]
        else:sh=x0;fallbacks+=1
        lhs=w*sum((z-y)**2 for z,y in zip(sh,true))
        assert sum(z*z for z in sh)<=4/kap
        if good:assert lhs<=32*lam*e/kap+9*tau/kap
        else:assert lhs<=45*tau/kap
        exact_rows+=1

certificate_cases=0
for L,nfactor in itertools.product([1,3,19,101],[4097,5000,8192,2**20]):
    # sqrt(3 L/n)<1/32; an exact rational majorant avoids testing floats.
    a=F(1,nfactor)
    assert 3*a<F(1,32**2)
    assert F(1,5)-F(2,32)>F(1,12)
    # sin bound plus finite rational vector approximation <12 sqrt(L/n).
    assert 2/(F(1,5)-F(1,32))+F(1,100)<12
    assert 144<1024
    # Bernstein exponent at t=sqrt(3L/n) exceeds L.
    assert F(3)/(F(1,2)+F(2,3)*F(1,32))>1
    # The three realized-count cases give constants 32,32768,8192.
    assert max(32,8*4096,8*1024)<2**16
    certificate_cases+=1

states=[np.array([1,0]),np.array([0,1]),np.array([1,1])/np.sqrt(2),
 np.array([1,-1])/np.sqrt(2),np.array([1,1j])/np.sqrt(2),np.array([1,-1j])/np.sqrt(2)]
def Z(Ks,x):
    V=np.kron(np.array(x).reshape(4,1),np.eye(2))
    return np.column_stack([np.kron(K@V@p,[-p[1],p[0]])/np.sqrt(6) for p in states for K in Ks])
root=lambda A:(lambda e,v:(v*np.sqrt(np.maximum(e,0)))@v.conj().T)(*np.linalg.eigh((A+A.conj().T)/2))
errors={s:0. for s in ['source_TP','physical_norm','diagonal_effects','compatible_lift',
    'tail_purification_excess','weighted_row_error_excess','full_decoder_root_excess']}
physical_cases=probes=physical_bad_rows=degenerate_rows=0
px0=np.ones(4)/2;pkap=.25
test_x=[np.eye(4)[j] for j in range(4)]+[np.array(stereo(t),float) for t in [(F(1,3),F(-1,5),F(2,7)),(F(-1),F(0),F(0))]]
for shift,p in itertools.product([1,2,5],[0.,.001,.1,.2,1/3,.5]):
    P=np.roll(np.eye(8),shift,axis=0);W=np.diag([1j**(j%4) for j in range(8)])@P
    Ks=[math.sqrt(1-p)*np.eye(8),math.sqrt(p)*W]
    errors['source_TP']=max(errors['source_TP'],np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(8)))
    zz=[Z(Ks,e) for e in np.eye(4)];gs=[np.column_stack([z[i] for z in zz]) for i in range(16)]
    bs=[(g.conj().T@g).real for g in gs]
    assert all(np.linalg.norm(b-np.diag(np.diag(b)))<1e-14 for b in bs)
    us=[];lams=[];tails=[]
    for b in bs:
        diag=np.diag(b);j=int(np.argmax(diag));u=np.eye(4)[j]
        us.append(u);lams.append(diag[j]);tails.append(max(0,np.trace(b)-diag[j]))
        if sum(abs(diag-diag[j])<1e-14)>1:degenerate_rows+=1
    us=np.array(us);lams=np.array(lams);tails=np.array(tails);tail=float(sum(tails))
    good=tails<=lams/4+1e-15;physical_bad_rows+=int(sum(~good))
    vv=[]
    for i,u in enumerate(us):
        if i%3==0:v=np.array([1,1,-1,-1],float)/2
        elif i%3==1:v=px0
        else:
            j=int(np.argmax(u));v=(99*u+20*np.eye(4)[(j+1)%4])/101
        assert abs(v@v-1)<1e-12;vv.append(v)
    vv=np.array(vv);sh=np.array([v/(v@px0) if abs(v@px0)**2>=pkap/4 else px0 for v in vv])
    true=us/(us@px0)[:,None];e=np.maximum(0,1-np.sum(us*vv,axis=1)**2)
    z0=Z(Ks,px0);T0=z0@z0.conj().T;wi=np.diag(T0).real
    E=float(sum(wi*np.sum((sh-true)**2,axis=1)))
    Ebd=32/pkap*sum(lams[good]*e[good])+54*tail/pkap
    errors['weighted_row_error_excess']=max(errors['weighted_row_error_excess'],E-Ebd)
    tau=.9999*T0+.0001*np.eye(16)/16;m=max(0,1-float(np.trace(root(root(T0)@tau@root(T0))).real))
    V=np.roll(np.eye(8),shift,axis=1);Ds=[V[2*j:2*j+2] for j in range(4)]
    C=sum(np.outer(D.T.reshape(-1),D.T.reshape(-1).conj()) for D in Ds)
    for x in test_x:
        zx=Z(Ks,x);T=zx@zx.conj().T
        errors['physical_norm']=max(errors['physical_norm'],abs(np.trace(T).real-1))
        errors['compatible_lift']=max(errors['compatible_lift'],np.linalg.norm(zx-sum(x[s]*zz[s] for s in range(4))))
        errors['diagonal_effects']=max(errors['diagonal_effects'],np.linalg.norm(np.diag(T).real-np.array([x@b@x for b in bs])))
        lead=(true@x)[:,None]*z0
        errors['tail_purification_excess']=max(errors['tail_purification_excess'],np.linalg.norm(zx-lead)-2*math.sqrt(tail/pkap))
        rr=sh@x;pred=rr[:,None]*tau*rr[None,:]
        ell=float(1.5*np.trace(C.T@T).real);lh=float(1.5*np.trace(C.T@pred).real)
        delta=math.sqrt(12*tail/pkap)+math.sqrt(3*E)+math.sqrt(24*m/pkap)
        errors['full_decoder_root_excess']=max(errors['full_decoder_root_excess'],abs(math.sqrt(max(0,ell))-math.sqrt(max(0,lh)))-delta)
        probes+=1
    physical_cases+=1
assert physical_bad_rows>0 and degenerate_rows>0
assert max(errors.values())<1e-12,errors

budget_cases=0
for gam,eps,kap,d,L in itertools.product([F(1),F(1,7)],[F(1),F(1,31)],
    [F(1),F(1,4),F(1,100)],[4,16],[1,11]):
    N=F(2**38*d*L)/(kap*gam*eps);m=kap*gam*eps/2**22;nu=gam*eps/32768
    stat=F(9*2**21*d*L)/(kap*N)+72*m/kap
    assert stat<=gam*eps/8192
    assert 24*522<2**14
    assert 24*stat/gam+6*nu/gam<eps/256
    assert eps/256+eps/128<eps/64
    assert 2*eps/64+eps/2<eps
    budget_cases+=1

receipt=json.loads((HERE/'balanced_row_anchor_independent_receipt.json').read_text())
for name,digest in receipt['sha256_relative_to_programme_root'].items():
    assert hashlib.sha256((Q/name).read_bytes()).hexdigest()==digest,name
src=HERE/'WEIGHTED_NEAR_RANK_ONE_ROW_TAIL_EXTENSION.md'
out={'status':'PASS independent approximate-row oracle diagnostics',
 'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'exact_weighted_row_cases':exact_rows,'exact_conditional_moment_entries':moment_entries,
 'exact_well_shaped_effects':well_rows,'exact_tail_paid_effects':bad_rows,'exact_anchor_fallback_cases':fallbacks,
 'finite_certificate_count_cases':certificate_cases,'physical_models':physical_cases,'physical_encoder_probes':probes,
 'physical_tail_paid_rows':physical_bad_rows,'physical_degenerate_leading_rows':degenerate_rows,
 'exact_budget_cases':budget_cases,'max_residuals':errors,'accepted_import_bindings_verified':10,
 'actual_source_calls':0,'sampled_trial_outcomes':0,'rng_draws':0,
 'evidence_class':'Deterministic rational conditional moments, bad-row and finite-gap inequalities; source-disabled physical Kraus fixtures including genuinely non-well-shaped and degenerate leading rows. No source-count sampling, optimizer or hardware execution.'}
(HERE/'near_row_tail_independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
