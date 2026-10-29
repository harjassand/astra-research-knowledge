"""Independent exact holdout Schur endpoint verification. Reads frozen data only."""
from pathlib import Path
import sympy as s,json,itertools
q=Path(__file__).parent;root=q/'normal_cone_localization_sampled_demo_20261028'
train=json.loads((root/'main_8192_certificate.json').read_text());test=json.loads((root/'larger_65536_certificate.json').read_text());cert=json.loads((root/'HOLDOUT_SCHUR_CERTIFICATE.json').read_text())
site=train['accepted_site'];quat=train['site_witnesses'][site]['candidate_quaternion_integers'];assert cert['candidate_quaternion_from_training']==quat and cert['candidate_physical_site']==site
I=s.eye(2);pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];k=s.kronecker_product
a,x,y,z=map(s.Integer,quat);D=a*a+x*x+y*y+z*z
R=s.Matrix([[a*a+x*x-y*y-z*z,2*(x*y-a*z),2*(x*z+a*y)],[2*(x*y+a*z),a*a-x*x+y*y-z*z,2*(y*z-a*x)],[2*(x*z-a*y),2*(y*z+a*x),a*a-x*x-y*y+z*z]])/D
assert R.T*R==s.eye(3) and R.det()==1
B=[sum((R[a,j]*pa[a] for a in range(3)),s.zeros(2)) for j in range(3)];M=s.Matrix([[s.Rational(v) for v in row] for row in test['site_witnesses'][site]['M_coefficients']]);C=[sum((M[a,j]*pa[a]/2 for a in range(3)),s.zeros(2)) for j in range(3)]
P=(s.eye(4)+sum((k(p.T,b) for p,b in zip(pa,B)),s.zeros(4)))/4;T=s.eye(4)-P
assert (P*P-P).applyfunc(s.simplify)==s.zeros(4) and s.trace(P)==1
Y=sum(((c*b+b*c)/2 for c,b in zip(C,B)),s.zeros(2));Q=k(I,Y)-sum((k(p.T,c) for p,c in zip(pa,C)),s.zeros(4));Z=T*Q*P;W=T*Q*T
assert (P*Q*P).applyfunc(s.simplify)==s.zeros(4)
z2=s.simplify(s.trace(Z.H*Z));assert z2==s.Rational(cert['empirical_Z_squared_norm_exact'])
zup=s.Rational(cert['empirical_Z_norm_upper_exact']);assert zup>=0 and zup*zup>=z2
kh=s.Rational(cert['empirical_transverse_lower_bound_exact']);slack=W-kh*T;minors=[]
for size in range(1,5):
 for inds in itertools.combinations(range(4),size):
  d=s.simplify(slack.extract(inds,inds).det());assert d>=0;minors.append(str(d))
assert minors==cert['all_15_transverse_PSD_principal_minors_exact']
eta=s.Rational(test['coefficient_radius_upper_exact']);a=s.Rational(cert['qubit_operator_error_radius_exact']);assert a>0 and a*a>=3*eta*eta/4
kap=kh-6*a;zz=zup+6*a;assert kap>0 and kap==s.Rational(cert['certified_true_transverse_gap_exact']) and zz==s.Rational(cert['certified_true_stationarity_norm_upper_exact'])
quad=zz*zz/(2*kap);sharp=s.Rational(cert['sharper_local_regret_upper_exact']);lam=2*sharp
assert quad==s.Rational(cert['local_full_CPTP_oracle_regret_upper_exact']) and lam>=0 and lam*(kap+lam)>=zz*zz and sharp<=quad
out={'status':'PASS_EXACT_INDEPENDENT_HOLDOUT_SCHUR_ENDPOINT','exact_P_rank':1,'transverse_PSD_minors':15,'candidate_bank':'main_8192','holdout_bank':'larger_65536','physical_site':site,'regret_upper_exact':str(sharp),'regret_upper':float(sharp),'quadratic_upper':float(quad),'scope':'Derived same-channel native-regret certificate from previously audited simulated data, not a newly executed payload or hardware experiment.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
