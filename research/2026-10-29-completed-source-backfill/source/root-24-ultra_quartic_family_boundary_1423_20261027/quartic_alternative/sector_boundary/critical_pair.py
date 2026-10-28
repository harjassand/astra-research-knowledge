"""Serialize a fixed exact rank-one witness for every tau below the edge."""
from pathlib import Path
import json
import sympy as s
from acoustic_boundary import acoustic

ROOT=Path(__file__).resolve().parent


def main():
    z=s.symbols('z');r=s.sqrt(42);tau=89-12*r;K=s.QQ.algebraic_field(r)
    mc=-s.Rational(39,58)+s.Rational(15,29)*r
    modulus=s.Poly(z**4-mc*z*z+1,z,domain=K)
    source=json.loads((ROOT/'CRITICAL_SELECTOR.json').read_text())
    A=[s.Poly(s.sympify(e,locals={'z':z}),z,domain=K) for e in source['kernel_vector']]
    Q=acoustic(tau,z)
    assert all(s.Poly(sum(Q[i,j]*A[j].as_expr() for j in range(4)),z,domain=K).rem(modulus).is_zero
               for i in range(4))
    g=s.Poly(A[3].as_expr()-z*A[2].as_expr(),z,domain=K).rem(modulus)
    assert set(e[0] for e,c in g.terms()) <= {0,2}
    def pair(e):
        e=s.expand(e);b=e.coeff(r);a=s.expand(e-b*r)
        assert a.is_Rational and b.is_Rational
        return [str(a),str(b)]
    out={'status':'EXACT_FIXED_ACOUSTIC_WITNESS_ACQUIRED',
         'tau':['89','-12'],'critical_m':pair(mc),
         'z_definition':'unique real z>sqrt(2) solving z^4-m*z^2+1=0',
         'A_polynomial_coefficients':[[pair(p.nth(j)) for j in range(4)] for p in A],
         'rank_one_H':['1','z','0','0'],
         'kernel_identity':'Q_tau_c(z)*A(z)=0 modulo z^4-m*z^2+1',
         'cofactor_pairing_g0':pair(g.nth(0)),
         'cofactor_pairing_g2':pair(g.nth(2)),
         'nonzero_proof':'m>5/2 implies z^2>2; g2<0 and g0+2*g2<0 imply d-z*c<0',
         'all_lower_tau_identity':'D2F_tau(A)[H,H]=2*(tau-tau_c)*(d-z*c)^2<0'}
    (ROOT/'CRITICAL_PAIR.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
