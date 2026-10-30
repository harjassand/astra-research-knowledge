exec(open(__file__.replace('cubic_heat.py','heat_probe.py')).read().split("E=s.factor")[0])
from itertools import combinations
X=x1+s.I*x2;Y=y1+s.I*y2;P=p+s.I*q;QQ=r+s.I*v;RR=t+s.I*u
S1=s.conjugate(X)*P+2*s.conjugate(Y)*QQ
S2=s.conjugate(Y)*RR+s.conjugate(X)*QQ+Y*s.conjugate(QQ)
S3=s.conjugate(X)*QQ+2*Y*s.conjugate(QQ)
# All symbols above are real; apply explicit conjugate replacement.
realvars=[x1,x2,y1,y2,p,q,r,v,t,u]
cc=lambda z:s.expand(s.conjugate(z).subs({s.conjugate(z):z for z in realvars}))
re=lambda z:s.expand((z+cc(z))/2)
S1=cc(cc(S1));S2=cc(cc(S2));S3=cc(cc(S3))
Cxy=x1*(y1*y1-y2*y2)+2*x2*y1*y2
C=Cxy.subs({x1:a+d,x2:c-b,y1:a-d,y2:c+b},simultaneous=True)
HC=s.hessian(C,A)
unknown=s.symbols('w:24');omega=s.zeros(4);k=0
for i,j in combinations(range(4),2):
 omega[i,j]=sum(unknown[k+l]*A[l] for l in range(4));omega[j,i]=-omega[i,j];k+=4
EC=s.expand((B1.T*HC*B1)[0]+(B2.T*HC*B2)[0]+(B1.T*omega*B2)[0]).subs(subs,simultaneous=True).expand()
f1,f2,f3=s.symbols('f1 f2 f3',real=True)
expr=s.Poly(s.expand(EC-16*re(RR*(f1*cc(S1)+f2*S2+f3*S3))),realvars)
eqs=list(expr.coeffs())
for i,j,k in combinations(range(4),3):eqs.append(s.diff(omega[j,k],A[i])-s.diff(omega[i,k],A[j])+s.diff(omega[i,j],A[k]))
sol=s.linsolve(eqs,unknown+(f1,f2,f3));print(sol)
