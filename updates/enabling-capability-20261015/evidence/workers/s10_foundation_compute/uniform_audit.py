"""Independent exact d=3 action replay of a08's uniform-reference reduction.

Uses a direct partial-trace construction of Phi, not producer diagrams.
Finite replay supports implementation only; conceptual all-d completeness
is separately audited in UNIFORM_AUDIT.txt.
"""
from itertools import product
from pathlib import Path
import hashlib,json,time
import sympy as sp
from independent_replay import direct


def main():
    start=time.perf_counter();d=3;n=d*d;N=n*n
    u=sp.zeros(n,1)
    for i in range(d):u[d*i+i]=1
    C,S=direct(u,d,d)
    tuples=list(product(range(d),repeat=4))
    def T(X,j):
        v=[]
        for a,b,c,e in tuples:
            if j==0:v.append(int(a==b)*X[c,e])
            elif j==1:v.append(X[a,b]*int(c==e))
            elif j==2:v.append(int(a==e)*X[c,b])
            elif j==3:v.append(X[a,e]*int(c==b))
        return sp.Matrix(v)
    V0=sp.Matrix.hstack(T(sp.eye(d),0),T(sp.eye(d),2))
    C0=sp.Matrix([[sp.Rational(5,4),-1],[-1,sp.Rational(5,4)]])
    S0=sp.Matrix([[sp.Rational(5,4),-sp.Rational(10*d*d-25*d+12,2*(d-1)*(5*d-4))],
                  [-1,sp.Rational(11*d*d-37*d+20,4*(d-1)*(5*d-4))]])
    C1=sp.Matrix([[1,sp.Rational(1,4),-sp.Rational(1,2),-sp.Rational(1,2)],
                  [sp.Rational(1,4),1,-sp.Rational(1,2),-sp.Rational(1,2)],
                  [-sp.Rational(1,2),-sp.Rational(1,2),1,sp.Rational(1,4)],
                  [-sp.Rational(1,2),-sp.Rational(1,2),sp.Rational(1,4),1]])
    a=sp.Rational(10*d*d-37*d+20,4*(d-1)*(5*d-4))
    b=sp.Rational(9*d-4,4*(d-1)*(5*d-4))
    c=sp.Rational(6*d*d-23*d+12,4*(d-1)*(5*d-4))
    S1=sp.Matrix([[1,sp.Rational(d-5,4*(d-1)),-a,-a],
                  [sp.Rational(1,4),0,b,b],
                  [-sp.Rational(1,2),sp.Rational(1,2*(d-1)),-sp.Rational(1,2*(d-1)),c],
                  [-sp.Rational(1,2),sp.Rational(1,2*(d-1)),c,-sp.Rational(1,2*(d-1))]])
    G0=sp.Matrix([[d*d,d],[d,d*d]])
    G1=sp.Matrix([[d,0,1,1],[0,d,1,1],[1,1,d,0],[1,1,0,d]])
    basis=[]
    for i,j in product(range(d),repeat=2):
        if i!=j:
            X=sp.zeros(d);X[i,j]=1;basis.append(X)
    for i in range(d-1):
        X=sp.zeros(d);X[i,i]=1;X[i+1,i+1]=-1;basis.append(X)
    checks={'trivial_C_action':C*V0==V0*C0,'trivial_S_action':S*V0==V0*S0,
            'trivial_Gram':V0.H*V0==G0,'adjoint_C_actions':True,'adjoint_S_actions':True,
            'adjoint_Grams':True,'trivial_adjoint_orthogonality':True}
    vparts=[V0]
    for X in basis:
        V=sp.Matrix.hstack(*(T(X,j) for j in range(4)))
        checks['adjoint_C_actions'] &= C*V==V*C1
        checks['adjoint_S_actions'] &= S*V==V*S1
        checks['adjoint_Grams'] &= V.H*V==sp.trace(X.H*X)*G1
        checks['trivial_adjoint_orthogonality'] &= V0.H*V==sp.zeros(2,4)
        vparts.append(V)
    V=sp.Matrix.hstack(*vparts)
    FA=sp.zeros(N);FB=sp.zeros(N)
    index={z:i for i,z in enumerate(tuples)}
    for k,(a,b,c,e) in enumerate(tuples):
        FA[index[c,b,a,e],k]=1;FB[index[a,e,c,b],k]=1
    gamma=sp.Rational(d*d-9*d+4,4*(d-1)*(5*d-4))
    P=sp.Rational(1,4*(d-1))*(FA+FB)+gamma*FA*FB
    residual=S-P
    checks['S_Hermitian']=S==S.H
    checks['S_residual_range_inside_contraction_span']=V.row_join(residual).rank()==V.rank()
    checks['contraction_span_dimension']=V.rank()==4*d*d-2
    checks['contraction_span_FA_invariant']=V.row_join(FA*V).rank()==V.rank()
    checks['contraction_span_FB_invariant']=V.row_join(FB*V).rank()==V.rank()
    source=Path(__file__).parent.parent/'a08_grouped_werner'/'uniform_schmidt.json'
    out={'status':'INDEPENDENT_EXACT_D3_UNIFORM_ACTION_REPLAY_PASSED' if all(checks.values()) else 'FAILED',
         'scope':'Finite exact d3 replay plus conceptual audit in UNIFORM_AUDIT.txt; no numerical extrapolation',
         'source_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'checks':checks,'d3_H_dimension':N,'d3_contraction_span_dimension':V.rank(),
         'd3_complement_dimension':N-V.rank(),'elapsed_code_seconds':time.perf_counter()-start}
    assert all(checks.values())
    Path(__file__).with_name('uniform_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
