from pathlib import Path
import sympy as s,json,runpy,sys
p=Path('/workspace/scratch/57d8dd795b13/morrey_law_first_stress_20261026/cube_brownian_completion');sys.path.insert(0,str(p));j=json.loads((p/'same_law_AC/negative_subtree_posterior_point_receipt.json').read_text());x=s.symbols('p0:8');Y=s.Matrix(j['frontier_points']).T.applyfunc(s.Rational);J=s.ones(3)-s.eye(3);p0=s.Matrix(j['frontier_probabilities']).applyfunc(s.Rational);T=s.Matrix(j['tangent_at_point']).applyfunc(s.Rational);fs=[s.sympify(v,locals=dict(zip(map(str,x),x)))for v in j['constraint_expressions']]
def defect(ids):
 w=sum(x[i]for i in ids);v=sum((x[i]*Y[:,i]for i in ids),s.zeros(3,1));return s.factor(w*sum(x[i]*(Y[:,i].T*J*Y[:,i])[0]for i in ids)-(v.T*J*v)[0])
assert s.factor(defect(range(8))-fs[1])==0
assert s.factor(defect(range(4))-fs[2])==0
assert s.rem(s.Poly(defect(range(4,8)),*x),s.Poly(fs[3],*x))==0
for i in range(0,8,2):assert ((Y[:,i]-Y[:,i+1]).T*J*(Y[:,i]-Y[:,i+1]))[0]==0
sub=dict(zip(x,p0));assert all(f.subs(sub)==0 for f in fs)
C=s.Matrix([[s.diff(f,v).subs(sub)for v in x]for f in fs]);assert C.rank()==4 and C*T==s.zeros(4) and T[[3,4,5,7],:]==s.eye(4)
Hs=[s.hessian(f,x)/2 for f in fs if s.total_degree(f)==2];assert Hs==[s.Matrix(h).applyfunc(s.Rational)for h in j['quadratic_constraint_matrices']]
hc=T.T*Hs[1]*T;assert hc.rank()==2 and s.trace(hc)**2-s.trace(hc*hc)<0
print('INDEPENDENT ACTUAL TREE CONSTRAINT/HESSIAN/TANGENT CHECK PASS',flush=True)
old=Path.write_text;Path.write_text=lambda self,data,*a,**k: len(data) if self.read_text()==data else (_ for _ in ()).throw(AssertionError(str(self)))
try:runpy.run_path(str(p/'receive_shear_covariance_identity.py'),run_name='__main__')
finally:Path.write_text=old
