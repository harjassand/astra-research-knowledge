import sympy as s,json
from pathlib import Path
I=s.I;rows=[]
def run(Ks,k,d,name):
 assert (sum((K.conjugate().T*K for K in Ks),s.zeros(k))-s.eye(k)).applyfunc(s.simplify)==s.zeros(k)
 def N(X):return sum((K*X*K.conjugate().T for K in Ks),s.zeros(d))
 basis=[s.eye(k)[:,i] for i in range(k)];di=[N(v*v.T) for v in basis];out=[[None]*k for _ in range(k)];settings=k
 for i in range(k):out[i][i]=di[i]
 for i in range(k):
  for j in range(i+1,k):
   vi,vj=basis[i],basis[j]
   rp=(vi+vj)*(vi+vj).T/2;rm=(vi-vj)*(vi-vj).T/2
   ip=(vi+I*vj)*(vi+I*vj).conjugate().T/2;im=(vi-I*vj)*(vi-I*vj).conjugate().T/2
   yr=N(rp)-N(rm);yi=N(ip)-N(im);out[i][j]=s.simplify((yr+I*yi)/2);out[j][i]=out[i][j].conjugate().T;settings+=4
 for i in range(k):
  for j in range(k):assert (out[i][j]-N(basis[i]*basis[j].T)).applyfunc(s.simplify)==s.zeros(d)
 J=s.BlockMatrix(out).as_explicit()/k
 assert (J-J.conjugate().T).applyfunc(s.simplify)==s.zeros(k*d) and s.simplify(s.trace(J))==1
 # Exact marginal and Hermitian-conjugate matrix-unit reconstruction.
 for i in range(k):
  for j in range(k):assert s.simplify(s.trace(out[i][j]))==(1 if i==j else 0)
 rows.append(dict(name=name,k=k,d=d,input_preparations=settings,measurement_settings=settings*d*d,all_matrix_units_exact=True,Choi_marginal_exact=True))
a=s.Rational(4,5);b=s.Rational(3,5);X=s.Matrix([[0,1],[1,0]]);U=(3*s.eye(2)-4*I*X)/5
H=s.eye(3)-2*s.Matrix([1,2,2])*s.Matrix([[1,2,2]])/9;V=H[:,:2]
run([V*s.diag(1,a)*U,V*s.Matrix([[0,b],[0,0]])*U],2,3,'complex rectangular amplitude damping')
U3=s.diag(1,I,-1)*H
run([s.Matrix([[1,0,0],[0,a,0]])*U3,s.Matrix([[0,b,0],[0,0,1]])*U3],3,2,'complex dimensional reduction')
run([s.eye(2)],2,2,'identity')
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'Exact known-input matrix-unit process reconstruction; no physical Schur pipeline or remote experiment','cases':rows,'entry_component_bound':'2 e0/k','setting_count':'(2k^2-k)d^2'},indent=2)+'\n');print(rows)
