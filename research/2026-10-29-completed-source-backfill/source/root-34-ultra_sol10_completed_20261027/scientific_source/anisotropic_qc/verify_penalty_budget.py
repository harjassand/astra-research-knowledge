#!/usr/bin/env python3
"""Exact value-preserving off-plane extension budget for the actual target.

This is a restricted-construction obstruction, not non-quasiconvexity.
No numerical optimizer or producer module is imported.
"""
from pathlib import Path
import json,time
import sympy as S
HERE=Path(__file__).resolve().parent

def run():
    start=time.perf_counter()
    alpha=S.sqrt(110)/240
    norm_squared=S.Rational(3591,10000)
    U=S.Matrix([[alpha*S.Rational(12,5),-alpha*S.Rational(12,5)],
                [-S.Rational(1,25),-S.Rational(1,25)]])/S.sqrt(norm_squared)
    V=S.Matrix([[1,S.Rational(11,20)/(alpha*S.Rational(12,5))],
                [1,-S.Rational(11,20)/(alpha*S.Rational(12,5))]])
    A=S.diag(36,35)/S.sqrt(2521)
    z=S.symbols('z0:4',real=True);C=S.Matrix(2,2,z)
    B=A+U*C*V
    def F(M):
        aa,bb,cc,dd=list(M);u=aa*aa+cc*cc;v=bb*bb+dd*dd;q=aa*dd-bb*cc
        return S.expand((u+v)**2+S.Rational(252,25)*q*q+S.Rational(99,25)*q*(u-v))
    target=F(B)
    f=S.expand(target.subs({z[1]:0,z[2]:0}))
    H=S.simplify(S.hessian(f,[z[0],z[3]]).subs({z[0]:0,z[3]:0})/2)
    a,b,c=H[0,0],H[0,1],H[1,1]
    assert a==c and b>a>0
    Mlo=S.factor(b-a)
    assert Mlo==S.Rational(59139344,45264555)>1
    R=S.Matrix([[1,1],[-1,-1]])
    assert R.det()==0 and R.rank()==1
    m,t=S.symbols('m t',real=True)
    off=z[1]*z[1]+z[2]*z[2];norm=sum(x*x for x in z)
    h=f+m*off*(1+norm)
    line=S.Poly(h.subs(dict(zip(z,list(t*R))),simultaneous=True),t)
    assert S.factor(line.coeff_monomial(t*t)-2*(m-Mlo))==0
    a4=S.factor(line.coeff_monomial(t**4).subs(m,0))
    assert a4>0 and S.factor(line.coeff_monomial(t**4)-a4-8*m)==0
    loss=S.factor((Mlo-1)**2/(a4+8))
    amplitude_squared=S.factor((Mlo-1)/(a4+8))
    assert loss>0 and amplitude_squared>0
    directions=[]
    for i,j in [(0,0),(0,1),(1,0),(1,1)]:
        E=S.zeros(2);E[i,j]=1;P=U*E*V
        assert P.det()==0 and S.simplify(sum(x*x for x in P)-1)==0
        assert S.simplify(F(P)-1)==0
        directions.append({'index':[i,j],'rank_one':True,'Frobenius_norm_squared':'1','target_quartic_coefficient':'1'})
    # The convex QC floor M(|off|^2+|off|^4) is below the obstacle:
    # h-floor=f+M |off|^2 |diag|^2>=0 (F>=0, M>=0).
    floor=m*(off+off*off)
    assert S.expand(h-floor-f-m*off*(z[0]*z[0]+z[3]*z[3]))==0
    result={'status':'EXACT_RESTRICTED_EXTENSION_BUDGET_PASS',
        'A_normalized':list(map(str,list(A))),
        'U':list(map(str,list(U))),'V':list(map(str,list(V))),
        'half_diagonal_Hessian':[[str(x) for x in row] for row in H.tolist()],
        'value_preserving_contact_requires_M_at_least':str(Mlo),
        'M_lower_minus_1':str(Mlo-1),'growth_subordination_requires_M_at_most':'1',
        'rank_one_test_C':[[1,1],[-1,-1]],
        'test_quadratic_coefficient':str(line.coeff_monomial(t*t)),
        'test_quartic_base_coefficient':str(a4),
        'all_M_between_0_and_1_envelope_value_loss_at_least':str(loss),
        'M1_optimizing_rank_one_amplitude_squared':str(amplitude_squared),
        'four_physical_directions':directions,
        'floor_identity':'h_M-M(|off|^2+|off|^4)=f+M|off|^2|diag|^2',
        'scope':'Qh_M cannot both preserve target value at0 and be globally subordinate; arbitrary affine-recentered contacts and unequal penalties are not excluded',
        'target_quasiconvexity':'UNKNOWN','seconds':time.perf_counter()-start}
    (HERE/'PENALTY_BUDGET_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
