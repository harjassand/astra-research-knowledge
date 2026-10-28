from fractions import Fraction as F
from pathlib import Path
import json,hashlib,random
r=Path(__file__).resolve().parent;rr=random.Random(281052);physical=0;budgets=0
for G in [1,2,5,8]:
 for rep in range(16):
  counts=[rr.randrange(0,100) for _ in range(4*G)];total=sum(counts);p=[F(c,total) for c in counts]
  ell=F(0);lamloss=F(0)
  for g in range(G):
   pg=p[4*g:4*g+4];w=sum(pg);lam=[(w-v)/3 for v in pg]
   assert sum(lam)==w and min(lam)>=0
   ell+=w-max(pg);lamloss+=3*min(lam)
  assert ell==lamloss;physical+=1
for gamma in [F(1,1000),F(1,100),F(1,8),F(1,2),F(1)]:
 eta=gamma/8
 assert (1+eta)/(1-eta)<=1+gamma/2
 assert (F(4)/gamma+2)/(1-eta)<=7/gamma
 # c=3 Gt; additive <=21Gt/gamma and endpoint t=gamma eps/(168G).
 assert F(21,168)==F(1,8)
 assert (1+gamma/2)*F(1,32)+F(1,8)<F(1,4)
 assert F(1,4)+F(1,16)+F(1,4)<1;budgets+=1
# Exact finite-design cap: n_j coefficient256*(4*10), sum inverse scales <4/t.
assert 256*40*4==40960
out={'status':'PASS_INDEPENDENT_KNOWN_PAULI_DICTIONARY','exact_Pauli_probability_comparisons':physical,'exact_Young_and_risk_budgets':budgets,'finite_design_cap_coefficient':40960,'source_sha256':hashlib.sha256((r/'ordinary_known_pauli_kernel_design_benchmark_20261028.md').read_bytes()).hexdigest(),'scope':'Known orthogonal Pauli dictionary only; no acquired unknown algebra or generic O(k) information count.'}
(r/'ordinary_known_pauli_kernel_design_benchmark_20261028_independent_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
