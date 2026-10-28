"""Supplementary exact-budget/QR checks for the independent full-module receipt."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math
root=Path(__file__).resolve().parent
expected='483a8507c4ca0dfef510c888a2fc755e84b653bcee81a0329830d152b9ed3968'
source=root/'ordinary_adaptive_pure_matrix_query_20261028.md'
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
old=json.loads((root/'ordinary_adaptive_pure_known_center_independent_audit_20261028_check.json').read_text())
assert old['status']=='PASS_KNOWN_CENTER_ONLY'
qr_cases=0;max_ratio=F(0);max_bits=0
for d in [1,2,3,4,8,16,32]:
 for m in [2,7,32]:
  for p in [4,10,20]:
   theta=F(1,10**p);D=d+1;l=max(m,p);M=10*l*D
   B=math.ceil(math.sqrt(d*math.log(float(100*m*d*d/theta))))+1
   a=theta/(100*m*d) # conservative rational choice, below sqrt(required cap)
   assert a*a<=theta/(100*m*d)
   kap=min(theta/(100*m),theta/(100*M),a/(100*d*B))
   L=1+4*B/a
   delta=kap*a/(100*d*d*L**d) # stronger than displayed d^(3/2) cap
   total=F(0);max_resid=F(0)
   for _ in range(d):
    resid=d*delta+2*B*total # d is conservative upper bound for sqrt(d)
    max_resid=max(max_resid,resid)
    total+=2*resid/a
   assert total<=kap/10 and max_resid<=a/2
   max_ratio=max(max_ratio,total/kap)
   max_bits=max(max_bits,delta.denominator.bit_length())
   qr_cases+=1
budget_cases=0;max_mean=F(0);max_mse=F(0)
for D in [2,3,8,32,128]:
 for m in [2,3,10,100]:
  for zeta in [F(1,m*m),F(1,100*m*m),F(1,10**12*m*m)]:
   l=m
   while F(1,4**l)>zeta/4:l+=1
   M=10*l*D;beta=zeta/(1000*l*l*D*D*m*m)
   theta=zeta/(10**6*l*l*D*D*m*m)
   bias=F(1,4**(l+2))
   ideal_mean=bias+(M+1)*beta
   ideal_extra_mse=bias*bias+(M+1)**2*beta
   # Conservative transfer envelope after coupling and other-channel subbudgets.
   mean=ideal_mean+10*M*theta
   extra=ideal_extra_mse+30*M*M*theta
   assert ideal_mean<=zeta/4 and mean<=zeta
   assert 80+extra*m*m<100
   max_mean=max(max_mean,mean/zeta);max_mse=max(max_mse,extra*m*m)
   budget_cases+=1
receipt=root/'ordinary_adaptive_pure_matrix_query_20261028_independent_receipt.md'
result={'status':'RECEIVED_SCOPED_LOCAL_MATRIX_QUERY','source_sha256':expected,'receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),'known_center_independent_check':old,'exact_rational_QR_recurrence_cases':qr_cases,'maximum_sum_column_error_over_kappa':float(max_ratio),'largest_checked_delta_denominator_bits':max_bits,'exact_all_history_budget_cases':budget_cases,'maximum_total_bias_over_zeta':float(max_mean),'maximum_additional_MSE_coefficient':float(max_mse),'rank_at_most_extension':'Analytic continuity proof in receipt; no source support supplied.','primary_source':'https://arxiv.org/html/2511.15806v1','scope':'No full hardware execution, all-decoder confidence, Loewner envelope, or global encoder sharing.'}
(root/'ordinary_adaptive_pure_matrix_query_20261028_independent_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
