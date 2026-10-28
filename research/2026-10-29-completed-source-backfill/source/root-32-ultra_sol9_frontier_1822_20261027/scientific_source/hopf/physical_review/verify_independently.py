#!/usr/bin/env python3
"""Independent completion review: literal Fraction and symbolic identities.

No producer import or producer-verifier execution. Barrier smoothness and
convexity are proved analytically in REVIEW.md, not inferred from quadrature.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,time
import sympy as S

HERE=Path(__file__).resolve().parent

def determinant(M):return M[0]*M[3]-M[1]*M[2]
def quartic(M):
    a,b,c,d=M
    u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
    return (u+v)**2+Q(252,25)*q*q+Q(99,25)*q*(u-v)

def run():
    start=time.perf_counter()
    A=list(map(Q,[36,0,0,35]))
    increments=[[Q(-264,28745),Q(-63481,114980),Q(5771,143725),Q(528,28745)],
                [Q(0),Q(11,20),Q(-1,25),Q(0)],
                [Q(12,5),Q(0),Q(0),Q(-24,5)]]
    weights=[Q(5749,11542),Q(1,2),Q(11,5771)]
    points=[[a+x for a,x in zip(A,X)] for X in increments]
    assert sum(weights)==1 and min(weights)>0
    assert all(sum(l*B[j] for l,B in zip(weights,points))==A[j] for j in range(4))
    determinants=[determinant(A)]+[determinant(B) for B in points]
    assert min(determinants)>Q(1,2)
    assert sum(l*determinant(B) for l,B in zip(weights,points))==determinant(A)
    gap=sum(l*quartic(B) for l,B in zip(weights,points))-quartic(A)
    assert gap==Q(-13534664264487807,296890944920312500)
    cs=Q(25399,10000)
    flat=lambda M:quartic(M)-8*cs*determinant(M)+4*cs
    assert sum(l*flat(B) for l,B in zip(weights,points))-flat(A)==gap

    a,b,c,d,beta,r=S.symbols('a b c d beta r',real=True)
    av=S.Matrix([a,b,c,d]);q=a*d-b*c
    x=a*a+c*c-b*b-d*d;y=2*(a*b+c*d)
    f=x*x+y*y+4*beta*q*x+4*r*q*q
    w=f-8*(r-beta*beta)*q+4*(r-beta*beta)
    rhs=(x+2*beta*q)**2+y*y+4*(r-beta*beta)*(q-1)**2
    assert S.expand(w-rhs)==0
    # Parameterize the exact natural well algebraically: u=t, v=1/t,
    # beta=(1/t-t)/2, q=1. This avoids relying on nested-root simplification.
    s=S.symbols('s',positive=True);bs=(1/s**2-s**2)/2
    well={a:s,b:0,c:0,d:1/s,beta:bs}
    assert S.simplify(w.subs(well,simultaneous=True))==0
    grad=[S.simplify(S.diff(w,z).subs(well,simultaneous=True)) for z in av]
    assert grad==[0]*4
    # General material-anisotropy calculation after right normalization.
    A0=S.diag(s,1/s);D=S.diag(2,1);Rot=S.Matrix([[0,-1],[1,0]])
    def evaluate(M):return S.expand(f.subs({a:M[0,0],b:M[0,1],c:M[1,0],d:M[1,1]},simultaneous=True))
    anis=S.factor((evaluate(D*A0)-evaluate(D*Rot*A0)).subs(beta,bs))
    # sqrt(1+beta^2)=(s^2+s^-2)/2 at the parameterized well.
    expected=-12*bs*(s*s+1/(s*s))/2
    assert S.simplify(anis-expected)==0
    # Rank-one determinant chain rule: D2det[R,R]=2detR identically.
    R=S.Matrix(S.symbols('r0:4',real=True))
    det_hessian=S.hessian(q,av)
    assert S.expand((R.T*det_hessian*R)[0]-2*(R[0]*R[3]-R[1]*R[2]))==0
    # Exact minor/mean transport by an arbitrary det-one right normalization.
    v1,v2,v3,v4=S.symbols('v1:5');B=S.Matrix([[v1,v2],[v3,v4]])
    assert S.expand((B*A0.inv()).det()-B.det())==0
    # GL+ graph convex hull: constructive two-point identity for invertible B.
    alpha=S.symbols('alpha',real=True)
    u=(1-alpha)/2;v=(1+alpha)/2;Z=S.Matrix([[u,v],[-v,-u]])
    assert S.trace(Z)==0 and S.factor(Z.det()-alpha)==0
    assert S.factor((S.eye(2)+Z).det()-(1+alpha))==0
    assert S.factor((S.eye(2)-Z).det()-(1+alpha))==0
    # Exact infinite-family feasible scale and orientation margin.
    z=S.symbols('z',nonnegative=True);m=197+z;bm=(m*m-1)/(m*m+1)
    tstar=S.factor((18*bm-14)/(24*bm+73))
    assert all(x>0 for x in S.Poly(S.fraction(tstar)[0],z).all_coeffs())
    room=S.factor(S.Rational(4,97)-tstar)
    assert all(x>0 for x in S.Poly(S.fraction(room)[0],z).all_coeffs())
    qstar=S.factor((1+tstar)*(1-2*tstar))
    qroom=S.factor(qstar-S.Rational(8989,9409))
    assert all(x>0 for x in S.Poly(S.fraction(qroom)[0],z).all_coeffs())
    assert S.Rational(8989,9409)>S.Rational(1,2)
    # Reconstruct tstar directly from the literal one-variable quartic.
    tt=S.symbols('tt',real=True);Rminus=S.diag(1,-2)
    Fline=S.Poly(evaluate(Rminus+tt*S.eye(2)).subs(r,4),tt)
    minscale=S.factor(-Fline.coeff_monomial(tt)/(2*Fline.coeff_monomial(1)))
    assert S.factor(minscale-(18*beta-14)/(24*beta+73))==0
    # Independent exact integral in the barrier's divergence estimate.
    qq,delta,t=S.symbols('qq delta t',positive=True)
    lower_integral=S.integrate(1/(2*t**3),(t,2*qq,delta/2))
    assert S.simplify(lower_integral-(1/(16*qq**2)-1/delta**2))==0
    exponent_difference=S.factor(-1/(delta-t)+2/delta)
    assert S.factor(exponent_difference-(delta-2*t)/(delta*(delta-t)))==0

    result={'status':'INDEPENDENT_COMPLETION_IDENTITIES_PASS',
        'main_determinants':list(map(str,determinants)),
        'exact_mean_and_minors':'PASS','Jensen_defect':str(gap),
        'completed_Jensen_defect':str(gap),'square_completion_identity':'PASS',
        'natural_well_parameter':'diag(s,1/s), beta=(s^-2-s^2)/2',
        'stress_free_gradient':list(map(str,grad)),
        'anisotropy_general_identity':'-12 beta sqrt(1+beta^2)',
        'right_det_one_transport':'PASS','GL_positive_graph_two_point_identity':'PASS',
        'family_minimizing_scale':str(minscale),'family_positive_scale_and_barrier_slack':'PASS',
        'family_determinant_lower':'8989/9409>1/2',
        'barrier_integral_lower':str(lower_integral),
        'scope':'exact algebra and finite witness; analytic barrier and domain arguments in REVIEW.md; accepted ROC premise retained',
        'seconds':time.perf_counter()-start}
    (HERE/'REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
