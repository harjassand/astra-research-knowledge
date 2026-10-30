exec(open(__file__.replace('heat_null_modes.py','heat_probe.py')).read().split("E=s.factor")[0])
from itertools import combinations
for sign in [1,-1]:
 Cxy=x1*(y1*y1-y2*y2)+sign*2*x2*y1*y2
 C=Cxy.subs({x1:a+d,x2:c-b,y1:a-d,y2:c+b},simultaneous=True)
 HC=s.hessian(C,A)
 unknown=s.symbols('w:24');omega=s.zeros(4);kk=0
 for i,j in combinations(range(4),2):
  omega[i,j]=sum(unknown[kk+l]*A[l] for l in range(4));omega[j,i]=-omega[i,j];kk+=4
 EC=s.expand((B1.T*HC*B1)[0]+(B2.T*HC*B2)[0]+(B1.T*omega*B2)[0]).subs(subs,simultaneous=True).expand()
 eqs=[]
 for E0 in [EC.subs({y1:0,y2:0,p:0,q:0,r:0,v:0}),EC.subs({x1:0,x2:0,r:0,v:0,t:0,u:0})]:
  eqs.extend(s.Poly(E0,x1,x2,y1,y2,p,q,r,v,t,u).coeffs())
 for i,j,k in combinations(range(4),3):eqs.append(s.diff(omega[j,k],A[i])-s.diff(omega[i,k],A[j])+s.diff(omega[i,j],A[k]))
 print('sign',sign,'null constraints',s.linsolve(eqs,unknown))
