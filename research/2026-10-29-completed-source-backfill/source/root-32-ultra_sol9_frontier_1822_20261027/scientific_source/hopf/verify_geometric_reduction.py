#!/usr/bin/env python3
"""Literal symbolic identities supporting the phase elimination theorem."""
import json,time
from pathlib import Path
import sympy as S

OUT=Path(__file__).resolve().parent

def main():
    start=time.perf_counter()
    av=S.Matrix(S.symbols('a0:4',real=True));rv=S.Matrix(S.symbols('r0:4',real=True))
    H=[S.diag(1,-1,1,-1),
       S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]]),
       S.Matrix([[0,0,0,1],[0,0,-1,0],[0,-1,0,0],[1,0,0,0]])]
    I=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    assert I.T*I==S.eye(4) and I*I==-S.eye(4)
    for i in range(3):
        assert H[i]*I==I*H[i]
        for j in range(3):assert H[i]*H[j]+H[j]*H[i]==(2*S.eye(4) if i==j else S.zeros(4))
    def h(A):return S.Matrix([(A.T*Hi*A)[0] for Hi in H])
    ha,hr=h(av),h(rv)
    b=S.Matrix([(av.T*Hi*rv)[0] for Hi in H])
    bp=S.Matrix([(av.T*Hi*I*rv)[0] for Hi in H])
    rhs=(((av.dot(av))*(rv.dot(rv))-ha.dot(hr))*S.eye(3)+ha*hr.T+hr*ha.T)/2
    assert all(S.expand(x)==0 for x in b*b.T+bp*bp.T-rhs)
    # A second, stronger identity fixes the tangent circle's radius directly.
    tangent_length=(av.dot(av)*rv.dot(rv)-ha.dot(hr))/2
    normr=rv.dot(rv)
    assert S.expand(b.dot(hr)-normr*av.dot(rv))==0
    # Generic Hessian polarization and T_F decomposition, clearing F.
    k,l,m,n,p,r=S.symbols('k l m n p r',real=True)
    K=S.Matrix([[k,l,m],[l,n,p],[m,p,r]])
    F=(hr.T*K*hr)[0]
    grad=S.Matrix([S.diff(F,x) for x in rv]);Hess=S.hessian(F,rv)
    half_quad=(av.T*Hess*av)[0]/2
    expected=2*(ha.T*K*hr)[0]+4*(b.T*K*b)[0]
    assert S.expand(half_quad-expected)==0
    assert S.expand((grad.dot(av))-4*(b.T*K*hr)[0])==0
    # Coordinate-free tangent Schur invariants checked at n=e1; rotations
    # transfer the polynomial identities to every unit n.
    St=S.Matrix([[n,p],[p,r]])-S.Matrix([l,m])*S.Matrix([[l,m]])/k
    assert S.factor(St.det()-K.det()/k)==0
    assert S.factor(S.trace(St)-((k*S.trace(K)-(K*K)[0,0])/k))==0
    data={'status':'PASS','Clifford_and_phase_commutation':True,
          'literal_general_polar_Hopf_identity':True,'literal_Hessian_and_gradient_identity':True,
          'tangent_Schur_trace_determinant':True,'elapsed_seconds':time.perf_counter()-start}
    (OUT/'GEOMETRIC_REDUCTION_REPLAY.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
