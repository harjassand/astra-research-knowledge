from fractions import Fraction as F
from pathlib import Path
import itertools,json,hashlib,math
Q=Path(__file__).parent;tau=F(1,80)
constants=0;caps=0;power=0
for gamma,eps,M in itertools.product([F(1),F(1,2),F(1,10),F(1,100)],[F(1),F(1,2),F(1,10),F(1,1000)],[1,2,10,100]):
 alpha=gamma/2;e=eps/(8*M);a=tau*(gamma+e)/64
 assert a<=9*tau/512 and a<tau/4
 assert tau+a<2*tau==F(1,40)
 lowopt=tau-2*a
 assert lowopt>=tau/2
 assert a<=gamma*lowopt/32+e/64<=alpha*lowopt+e
 # Exact accepted pilot constants: epsilon0=4a, delta=a/256.
 assert 168*a/256+(4*a)/32<a
 assert F(2)>=F(9,8)
 assert 1/(gamma+e)**2<=2*M/(gamma*eps)
 assert 2*M*e+eps/4+2*(eps/64+eps/64)+eps/4==13*eps/16
 constants+=1
 for k in [2,8]:
  DG=1<<(64*k*k-1).bit_length();LG=2+(2*DG-1).bit_length()
  raw=F(20480*DG*LG)/(alpha*e);n=(raw.numerator+raw.denominator-1)//raw.denominator;refs=3*n
  L=0
  while F(refs,5)*F(1,4)**(2**L)>eps/4:L+=1
  B=refs*5**L
  assert B>=refs and F(refs,5)*F(1,4)**(2**L)<=eps/4
  assert 40*DG*LG/F(n)+alpha*e/512<=alpha*e/256
  caps+=1
for M,a0,i in itertools.product([1,2,3,5,10,20],range(1,11),range(11)):
 astar=F(a0,10);f=astar*F(i,10)
 assert astar**M-f**M<=M*astar**(M-1)*(astar-f)
 assert M*astar**(M-1)*(1-astar)<=1-astar**M
 for pg in [F(0),F(1,10),F(1,2),F(9,10),F(1)]:
  assert 2*(1-pg*f**M)<=2*(1-f**M)+2*(1-pg)
 power+=1
# Shared-history product warning, exact two-point mixture.
f1,f2,w=F(1),F(1,2),F(1,3)
assert w*f1**2+(1-w)*f2**2>(w*f1+(1-w)*f2)**2
out={'status':'PASS_AUTHOR_GENERIC_SEED_DICHOTOMY_CONSTANTS_AND_CAPS','exact_branch_confidence_budget_cases':constants,'exact_coherent_and_code_cap_cases':caps,'exact_power_and_bad_mass_cases':power,'source_sha256':hashlib.sha256((Q/'GENERIC_SEED_OR_RELATIVE_SLACK_BOOTSTRAP.md').read_bytes()).hexdigest(),'scope':'Exact Fraction branch, good-event, source-cap and complete-error algebra; no simulated warm source observations, SDPs, quantum banks, compiled large circuits or hardware.'}
(Q/'seed_dichotomy_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
