"""Literal acoustic determinant: algebraic diagnostics, not a PSD proof."""
from pathlib import Path
import json
import sympy as s


def acoustic(tau, z):
    m11=s.Matrix([[12,0,0,12],[0,6,-4,0],[0,-4,4,0],[12,0,0,2*tau]])
    m12=s.Matrix([[0,6,-4,0],[6,0,0,-4],[-4,0,0,3-tau],[0,-4,3-tau,0]])
    m22=s.Matrix([[6,0,0,-4],[0,12,12,0],[0,12,2*tau,0],[-4,0,0,4]])
    return m11+2*z*m12+z*z*m22


def main():
    tau,z,y,m=s.symbols('tau z y m')
    Q=acoustic(tau,z)
    det=s.factor(Q.det());p=s.Poly(det,z)
    assert all(e[0]%2==0 for e,c in p.terms())
    py=s.Poly(sum(c*y**(e[0]//2) for e,c in p.terms()),y)
    assert py==s.Poly(y**py.degree()*py.as_expr().subs(y,1/y),y)
    # Reciprocal quartic in y divided by y² is quadratic in m=y+1/y.
    assert py.degree()==4
    coeff=py.all_coeffs()
    reduced=s.factor(coeff[0]*(m*m-2)+coeff[1]*m+coeff[2])
    vertex=s.factor(-s.diff(reduced,m).subs(m,0)/s.diff(reduced,m,2))
    critical=s.factor(reduced.subs(m,vertex))
    out={'status':'EXACT_ALGEBRA_DIAGNOSTIC_NOT_GLOBAL_PSD',
         'det_Q':str(det),'reciprocal_reduction':str(reduced),
         'm_domain':'m=z^2+z^(-2)>=2', 'vertex_m':str(vertex),
         'vertex_value':str(critical),
         'tau_roots':[str(r) for r in s.solve(s.fraction(critical)[0],tau)],
         'boundary_m_value':str(s.factor(reduced.subs(m,2)))}
    (Path(__file__).resolve().parent/'ACOUSTIC_ALGEBRA.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
