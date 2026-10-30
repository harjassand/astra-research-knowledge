import sympy as S
import scipy.integrate as I
import math,json
from pathlib import Path
# Order A,C,E; conversion A->C->E->A. Birth only from A.
Q=S.Matrix([[-1,1,0],[0,-1,1],[1,0,-1]])
b=S.Matrix([1,0,0]); k=3
p=S.symbols('p0:3'); sol=S.solve(list(Q.T*S.Matrix(p))+[sum(p)-1],p);pi=S.Matrix([[sol[z] for z in p]])
beta=(pi*b)[0];hs=S.symbols('h0:3');solh=S.solve(list(Q*S.Matrix(hs)-(S.ones(k,1)*beta-b))+[(pi*S.Matrix(hs))[0]],hs)
h=S.Matrix([solh[z] for z in hs]);h=h-S.ones(k,1)*min(h);H=max(h)
M=max(sum(Q[i,j]*(h[j]-h[i])**2 for j in range(k) if j!=i) for i in range(k));s=2
cb=S.Rational(s)/(S.Rational(5,2)**(s+1));Cs=S.Rational(s*(s+1),2)*S.Rational(4,3)**(s+2)
eps=min(S.Rational(1,2),1/(2*H),cb/(2*s),s*beta/(Cs*M));v=S.ones(k,1)+eps*h
arrival=[]
for n in [10,100,1000,10000]:
 # scaled u=sqrt(n)*t avoids underflow and proves no numerical tail shortcut.
 val,err=I.quad(lambda u: math.exp(n*(math.log1p(u/math.sqrt(n))-u/math.sqrt(n))),0,50,epsabs=1e-11)
 arrival.append({'M':n,'sqrt_M_times_mean':val,'asymptotic':math.sqrt(math.pi/2),'quad_error':err})
out={'Q':str(Q),'pi':str(pi),'beta':str(beta),'h_shifted':str(h),'epsilon_s2':str(eps),'v_s2':str(v),'claimed_drift_rate':str(S.Rational(s,5)*eps*beta),'first_arrival_checks':arrival,'scope':'Compiler algebra and exact-law numerical comparison; no distinguished-A closure or general recurrence.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
