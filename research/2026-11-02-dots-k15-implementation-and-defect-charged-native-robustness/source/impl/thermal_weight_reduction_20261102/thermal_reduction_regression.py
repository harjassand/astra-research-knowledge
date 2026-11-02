#!/usr/bin/env python3
"""Finite F2 contractions and complete thermal syndrome enumeration. Not a full HLL implementation."""
import itertools,json,math
from pathlib import Path
import numpy as np
OUT=Path(__file__).parent
rng=np.random.default_rng(271828)
def mm(a,b):return (a@b)%2
def eq(a,b):return bool(np.array_equal(a%2,b%2))
def span_basis_columns(a):
 out={tuple([0]*a.shape[0])}
 for col in a.T:
  out|={tuple((np.array(v,dtype=int)+col)%2) for v in list(out)}
 return sorted(out)
def inv(a):
 n=len(a);x=np.concatenate((a.copy()%2,np.eye(n,dtype=int)),axis=1)
 for k in range(n):
  p=next(i for i in range(k,n) if x[i,k]);x[[k,p]]=x[[p,k]]
  for i in range(n):
   if i!=k and x[i,k]:x[i]^=x[k]
 return x[:,n:]
def blockdegree(M,inds1,inds2):return M[np.ix_(inds1,inds2)]
# A source with one logical qubit and a redundant Z-check row.
d2=np.array([[1],[1],[0],[0]],dtype=int)
d1=np.array([[1,1,0,0],[0,0,1,1],[1,1,1,1]],dtype=int)
base_degrees=[2]+[1]*4+[0]*3
# Each local block: one homology coordinate plus one contractible pair in each adjacent degree.
coords=[]
for b,deg in enumerate(base_degrees):
 coords += [(b,'h',deg),(b,'b0',0),(b,'t1',1),(b,'b1',1),(b,'t2',2)]
N=len(coords);inds={k:[i for i,c in enumerate(coords) if c[2]==k] for k in range(3)}
baseids=[5*b for b in range(len(base_degrees))]
d0=np.zeros((N,N),dtype=int);h=np.zeros((N,N),dtype=int)
for b in range(len(base_degrees)):
 d0[5*b+1,5*b+2]=1;h[5*b+2,5*b+1]=1
 d0[5*b+3,5*b+4]=1;h[5*b+4,5*b+3]=1
p=np.zeros((len(baseids),N),dtype=int)
for b,j in enumerate(baseids):p[b,j]=1
i=p.T.copy();ds=np.zeros((len(baseids),len(baseids)),dtype=int)
ds[1:5,0:1]=d2;ds[5:8,1:5]=d1
Dc=(d0+mm(mm(i,ds),p))%2
checks=[];decoder_cases=0;thermal_cases=0
for trial in range(5):
 T=np.eye(N,dtype=int)
 # Degree-preserving triangular transformations, ensuring all cross-block arrows lower stratum.
 for r,cr in enumerate(coords):
  for c,cc in enumerate(coords):
   if cr[2]==cc[2] and base_degrees[cr[0]]<base_degrees[cc[0]] and rng.random()<.10:
    T[r,c]=1
 D=mm(mm(T,Dc),inv(T));delta=(D+d0)%2
 hd=mm(h,delta);dh=mm(delta,h)
 I=mm((np.eye(N,dtype=int)+hd+mm(hd,hd))%2,i)
 P=mm(p,(np.eye(N,dtype=int)+dh+mm(dh,dh))%2)
 H=mm((np.eye(N,dtype=int)+hd+mm(hd,hd))%2,h)
 deff=(mm(mm(p,delta),i)+mm(mm(mm(mm(p,delta),h),delta),i))%2
 tests={'nilpotent_D':not D.any() if False else eq(mm(D,D),np.zeros((N,N),dtype=int)),
        'hdelta_cubed_zero':not mm(mm(hd,hd),hd).any(),
        'effective_source':eq(deff,ds),
        'PI':eq(mm(P,I),np.eye(len(baseids),dtype=int)),
        'PD_dP':eq(mm(P,D),mm(ds,P)),
        'DI_Id':eq(mm(D,I),mm(I,ds)),
        'homotopy':eq((mm(D,H)+mm(H,D))%2,(np.eye(N,dtype=int)+mm(I,P))%2),
        'PH_HI_HH':not mm(P,H).any() and not mm(H,I).any() and not mm(H,H).any()}
 assert all(tests.values()),tests
 D1=blockdegree(D,inds[0],inds[1]);D2=blockdegree(D,inds[1],inds[2])
 P0=P[np.ix_(list(range(5,8)),inds[0])];P1=P[np.ix_(list(range(1,5)),inds[1])]
 I0=I[np.ix_(inds[0],list(range(5,8)))];I1=I[np.ix_(inds[1],list(range(1,5)))]
 H0=H[np.ix_(inds[1],inds[0])]
 S=set(span_basis_columns(d1));Sf=set(span_basis_columns(D1))
 pre=set(v for v in itertools.product(range(2),repeat=D1.shape[0]) if tuple(mm(P0,np.array(v,dtype=int))) in S)
 assert pre==Sf
 R={}
 for v in itertools.product(range(2),repeat=4):
  v=np.array(v,dtype=int);s=tuple(mm(d1,v))
  if s not in R or v.sum()<R[s].sum():R[s]=v
 for sv in Sf:
  sf=np.array(sv,dtype=int);s=tuple(mm(P0,sf));rf=(mm(I1,R[s])+mm(H0,sf))%2
  assert eq(mm(D1,rf),sf);assert eq(mm(P1,rf),R[s]);decoder_cases+=1
 # Full finite-temperature marginals over every fine syndrome.
 Bs=rng.uniform(.3,3.1,size=D1.shape[0]);weights={sv:math.exp(-float(Bs@np.array(sv))) for sv in Sf};z=sum(weights.values())
 coarse={s:0. for s in S};fine_pred={s:0. for s in S}
 for sv,w in weights.items():coarse[tuple(mm(P0,np.array(sv)))]+=w/z
 # Independent-bit distribution conditioned on coarse validity, with all vectors retained.
 norm=np.prod(1+np.exp(-Bs));condz=0.
 for sv in itertools.product(range(2),repeat=D1.shape[0]):
  s=tuple(mm(P0,np.array(sv)))
  if s in S:
   w=math.exp(-float(Bs@np.array(sv)))/norm;fine_pred[s]+=w;condz+=w
 err=max(abs(coarse[s]-fine_pred[s]/condz) for s in S);assert err<1e-12;thermal_cases+=1
 # Opposite projection I2.T and dual chain identity.
 pdual=I.T;idual=P.T;hdual=H.T;Ddual=D.T;ddual=ds.T
 assert eq(mm(pdual,Ddual),mm(ddual,pdual));assert eq((mm(Ddual,hdual)+mm(hdual,Ddual))%2,(np.eye(N,dtype=int)+mm(idual,pdual))%2)
 checks.append({'trial':trial,'fine_dimensions':{str(k):len(v) for k,v in inds.items()},'allowed_fine_syndromes':len(Sf),'allowed_source_syndromes':len(S),'identities':tests,'thermal_marginal_max_error':err})
# Exact disjoint parity fibers with dependent coarse syndromes.
paritytests=[]
for r in [1,2,3,4,8,180]:
 for B_old in [.2,1.,3.,8.,20.]:
  Bnew=B_old+math.log(r);q=math.exp(-Bnew);qeff=math.tanh(r*math.atanh(q));Beff=-math.log(qeff)
  assert Beff+1e-11>=B_old
  paritytests.append({'r':r,'B_old':B_old,'B_new':Bnew,'B_eff':Beff})
# Explicit overlapping columns make old bits correlated, even with no source relations.
Pex=np.array([[1,0,1],[0,1,1]],dtype=int);B=2.;probs={s:0. for s in itertools.product(range(2),repeat=2)}
for v in itertools.product(range(2),repeat=3):
 probs[tuple(mm(Pex,np.array(v)))]+=math.exp(-B*sum(v))/(1+math.exp(-B))**3
p0=sum(v for s,v in probs.items() if s[0]);p1=sum(v for s,v in probs.items() if s[1]);cov=probs[(1,1)]-p0*p1
assert cov>0
# Duplicated generator Gibbs ratio vs bounded local-fiber translation.
no_go=[]
for r in [7,30,180]:
 for df in [2,6]:
  no_go.append({'duplicate_count':r,'fine_degree':df,'required_Jnew_over_Jold':r/df})
out={'status':'PASS','scope':'Generic bounded local cone contraction and thermal identities; not a compiled HLL/sheaf gadget','contractions':checks,'decoder_syndrome_cases':decoder_cases,'complete_thermal_cases':thermal_cases,'logarithmic_fiber_tests':paritytests,'overlap_counterexample':{'P':Pex.tolist(),'B':B,'probabilities':{str(k):v for k,v in probs.items()},'covariance':cov},'duplicate_energy_obstruction':no_go}
(OUT/'thermal_reduction_regression.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'status':out['status'],'decoder_syndrome_cases':decoder_cases,'complete_thermal_cases':thermal_cases,'parity_cases':len(paritytests),'overlap_covariance':cov},indent=2))
