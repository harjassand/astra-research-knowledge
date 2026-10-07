"""Independent exact rational transcription checks of the stopped generator.

All-N proof is in revisions/S02_STOPPED_DIFFUSION_AUDIT.txt. Fixtures alone
do not establish that theorem or novelty. No quantum hardware is used.
"""
import json
import time
from pathlib import Path
import sympy as sp

def tensor(factors):
    answer=sp.ones(1,1)
    for f in factors:
        answer=sp.kronecker_product(answer,f)
    return answer

def fixture(N):
    I=sp.eye(2)
    sig=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    m=sp.Matrix([sp.Rational(1,20),-sp.Rational(1,30),sp.Rational(1,25)])
    C=sp.Matrix([[sp.Rational(3,2),sp.Rational(1,8),0],
                 [sp.Rational(1,8),sp.Rational(5,4),sp.Rational(1,16)],
                 [0,sp.Rational(1,16),sp.Rational(7,4)]])
    b=sp.Matrix([sp.Rational(1,9),-sp.Rational(1,11),sp.Rational(1,13)])
    tau=(I+sum((m[i]*sig[i] for i in range(3)),sp.zeros(2)))/2
    k=tensor([tau]*N)
    grad=[]
    Hess=[]
    for i in range(3):
        grad.append(sum((tensor([sig[i]/2 if j==a else tau for j in range(N)]) for a in range(N)),sp.zeros(2**N)))
        Hess.append([])
        for h in range(3):
            Hess[i].append(sum((tensor([sig[i]/2 if j==a else sig[h]/2 if j==c else tau for j in range(N)])
                                   for a in range(N) for c in range(N) if a!=c),sp.zeros(2**N)))
    Js=[]
    for i in range(3):
        Js.append(sum((tensor([sig[i]/2 if j==a else I for j in range(N)]) for a in range(N)),sp.zeros(2**N)))
    H=sum((C[i,j]*(Js[i]*Js[j]+Js[j]*Js[i])/2 for i in range(3) for j in range(3)),sp.zeros(2**N))
    H+=sum((b[i]*Js[i] for i in range(3)),sp.zeros(2**N))
    Vmat=sp.eye(3)-m*m.T
    cross=sp.Matrix([[0,-m[2],m[1]],[m[2],0,-m[0]],[-m[1],m[0],0]])
    D=Vmat*C*Vmat-cross*C*cross.T
    a=sp.Rational(N-1,2)*Vmat*C*m+Vmat*b/2
    mCm=(m.T*C*m)[0]
    V=(N*N*mCm+N*(sp.trace(C)-mCm))/4+N*(b.T*m)[0]/2
    G=V*k+sum((a[i]*grad[i] for i in range(3)),sp.zeros(2**N))
    G+=sum((D[i,j]*Hess[i][j]/4 for i in range(3) for j in range(3)),sp.zeros(2**N))
    diff=((H*k+k*H)/2-G).applyfunc(sp.expand)
    assert diff==sp.zeros(2**N)
    return {'N':N,'dimension':2**N,'full_generator_identity_exact':True}

def symbolic_drift():
    xs=sp.symbols('m0:3')
    ns=sp.symbols('n0:3')
    m,n=sp.Matrix(xs),sp.Matrix(ns)
    u=(n.T*m)[0]
    v=n-u*m
    r=n.cross(m)
    value=v.jacobian(m)*v-r.jacobian(m)*r+2*u*v
    assert all(sp.expand(z)==0 for z in value)
    return {'identity':'(v.grad)v-(r.grad)r=-2(n.m)v','all_polynomial_coefficients_zero':True}

if __name__=='__main__':
    start=time.monotonic()
    result={'scope':'Exact rational finite fixtures and a symbolic drift identity, not certification of all-N stopped diffusion.',
            'symbolic_drift':symbolic_drift(),'full_kernel_fixtures':[fixture(N) for N in [1,2,3]],
            'global_PSD_counterexample':{'C':'diag(1,2,3)','m':'(1,0,0)','D':'diag(0,-1,1)',
                 'meaning':'Confirms the need for the certified inner ball.'},
            'wall_seconds':time.monotonic()-start}
    target=Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
