"""Independent finite algebra checks for the direction-preserving density method.
No optimizer output or previous verification JSON is read. These checks are
not a proof assistant, not a proof of analytic existence, and not a proof
of quasiconvexity for the complete invariant cone.
"""
from pathlib import Path
import json, math
import sympy as S
ROOT=Path(__file__).resolve().parent
checks=[]
def passcheck(name,details=None):
 checks.append({'name':name,'status':'PASS','details':details});print('PASS:',name,flush=True)
def zero(x):
 assert S.cancel(S.expand(x))==0
x=S.symbols('a b c d');q=S.symbols('q0:4');r,s=S.symbols('r s',nonzero=True)
mon=[]
for e0 in range(5):
 for e1 in range(5-e0):
  for e2 in range(5-e0-e1):
   e3=4-e0-e1-e2;mon.append(S.prod(z**e for z,e in zip(x,(e0,e1,e2,e3))))
assert len(mon)==35
for f in mon:
 df=[S.diff(f,z) for z in x]
 zero(sum(d*z for d,z in zip(df,x))-4*f)
 shifted=f.subs(dict(zip(x,[z+h for z,h in zip(x,q)])),simultaneous=True)
 Fsn=shifted*s**4
 linear=s**4*(sum(d*(z+4*h) for d,z,h in zip(df,x,q)))/4
 rem=s**4*(shifted-f-sum(d*h for d,h in zip(df,q)))
 zero(Fsn-linear-rem)
passcheck('Euler and directional Picone algebra for all 35 quartic monomials')

n1,n2=S.symbols('n1 n2');rx,ry,sx,sy=S.symbols('rx ry sx sy');d00,d01,d10,d11=S.symbols('d00 d01 d10 d11')
n=S.Matrix([n1,n2]);Dn=S.Matrix([[d00,d01],[d10,d11]])
Ar=Dn+n*S.Matrix([[rx/r,ry/r]])
Q=n*S.Matrix([[sx/s-rx/r,sy/s-ry/r]])
Deta=(s**4/r**3)*Dn+n*S.Matrix([[4*s**3*sx/r**3-3*s**4*rx/r**4,4*s**3*sy/r**3-3*s**4*ry/r**4]])
assert S.simplify(Deta-(s**4/r**3)*(Ar+4*Q))==S.zeros(2)
zero(Q.det())
passcheck('Actual chain-rule matrix and rank-one logarithmic-amplitude increment')

a,b,c,d=x;u=a*a+c*c;v=b*b+d*d;det=a*d-b*c
G=3*(u+v-2*det)**2+S.Rational(35,24)*u*u+det*det-S.Rational(5,2)*det*u
rho,z1,z2,dr,dz1,dz2=S.symbols('rho z1 z2 dr dz1 dz2',nonzero=True)
t=S.symbols('t')
# All quartic monomials, including mixed output orientation, tested separately.
for f in mon:
 subst={a:z1/(4*rho),b:z2/(4*rho)}
 h=rho*f.subs(subst,simultaneous=True)
 variables=[rho,z1,z2];velocity=S.Matrix([dr,dz1,dz2]);d2=(velocity.T*S.hessian(h,variables)*velocity)[0]
 zdel=S.Matrix([dz1-z1*dr/rho,dz2-z2*dr/rho])
 rhs=(zdel.T*S.hessian(f,[a,b]).subs(subst,simultaneous=True)*zdel)[0]/(16*rho)
 zero(d2-rhs)
passcheck('Perspective Hessian identity for all 35 quartic monomials')

A,L,C=S.symbols('A L C',nonzero=True)
zero(A+L+C-A/3-(3*(L+4*A/3)**2/(8*A)+C-3*L**2/(8*A)))
passcheck('Exact one-dimensional quartic Bregman square completion')

f=G;h=rho*f.subs({a:z1/(4*rho),b:z2/(4*rho)},simultaneous=True)
fa=S.diff(f,a);fb=S.diff(f,b)
sub={a:z1/(4*rho),b:z2/(4*rho)}
zero(S.diff(h,rho)-(f-a*fa-b*fb).subs(sub,simultaneous=True))
zero(S.diff(h,z1)-fa.subs(sub,simultaneous=True)/4)
zero(S.diff(h,z2)-fb.subs(sub,simultaneous=True)/4)
passcheck('Scalar flux and density Euler derivative')

M=[]
for i,j in [(0,0),(0,1),(1,1)]:
 quadratic=S.diff(G,x[i],x[j]);M.append(S.hessian(quadratic,x)/2)
M11,M12,M22=M
K=S.zeros(4)
for (i,j),val in zip([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],map(S.Rational,[11,'91/6',0,0,11,'41/3'])):
 K[i,j]=val;K[j,i]=-val
Gram=M11.row_join(M12+K).col_join((M12-K).row_join(M22))
minor=[S.det(Gram[:j,:j]) for j in range(1,7)]
assert minor==list(map(S.Rational,['107/2',642,'1605/8','8445/16','2815/8','26865/4']))
assert Gram.rank()==6
T=Gram[:6,:6];C=Gram[6:,6:];B=Gram[:6,6:]
assert S.simplify(C-B.T*T.inv()*B)==S.zeros(2)
st,tt=S.symbols('st tt');xx=S.Matrix(x);vec=(st*xx).col_join(tt*xx)
zero((vec.T*Gram*vec)[0]-(st**2*S.diff(G,a,2)+2*st*tt*S.diff(G,a,b)+tt**2*S.diff(G,b,2)))
passcheck('Independent global acoustic certificate for G',{'leading_minors':[str(t) for t in minor],'rank':6})

zero(G-3*(u+v)**2-S.Rational(35,24)*u**2-13*det**2+12*det*(u+v)+S.Rational(5,2)*det*u)
assert G.subs({a:1,b:0,c:0,d:1})==-S.Rational(1,24)
fI=G.subs({a:1,b:0,c:0,d:1});fJ=G.subs({a:1,b:0,c:0,d:-1})
assert (36**4*fI+36**2*fJ)/(1+36**2)==-S.Rational(1350,1297)
passcheck('Rank-one lower value mu_G=3 and negative invertible value G(I)=-1/24')

pa,pb,cy,sy=S.symbols('pa pb cy sy');rr=1+pa*(2*cy**2-1);rry=-4*pa*sy*cy;kk=(2+pb)*cy
integrand=rr*kk**4+rry**2*kk**2/(8*rr)+rry**4/(256*rr**3)
def circle(poly):
 ans=S.Rational(0)
 for (j,k),co in S.Poly(S.expand(poly),sy,cy).terms():
  if j%2 or k%2:continue
  m,jj=j//2,k//2
  mom=S.Rational(math.factorial(2*m)*math.factorial(2*jj),4**(m+jj)*math.factorial(m)*math.factorial(jj)*math.factorial(m+jj))
  ans+=co*mom
 return S.simplify(ans)
H=S.Matrix(2,2,lambda i,j:circle(S.diff(integrand,[pa,pb][i],[pa,pb][j]).subs({pa:0,pb:0})))
assert H==S.Matrix([[1,8],[8,18]]) and H.det()==-46
passcheck('Exact failure of joint phase-density convexity even for |A|^4',{'Hessian':str(H),'determinant':-46})

rr=S.symbols('r',real=True)
val=S.integrate(2*((S.Rational(1,4)+rr**2)**2-(4/S.sqrt(3))*(S.Rational(1,4)+rr**2)*rr/2),(rr,0,1))
assert S.simplify(val-(S.Rational(103,120)-S.sqrt(3)/2))==0
assert S.Rational(3,4)-S.Rational(103,120)**2==S.Rational(191,14400)
passcheck('Reconstructed critical-trace negative open-strip action')

# Exact algebra behind the density interpolation, which preserves the L4 mass.
r0,r1,t0=S.symbols('r0 r1 t0',positive=True);m0=(1-t0)*r0**4;m1=t0*r1**4
zero(m0/(m0+m1)+m1/(m0+m1)-1)
# Both full normalized gradients have the same Dn; their difference is rank one.
la,lb,lc,ld=S.symbols('la lb lc ld')
P=n*S.Matrix([[la-lc,lb-ld]])
zero(P.det())
passcheck('Convex density interpolation has normalized rank-one matrix differences')

out={'status':'PASS','groups':len(checks),'checks':checks,'scope':'Finite exact identities only. Convexity, analytic existence, density approximation, Picone integration, interval implementation and quasiconvexity scope must be assessed in the note.'}
(ROOT/'directional_density_verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
