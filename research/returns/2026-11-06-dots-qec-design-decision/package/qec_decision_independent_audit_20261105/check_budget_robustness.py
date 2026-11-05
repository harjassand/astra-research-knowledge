from pathlib import Path
from fractions import Fraction as F
from math import comb,ceil
import importlib.util,json,math,time
from scipy.stats import beta
P=Path(__file__).resolve().parent;R=P.parent
s=importlib.util.spec_from_file_location('cs',(R/'qec_design_direct_20261105/sequential_decision.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rows=[]
for den in [6000,9000,12000]:
 m.ALPHA=F(1,den)
 for d in [19,23]:
  r=json.loads((R/f'qec_design_direct_20261105/d{d}_decision.json').read_text());a,b=m.confidence_sequence(r['shots'],r['counts']['accepted']);z=F(r['normalizer_exact']);tv=F(r['conversion_TV_upper_exact']);L=max(F(0),z*a-tv);U=min(F(1),z*b+tv)
  # Independently check both endpoint inequalities with fractions.
  n=r['shots'];k=r['counts']['accepted'];fac=F(n+1)*comb(n,k)
  assert fac*a**k*(1-a)**(n-k)<=m.ALPHA
  assert fac*b**k*(1-b)**(n-k)<=m.ALPHA
  rows.append({'distance':d,'alpha_exact':str(m.ALPHA),'shots':n,'accepts':k,'acceptance_interval_exact':[str(a),str(b)],'failure_interval_exact':[str(L),str(U)],'failure_interval_decimal':[float(L),float(U)],'decision':'pass' if U<=F(1,10**12) else 'reject' if L>F(1,10**12) else 'inconclusive'})
r=json.loads((R/'qec_fault_tuple_20261105/production_d21_10000.json').read_text());meta=json.loads((R/'qec_fault_tuple_20261105/d21/parameters.json').read_text());z=F(r['normalizer_exact']);tv=F(meta['conversion_TV_upper_exact']);n=10000;k=55;D=1<<24;big=D**n
for den in [6000,12000]:
 a=F(int(beta.ppf(1/(2*den),k,n-k+1)*D),D);b=F(ceil(beta.ppf(1-1/(2*den),k+1,n-k)*D),D)
 def cdf(j,l):
  t=comb(n,l)*j**l*(D-j)**(n-l);s=t
  for ell in range(l,0,-1):t,rem=divmod(t*ell*(D-j),(n-ell+1)*j);assert rem==0;s+=t
  return s
 assert (big-cdf(int(a*D),k-1))*2*den<=big
 assert cdf(int(b*D),k)*2*den<=big
 L=z*a-tv;U=z*b+tv
 assert L>F(1,10**12)
 rows.append({'distance':21,'alpha_exact':f'1/{den}','shots':n,'accepts':k,'acceptance_interval_exact':[str(a),str(b)],'failure_interval_exact':[str(L),str(U)],'failure_interval_decimal':[float(L),float(U)],'decision':'reject'})
out={'purpose':'Budget-sensitivity reanalysis of unchanged, preserved runs. These are not fresh samples and do not by themselves prescribe the globally appropriate multiplicity family.','rows':rows}
(P/'budget_robustness.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
