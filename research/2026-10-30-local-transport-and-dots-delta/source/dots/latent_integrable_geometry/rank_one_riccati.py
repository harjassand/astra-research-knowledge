"""Acquire rank-one matrix-Riccati geometry from scalar quadratic equations.

Only raw coefficient equations enter acquire. No matrix basis, measurement
direction, matrix size, Jordan unit, Lax pair, or decoder is supplied.
"""
from pathlib import Path
import json,time,hashlib
import sympy as s
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp


def pairs(m):return [(i,j) for i in range(m) for j in range(i,m)]
def sym(v,m):
    X=s.zeros(m)
    for a,(i,j) in zip(v,pairs(m)):X[i,j]=X[j,i]=a
    return X
def vec(X):return s.Matrix([X[i,j] for i,j in pairs(X.rows)])
def solve_unique(expressions,unknowns):
    M,b=s.linear_eq_to_matrix(expressions,unknowns)
    try:solution,params=M.gauss_jordan_solve(b)
    except ValueError:return None
    if params.rows:return None
    return solution


def acquire(raw,x):
    start=time.perf_counter();raw=s.Matrix(raw);d=len(x)
    m=next((k for k in range(1,d+1) if k*(k+1)//2==d),None)
    if m is None:return {'status':'NOT_SYMMETRIC_MATRIX_DIMENSION'}
    polys=[s.Poly(v,*x) for v in raw]
    if max(p.total_degree() for p in polys)>2:return {'status':'NOT_QUADRATIC'}
    f2=s.Matrix([sum((c*s.prod(v**a for v,a in zip(x,mon)) for mon,c in p.terms() if sum(mon)==2),s.Integer(0)) for p in polys])
    Hessians=[s.hessian(-v,x) for v in f2]
    stacked=s.Matrix.vstack(*Hessians);rows=stacked.rowspace();r=len(rows)
    if r!=m:return {'status':'ESSENTIAL_QUADRATIC_DIMENSION_MISMATCH','matrix_size':m,'essential_dimension':r}
    B=s.Matrix.vstack(*rows)
    # Rational right inverse, no spectral/idempotent or polynomial system solve.
    pivotcols=B.rref()[1];E=s.zeros(d,m)
    for i,j in enumerate(pivotcols):E[j,i]=1
    right=E*(B*E).inv();assert B*right==s.eye(m)
    w=s.symbols('w0:'+str(m));restricted=(-f2).subs(dict(zip(x,right*s.Matrix(w))),simultaneous=True)
    K=s.Matrix([[s.Poly(v,*w).coeff_monomial(w[i]*w[j]) for i,j in pairs(m)] for v in restricted])
    if K.det()==0:return {'status':'QUADRATIC_IMAGE_NOT_FULL_SYMMETRIC_SQUARE'}
    # Do not rely only on the annihilator computation: global factor identity.
    assert all(s.expand(v)==0 for v in -f2-K*vec((B*s.Matrix(x))*(B*s.Matrix(x)).T))
    z=s.symbols('z0:'+str(d));Z=sym(z,m);rho=s.symbols('r0:'+str(m))
    residual=B*K*s.Matrix(z)-Z*s.Matrix(rho)
    equations=[s.Poly(v,*z).coeff_monomial(zj) for v in residual for zj in z]
    rv=solve_unique(equations,rho)
    if rv is None:return {'status':'NOT_MATRIX_VECTOR_CONTRACTION'}
    zero=dict.fromkeys(x,0);constant=raw.subs(zero);L=raw.jacobian(x).subs(zero)
    Lhat=K.inv()*L*K;av=s.symbols('a0:'+str(m*m));A=s.Matrix(m,m,av)
    residual=sym(Lhat*s.Matrix(z),m)-A*Z-Z*A.T
    equations=[s.Poly(v,*z).coeff_monomial(zj) for v in residual for zj in z]
    solution=solve_unique(equations,av)
    if solution is None:return {'status':'LINEAR_PART_NOT_LYAPUNOV'}
    A=s.Matrix(m,m,solution);Q=sym(K.inv()*constant,m);R=rv*rv.T
    X=sym(K.inv()*s.Matrix(x),m)
    transformed=sym(K.inv()*raw,m)
    target=A*X+X*A.T+Q-X*R*X
    checks=[s.expand(v)==0 for v in transformed-target];assert all(checks)
    H=(-A.T).row_join(R).col_join(Q.row_join(A))
    return {'status':'ACQUIRED_RANK_ONE_MATRIX_RICCATI','raw_dimension':d,'matrix_size':m,
      'essential_dimension':r,'annihilator_dimension':d-r,'quotient':B,'chart_inverse_matrix':K,
      'matrix_chart':X,'A':A,'Q':Q,'R':R,'measurement_vector':rv,'block_generator':H,
      'global_matrix_component_identities':checks,'acquisition_seconds':time.perf_counter()-start}


def serialize(v):
    if isinstance(v,s.MatrixBase):return [[str(a) for a in row] for row in v.tolist()]
    if isinstance(v,dict):return {k:serialize(a) for k,a in v.items()}
    if isinstance(v,(list,tuple)):return [serialize(a) for a in v]
    return v


def evaluate(result,x0,t):
    K=np.array(result['chart_inverse_matrix'],dtype=float);m=result['matrix_size']
    X0=np.array(sym(s.Matrix(np.linalg.solve(K,np.array(x0,float))),m),float)
    frame=expm(t*np.array(result['block_generator'],float))@np.vstack([np.eye(m),X0])
    U,V=frame[:m],frame[m:];X=np.linalg.solve(U.T,V.T).T
    return K@np.array([X[i,j] for i,j in pairs(m)]),float(np.linalg.cond(U))


def main():
    # Published Berry-Harlim continuous-observation model Eq.2.1, using parameter
    # values also used in Fig.1. epsilon=1/10 is our explicit chosen member.
    # Eq.2.2 is the steady-state ALGEBRAIC Riccati equation; our transient ODE
    # follows standard Kalman-Bucy theory. Fig.1's discrete-observation experiment
    # is NOT reproduced here.
    # A=[[-1,1],[-10,-10]], noise Q=diag(2,20), H=(1,0), obs variance=1/2.
    # The acquisition function below receives only these scalar equations.
    p,q,r=s.symbols('p q r');x=(p,q,r)
    raw=s.Matrix([-2*p+2*q+2-2*p*p, r-10*p-11*q-2*p*q,-20*q-20*r+20-2*q*q])
    got=acquire(raw,x);assert got['status']=='ACQUIRED_RANK_ONE_MATRIX_RICCATI'
    rhs=s.lambdify(x,raw,'numpy');initial=[1,0,1]
    numerical=[]
    for t in [.01,.1,.5,1,2,4]:
        prediction,condition=evaluate(got,initial,t)
        reference=solve_ivp(lambda t,a:np.asarray(rhs(*a),float).ravel(),(0,t),initial,
                            rtol=2e-12,atol=2e-13,method='DOP853')
        error=float(np.max(abs(prediction-reference.y[:,-1])))
        numerical.append({'t':t,'max_error_against_high_accuracy_time_stepping':error,'frame_U_condition':condition,
                          'nfev_reference':reference.nfev})
        if t<=1:assert error<1e-8
    # Coordinate-invariance stress test, not a second manufactured scientific model.
    T=s.Matrix([[1,2,1],[0,1,-1],[1,0,1]]);assert T.det()!=0
    u=s.symbols('u0:3');mixed=(T*raw).subs(dict(zip(x,T.inv()*s.Matrix(u))),simultaneous=True).applyfunc(s.expand)
    hidden=acquire(mixed,u);assert hidden['status']=='ACQUIRED_RANK_ONE_MATRIX_RICCATI'
    mixchecks=[]
    for t in [.03,.3,.7]:
        a,condition=evaluate(hidden,np.array(T,float)@initial,t);b,_=evaluate(got,initial,t)
        err=float(np.max(abs(a-np.array(T,float)@b)));assert err<1e-8;mixchecks.append(err)
    controls={}
    controls['quadratic_noncontraction']=acquire([-p*p-q*q,-p*q,-q*q],x)
    controls['bad_linear_part']=acquire(list(raw+s.Matrix([r,0,0])),x)
    controls['rank_two_measurement']=acquire([-p*p-q*q,-p*q-q*r,-q*q-r*r],x)
    assert controls['quadratic_noncontraction']['status']=='NOT_MATRIX_VECTOR_CONTRACTION'
    assert controls['bad_linear_part']['status']=='LINEAR_PART_NOT_LYAPUNOV'
    assert controls['rank_two_measurement']['status']=='ESSENTIAL_QUADRATIC_DIMENSION_MISMATCH'
    # No unit exists in the quadratic homotope: direct attempted linear solve.
    unit=s.symbols('e0:3');H2=s.Matrix([2*p*p,2*p*q,2*q*q]);bilinear=H2.jacobian(x)*s.Matrix(unit)/2
    unit_eq=[s.Poly(v,*x).coeff_monomial(xj) for v in bilinear-s.Matrix(x) for xj in x]
    assert solve_unique(unit_eq,unit) is None
    out={'anchor_source':'https://pmc.ncbi.nlm.nih.gov/articles/PMC4032560/',
         'anchor_scope':'Transient continuous-observation Kalman-Bucy covariance derived from published Eq2.1, epsilon=1/10. Eq2.2 is steady-state only. Not a reproduction of Fig1 discrete-observation experiment or nonlinear Lorenz-96 examples.',
         'raw_equations':[str(v) for v in raw],'variables':list(map(str,x)),'acquired':serialize(got),
         'quadratic_algebra_has_no_unit':True,'numerical_checks':numerical,
         'mixed_coordinate_stress':{'raw_equations':[str(v) for v in mixed],'acquired':serialize(hidden),'trajectory_agreement':mixchecks},
         'controls':serialize(controls),'comparison':'Conventional Kalman/Riccati solvers already know the physical matrix model; no speed advantage claimed.',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name('rank_one_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
