"""Tiny exploratory SDP. Its floating output is NOT an exact witness."""
from pathlib import Path
import itertools, json, time, sys
import numpy as np
import cvxpy as cp

ROOT=Path(__file__).resolve().parent
n=4
def mons(d):
    return [a for k in range(d+1) for a in itertools.product(range(k+1),repeat=n) if sum(a)==k]
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def exp(i,p=1): return tuple(p if j==i else 0 for j in range(n))
zero=(0,)*n
M=mons(4); idx={a:k for k,a in enumerate(M)}; basis=mons(2); lin=mons(1)
ys=cp.Variable(len(M))
def L(a): return ys[idx[a]]
def moment(bs,terms={zero:1}):
    return cp.bmat([[sum(c*L(add(add(a,b),t)) for t,c in terms.items()) for b in bs] for a in bs])
cons=[L(zero)==1,moment(basis)>>0]
for a in M:
    if sum(a)%2: cons.append(L(a)==0)
    sw=(a[1],a[0],a[3],a[2])
    cons.append(L(a)==L(sw))
for a in basis:
    cons += [L(add(a,add(exp(0),exp(2))))==L(a),L(add(a,add(exp(1),exp(3))))==L(a)]
b=float(sys.argv[1]) if len(sys.argv)>1 else 4.0
for i in (0,1):
    cons += [moment(lin,{exp(i,2):1,zero:-1})>>0,moment(lin,{exp(i,2):-1,zero:b})>>0]
for i in (2,3):
    cons += [moment(lin,{exp(i,2):1,zero:-1/64})>>0,moment(lin,{exp(i,2):-1,zero:64})>>0]
obj=L(exp(0,2))+L(exp(1,2))-2*L(add(exp(0),exp(1)))-L(exp(2,2))-L(exp(3,2))+2*L(add(exp(2),exp(3)))
problem=cp.Problem(cp.Minimize(obj),cons)
start=time.monotonic()
problem.solve(solver='CLARABEL',max_iter=150,time_limit=45,tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9)
result={'status':problem.status,'objective':problem.value,'wall_seconds':time.monotonic()-start,'b':b,'variables':['x','y','u','v'],'monomials':M,'moments':ys.value.tolist() if ys.value is not None else None,'solver':problem.solver_stats.solver_name,'solver_seconds':problem.solver_stats.solve_time}
if ys.value is not None:
    result['minimum_moment_eigenvalue']=float(np.linalg.eigvalsh(moment(basis).value)[0])
    result['max_constraint_violation']=float(max(float(np.max(c.violation())) for c in cons))
target=ROOT/f'search_b{str(b).replace(".","p")}.json'
target.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('moments','monomials')},indent=2))
