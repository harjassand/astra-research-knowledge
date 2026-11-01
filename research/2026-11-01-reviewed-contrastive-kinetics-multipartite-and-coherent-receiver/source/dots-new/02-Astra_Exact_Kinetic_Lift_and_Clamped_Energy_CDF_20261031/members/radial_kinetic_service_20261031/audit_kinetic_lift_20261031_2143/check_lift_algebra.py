#!/usr/bin/env python3
"""Independent symbolic lift audit; no candidate code imported."""
import sympy as S
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
checks=[]
def eq(n,a,b=0):
 if isinstance(a,S.MatrixBase):
  residue=(a-b).applyfunc(S.cancel)
  assert residue==S.zeros(*residue.shape),(n,residue)
 else:
  residue=S.cancel(a-b);assert residue==0,(n,residue)
 checks.append(n)
def truth(n,a):
 assert a,n;checks.append(n)
beta,v=S.symbols('beta v',positive=True)
for dim,degree in [(2,2),(3,2),(4,4)]:
 z=S.Matrix(S.symbols('z0:'+str(dim),real=True));U=sum((i+1)*z[i]**degree for i in range(dim))
 if degree==4:U+=7*z[0]**2*z[1]**2+3*z[2]**2*z[3]**2
 g=S.Matrix([S.diff(U,zz) for zz in z]);H=S.hessian(U,z)
 mr=z*z.T/(degree**2*U)
 div=lambda T:S.Matrix([sum(S.diff(T[i,j],z[j]) for j in range(dim)) for i in range(dim)])
 eq('Euler '+str((dim,degree)),(z.T*g)[0],degree*U)
 eq('Euler Hessian '+str((dim,degree)),(z.T*H*z)[0],degree*(degree-1)*U)
 eq('radial divergence '+str((dim,degree)),div(mr),(dim+1-degree)*z/(degree**2*U))
 eq('radial force '+str((dim,degree)),mr*g,z/degree)
 eq('energy quadratic '+str((dim,degree)),(g.T*mr*g)[0],U)
 eq('energy drift '+str((dim,degree)),(div(mr).T*g)[0]/beta+S.trace(mr*H)/beta-v*(g.T*mr*g)[0],S.Rational(dim,degree)/beta-v*U)
 T=S.zeros(dim)
 for i in range(dim):
  for j in range(i+1,dim):
   X=S.zeros(dim,1);X[i]=g[j];X[j]=-g[i]
   eq('tangent pair '+str((dim,degree,i,j)),(X.T*g)[0],0)
   eq('pair divergence '+str((dim,degree,i,j)),sum(S.diff(X[k],z[k]) for k in range(dim)),0)
   T+=X*X.T
 eq('pair tensor '+str((dim,degree)),T,(g.T*g)[0]*S.eye(dim)-g*g.T)
 eq('tensor divergence '+str((dim,degree)),div(T),H*g-S.trace(H)*g)
 eq('tangent energy annihilation '+str((dim,degree)),(div(T).T*g)[0]+S.trace(T*H),0)
 eq('tangent quadratic annihilation '+str((dim,degree)),(g.T*T*g)[0],0)
 P=S.eye(dim)-g*g.T/(g.T*g)[0]
 eq('tangent projection square '+str((dim,degree)),P*P,P)
 eq('tangent noise square '+str((dim,degree)),(g.T*g)[0]*P*P,T)
 # Non-divergence-free tangent fields still annihilate energy in divergence form.
 X=S.zeros(dim,1);X[0]=z[0]*g[1];X[1]=-z[0]*g[0]
 divX=sum(S.diff(X[k],z[k]) for k in range(dim))
 truth('nonzero div X fixture '+str((dim,degree)),S.expand(divX)!=0)
 Tn=X*X.T
 eq('nondivfree tangent '+str((dim,degree)),(X.T*g)[0],0)
 eq('nondivfree energy drift cancellation '+str((dim,degree)),(div(Tn).T*g)[0]+S.trace(Tn*H),0)
 # Exact SPD checks at representative nonzero rational points (general proof in receipt).
 for nums in [[1]*dim,list(range(1,dim+1)),[1]+[0]*(dim-1),[-1]+[1]*(dim-1)]:
  MM=(mr+T).subs(dict(zip(z,nums)))
  for size in range(1,dim+1):
   truth('SPD principal minor '+str((dim,degree,nums,size)),MM[:size,:size].det()>0)
# Projected reversible drift, Lyapunov, boundary scale and affine transform.
y,u,k,alpha,theta,E,B,u0=S.symbols('y u k alpha theta E B u0',positive=True)
vv=1+k*(1-y*y)**2;c=2*k+1
rho=u**(alpha-1)*S.exp(-beta*vv*u)
eq('projected y stationary flux',S.diff(rho,y)/(beta*rho),-S.diff(vv,y)*u)
eq('projected u stationary flux',S.diff(u*rho,u)/(beta*rho),alpha/beta-vv*u)
eq('yvprime lower identity',y*S.diff(vv,y)+k,k*(2*y*y-1)**2)
eq('Lyapunov bracket decomposition',2*y*S.diff(vv,y)+c*vv-1,2*(y*S.diff(vv,y)+k)+c*(vv-1))
eq('Bessel scale alpha1',S.diff(S.log(u),u)+u*S.diff(S.log(u),u,2),0)
eq('Bessel scale alpha>1',alpha*S.diff(u**(1-alpha),u)+u*S.diff(u**(1-alpha),u,2),0)
logLT=-alpha*S.log(1+B*theta)-E*u0*theta/(1+B*theta)
eq('Laplace mean',-S.diff(logLT,theta).subs(theta,0),alpha*B+E*u0)
eq('Laplace variance',S.diff(logLT,theta,2).subs(theta,0),alpha*B**2+2*E*B*u0)
b,e=S.symbols('b e',positive=True)
lam=e*theta/(1+b*theta)
eq('affine composition denominator',(1+b*theta)*(1+B*lam),1+(b+e*B)*theta)
eq('affine composition exponent',E*u0*lam/(1+B*lam),E*e*u0*theta/(1+(b+e*B)*theta))
eq('Poisson mixture exponent',(E*u0/B)*(1/(1+B*theta)-1),-E*u0*theta/(1+B*theta))
for a in range(1,17):
 x=S.symbols('x',positive=True)
 cdf=1-S.exp(-x)*sum(x**j/S.factorial(j) for j in range(a))
 eq('integer gamma density '+str(a),S.diff(cdf,x),S.exp(-x)*x**(a-1)/S.factorial(a-1))
 eq('integer gamma CDF zero '+str(a),cdf.subs(x,0),0)
# Omitted nonnegative mixed coefficient premise really mattered.
a,b=S.symbols('a b',real=True)
bad=a**4+b**4-3*a*a*b*b
truth('old grammar negative quartic counterexample',bad.subs({a:1,b:1})==-1)
# Input binding, not implementation acceptance.
for name,row in json.loads((HERE/'input_hashes.json').read_text()).items():
 data=(HERE.parent/name).read_bytes()
 truth('source unchanged '+name,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'theorem algebra only; no executable CDF or full-state simulation accepted','checks':checks}
(HERE/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
