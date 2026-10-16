import sympy as s,json
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Zp=s.diag(1,-1)
sig=[(I+s.Rational(3,5)*B)/2 for B in [X,Y,Zp]]
Q=s.Matrix([[s.Rational(2,3),s.Rational(1,3),-s.Rational(2,3)],[s.Rational(2,3),-s.Rational(2,3),s.Rational(1,3)]])
svec=[s.Rational(1,3),s.Rational(2,3),s.Rational(2,3)]
vs=[Q[:,i] for i in range(3)]; zs=[svec[i]*vs[i] for i in range(3)];R0=[v*v.T for v in vs]
e=s.Rational(1,1000);delta=e;q=s.Rational(6,25)
Rs=[(R+e*I)/(1+3*e) for R in R0]
A=sum([s.kronecker_product(B,R) for B,R in zip(sig,Rs)],s.zeros(4))
T=sum(sig,s.zeros(2))/3
W=sum([s.kronecker_product(B,z) for B,z in zip(sig,zs)],s.zeros(4,2))
L=s.kronecker_product(I,A)+delta*s.kronecker_product(T.T,s.eye(4))
vecW=s.Matrix([W[i,j] for j in range(2) for i in range(4)])
u=L.inv()*vecW
N=s.simplify(4*(vecW.conjugate().T*u)[0])
E=s.simplify(4*sum([(z.T*(R+delta*I/3).inv()*z)[0] for z,R in zip(zs,Rs)]))
ratio=s.factor(N/E);margin=s.factor(N-q*E)
assert margin>0
# Physical 3-level reference blocks and binary perturbation.
t=s.Rational(1,10000)
B=[s.diag(R,delta/3) for R in Rs]
H=[R.row_join(z).col_join(z.T.row_join(s.zeros(1))) for R,z in zip([s.zeros(2)]*3,zs)]
assert sum(H,s.zeros(3))==s.zeros(3)
# Positive definiteness via Schur complements for BOTH signs.
sc=[s.factor(delta/3-t*t*(z.T*R.inv()*z)[0]) for R,z in zip(Rs,zs)]
assert all(x>0 for x in sc)
result={'epsilon':str(e),'delta':str(delta),'q':str(q),'binary_amplitude':str(t),'reference_dimension':3,'input_SLD':str(E),'output_SLD':str(N),'ratio':str(ratio),'ratio_decimal':float(ratio),'output_minus_q_input':str(margin),'positive_Schur_complements':[str(x) for x in sc],'all_assertions':'PASS'}
print(json.dumps(result,indent=2))

from pathlib import Path
assert json.loads(Path(__file__).with_name('FINITE_SLD_WITNESS.json').read_text()) == result, 'Exact finite SLD fixture mismatch'
