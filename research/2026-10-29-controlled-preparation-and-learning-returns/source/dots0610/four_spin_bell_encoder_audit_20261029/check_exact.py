import sympy as s,json,sys,numpy as np
from pathlib import Path
p=Path(__file__).parent;source=p.parent/'four_spin_bell_encoder_20261029';sys.path.insert(0,str(source));import check_bell_encoder as author
X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
def embed(M,t,n=4):
 return s.kronecker_product(*[M if j==t else s.eye(2) for j in reversed(range(n))])
def CX(c,t):
 M=s.zeros(16)
 for i in range(16):M[i^((1<<t) if i&(1<<c) else 0),i]=1
 return M
def Rycs(c,v):return s.Matrix([[c,-v],[v,c]])
c1=s.sqrt((1+1/s.sqrt(3))/2);s1=s.sqrt((1-1/s.sqrt(3))/2)
c2=s.sqrt(2+s.sqrt(2))/2;s2=s.sqrt(2-s.sqrt(2))/2
R1=Rycs(c1,-s1);R2=Rycs(c2,s2)
gs=[embed(X,0),embed(X,1),embed(X,0),embed(R1,1),CX(0,1),embed(R1.T,1),CX(0,1),embed(X,0),embed(X,1),embed(R2,0),CX(1,0),embed(R2.T,0),CX(1,0),embed(X,1),embed(Z,0),embed(Z,1),CX(0,2),CX(1,3),embed(H,0),CX(0,1),embed(H,2),CX(2,3)]
U=s.eye(16)
for G in gs:U=s.simplify(G*U)
E=s.zeros(16,2)
for i,v in [(5,1),(6,-1),(9,-1),(10,1)]:E[i,0]=s.Rational(v,2)
for i,v in [(3,1),(12,1),(5,-s.Rational(1,2)),(6,-s.Rational(1,2)),(9,-s.Rational(1,2)),(10,-s.Rational(1,2))]:E[i,1]=v/s.sqrt(3)
assert s.simplify(U[:,:2]-E)==s.zeros(16,2)
assert all(s.simplify(G.T*G)==s.eye(16) for G in gs)
# Exact unitarity follows by product of individually verified unitary gates.
A=np.eye(16,dtype=complex)
for g in author.gates():author.apply(A,g)
err=np.linalg.norm(A-np.array(U,float));assert err<1e-12
# Canonical reset Choi is independent of the chosen unitary completion.
Ks=[U.T[:2,:]]
for a in range(1,8):
 for b in range(2):
  k=s.zeros(2,16);k[0,:]=U.T[2*a+b,:];Ks.append(k)
assert s.simplify(sum([k.T*k for k in Ks],s.zeros(16))-U*U.T)==s.zeros(16)
# This equals identity by the exact gatewise unitarity argument above.
# Since all matrices real, E†=E^T. Flatten convention is output first.
J=s.zeros(32)
for k in Ks:
 v=s.Matrix(list(k));J+=v*v.T
v=s.Matrix(list(E.T));want=v*v.T;want[:16,:16]+=U*U.T-E*E.T
assert s.simplify(J-want)==s.zeros(32)
out={'exact_radical_full_gate_product':True,'exact_encoded_columns':True,'exact_full_unitarity':True,'exact_canonical_reset_Choi_and_TP':True,'CNOT_count':8,'single_qubit_count':14,'work_ancillas':0,'float_compiler_vs_exact_matrix_Frobenius':float(err),'scope':'Exact symbolic ideal gate identities. Stored floating angles and physical gate fidelity are not certified.'};(p/'exact_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
