import json, random
from pathlib import Path
import sympy as s
r=random.Random(731)
def mat(n,m): return s.Matrix(n,m,lambda i,j:s.Integer(r.randrange(-2,3))+s.I*r.randrange(-2,3))
def dissip(ls,rho):
    z=s.zeros(rho.rows)
    for l in ls:
        z+=l*rho*l.H-(l.H*l*rho+rho*l.H*l)/2
    return z.applyfunc(s.simplify)
checks=0
for case in range(8):
    d=2;m=2
    D=s.diag(1,4); t=mat(m,m);F=t+t.H
    N=F-s.I*D; B=mat(m*d,d)
    X=s.kronecker_product(N.inv(),s.eye(d))*B
    E=s.kronecker_product(s.diag(s.sqrt(2),2*s.sqrt(2)),s.eye(d))*X
    K=D**s.Rational(-1,2)*F*D**s.Rational(-1,2)
    S=-B.H*s.kronecker_product((N.inv()+N.inv().H)/2,s.eye(d))*B
    assert (S+E.H*s.kronecker_product(K,s.eye(d))*E/2).applyfunc(s.simplify)==s.zeros(d);checks+=1
    es=[E[i*d:(i+1)*d,:] for i in range(m)]
    e=[s.trace(x)/d for x in es]; aa=[x-v*s.eye(d) for x,v in zip(es,e)]
    He=sum((s.I*(s.conjugate(v)*a-v*a.H)/2 for v,a in zip(e,aa)),s.zeros(d))
    for i in range(d):
      for j in range(d):
        rho=s.zeros(d);rho[i,j]=1
        assert (dissip(es,rho)-dissip(aa,rho)+s.I*(He*rho-rho*He)).applyfunc(s.simplify)==s.zeros(d);checks+=1
    nu=sum(s.trace(a.H*a)/d for a in aa)
    alt=sum(s.trace(l.H*l)/d-abs(v)**2 for l,v in zip(es,e))
    assert s.simplify(nu-alt)==0;checks+=1
# Data-dependent counter-scope: scalar jump, nontrivial leading Hamiltonian.
Z=s.diag(1,-1);N=Z-s.I*s.eye(2);B=N/3;X=(N.inv()*B).applyfunc(s.simplify)
assert X==s.eye(2)/3
E=s.sqrt(2)*X; S=-X.H*Z*X
assert S==-Z/9 and dissip([E],s.Matrix([[1,2],[3,4]]))==s.zeros(2);checks+=2
out={'status':'pass','exact_identity_checks':checks,'random_seed':731,'scope':'Exact elimination and Lindblad gauge algebra; not finite-rate bounds, norm-inequality verification or hardware evidence.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
