"""Independent classical Bernstein-Peirce acquisition and receipt replay.

No imports from producer; receives only raw scalar quadratic equations. This
implements an elementary specialization of classical Bernstein idempotent and
Peirce constructions, not a claim that this exact program appeared historically.
"""
from pathlib import Path
import json, hashlib, time
import sympy as s
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]

def pairs(m): return [(i,j) for i in range(m) for j in range(i,m)]
def sym(v,m):
    X=s.zeros(m)
    for c,(i,j) in zip(v,pairs(m)): X[i,j]=X[j,i]=c
    return X
def vec(X): return s.Matrix([X[i,j] for i,j in pairs(X.rows)])
def zero(v): return all(s.expand(a)==0 for a in v)
def acquire(raw,x):
    start=time.perf_counter();d=len(x)
    m=next((m for m in range(1,d+1) if m*(m+1)//2==d),None)
    if m is None: return {'status':'dimension_reject'}
    raw=s.Matrix(raw);q=s.Matrix([-sum(c*s.prod(v**a for v,a in zip(x,mon))
        for mon,c in s.Poly(f,*x).terms() if sum(mon)==2) for f in raw])
    L=q.jacobian(x)/2
    omega=s.expand(2*s.trace(L)/(m+1))
    ow=s.Matrix([[omega.diff(v) for v in x]])
    if not any(ow): return {'status':'weight_reject'}
    a=s.eye(d)[:,next(i for i in range(d) if ow[i])]
    def prod(u,v): return L.subs(dict(zip(x,u)),simultaneous=True)*v
    e=prod(a,a)/(ow*a)[0]**2
    if not zero(prod(e,e)-e): return {'status':'idempotent_reject'}
    Le=L.subs(dict(zip(x,e)),simultaneous=True)
    U=(Le-s.eye(d)/2).nullspace()
    if len(U)!=m-1: return {'status':'peirce_dimension_reject'}
    columns=[]
    for i,j in pairs(m):
        columns.append(e if j==0 else U[j-1] if i==0 else
                       prod(U[i-1],U[j-1])*(1 if i==j else 2))
    K=s.Matrix.hstack(*columns)
    if K.det()==0: return {'status':'peirce_products_reject'}
    z=s.symbols('z:'+str(d));X=sym(z,m);r=s.eye(m)[:,0]
    quadratic=K.inv()*q.subs(dict(zip(x,K*s.Matrix(z))),simultaneous=True)
    if not zero(quadratic-vec(X*r*r.T*X)): return {'status':'quadratic_identity_reject'}
    at=s.symbols('a:'+str(m*m));A=s.Matrix(m,m,at)
    c=raw.subs(dict.fromkeys(x,0));drift=raw.jacobian(x).subs(dict.fromkeys(x,0))
    residual=sym(K.inv()*drift*K*s.Matrix(z),m)-A*X-X*A.T
    eq=[s.Poly(v,*z).coeff_monomial(zj) for v in residual for zj in z]
    lhs,rhs=s.linear_eq_to_matrix(eq,at)
    try: av,params=lhs.gauss_jordan_solve(rhs)
    except ValueError: return {'status':'drift_reject'}
    assert not params.rows
    A=s.Matrix(m,m,av);Q=sym(K.inv()*c,m)
    assert zero(s.Matrix(q)-K*vec(sym(K.inv()*s.Matrix(x),m)*r*r.T*sym(K.inv()*s.Matrix(x),m)))
    assert zero(s.Matrix(raw)-K*vec(A*sym(K.inv()*s.Matrix(x),m)+sym(K.inv()*s.Matrix(x),m)*A.T+Q-sym(K.inv()*s.Matrix(x),m)*r*r.T*sym(K.inv()*s.Matrix(x),m)))
    return {'status':'acquired','m':m,'weight':str(omega),'peirce_U_dimension':len(U),
            'peirce_Z_dimension':len(Le.nullspace()),'K':str(K),'A':str(A),'Q':str(Q),
            'global_identities':True,'seconds':time.perf_counter()-start}

def replay_record(raw,x,record):
    M=lambda k:s.Matrix([[s.sympify(v) for v in row] for row in record[k]])
    K,A,Q,R,B,r,H=map(M,['chart_inverse_matrix','A','Q','R','quotient','measurement_vector','block_generator'])
    m=A.rows;X=sym(K.inv()*s.Matrix(x),m)
    assert zero(s.Matrix(raw)-K*vec(A*X+X*A.T+Q-X*R*X))
    z=s.symbols('z:'+str(len(x)));Z=sym(z,m)
    assert zero(B*K*s.Matrix(z)-Z*r)
    assert H==(-A.T).row_join(R).col_join(Q.row_join(A))
    assert R==r*r.T
    return {'exact_global_identity_components':m*m,'K_invertible':K.det()!=0,'contraction':True,'block_sign':True}

def decode_and_check(raw,x,acquired,x0):
    # Same conventional Hamiltonian block flow, using only this comparator's
    # independently acquired chart and coefficients.
    K,A,Q=[np.array(s.sympify(acquired[k]),float) for k in ['K','A','Q']]
    m=acquired['m'];R=np.zeros((m,m));R[0,0]=1
    H=np.block([[-A.T,R],[Q,A]])
    X0=np.array(sym(s.Matrix(np.linalg.solve(K,x0)),m),float)
    rhs=s.lambdify(x,raw,'numpy');checks=[]
    for t in [.03,.3,.7]:
        frame=expm(t*H)@np.vstack([np.eye(m),X0]);U,V=frame[:m],frame[m:]
        X=np.linalg.solve(U.T,V.T).T
        predicted=K@np.array([X[i,j] for i,j in pairs(m)])
        ref=solve_ivp(lambda _,v:np.array(rhs(*v),float).ravel(),(0,t),x0,
                      rtol=2e-12,atol=2e-13,method='DOP853')
        error=float(np.max(np.abs(predicted-ref.y[:,-1])))
        assert ref.success and error<1e-8
        checks.append({'t':t,'max_error_against_DOP853':error,'frame_U_condition':float(np.linalg.cond(U))})
    return checks

def main():
    receipt_path=ROOT/'rank_one_results.json';receipt=json.loads(receipt_path.read_text())
    p,q,r=s.symbols('p q r');x=(p,q,r)
    raw=s.Matrix([s.sympify(v,locals=dict(zip(receipt['variables'],x))) for v in receipt['raw_equations']])
    out={'producer_sha256':hashlib.sha256((ROOT/'rank_one_riccati.py').read_bytes()).hexdigest(),
         'receipt_sha256':hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
         'raw_anchor':acquire(raw,x),'receipt_replay':replay_record(raw,x,receipt['acquired'])}
    mixed=receipt['mixed_coordinate_stress'];u=s.symbols('u0:3')
    f=s.Matrix([s.sympify(v,locals=dict(zip(map(str,u),u))) for v in mixed['raw_equations']])
    out['mixed_anchor']=acquire(f,u);out['mixed_replay']=replay_record(f,u,mixed['acquired'])
    out['raw_decoded_checks']=decode_and_check(raw,x,out['raw_anchor'],np.array([1.,0.,1.]))
    out['mixed_decoded_checks']=decode_and_check(f,u,out['mixed_anchor'],np.array([2.,-1.,2.]))
    out['controls']={'noncontraction':acquire([-p*p-q*q,-p*q,-q*q],x),
                     'bad_drift':acquire(raw+s.Matrix([r,0,0]),x),
                     'rank_two':acquire([-p*p-q*q,-p*q-q*r,-q*q-r*r],x)}
    # A larger exact generic rank-one input is a comparator completeness test,
    # not a second scientific anchor. Hidden chart is used only by constructor.
    m=3;d=6;v=s.symbols('v:6');X=sym(v,m);rr=s.Matrix([2,-1,3]);A=s.Matrix([[1,2,0],[-1,0,1],[0,-2,-1]])
    base=vec(A*X+X*A.T+s.diag(1,2,3)-X*rr*rr.T*X)
    T=s.eye(d)
    for i in range(d-1):T[i,i+1]=i+1
    T[-1,0]=1
    assert T.det()!=0
    y=s.symbols('y:6');f=(T*base).subs(dict(zip(v,T.inv()*s.Matrix(y))),simultaneous=True)
    out['generic_m3_stress']=acquire(f,y)
    assert all(out[k]['status']=='acquired' for k in ['raw_anchor','mixed_anchor','generic_m3_stress'])
    assert all(v['status']!='acquired' for v in out['controls'].values())
    target=Path(__file__).with_suffix('.json');target.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
