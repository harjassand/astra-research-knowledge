import sympy as s,json,sys,numpy as np
from pathlib import Path
p=Path(__file__).parent;sys.path.insert(0,str(p.parent/'four_spin_encoder_compiler_20261029'));import compiler
E=s.zeros(16,2)
for i,v in [(5,1),(6,-1),(9,-1),(10,1)]:E[i,0]=s.Rational(v,2)
for i,v in [(3,1),(12,1),(5,-s.Rational(1,2)),(6,-s.Rational(1,2)),(9,-s.Rational(1,2)),(10,-s.Rational(1,2))]:E[i,1]=v/s.sqrt(3)
assert s.simplify(E.T*E)==s.eye(2)
A=E.copy();reds=[]
for col in range(2):
 for row in range(15,col,-1):
  x,y=s.simplify(A[col,col]),s.simplify(A[row,col])
  if y==0:continue
  r=s.sqrt(x*x+y*y);G=s.simplify(s.Matrix([[x,y],[-y,x]])/r);V=s.simplify(G*A[[col,row],:])
  A[col,:]=V[0,:];A[row,:]=V[1,:];reds.append((col,row,G))
assert s.simplify(A-s.eye(16)[:,:2])==s.zeros(16,2)
U=s.eye(16);two=[]
for a,b,G in reds[::-1]:
 G=G.T;V=s.simplify(G*U[[a,b],:]);U[a,:]=V[0,:];U[b,:]=V[1,:];two.append((a,b,G))
assert s.simplify(U.T*U)==s.eye(16) and s.simplify(U[:,:2]-E)==s.zeros(16,2)
paulis=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
for P in paulis:
 S=s.zeros(16)
 for j in range(4):
  factors=[s.eye(2)]*4;factors[j]=P;S+=s.kronecker_product(*factors)/2
 assert s.simplify(S*E)==s.zeros(16,2)
ref=compiler.build()[3];assert len(ref)==len(two)==9
err=max(np.linalg.norm(np.array(M,float)-R) for (a,b,M),(aa,bb,R) in zip(two,ref) if (a,b)==(aa,bb));assert all((a,b)==(aa,bb) for (a,b,M),(aa,bb,R) in zip(two,ref))
rows=[{'a':a,'b':b,'exact_matrix':[[str(v) for v in row] for row in M.tolist()]} for a,b,M in two]
out={'exact_symbolic_QR_target_unitarity_and_spin_checks':True,'two_level_gate_count':len(two),'analytic_count_addressed_primitives':sum(2*((a^b).bit_count()-1)+1 for a,b,M in two),'floating_author_twolevel_matrix_difference':float(err),'ideal_twolevel_gates':rows,'scope':'Exact SymPy radical arithmetic verifies QR and singlet core. Does not interval-certify stored floating controlled-gate angles.'};(p/'exact_QR_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
