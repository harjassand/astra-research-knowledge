"""Independent raw replay and exact physical/score/confidence audit. Does not alter package."""
from pathlib import Path
import json,hashlib,itertools,math
from fractions import Fraction as F
import numpy as np
import sympy as s
Q=Path(__file__).parent;root=Q/'normal_cone_localization_sampled_demo_20261028';design=json.loads((root/'PREDECLARED_DESIGN.json').read_text());cfg=json.loads((root/'SOURCE_ONLY.json').read_text());manifest=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
for name,h in manifest['files'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h
for name,h in manifest['governing_dependencies'].items():assert hashlib.sha256((Q/name).read_bytes()).hexdigest()==h
I=s.eye(2);P=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];k=s.kronecker_product
def rotation(q):
 a,x,y,z=map(s.Integer,q);D=a*a+x*x+y*y+z*z
 return s.Matrix([[a*a+x*x-y*y-z*z,2*(x*y-a*z),2*(x*z+a*y)],[2*(x*y+a*z),a*a-x*x+y*y-z*z,2*(y*z-a*x)],[2*(x*z-a*y),2*(y*z+a*x),a*a-x*x-y*y+z*z]])/D
RL=rotation(cfg['logical_rotation_quaternion']);RG=rotation(cfg['gauge_rotation_quaternion']);la=s.Rational(cfg['lambda']);ep=s.Rational(cfg['epsilon'])
assert RL.T*RL==s.eye(3) and RL.det()==1 and RG.T*RG==s.eye(3) and RG.det()==1
# Build actual rotated+swapped contrast states, not the author's probability shortcut.
C=[]
for j in range(3):
 logical=sum((RL[a,j]*P[a] for a in range(3)),s.zeros(2));gauge=sum((RG[a,2]*P[a] for a in range(3)),s.zeros(2))
 C.append(la*k(I,logical)/4+(ep*k(gauge,I)/4 if j==2 else s.zeros(4)))
# Spectrum checked in unrotated basis; exact unitary conjugation preserves it.
def Uquat(q):
 a,x,y,z=map(s.Integer,q)
 return (a*I-s.I*(x*P[0]+y*P[1]+z*P[2]))/s.sqrt(a*a+x*x+y*y+z*z)
UL=Uquat(cfg['logical_rotation_quaternion']);UG=Uquat(cfg['gauge_rotation_quaternion']);V=k(UG,UL)
C0=[la*k(I,p)/4+(ep*k(P[2],I)/4 if j==2 else s.zeros(4)) for j,p in enumerate(P)]
for j in range(3):assert (V*C0[j]*V.H-C[j]).applyfunc(s.simplify)==s.zeros(4)
JN0=(k(I,s.eye(4)/4)+sum((k(p.T,c) for p,c in zip(P,C0)),s.zeros(8)))/2
assert all(x>=s.Rational(1,80) for x in JN0.eigenvals())
B0=[k(I,p) for p in P];PB0=(s.eye(8)+sum((k(p.T,b) for p,b in zip(P,B0)),s.zeros(8)))/4
Y0=sum((c*b for c,b in zip(C0,B0)),s.zeros(4));slack0=k(I,Y0)-sum((k(p.T,c) for p,c in zip(P,C0)),s.zeros(8))
assert slack0*PB0==s.zeros(8) and all(x>=0 for x in (slack0-s.Rational(3,4)*(s.eye(8)-PB0)).eigenvals())
# Exact 216 joint probabilities from Born traces.
cdf=np.zeros((3,2,3,3,4),dtype=np.int64);den=1800;probs=0
for j,si,a,b in itertools.product(range(3),range(2),range(3),range(3)):
 rho=s.eye(4)/4+(2*si-1)*C[j];total=0
 for o,(u,v) in enumerate(itertools.product([-1,1],repeat=2)):
  p=s.simplify(s.trace(k((I+u*P[a])/2,(I+v*P[b])/2)*rho));assert p>0 and (den*p).is_Integer
  total+=int(den*p);cdf[j,si,a,b,o]=total;probs+=1
 assert total==den
# Mathematical log bound, independent outward square-root arithmetic.
assert sum(F(9)**i/F(math.factorial(i)) for i in range(21))>3600
reports=[]
for bank in design['banks']:
 name=bank['name'];N=bank['calls'];z=np.load(root/(name+'_records.npz'));records=z['records'];assert records.shape==(N,6)
 rng=np.random.default_rng(bank['seed']);j=rng.integers(0,3,N);si=rng.integers(0,2,N);a=rng.integers(0,3,N);b=rng.integers(0,3,N);coin=rng.integers(0,den,N)
 out=np.array([np.searchsorted(cdf[j[t],si[t],a[t],b[t]],coin[t],side='right') for t in range(N)])
 replay=np.stack([j,2*si-1,a,b,2*(out//2)-1,2*(out%2)-1],axis=1).astype(np.int8);assert np.array_equal(records,replay)
 cert=json.loads((root/(name+'_certificate.json')).read_text());assert hashlib.sha256(records.tobytes()).hexdigest()==cert['records_sha256']
 eta=F(cert['coefficient_radius_upper_exact']);h=F(cert['score_halfwidth_upper_exact']);linear=F(60,N);sqr=eta-linear;assert sqr>=0 and sqr*sqr>=F(162,N)
 root3=h/(F(3,4)*eta);assert root3*root3>=3
 intervals=[];minorcount=0;confidence_actual=True
 for site in range(2):
  witness=cert['site_witnesses'][site];counts=np.zeros((3,3),dtype=np.int64)
  for aa,jj in itertools.product(range(3),repeat=2):
   use=(records[:,2+site]==aa)&(records[:,0]==jj);counts[aa,jj]=np.sum(records[use,1].astype(np.int64)*records[use,4+site])
  assert np.array_equal(counts,z['integer_signed_counts'][site]) and counts.tolist()==witness['integer_signed_counts']
  M=s.Matrix(3,3,lambda a,j:s.Rational(9*int(counts[a,j]),N));assert [[str(v) for v in row] for row in M.tolist()]==witness['M_coefficients']
  R=rotation(witness['candidate_quaternion_integers']);assert R.T*R==s.eye(3) and R.det()==1
  A=[sum((R[a,j]*P[a] for a in range(3)),s.zeros(2)) for j in range(3)]
  KA=(s.eye(4)+sum((k(p.T,aa) for p,aa in zip(P,A)),s.zeros(4)))/2;assert (KA*KA-2*KA).applyfunc(s.simplify)==s.zeros(4) and s.trace(KA)==2
  H=sum((M[a,j]*k(P[j].T,P[a])/2 for a,j in itertools.product(range(3),repeat=2)),s.zeros(4))
  primal=s.simplify(s.trace(H*KA));assert primal==s.Rational(witness['primal_objective_exact'])
  y=s.Rational(witness['dual_scalar_y_exact']);dual=2*y;W=y*s.eye(4)-H;minors=[]
  for size in range(1,5):
   for inds in itertools.combinations(range(4),size):
    val=s.simplify(W.extract(inds,inds).det());assert val.is_real and val>=0;minors.append(str(val));minorcount+=1
  assert minors==witness['all_15_dual_principal_minors_exact'] and dual==s.Rational(witness['dual_objective_exact'])
  hh=s.Rational(h.numerator,h.denominator);lo=max(0,(1+primal)/4-hh);hi=min(1,(1+dual)/4+hh)
  assert lo==s.Rational(witness['fidelity_lower_exact']) and hi==s.Rational(witness['fidelity_upper_exact']);intervals.append((lo,hi))
  trueM=la*RL if site==1 else s.Matrix(3,3,lambda a,j:ep*RG[a,2] if j==2 else 0)
  confidence_actual&=all(abs(M[a,j]-trueM[a,j])<=s.Rational(eta.numerator,eta.denominator) for a,j in itertools.product(range(3),repeat=2))
 accepted=[i for i in range(2) if intervals[i][0]>intervals[1-i][1]];decision=accepted[0] if accepted else None
 assert decision==cert['accepted_site'] and confidence_actual
 reports.append({'name':name,'records_replayed':N,'accepted_site':decision,'exact_dual_minors':minorcount,'true_coefficient_confidence_event_validated_posthoc':bool(confidence_actual),'records_sha256':cert['records_sha256']})
add=json.loads((root/'NONZERO_REJECTED_SITE_CONTRAST.json').read_text());large=json.loads((root/'larger_65536_certificate.json').read_text());observed=s.Rational(large['site_witnesses'][0]['M_coefficients'][0][2]);radius=s.Rational(large['coefficient_radius_upper_exact']);lower=observed-radius
assert observed==s.Rational(add['observed_signed_coefficient_exact']) and radius==s.Rational(add['simultaneous_radius_exact']) and lower==s.Rational(add['strict_positive_lower_bound_exact']) and lower>0
out={'status':'PASS_INDEPENDENT_EXECUTED_SIMULATION_AND_EXACT_CERTIFICATES','exact_joint_Born_probabilities':probs,'total_records':sum(b['calls'] for b in design['banks']),'rejected_site_nonzero_contrast_lower_exact':str(lower),'banks':reports,'scope':'Reproducible stationary pseudorandom source simulation with exact primal/dual/confidence guards; not laboratory independence, external pre-registration, physical controls or future-memory validation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
