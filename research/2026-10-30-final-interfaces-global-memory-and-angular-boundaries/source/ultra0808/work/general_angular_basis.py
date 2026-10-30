"""Closed P5/T forms for the whole even Hopf sector, without extra reflections."""
from pathlib import Path
import sympy as S,json,time,signal
signal.alarm(180);start=time.perf_counter();here=Path(__file__).parent
A=S.symbols('a b c d',real=True);h=S.symbols('h0:6',real=True)
def degrees(total,n):
    if n==1:yield(total,)
    else:
        for j in range(total+1):
            for p in degrees(total-j,n-1):yield(j,)+p
perm=(3,2,1,0);sign=(1,-1,1,-1);keys=[(i,p) for i in range(4) for p in degrees(5,4)]
seen=set();basis=[]
for key in keys:
    if key in seen:continue
    i,p=key;ee=[0]*4
    for j in range(4):ee[perm[j]]=p[j]
    other=(perm[i],tuple(ee));coef=sign[i]*S.prod(sign[j]**p[j] for j in range(4))
    seen.update((key,other));vec=S.zeros(4,1)
    vec[i]+=S.prod(A[j]**p[j] for j in range(4));k,q=other
    vec[k]+=coef*S.prod(A[j]**q[j] for j in range(4))
    if vec!=S.zeros(4,1):basis.append(vec)
z=S.symbols('z:'+str(len(basis)));P=sum((c*x for c,x in zip(z,basis)),S.zeros(4,1))
J=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
lie=P.jacobian(A)*J*S.Matrix(A)+J.T*P
eq=[v for ex in lie for v in S.Poly(S.expand(ex),A).coeffs()]
MM,_=S.linear_eq_to_matrix(eq,z);N=S.Matrix.hstack(*MM.nullspace());v=S.symbols('v:'+str(N.cols),real=True)
P=P.subs(dict(zip(z,N*S.Matrix(v)))).applyfunc(S.expand)
print('spin-flip basis',len(basis),'rotation dimension',len(v),time.perf_counter()-start,flush=True)
T=sum(x*x for x in A);jac=P.jacobian(A);W=S.zeros(4)
for i in range(4):
    for j in range(i+1,4):
        W[i,j]=S.expand(T*(jac[j,i]-jac[i,j])-2*(A[i]*P[j]-A[j]*P[i]));W[j,i]=-W[i,j]
rows=[]
for i in range(4):
    for j in range(i+1,4):
        for val in S.Poly(W[i,j],A).coeffs():rows.append([S.diff(val,x) for x in v])
piv=S.Matrix(rows).rref()[1];gauge={v[j]:0 for j in range(len(v)) if j not in piv}
P=P.subs(gauge);W=W.subs(gauge);v=[x for x in v if x not in gauge]
u,l,p,n,q,r=S.symbols('u l p n q r',real=True);a,b,c,d=A
X=a*a+c*c-b*b-d*d;Y=2*(a*b+c*d);Z=2*(a*d-b*c)
F=u*X*X+2*l*X*Y+2*p*X*Z+n*Y*Y+2*q*Y*Z+r*Z*Z
H=S.hessian(F,A);B1=S.Matrix([h[0],h[1],h[3],h[4]]);B2=S.Matrix([h[1],h[2],h[4],h[5]])
C=S.hessian(S.expand(T*T*(B1.T*H*B1+B2.T*H*B2)[0]+(B1.T*W*B2)[0]),h)/2
out={'variables':list(map(str,v)),'P':list(map(str,P)),
     'C':[[str(S.expand(x)) for x in row] for row in C.tolist()],
     'symmetry':'left SO2 invariant, Gamma(A)=(d,-c,b,-a) positive pullback; no CAC or column-swap symmetry imposed',
     'gauges_removed':len(gauge),'seconds':time.perf_counter()-start}
(here/'general_angular_basis.json').write_text(json.dumps(out))
print('effective density parameters',len(v),'gauges',len(gauge),'seconds',out['seconds'],flush=True)
