import sympy as s,json,hashlib
from pathlib import Path
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);ps=[X,Y,Z]
# Generate SO3 signed-permutation group from two quarter-turn generators.
Gx=s.Matrix([[1,0,0],[0,0,-1],[0,1,0]]);Gz=s.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
group={tuple(s.eye(3)):s.eye(3)};todo=[s.eye(3)]
while todo:
 A=todo.pop()
 for B in [Gx,Gz]:
  C=B*A;k=tuple(C)
  if k not in group:group[k]=C;todo.append(C)
assert len(group)==24
Vs=[s.Rational(3,5)*I-s.I*s.Rational(4,5)*p for p in [X,Y,Z,X+0*Y]]
# Deliberately nonidentity reference gauge and differing relative rotations.
Vs[3]=s.Rational(5,13)*I-s.I*s.Rational(12,13)*Y
Rs=[s.Matrix(3,3,lambda a,b:s.simplify(s.trace(ps[a]*u*ps[b]*u.conjugate().T)/2)) for u in Vs]
for j in [1,2,3]:
 A=sum((s.kronecker_product(Rs[j]*g*Rs[j].T,Rs[0]*g*Rs[0].T) for g in group.values()),s.zeros(9))/24
 C=Rs[j]*Rs[0].T;c=s.Matrix(list(C));assert A==c*c.T/3
# Two explicit unnormalized singlet-carrier vectors, exact collective Lie-algebra test.
v=s.Matrix([0,1,-1,0]);e0=s.kronecker_product(v,v);e1=s.zeros(16,1)
for k in [3,12]:e1[k]=1
for k in [5,6,9,10]:e1[k]=-s.Rational(1,2)
E=s.Matrix.hstack(e0,e1);assert E.rank()==2
for p in ps:
 J=s.zeros(16)
 for j in range(4):
  f=[I]*4;f[j]=p;J+=s.kronecker_product(*f)
 assert J*E==s.zeros(16,2)
# Thus arbitrary collective SU2, not just24 chosen representatives, fixes this carrier.
W=s.kronecker_product(*Vs);relative=[u*Vs[0].conjugate().T for u in Vs]
Wr=s.kronecker_product(*relative)
assert (W*E-Wr*E).applyfunc(s.simplify)==s.zeros(16,2)
res={'group_size':24,'exact_relative_star_transfer_checks':3,'collective_generator_kernel_checks':3,'protected_dimension':2,'relative_frames_suffice_on_carrier':True,'scope':'Exact rational/symbolic independent check; no hardware or generic source claim'}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(res)
