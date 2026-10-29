"""Acquire a small nonlinear chart from divergence, then acquire its inverse.

No constructor/chart/inverse enters acquire_chart. Constant Jacobian is not
treated as proof of invertibility: BOTH global inverse compositions are checked.
"""
import json,time
from pathlib import Path
from fractions import Fraction as F
import sympy as sp
import numpy as np
from scipy.linalg import expm
import experiment as ex

def acquire_cyclic_one(raw_poly,rank_budget=3):
    q={}
    for i,f in enumerate(raw_poly):q=ex.add(q,ex.deriv(f,i),F(-1,len(raw_poly)+1))
    def T(p):
        out=ex.mul(q,p)
        for i,f in enumerate(raw_poly):out=ex.add(out,ex.mul(ex.deriv(p,i),f))
        return out
    basis=[{(0,0):F(1)}];pivots=[(0,0)];rows=[];idx=0
    while idx<len(basis):
        p=T(basis[idx]);row={}
        for j,(b,a) in enumerate(zip(basis,pivots)):
            c=p.get(a,F(0))
            if c:row[j]=c;p=ex.add(p,b,-c)
        if p:
            a=ex.pivot(p);c=p[a];row[len(basis)]=c
            basis.append({a:v/c for a,v in p.items()});pivots.append(a)
            if len(basis)>rank_budget:return dict(status='RANK_BUDGET_EXCEEDED',rank_lower_bound=len(basis))
        rows.append(row);idx+=1
    A=sp.Matrix([[sp.Rational(rows[i].get(j,F(0))) for j in range(len(basis))] for i in range(len(basis))])
    phi=sp.Matrix([ex.tosym(p) for p in basis])
    for i,b in enumerate(basis):
        residual=T(b)
        for j in range(len(basis)):residual=ex.add(residual,basis[j],-F(A[i,j]))
        assert not residual
    return dict(status='CLOSED',basis=phi,matrix=A,q=ex.tosym(q))

def truncate(expr,variables,degree):
    return sp.Add(*(c*sp.prod(v**a for v,a in zip(variables,powers)) for powers,c in sp.Poly(sp.expand(expr),variables).terms() if sum(powers)<=degree))

def acquire_polynomial_inverse(chart,variables,max_degree=16):
    """Adaptive formal inverse with exact global two-sided admission."""
    n=len(variables);zero={v:0 for v in variables};c=chart.subs(zero)
    J=chart.jacobian(variables).subs(zero)
    if J.det()==0:return dict(status='SINGULAR_BASEPOINT')
    normalized=sp.simplify(J.inv()*(chart-c))
    z=sp.Matrix(sp.symbols('z0:'+str(n)));zvars=tuple(z)
    history=[];D=1
    while D<=max_degree:
        G=z.copy()
        for _ in range(D-1):
            FG=normalized.subs(dict(zip(variables,G)),simultaneous=True)
            G=sp.Matrix([truncate(z[i]+G[i]-FG[i],zvars,D) for i in range(n)])
        left=normalized.subs(dict(zip(variables,G)),simultaneous=True)-z
        right=G.subs(dict(zip(zvars,normalized)),simultaneous=True)-sp.Matrix(variables)
        passed=all(sp.expand(p)==0 for p in list(left)+list(right))
        history.append(dict(degree_budget=D,two_sided_global_identities=passed))
        if passed:
            # Return inverse of original chart, not only of its normalization.
            Y=sp.Matrix(sp.symbols('Y0:'+str(n)))
            inverse=G.subs(dict(zip(zvars,J.inv()*(Y-c))),simultaneous=True).applyfunc(sp.expand)
            assert all(sp.expand(p)==0 for p in chart.subs(dict(zip(variables,inverse)),simultaneous=True)-Y)
            assert all(sp.expand(p)==0 for p in inverse.subs(dict(zip(Y,chart)),simultaneous=True)-sp.Matrix(variables))
            return dict(status='EXACT_POLYNOMIAL_INVERSE',inverse=inverse,target_variables=Y,history=history,degree=max(sp.Poly(p,tuple(Y)).total_degree() for p in inverse))
        if D==max_degree:break
        D=min(2*D,max_degree)
    return dict(status='INVERSE_NOT_ACQUIRED',history=history)

def acquire_chart(raw_poly,rank_budget=3,inverse_degree_budget=16):
    start=time.perf_counter();module=acquire_cyclic_one(raw_poly,rank_budget)
    if module['status']!='CLOSED':return module
    n=len(raw_poly)
    if len(module['basis'])!=n+1:return dict(status='CYCLIC_CHART_NOT_FULL_DIMENSION',dimension=len(module['basis']))
    chart=module['basis'][1:,:]
    inv=acquire_polynomial_inverse(chart,ex.VARS,inverse_degree_budget)
    if inv['status']!='EXACT_POLYNOMIAL_INVERSE':return inv
    return dict(status='ACQUIRED_EXACT_PROJECTIVE_CHART',basis=[str(p) for p in module['basis']],matrix=[[str(c) for c in row] for row in module['matrix'].tolist()],q=str(module['q']),jacobian_determinant=str(sp.factor(chart.jacobian(ex.VARS).det())),inverse=[str(p) for p in inv['inverse']],inverse_variables=[str(p) for p in inv['target_variables']],inverse_degree=inv['degree'],inverse_history=inv['history'],end_to_end_acquisition_seconds=time.perf_counter()-start,_module=module,_inverse=inv)

def main():
    u,v=sp.symbols('u v');h=sp.Matrix([u+v*v,v+(u+v*v)**2])
    hidden_inverse={u:ex.x-(ex.y-ex.x**2)**2,v:ex.y-ex.x**2}
    # The denominator row now sees both modes; its projective Krylov rank is 3.
    base=sp.Matrix([u-u*(u+v),7*v-v*(u+v)])
    raw=[sp.expand(p.subs(hidden_inverse,simultaneous=True)) for p in h.jacobian([u,v])*base]
    result=acquire_chart(list(map(ex.fromsym,raw)))
    assert result['status']=='ACQUIRED_EXACT_PROJECTIVE_CHART'
    phi=result['_module']['basis'];A=np.array(result['_module']['matrix']).astype(float)
    inv=result['_inverse'];inverse_func=sp.lambdify(tuple(inv['target_variables']),inv['inverse'],'numpy')
    checks=[]
    for u0,v0 in [(0.2,0.1),(.7,-.02),(-.05,.03)]:
        x0=u0+v0*v0;y0=v0+x0*x0
        b0=np.array(phi.subs({ex.x:x0,ex.y:y0}),dtype=float).ravel()
        for t in [0.,.03,.11,.2]:
            z=expm(t*A)@b0
            predicted=np.array(inverse_func(*(z[1:]/z[0])),dtype=float).ravel()
            den=1+u0*(np.exp(t)-1)+(v0/7)*(np.exp(7*t)-1)
            ut=u0*np.exp(t)/den;vt=v0*np.exp(7*t)/den
            truth=np.array([ut+vt*vt,vt+(ut+vt*vt)**2])
            err=float(np.max(np.abs(predicted-truth)));assert err<1e-10
            checks.append(dict(initial=[u0,v0],t=t,max_absolute_error=err))
    result={k:v for k,v in result.items() if not k.startswith('_')}
    result['raw_vector_field']=[str(p) for p in raw];result['checks']=checks
    Path(__file__).with_name('chart_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ['checks','raw_vector_field']},indent=2))
    print('max trajectory error:',max(c['max_absolute_error'] for c in checks))

if __name__=='__main__':main()
