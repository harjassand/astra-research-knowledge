from pathlib import Path
from fractions import Fraction as F
import json,math
P=Path(__file__).resolve().parents[1]
data=json.loads((P/'integrated_budget_v1.json').read_text())
def tail(m,t,p):
 if not m:return F(0)
 N=m+t;a=p.numerator;d=p.denominator;b=d-a
 term=b**N;num=term
 for j in range(m-1):
  top=term*(N-j)*a;bottom=(j+1)*b
  assert top%bottom==0;term=top//bottom;num+=term
 return F(num,d**N)
def ceil_log2_ratio(x):
 c=0
 while x*(1<<c)<1:c+=1
 return c
rows=[]
for row in data['fixed_rate_cases']+[data['paid_remote_case']]:
 B=row['B'];h=(B-1).bit_length();k=row['k0'];n=row['n'];u=max(1,(h+k-1)//k);s=u*k//h;t=row['t'];J=u*B;K=s*h*(B-4*t);q=F(row['service_probability']);p=1-q;m=2*(n-k)
 assert (h,u,s,J,K,m)==(row['h'],row['u'],row['stripes'],row['J'],row['K'],row['m'])
 assert 4*t<B and 2*s*h>=u*k and row['padding_per_group']==u*k-s*h
 eps=F(row['epsilon_fault']);exact=tail(m,t,p);assert exact<=eps
 assert abs(float(exact)-row['exact_fault_tail'])<1e-15
 if 'max_source_calls' in row:
  delta=F(row['cap_error_bound']);L=row['max_source_calls'];c=ceil_log2_ratio(delta)
  assert L*q>=max(2*J,8*c)
  rate=q*K/(n*J);assert rate>=F(k,8*n)
  assert F(K,n*L)<=rate
  rows.append({'n':n,'k0':k,'kind':'direct','exact_expected_rate':str(rate),'exact_cap_rate':str(F(K,n*L))})
 else:
  delta=F(row['seed_abort_bound']);Pcap=row['probe_cap'];c=ceil_log2_ratio(delta)
  assert 0<p<=F(1,4) and Pcap>=max(4*p*J,6*c)
  assert p*(J+Pcap)<=F(Pcap,2)
  assert row['trusted_seed_ebits']==n*Pcap and row['conservative_net_ebits']==K-n*Pcap
  assert row['source_call_cap']==J+Pcap
  if t:assert tail(m,t-1,p)>eps
  rows.append({'n':n,'k0':k,'kind':'paid_remote_resource','NB_quantile_minimal':True,'exact_capped_net_rate':str(F(K-n*Pcap,n*(J+Pcap)))})
result={'status':'PASS_EXACT_INTEGER_AND_RATIONAL_BUDGET_CHECKS','cases':rows,'scope':'No large circuit materialized; asymptotic remote rate governed by separate qualification.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
