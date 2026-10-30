"""Acquire a closed angular completion for a generic non-aligned exposed ray."""
from pathlib import Path
import sympy as S,numpy as np,cvxpy as cp,json,time,signal
signal.alarm(180);start=time.perf_counter();here=Path(__file__).parent;case=here/'general_ray';case.mkdir(exist_ok=True)
raw=json.loads((here/'general_angular_basis.json').read_text());ray=json.loads((here/'generic_nonpc_ray.json').read_text())
a,b,c,d=S.symbols('a b c d',real=True);A=(a,b,c,d);v=[S.Symbol(n,real=True) for n in raw['variables']]
kk=S.symbols('u l p n q r',real=True);loc={str(x):x for x in (*A,*v,*kk)}
C=S.Matrix([[S.sympify(x,locals=loc) for x in row] for row in raw['C']]).subs(dict(zip(kk,map(S.Rational,ray['K_coefficients']))))
A0=list(map(S.Rational,ray['A0']));eq=list(C.subs(dict(zip(A,A0)))[:,0])
M,rhs=S.linear_eq_to_matrix(eq,v);sol=next(iter(S.linsolve((M,rhs),v)));free=sorted(set().union(*(x.free_symbols for x in sol)),key=str)
print('exact acoustic jet rank',M.rank(),'free',len(free),time.perf_counter()-start,flush=True)
sub=dict(zip(v,sol));Cc=C.subs(sub,simultaneous=True).subs({a:1,c:0}).applyfunc(S.expand)
zero=dict.fromkeys(free,0);pieces=[Cc.subs(zero)]+[Cc.diff(x) for x in free]
funcs=[S.lambdify((b,d),x,'numpy',cse=True) for x in pieces]
bc,dc=map(S.Rational,ray['canonical_zero']);N=16
points=[(i/N,j/N) for i in range(-N,N+1) for j in range(-N,N+1) if i*i+j*j<=N*N]
# Resolve the near-conformal region containing the lifted predecessor zero.
points.extend((i/400,.9+j/400) for i in range(-20,21) for j in range(41)
              if (i/400)**2+(.9+j/400)**2<=1)
if (case/'obligation_points.json').exists():
    points.extend(tuple(float(S.Rational(x)) for x in row) for row in json.loads((case/'obligation_points.json').read_text()))
points.append((float(bc),float(dc)))
y=cp.Variable(len(free));margin=cp.Variable();constraints=[]
# The grid does not control the quadratic approach to an acoustic zero.
# Enforce the actual transverse lifted matrix at that zero as an affine LMI.
order=(5,0,1,2,3,4);kc=S.Matrix([1,0,0,S.Rational(ray['parameters'][1]),0,0])
QQ=S.eye(6);QQ[:,0]=kc;CP=(QQ.T*Cc.extract(order,order)*QQ).applyfunc(S.expand)
at={b:bc,d:dc};J0=S.zeros(7)
J0[0,0]=S.diff(CP[0,0],b,2).subs(at)/2
J0[0,1]=J0[1,0]=S.diff(CP[0,0],b,d).subs(at)/2
J0[1,1]=S.diff(CP[0,0],d,2).subs(at)/2
for j in range(1,6):
    J0[0,j+1]=J0[j+1,0]=S.diff(CP[0,j],b).subs(at)
    J0[1,j+1]=J0[j+1,1]=S.diff(CP[0,j],d).subs(at)
    for i in range(1,6):J0[i+1,j+1]=CP[i,j].subs(at)
jet_mats=[np.array(J0.subs(zero),float)]+[np.array(J0.diff(x),float) for x in free]
Jtarget=cp.Constant(jet_mats[0])
for i in range(len(free)):Jtarget+=y[i]*jet_mats[i+1]
constraints.append(Jtarget/(1+float(bc)**2+float(dc)**2)**3-margin*np.eye(7)>>0)
for index,(bb,dd) in enumerate(points):
    T=1+bb*bb+dd*dd;mm=[np.array(f(bb,dd),float)/T**3 for f in funcs]
    target=cp.Constant(mm[0])
    for i in range(len(free)):target+=y[i]*mm[i+1]
    if index==len(points)-1:
        gram=sum(x.T@x for x in mm);vals,vec=np.linalg.eigh(gram);Q=vec[:,vals>1e-7]
        constraints.append(Q.T@target@Q>>0);continue
    weight=(bb-float(bc))**2+(dd-float(dc))**2
    constraints.append(target-margin*weight*np.eye(6)>>0)
if (case/'reference.json').exists():
    ref=json.loads((case/'reference.json').read_text())['parameters'];aff=[]
    for expression in sol:
        value=float(expression.subs(zero))
        for i,x in enumerate(free):value+=float(S.diff(expression,x))*y[i]
        aff.append(value)
    constraints.append(margin>=1e-5)
    objective=cp.Minimize(cp.sum_squares(cp.hstack(aff)-np.array([ref[str(x)] for x in v])))
else:objective=cp.Maximize(margin)
model=cp.Problem(objective,constraints);err=None
try:model.solve(solver='CLARABEL',tol_gap_abs=1e-11,tol_gap_rel=1e-11,tol_feas=1e-11,max_iter=260)
except Exception as e:err=repr(e)
out={'status':model.status,'error':err,'margin':None if margin.value is None else float(margin.value),
     'free':list(map(str,free)),'parameters':None if y.value is None else y.value.tolist(),'seconds':time.perf_counter()-start,
     'scope':'Finite proposal; exact whole-gradient validation still required.'}
(case/'proposal.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if y.value is None:raise ValueError('No numerical proposal')
fixed={x:S.Rational(round(float(val)*10**12),10**12) for x,val in zip(free,y.value)}
coef={x:S.factor(xx.subs(fixed)) for x,xx in zip(v,sol)}
P=[S.expand(S.sympify(x,locals=loc).subs(coef)) for x in raw['P']]
CC=C.subs(coef).subs({a:1,c:0}).applyfunc(S.expand)
order=(5,0,1,2,3,4);Cperm=CC.extract(order,order);kernel=S.Matrix([1,0,0,S.Rational(ray['parameters'][1]),0,0])
Q=S.eye(6);Q[:,0]=kernel;Cp=(Q.T*Cperm*Q).applyfunc(S.expand)
w=b-bc;g=d-dc
q1,rem0=S.div(Cp[0,0],w,b);q2,rem1=S.div(q1,w,b)
cc,rz=S.div(rem0,g*g,d);assert rz==0
bb,rz=S.div(rem1,g,d);assert rz==0
Lift=S.zeros(7);Lift[0,0]=q2;Lift[0,1]=Lift[1,0]=bb/2;Lift[1,1]=cc
for j in range(1,6):
    pp,rr=S.div(Cp[0,j],w,b);qq,rz=S.div(rr,g,d);assert rz==0
    Lift[0,j+1]=Lift[j+1,0]=pp;Lift[1,j+1]=Lift[j+1,1]=qq
for i in range(1,6):
    for j in range(1,6):Lift[i+1,j+1]=Cp[i,j]
DD=S.zeros(7,6);DD[0,0]=w;DD[1,0]=g
for i in range(1,6):DD[i+1,i]=1
assert all(S.expand(x)==0 for x in DD.T*Lift*DD-Cp)
def pack(poly,variables):return [[*pw,int(co.p),int(co.q)] for pw,co in S.Poly(poly,*variables).terms()]
def pm(mat):return [[pack(x,(b,d)) for x in row] for row in mat.tolist()]
data={'primitive':[pack(x,A) for x in P],'C':pm(CC),'C_permuted':pm(Cperm),'M':pm(Lift),
      'permutation':list(order),'kernel':[pack(x,(b,d)) for x in kernel],'w':pack(w,(b,d)),'g':pack(g,(b,d)),
      'ray':ray,'profile_coefficients':{str(x):str(z) for x,z in coef.items()},'seconds':time.perf_counter()-start}
(case/'candidate.json').write_text(json.dumps(data))
print('rational candidate and exact local identity acquired',data['seconds'],flush=True)
