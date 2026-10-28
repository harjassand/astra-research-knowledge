"""Known-QC contact models at A=I; numeric suggestions require exact proof."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
from itertools import product,combinations_with_replacement as cw
import time,json
import numpy as np
import sympy as s
import scipy.sparse as sp
import cvxpy as cp
OUT=Path(__file__).resolve().parent
x=s.symbols('a b c d');X=s.Matrix(2,2,x);A=s.eye(2)
T=sum(z*z for z in X);q=X.det();xx=x[0]**2+x[2]**2-x[1]**2-x[3]**2
rows=sorted(e for e in product(range(5),repeat=4) if 2<=sum(e)<=4)
features=sorted(e for e in product(range(3),repeat=4) if 1<=sum(e)<=2)
assert len(rows)==65 and len(features)==14
index={e:i for i,e in enumerate(rows)}
def breg(poly):
    shifted=s.Poly(s.expand(poly.subs(dict(zip(x,list(X+A))),simultaneous=True)),*x)
    return np.array([float(shifted.coeff_monomial(e)) for e in rows])
pairs=list(cw(range(14),2));rr=[];cc=[];vv=[];sr=[];sc=[];sv=[]
for k,(i,j) in enumerate(pairs):
    rr.append(index[tuple(a+b for a,b in zip(features[i],features[j]))]);cc.append(k);vv.append(1 if i==j else 2)
    sr.append(14*i+j);sc.append(k);sv.append(1)
    if i!=j:sr.append(14*j+i);sc.append(k);sv.append(1)
G=sp.csr_matrix((vv,(rr,cc)),shape=(65,105));S=sp.csr_matrix((sv,(sr,sc)),shape=(196,105))
rot=[s.eye(2),s.Matrix([[0,-1],[1,0]]),s.Matrix([[s.Rational(3,5),s.Rational(-4,5)],[s.Rational(4,5),s.Rational(3,5)]])]
columns=[];metadata=[];seen=set();start=time.monotonic()
for p,n,angle,sign,shift in product([s.Rational(1,2),1,2],[s.Rational(1,2),1,2],range(3),[-1,1],[0,1,-1,2]):
    P=s.diag(p,1)*rot[angle];N=s.diag(n,1)
    B=P*(X-shift*A)*N;tt=sum(z*z for z in B);qq=B.det()
    energy=s.Poly(s.expand(tt*tt+sign*s.Rational(9,4)*tt*qq),*x)
    norm=sum(abs(c) for e,c in energy.terms() if sum(e)==4)
    poly=s.expand(energy.as_expr()/norm);v=breg(poly);key=tuple(v)
    if key in seen:continue
    seen.add(key);columns.append(v);metadata.append({'p':str(p),'n':str(n),'angle_index':angle,'sign':sign,'shift':shift,'normalization':str(norm)})
D=np.stack(columns,axis=1)
(OUT/'DICTIONARY.json').write_text(json.dumps({'models':metadata,'base':'I','features':features,'rows':rows},indent=2)+'\n')
np.savez(OUT/'COMPILED.npz',D=D,G=G.toarray(),S=S.toarray())
print('compiled',len(columns),'models',time.monotonic()-start,flush=True)
m=s.Integer(197);beta=(m*m-1)/(m*m+1)
target=T*T+12*q*q+4*beta*q*xx
control=s.Rational(101,100)*T*T-s.Rational(9,4)*q*T
qv=np.array([float(s.Poly(q,*x).coeff_monomial(e)) for e in rows])
report=[]
for label,poly,use in [('PC_target',target,False),('QC_control',control,True),('target_contacts',target,True)]:
    gr=cp.Variable(105);k=cp.Variable();rho=cp.Variable();R=cp.reshape(S@gr,(14,14),order='C')
    constraints=[R-rho*np.eye(14)>>0,rho<=1];lhs=G@gr+k*qv
    weights=cp.Variable(len(columns),nonneg=True) if use else None
    if use:lhs=lhs+D@weights;constraints.append(cp.sum(weights)<=10000)
    eq=lhs==breg(poly);constraints.append(eq)
    problem=cp.Problem(cp.Maximize(rho-(1e-10*cp.sum(weights) if use else 0)),constraints)
    now=time.monotonic();problem.solve(solver='CLARABEL',max_iter=180,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
    out={'label':label,'scope':'NUMERICAL_FIXED_BACKGROUND_CONTACT_ONLY','status':problem.status,'seconds':time.monotonic()-now,'margin':None if rho.value is None else float(rho.value)}
    if gr.value is not None:
        out.update(equality_error=float(np.max(np.abs(eq.violation()))),selector=float(k.value),weight_sum=0 if weights is None else float(sum(weights.value)))
        np.savez(OUT/(label+'.npz'),gram=R.value,k=k.value,rho=rho.value,weights=np.zeros(0) if weights is None else weights.value,dual=eq.dual_value)
    report.append(out);print(json.dumps(out),flush=True)
    (OUT/'ACQUISITION.json').write_text(json.dumps(report,indent=2)+'\n')
