from pathlib import Path
from fractions import Fraction as F
import json,itertools,math,hashlib
import numpy as np
import sympy as s
from run_demo import PA,rotation,sqrt_upper,rat
ROOT=Path(__file__).parent
train=json.loads((ROOT/'main_8192_certificate.json').read_text());test=json.loads((ROOT/'larger_65536_certificate.json').read_text());design=json.loads((ROOT/'PREDECLARED_DESIGN.json').read_text())
site=train['accepted_site'];assert site is not None
q=train['site_witnesses'][site]['candidate_quaternion_integers'];R=rotation(q);B=[sum((R[k,j]*PA[k] for k in range(3)),s.zeros(2)) for j in range(3)]
M=s.Matrix([[s.Rational(x) for x in row] for row in test['site_witnesses'][site]['M_coefficients']]);C=[sum((M[k,j]*PA[k]/2 for k in range(3)),s.zeros(2)) for j in range(3)]
P=(s.eye(4)+sum((s.kronecker_product(PA[j].T,B[j]) for j in range(3)),s.zeros(4)))/4;T=s.eye(4)-P;assert (P*P-P).applyfunc(s.simplify)==s.zeros(4) and (P.H-P).applyfunc(s.simplify)==s.zeros(4)
Y=sum(((C[j]*B[j]+B[j]*C[j])/2 for j in range(3)),s.zeros(2));H=sum((s.kronecker_product(PA[j].T,C[j]) for j in range(3)),s.zeros(4));Q=s.kronecker_product(s.eye(2),Y)-H
assert (P*Q*P).applyfunc(s.simplify)==s.zeros(4)
Z=T*Q*P;W=T*Q*T;z2=s.simplify(s.trace(Z.H*Z));assert z2>=0
# P is rank1, so Z has rank<=1 and squared op norm is exactly Tr Z^dagger Z.
D=design['rational_rounding_denominator'];zup=rat(sqrt_upper(F(int(s.numer(z2)),int(s.denom(z2))),D))
vals=np.linalg.eigvalsh(np.array(W).astype(complex));khat=s.Rational(math.floor(vals[1]*D)-2,D)
slack=W-khat*T;minors=[]
for k in range(1,5):
 for inds in itertools.combinations(range(4),k):minors.append(s.simplify(slack.extract(inds,inds).det()))
assert khat>0 and all(x.is_real and x>=0 for x in minors)
eta=s.Rational(test['coefficient_radius_upper_exact']);sqrt3=rat(sqrt_upper(F(3),D));a=sqrt3*eta/2
kcert=khat-6*a;zcert=zup+6*a;assert kcert>0
regret=s.simplify(zcert*zcert/(2*kcert))
# Sharper scalar-shift root, outward rational; either bound is valid.
lam=rat(sqrt_upper(F(int(s.numer(kcert*kcert+4*zcert*zcert)),int(s.denom(kcert*kcert+4*zcert*zcert))),D))/2-kcert/2
regret_sharp=lam/2
out={'status':'AUTHOR_DERIVED_EXACT_HOLDOUT_SCHUR_CERTIFICATE_PENDING_AUDIT','training_bank':'main_8192','holdout_bank':'larger_65536','candidate_physical_site':site,'candidate_quaternion_from_training':q,'training_data_calls':8192,'holdout_calls':65536,'candidate_source_parameters_used':False,'empirical_PQsymP_exact_zero':True,'empirical_transverse_lower_bound_exact':str(khat),'all_15_transverse_PSD_principal_minors_exact':list(map(str,minors)),'empirical_Z_squared_norm_exact':str(z2),'empirical_Z_norm_upper_exact':str(zup),'holdout_coefficient_radius_exact':str(eta),'qubit_operator_error_radius_exact':str(a),'certified_true_transverse_gap_exact':str(kcert),'certified_true_stationarity_norm_upper_exact':str(zcert),'local_full_CPTP_oracle_regret_upper_exact':str(regret),'local_full_CPTP_oracle_regret_upper':float(regret),'sharper_local_regret_upper_exact':str(regret_sharp),'sharper_local_regret_upper':float(regret_sharp),'global_scope':'Global oracle comparison additionally uses accepted localization and same stationary source; allocate training beta .01 plus holdout beta .01. Local Schur regret alone needs only holdout event. No true source score/rotation enters certificate.','scope':'Derived after initial demo, not a separately predeclared experimental endpoint. Training quaternion is a function only of the earlier independent bank. Uses predeclared complete simultaneous holdout coefficient event, no fitted-residual confidence interval.'}
(ROOT/'HOLDOUT_SCHUR_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if 'exact' not in k and 'minors' not in k},indent=2))
