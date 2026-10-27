from pathlib import Path
import json,runpy,sys,sympy as s
p=Path('/workspace/scratch/57d8dd795b13/morrey_law_first_stress_20261026/cube_brownian_completion');sys.path.insert(0,str(p));old=Path.write_text
Path.write_text=lambda self,data,*a,**k: len(data) if self.read_text()==data else (_ for _ in ()).throw(AssertionError(str(self)))
try:
 for n in ['receive_local_posterior_feasibility.py','receive_tree_completable_posterior.py']:
  print('BEGIN',n,flush=True);runpy.run_path(str(p/n),run_name='__main__');print('MATCH',n,flush=True)
finally:Path.write_text=old
j=json.loads((p/'same_law_AC/local_posterior_feasibility_receipt.json').read_text());Y=s.Matrix([list(map(s.Rational,r['point']))for r in j['rows']]).T;pp=s.symbols('p0:8');J=s.ones(3)-s.eye(3)
def q(v):return (v.T*J*v)[0]
def defect(ids):
 w=sum(pp[i] for i in ids);v=sum((pp[i]*Y[:,i] for i in ids),s.zeros(3,1));return s.factor(w*sum(pp[i]*q(Y[:,i])for i in ids)-q(v))
for a in range(0,8,2):assert q(Y[:,a]-Y[:,a+1])==0
left=defect(range(4));right=defect(range(4,8));print('left',left,'right',right)
assert s.factor(left-(pp[0]-pp[1])*(15*pp[2]+17*pp[3])/512)==0
assert s.factor(right+s.Rational(3,8)*(2*pp[4]*pp[7]-3*pp[5]*pp[6]-pp[5]*pp[7]))==0
for r in j['rows']:assert max(abs(s.Rational(v)) for v in r['point'])<1
p0=s.Matrix([s.Rational(r['original_probability'])for r in j['rows']]);assert sum(p0)==1 and p0[0]==p0[1]
assert 2*p0[4]*p0[7]-3*p0[5]*p0[6]-p0[5]*p0[7]==0
print('INDEPENDENT TREE CONSTRAINTS PASS',flush=True)
