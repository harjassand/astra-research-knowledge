"""Exact symbolic reconstruction of the received heat-flow correction."""
import json
from pathlib import Path
import sympy as s


def main():
    a,b,c,d,r,t=s.symbols('a b c d rho t',real=True)
    x1,x2,x3,y1,y2,y3=s.symbols('x1 x2 x3 y1 y2 y3',real=True)
    av=s.Matrix([a,b,c,d]); bv1=s.Matrix([x1,x2,y1,y2]);bv2=s.Matrix([x2,x3,y2,y3])
    norm=a*a+b*b+c*c+d*d;det=a*d-b*c
    theta=s.Matrix([-c,-d,a,b]);zeta=s.Matrix([-b,a,-d,c])
    q=norm**2+4*t*norm*det+(6*t*t-2)*det**2
    alpha=(-3*t*norm+6*(1-2*t*t)*det)*theta+(3*norm+6*t*det)*zeta
    domega=s.Matrix(4,4,lambda i,j:s.diff(alpha[j],av[i])-s.diff(alpha[i],av[j]))
    hess=s.hessian(q,av)
    corrected=(bv1.T*hess*bv1+bv2.T*hess*bv2+bv1.T*domega*bv2)[0]
    corrected=s.expand(corrected.subs({a:1,b:0,c:0,d:r}))
    ll,mm,delta=1+t*r,t+r,1-t*t
    sos=3*(2*ll*x1+ll*x3+mm*y2)**2+(ll*x3-mm*y2)**2+4*delta*(r*x3-y2)**2
    sos+=3*(ll*x2+mm*y1+2*mm*y3)**2+(ll*x2-mm*y1)**2+4*delta*(r*x2-y1)**2
    assert s.expand(corrected-sos)==0
    # Theorem 1 is the boundary parameter t=-1/sqrt(3): its det^2 term is zero.
    assert s.simplify(q.subs(t,-1/s.sqrt(3))-(norm**2-4/s.sqrt(3)*norm*det))==0
    kap=1+r*r-2*r/s.sqrt(3)
    mat=s.Matrix([[(r-s.sqrt(3))**2,(r-s.sqrt(3))**2/2,2*r-s.sqrt(3)*(1+r*r)/2],
                  [(r-s.sqrt(3))**2/2,kap,-(1+r*r)/(2*s.sqrt(3))],
                  [2*r-s.sqrt(3)*(1+r*r)/2,-(1+r*r)/(2*s.sqrt(3)),kap]])
    assert s.simplify(mat.det()-(r-s.sqrt(3))**2*(1-r*r)**2/6)==0
    assert s.simplify(mat[:2,:2].det()-s.Rational(3,4)*(r-s.sqrt(3))**2*((r-s.sqrt(3)/9)**2+s.Rational(8,27)))==0
    # A useful limit of the method: even polyconvex det^2 is not itself
    # monotone under heat. The paper subtracts this polyconvex ray separately.
    z=s.symbols('z',positive=True)
    heat_energy=z**3*(1-z)**2/2
    derivative=s.expand(-2*z*s.diff(heat_energy,z))
    assert s.simplify(derivative-z**3*(1-z)*(5*z-3))==0
    assert derivative.subs(z,s.Rational(4,5))==s.Rational(64,625)
    result=dict(source='https://arxiv.org/html/2608.06367v1',
                appendix_full_polynomial_SOS_identity=True,
                main_matrix_principal_minors=True,
                critical_family_matches=True,
                det_squared_heat_counterexample_derivative='64/625',
                conclusion='The stated ADM family is covered. No defect found in the reconstructed governing proof. General planar Morrey is separate.')
    Path('outputs/capability_first_20261101/bruno_pasqualotto_exact.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
