"""Own N=2 symbolic block check and numerical boundary diagnostics.

The all-field inside-radius conclusion is analytical, in the associated audit.
Numerical values here are diagnostics; no interval theorem is inferred.
"""
from pathlib import Path
import json
import sympy as s
import mpmath as m

alpha, eps, bz = s.symbols('alpha eps bz', real=True)
sx=s.Matrix([[0,1],[1,0]])/2
sy=s.Matrix([[0,-s.I],[s.I,0]])/2
sz=s.diag(s.Rational(1,2),-s.Rational(1,2))
J=[s.kronecker_product(x,s.eye(2))+s.kronecker_product(s.eye(2),x) for x in [sx,sy,sz]]
# Columns: triplet +, triplet 0, triplet -, singlet.
P=s.Matrix([[1,0,0,0],[0,1/s.sqrt(2),0,1/s.sqrt(2)],
            [0,1/s.sqrt(2),0,-1/s.sqrt(2)],[0,0,1,0]])
assert s.simplify(P.conjugate().T*P)==s.eye(4)
J2=sum((x*x for x in J),s.zeros(4))
easy=alpha*J2-eps*J[2]*J[2]+s.sqrt(2)*bz*J[2]
biax=alpha*J2+eps*(J[0]*J[0]-J[1]*J[1])+s.sqrt(2)*bz*J[2]
easy_expected=s.diag(2*alpha-eps+s.sqrt(2)*bz,2*alpha,
                     2*alpha-eps-s.sqrt(2)*bz,0)
biax_expected=s.Matrix([[2*alpha+s.sqrt(2)*bz,0,eps,0],
                        [0,2*alpha,0,0],[eps,0,2*alpha-s.sqrt(2)*bz,0],
                        [0,0,0,0]])
assert s.simplify(P.conjugate().T*easy*P-easy_expected)==s.zeros(4)
assert s.simplify(P.conjugate().T*biax*P-biax_expected)==s.zeros(4)

m.mp.dps=100
def radius(a,B):
    beta=10*a+2*B
    H=3*a+B
    k=16*a
    Q=max(H,m.mpf(1))
    R=H+3*m.log(2)+beta+3+m.log(2*Q)
    L=k/2+m.sqrt(k*k/4+k*R)
    x=2*m.log(2)+beta+L
    eta=m.exp(-x)
    return eta,a*eta*eta/40

def biax_condition(a,b,e):
    om=m.sqrt(2*b*b+e*e)
    lhs=abs(e)*m.sinh(om)/om if om else abs(e)
    rhs=(1+m.exp(-2*a))/2
    # Exactly one PT eigenvalue can be negative, the odd-block x-w.
    u=m.exp(2*a)
    trace=2*u*m.cosh(om)+u+1
    mineig=(u+1-2*u*lhs)/(2*trace)
    return {'criterion_lhs':m.nstr(lhs,30),'criterion_rhs':m.nstr(rhs,30),
            'pt_min_eigenvalue_diagnostic':m.nstr(mineig,30),
            'entangled_diagnostic':bool(lhs>rhs)}

inside=[]
for astr in ['0.1','1','10']:
    for bstr in ['0','1','10']:
        a=m.mpf(astr);B=m.mpf(bstr);eta,delta=radius(a,B)
        row={'alpha':astr,'B':bstr,'eta':m.nstr(eta,30),
             'delta_star':m.nstr(delta,30),'epsilon':'0.99 delta_star'}
        row.update(biax_condition(a,B,m.mpf('.99')*delta))
        assert not row['entangled_diagnostic']
        inside.append(row)
outside=biax_condition(m.mpf(1),m.mpf(10),m.mpf('.0001'))
outside.update({'alpha':'1','b':'10','epsilon':'0.0001',
                'admitted_delta_star':m.nstr(radius(m.mpf(1),m.mpf(10))[1],30),
                'scope':'Outside admitted anisotropy radius; shows field dependence matters.'})
assert outside['entangled_diagnostic']
out={'symbolic_easy_plane_and_biaxial_blocks_exact':True,
     'easy_plane_ppt_threshold':'epsilon <= log(2/(1-exp(-2 alpha))); independent of b',
     'biaxial_ppt_threshold':'abs(epsilon)*sinh(sqrt(2b^2+epsilon^2))/sqrt(2b^2+epsilon^2) <= (1+exp(-2alpha))/2',
     'inside_radius_diagnostics':inside,'outside_radius_entangled_control':outside,
     'precision_decimal_digits':100,
     'scope':'Numerical diagnostics only. Universal inside-radius inequality is proved analytically in the audit.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
