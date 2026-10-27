from pathlib import Path
import sympy as s,json,runpy,sys
p=Path('/workspace/scratch/57d8dd795b13/morrey_law_first_stress_20261026/cube_brownian_completion');sys.path.insert(0,str(p));old=Path.write_text
Path.write_text=lambda self,data,*a,**k: len(data) if self.read_text()==data else (_ for _ in ()).throw(AssertionError(str(self)))
try:runpy.run_path(str(p/'receive_guarded_posterior_control.py'),run_name='__main__')
finally:Path.write_text=old
j=json.loads((p/'same_law_AC/local_posterior_feasibility_receipt.json').read_text());Y=s.Matrix([list(map(s.Rational,r['point']))for r in j['rows']]).T;J=s.ones(3)-s.eye(3);G=Y.T*J*Y;q=s.Matrix([[G[i,i]for i in range(8)]]);d=s.Matrix([1,1,-2,0,0,0,0,0]);z=s.symbols('z0:4');base=s.zeros(8,1)
for i,v in zip([3,5,6,7],z):base[i]=v
base[4]=z[1]*(3*z[2]+z[3])/(2*z[3]);base[2]=1-sum(base)
L=(q*d-2*base.T*G*d)[0];a=s.factor(((base.T*G*base)[0]-(q*base)[0])/L);pp=base+a*d
assert s.factor((q*pp)[0]-(pp.T*G*pp)[0])==0
assert s.factor(2*pp[4]*pp[7]-3*pp[5]*pp[6]-pp[5]*pp[7])==0
assert sum(pp)==1 and pp[0]==pp[1]
p0=s.Matrix([s.Rational(r['original_probability'])for r in j['rows']]);subs=dict(zip(z,[p0[i]for i in [3,5,6,7]]));assert all(s.factor(pp[i].subs(subs)-p0[i])==0 for i in range(8))
x=s.Matrix(s.symbols('x0:8'));F1=2*x[4]*x[7]-3*x[5]*x[6]-x[5]*x[7];C=s.ones(1,8).col_join(s.Matrix([[1,-1,0,0,0,0,0,0]])).col_join(q-2*x.T*G).col_join(s.Matrix([[s.diff(F1,v)for v in x]]));ell=(q*d-2*x.T*G*d)[0]
assert s.factor(C[:,[0,1,2,4]].det()-2*x[7]*ell)==0
assert s.factor(ell.subs(dict(zip(x,pp)))-L)==0
print('EXACT CHART, SOURCE, AND PIVOT DENOMINATOR IDENTITY PASS',flush=True)
