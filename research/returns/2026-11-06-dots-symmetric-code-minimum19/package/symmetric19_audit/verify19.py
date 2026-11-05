from fractions import Fraction
from math import comb
import mpmath as mp
import sympy as s
import json
mp.mp.dps=100
x=s.symbols('q2 q4 q6 q8 q10 q12 q14 q16 q18')
q={0:s.Integer(1),**{2*i+2:xx for i,xx in enumerate(x)}}
F=[]; labels=[]
for a in [0,2,4]:
 for b in [1,3]:
  F.append(s.expand(sum(comb(15,2*k)*q[2*k+a]*q[19-2*k-b] for k in range(8))))
  labels.append(('D1',a,b))
for a in [0,2,4]:
 for b in [0,2,4]:
  if a<=b and a+b<4:
   F.append(s.expand(sum(comb(15,2*k)*(q[2*k+a]*q[2*k+b]-q[2*k+4-a]*q[2*k+4-b]) for k in range(8))))
   labels.append(('D2',a,b))
for a in [1,3]:
 for b in [1,3]:
  if a<=b and a+b<4:
   F.append(s.expand(sum(comb(15,2*k)*(q[19-2*k-a]*q[19-2*k-b]-q[19-2*k-4+a]*q[19-2*k-4+b]) for k in range(8))))
   labels.append(('D3',a,b))
assert len(F)==9
fun=s.lambdify(x,F,'mpmath')
init=[mp.mpf(t) for t in ['0.0477572','-0.0267249','-0.00506367','0.00332914','0.00527235','-0.000947223','0.0152707','0.00888631','0.32678']]
root=mp.findroot(fun,init,tol=mp.mpf('1e-90'),maxsteps=30)
print('Root:')
for i,rr in enumerate(root): print(f'q{2*i+2} = {mp.nstr(rr,90)}')
print('Numerical polynomial residual:',max(abs(r) for r in fun(*root)))
# Define exact rational center and exact rational inverse of center Jacobian.
c=s.Matrix([s.Rational(mp.nstr(rr,70)) for rr in root])
subs=dict(zip(x,c))
Fc=s.Matrix(F).subs(subs)
J=s.Matrix(F).jacobian(x)
Jc=J.subs(subs)
B=Jc.inv()
infnorm=lambda A:max(sum(abs(z) for z in A.row(i)) for i in range(A.rows))
eta=infnorm(B*Fc)
H=max(sum(abs(s.diff(fi,xj,xk)) for xj in x for xk in x) for fi in F)
Bnorm=infnorm(B)
r=s.Rational(1,10**50)
kappa=Bnorm*H*r
assert eta+kappa*r<r and kappa<1
print('Exact-rational Banach certificate:')
print('radius=',r)
print('eta <=',s.N(eta,12),' Bnorm <=',s.N(Bnorm,12),' Hessian bound=',H,' kappa <=',s.N(kappa,12))
print('eta < 1e-65:',eta<s.Rational(1,10**65))
print('Bnorm < 2:',Bnorm<2)
print('kappa < 1e-40:',kappa<s.Rational(1,10**40))
# Direct four-qubit reduced transition matrices in symmetric four-qubit Dicke basis.
qq=[mp.mpf(1)]+list(root)
alpha=[mp.mpf(0)]*20
for i,z in enumerate(qq):alpha[2*i]=z*mp.sqrt(comb(19,2*i))
norm=mp.sqrt(sum(z*z for z in alpha))
alpha=[z/norm for z in alpha]
beta=list(reversed(alpha))
def red(a,b):
 R=mp.matrix(5,5)
 for u in range(5):
  for v in range(5):
   R[u,v]=sum(mp.sqrt(comb(4,u)*comb(4,v))*comb(15,k)*a[k+u]*b[k+v]/mp.sqrt(comb(19,k+u)*comb(19,k+v)) for k in range(16))
 return R
rho0,rho1,cross=red(alpha,alpha),red(beta,beta),red(alpha,beta)
print('Normalizing factor N:',mp.nstr(norm,50))
print('Direct 4-qubit reduced KL maximum residual:',mp.nstr(max([abs(z) for z in rho0-rho1]+[abs(z) for z in cross]),20))
print('Dicke alpha even coefficients:')
for i in range(10): print(2*i,mp.nstr(alpha[2*i],50))
print('Equations:')
for lab,f in zip(labels,F):print(lab,str(f))
with open('symmetric19_audit/certificate_data.json','w') as out:json.dump({'center':[str(z) for z in c],'radius':str(r),'equations':[str(f) for f in F],'root_numerical':[mp.nstr(z,90) for z in root],'alpha_even_numerical':[mp.nstr(alpha[2*i],50) for i in range(10)],'eta':str(eta),'kappa':str(kappa),'H':str(H)},out,indent=2)
