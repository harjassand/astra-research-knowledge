#!/usr/bin/env python3
"""Deterministic source-disabled mathematical fixtures; no acquisition samples/RNG."""
import itertools, json, math, hashlib
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.linalg import expm

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
P=[I,X,Y,Z]; AX=[X,Y,Z]

def kron(*xs):
    y=np.array([[1]],complex)
    for x in xs: y=np.kron(y,x)
    return y

def site_op(a,k,n): return kron(*(a if l==k else I for l in range(n)))
def opnorm(a): return float(np.linalg.norm(a,2))
def trnorm(a): return float(np.sum(np.abs(np.linalg.eigvalsh((a+a.conj().T)/2))))
def partial_site(a,k,n):
    t=a.reshape([2]*(2*n))
    remaining=list(range(n))
    for l in reversed(range(n)):
        if l!=k:
            p=remaining.index(l); t=np.trace(t,axis1=p,axis2=p+len(remaining));remaining.pop(p)
    return t.reshape(2,2)
def bloch(a): return np.array([np.trace(p@a).real for p in AX])
def local_rotation(v):
    return np.array([[np.trace(a@v@b@v.conj().T).real/2 for b in AX] for a in AX])
def k_mat(m):
    k=np.empty((4,4));
    k[0,0]=m[0,0]+m[1,1]+m[2,2]
    k[1,1]=m[0,0]-m[1,1]-m[2,2]
    k[2,2]=-m[0,0]+m[1,1]-m[2,2]
    k[3,3]=-m[0,0]-m[1,1]+m[2,2]
    for a,b,v in [(0,1,m[2,1]-m[1,2]),(0,2,m[0,2]-m[2,0]),(0,3,m[1,0]-m[0,1]),(1,2,m[0,1]+m[1,0]),(1,3,m[0,2]+m[2,0]),(2,3,m[1,2]+m[2,1])]: k[a,b]=k[b,a]=v
    return k
def fit(m):
    vals,u=np.linalg.eigh(k_mat(m)); v=u[:,-1]; w=v[0]*I-1j*sum((v[j+1]*AX[j] for j in range(3)),np.zeros((2,2),complex)); return local_rotation(w),vals[-1]

def normalized(m):
    out=np.zeros((3,3))
    for j in [0,2]:
        x=m[:,j]; out[:,j]=x/np.linalg.norm(x) if np.linalg.norm(x)>1e-18 else np.eye(3)[:,j]
    return out

violations={}; tests={}; margins=[]; taus=[]; kappas=[]
def chk(key,v,tol=3e-11):
    violations[key]=max(violations.get(key,-1e300),float(v)); tests[key]=tests.get(key,0)+1
    assert v<=tol,(key,v)

physical_fixtures=[]
for q in [1,2]:
    n=q+1; d=2**q
    paulis=[kron(*(P[a] for a in alpha)) for alpha in itertools.product(range(4),repeat=q)]
    labels=list(itertools.product(range(4),repeat=q))
    vs=[expm(-1j*(0.31+0.07*l)*(X+2*Y-Z)/math.sqrt(6)) for l in range(q)]
    vfull=kron(*vs,I)
    h=sum((site_op(X,l,n)@site_op(Z,q,n)+0.6*site_op(Z,l,n)@site_op(X,q,n) for l in range(q)),np.zeros((2**n,2**n),complex))
    if q==2: h+=0.4*site_op(X,0,n)@site_op(Y,1,n)
    h/=opnorm(h)
    for theta in [0.015,0.055,0.105]:
        u=vfull@expm(-1j*theta*h)
        a={(l,j):site_op(vs[l]@AX[j]@vs[l].conj().T,l,n) for l in range(q) for j in [0,2]}
        b={(l,j):u@kron(site_op(AX[j],l,q),I)@u.conj().T for l in range(q) for j in [0,2]}
        tau=max(opnorm(a[key]-b[key]) for key in a);taus.append(tau);assert tau<=0.25
        c=1-tau*tau/2
        for mix in [1.,1/3,1/100,1/10000]:
            history=[]
            for t in range(5):
                base=[]
                for ai,alpha in enumerate(labels):
                    if ai==0: ga=I.copy()
                    else:
                        direction=np.array([math.sin(ai+t+.3),math.cos(2*ai-t+.7),math.sin(3*ai+2*t+.9)])
                        direction/=np.linalg.norm(direction)
                        ga=(0.045/(len(labels)-1))*(I+0.8*sum((direction[j]*AX[j] for j in range(3)),np.zeros((2,2),complex)))
                    base.append(ga)
                total=sum(base); normalizer=np.trace(total).real
                base=[x/normalizer for x in base];total/=normalizer
                gs=[mix*x+(1-mix)*total/len(labels) for x in base]
                for aa in gs: chk('gauge_positive',-np.linalg.eigvalsh(aa).min())
                for aa in gs: chk('global_cp_dominance',-np.linalg.eigvalsh(gs[0]-aa).min())
                hs={};lams={};deltas={};means={}
                for l in range(q):
                    for j in [0,2]:
                        char=[]
                        for pp in paulis:
                            sj=site_op(AX[j],l,q); char.append(round(np.trace(pp@sj@pp@sj).real/d))
                        hj=sum((sg*g for sg,g in zip(char,gs)),np.zeros((2,2),complex))
                        lam=np.trace(hj).real;hs[l,j]=hj;lams[l,j]=lam
                        # Direct safe supplied margin, verified below in Loewner order.
                        kap=float(np.linalg.eigvalsh(hj).min()/np.linalg.eigvalsh(total).max());kappas.append(kap);assert kap>0
                        chk('cp_margin',-np.linalg.eigvalsh(hj-kap*total).min())
                        rr=u@kron(np.eye(d)/d,hj)@u.conj().T
                        dd=b[l,j]@rr;deltas[l,j]=dd
                        chk('contrast_hermitian',opnorm(dd-dd.conj().T))
                        chk('contrast_lambda_trace_norm',abs(trnorm(dd)-lam))
                        for k in range(n):
                            red=partial_site(dd,k,n);mv=bloch(red);means[l,j,k]=mv
                            if k==l:
                                av=local_rotation(vs[l])[:,j]
                                chk('true_site_projection',lam*c-av@mv)
                                chk('true_site_norm_cap',np.linalg.norm(mv)-lam)
                                chk('relative_column_bias',np.linalg.norm(mv-lam*av)-tau*lam)
                                chk('normalized_column_bias',np.linalg.norm(mv/np.linalg.norm(mv)-av)-tau)
                            else:chk('wrong_site_leakage',np.linalg.norm(mv)-tau*lam)
                history.append((lams,means))
                if mix==1 and theta==0.055 and t==2: physical_fixtures.append((q,n,u,paulis,gs,means))
            # Coarse and normalized fine means from changing gauge histories.
            for l in range(q):
                lam=sum(x[0][l,0] for x in history)/len(history)
                coarse=[sum((x[1][l,0,k] for x in history),np.zeros(3))/len(history) for k in range(n)]
                gap=np.linalg.norm(coarse[l])-max(np.linalg.norm(coarse[k]) for k in range(n) if k!=l)
                chk('adaptive_average_gap',lam*(c-tau)-gap);margins.append(gap/lam)
                m=np.zeros((3,3));r=local_rotation(vs[l])
                for j in [0,2]:m[:,j]=sum((x[1][l,j,l] for x in history),np.zeros(3))/len(history)
                mt=normalized(m);err=np.linalg.norm(mt-r@np.diag([1,0,1]));chk('stacked_normalized_bias',err-math.sqrt(2)*tau)
                rh,lammax=fit(mt);pair=np.linalg.norm((rh-r)[:,[0,2]])
                chk('proper_fit_objective',abs(np.sum(rh*mt)-lammax));chk('proper_fit_feasibility',np.linalg.norm(rh.T@rh-np.eye(3))+abs(np.linalg.det(rh)-1))
                chk('direct_pair_fit',pair-2*err)
                ell=np.linalg.norm(rh-r)**2/8;chk('full_rotation_pair_bound',ell-pair*pair/4)

# Enumerate actual Born event laws: both logical axis choices and every output basis/outcome.
born_events=0
for q,n,u,paulis,gs,means in physical_fixtures:
    got=[np.zeros((3,3)) for _ in range(q)];probtotal=0.
    for js in itertools.product([0,2],repeat=q):
      for ss in itertools.product([-1,1],repeat=q):
        rin=kron(*((I+s*AX[j])/2 for s,j in zip(ss,js)))
        rout=sum((u@kron(pp@rin@pp,g)@u.conj().T for pp,g in zip(paulis,gs)),np.zeros((2**n,2**n),complex))
        for axes in itertools.product(range(3),repeat=n):
          for outs in itertools.product([-1,1],repeat=n):
            proj=kron(*((I+b*AX[a])/2 for a,b in zip(axes,outs)))
            pr=float(np.trace(proj@rout).real)/(4**q*3**n);chk('born_probability_nonnegative',-pr);probtotal+=pr;born_events+=1
            for l in range(q):got[l][axes[l],js[l]]+=pr*6*ss[l]*outs[l]
    chk('born_total_probability',abs(probtotal-1))
    for l in range(q):
        want=np.zeros((3,3));want[:,0]=means[l,0,l];want[:,2]=means[l,2,l]
        chk('actual_fine_feedback_identity',np.linalg.norm(got[l]-want))

# Exact rational normalization certificates from possible integer count vectors.
rational=[]
for n in [16,128,4096,10**8]:
  for raw in [(0,0,0),(1,0,0),(1,1,-1),(-3,5,-7)]:
    count=tuple(Fraction(6*k,n) for k in raw);sq=sum((x*x for x in count),Fraction(0));eta=Fraction(1,1024)
    if not sq:rational.append({'N':n,'counts':raw,'fallback':True});continue
    lo,hi=Fraction(0),Fraction(6);steps=0;target=6*eta/n
    while hi-lo>target:
        mid=(lo+hi)/2
        if mid*mid>=sq:hi=mid
        else:lo=mid
        steps+=1
    assert lo*lo<=sq<=hi*hi and hi-lo<=target and sq/(hi*hi)<=1
    assert any(x and abs(x)>=Fraction(6,n) for x in count)
    rational.append({'N':n,'counts':raw,'fallback':False,'steps':steps,'bound_steps':math.ceil(math.log2(n/float(eta)))+1,'exact_unit_ball':True,'exact_sqrt_bracket':True,'upper_denominator_bits':hi.denominator.bit_length()})

# Exact symbolic/rational parts of the announced constants.
c=Fraction(31,32)
assert c-Fraction(1,4)-Fraction(3,8)==Fraction(11,32)
root_constant=1/(4*math.sqrt(2)*float(c))+math.sqrt(2)/128+1/16
assert root_constant<1/3
assert Fraction(65536,55296)==Fraction(32,27)
assert Fraction(2,9)+Fraction(1,8)+Fraction(1,4)<1
out={'status':'PASS','scope':'Deterministic source-disabled matrix, Born-law, and exact rational-control fixtures; no sampled source calls, no RNG, no production learner execution.','q_values':[1,2],'n_values':[2,3],'unitary_angles':[.015,.055,.105],'noise_mix_values':[1,1/3,1/100,1/10000],'actual_tau_range':[min(taus),max(taus)],'supplied_kappa_range':[min(kappas),max(kappas)],'minimum_coarse_gap_divided_by_lambda':min(margins),'tests':tests,'max_positive_numerical_violation':max(0.,max(violations.values())),'max_violation_by_kind':violations,'born_events_enumerated':born_events,'rational_normalization_cases':rational,'root_statistical_finite_fit_constant':root_constant,'constant_target':1/3,'files':{}}
for name in ['approximate_onsite_acquisition_independent_20261028.md',Path(__file__).name]:out['files'][name]=hashlib.sha256(Path(name).read_bytes()).hexdigest()
Path('approximate_onsite_acquisition_independent_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','actual_tau_range','supplied_kappa_range','born_events_enumerated','max_positive_numerical_violation','root_statistical_finite_fit_constant']},indent=2))
