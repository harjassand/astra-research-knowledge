"""Independent whole certificate consumer. No producer Python imports/reruns.

Rebuild the target Hessian, compatible jets, exterior derivative and polynomial
identity with SymPy; qualify the supplied Gram by separate integer arithmetic;
evaluate the old actual non-polyconvex Jensen witness literally with Fraction.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from math import lcm
import hashlib
import json
import time
import sympy as sp

BASE = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE = BASE / "work/sol25_capability_frontiers_20261030/a_independent/heat_form"


def rational(text):
    value = Q(text)
    return sp.Rational(value.numerator, value.denominator)


def quartic(A):
    a, b, c, d = A
    T = a*a+b*b+c*c+d*d
    det = a*d-b*c
    x = a*a+c*c-b*b-d*d
    return T*T+Q(252,25)*det*det+Q(99,25)*det*x


def det(A):
    return A[0]*A[3]-A[1]*A[2]


def main():
    started = time.perf_counter()
    certificate_path = SOURCE / "RATIONAL_EXACT_CERTIFICATE.json"
    raw = certificate_path.read_bytes()
    c = json.loads(raw)
    assert c["target"] == "T^2+(252/25)q^2+(99/25)qx"
    a = sp.symbols("a b c d")
    h = sp.symbols("h0:6")
    T = sum(v*v for v in a)
    F = quartic(a)
    H = sp.hessian(F, a)
    B1, B2 = sp.Matrix([h[0],h[1],h[3],h[4]]), sp.Matrix([h[1],h[2],h[4],h[5]])
    J = sp.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
    assert J.T == -J and J*J == -sp.eye(4)
    nu = rational(c["nu"])
    diss = (B1.T*H*B1)[0]+(B2.T*H*B2)[0]+nu*((B1.T*H*J*B2)[0]+(B2.T*H*J*B1)[0])
    primitives = c["primitives"]
    assert len(primitives) == len(c["alpha"]) == 224
    assert len({(s,tuple(e)) for s,e in primitives}) == 224
    assert all(0 <= s < 4 and len(e) == 4 and sum(e) == 5 for s,e in primitives)
    P = [sp.Integer(0) for _ in a]
    for (s,e), coefficient in zip(primitives, c["alpha"]):
        P[s] += rational(coefficient)*sp.prod(v**k for v,k in zip(a,e))
    exterior_numerator = sp.Integer(0)
    for i in range(4):
        for j in range(i+1,4):
            omega = T*(sp.diff(P[j],a[i])-sp.diff(P[i],a[j])) - 2*a[i]*P[j]+2*a[j]*P[i]
            exterior_numerator += omega*(B1[i]*B2[j]-B1[j]*B2[i])
    target = sp.Poly(sp.expand(T*T*diss+exterior_numerator), a+h)
    assert all(sum(m[:4]) == 6 and sum(m[4:]) == 2 for m,_ in target.terms())

    z = [tuple(e) for e in c["z"]]
    assert len(z) == len(set(z)) == 120
    expected = {aa+hh for aa in product(range(4),repeat=4) if sum(aa)==3
                for hh in product((0,1),repeat=6) if sum(hh)==1}
    assert set(z) == expected
    gram = [[Q(v) for v in row] for row in c["Q"]]
    assert len(gram) == 120 and all(len(row)==120 for row in gram)
    assert all(gram[i][j] == gram[j][i] for i in range(120) for j in range(120))
    polynomial = {}
    for i in range(120):
        for j in range(i,120):
            exponent = tuple(x+y for x,y in zip(z[i],z[j]))
            polynomial[exponent] = polynomial.get(exponent,Q(0)) + (1 if i==j else 2)*gram[i][j]
    polynomial = {e:v for e,v in polynomial.items() if v}
    target_dict = {e:Q(int(v.p),int(v.q)) for e,v in target.terms()}
    assert polynomial == target_dict
    identity_seconds = time.perf_counter()-started

    # Entire PSD proof from literal integers. No floating factor/eigenvalue call.
    shift = Q(c["gram_shift"])
    L = c["factor_integer"]
    denominator = c["factor_denominator"]
    assert len(L)==120 and all(len(row)==120 for row in L)
    assert all(isinstance(x,int) for row in L for x in row)
    common = lcm(denominator**2,shift.denominator,*(v.denominator for row in gram for v in row))
    factor = common // denominator**2
    row_error = [0]*120
    for i in range(120):
        for j in range(120):
            residual = gram[i][j]-(shift if i==j else 0)
            integer_gram = residual.numerator*(common//residual.denominator)
            integer_factor = sum(L[i][k]*L[j][k] for k in range(120))*factor
            row_error[i] += abs(integer_gram-integer_factor)
    error = Q(max(row_error),common)
    assert error == Q(c["exact_factor_residual_row_sum"])
    assert shift-error > Q(1,2000)
    assert abs(Q(c["nu"])) < Q(1,1000)

    # The accepted old source's literal three atoms. This is NOT a gradient law.
    A = [Q(36),Q(0),Q(0),Q(35)]
    increments = [[Q(-264,28745),Q(-63481,114980),Q(5771,143725),Q(528,28745)],
                  [Q(0),Q(11,20),Q(-1,25),Q(0)],
                  [Q(12,5),Q(0),Q(0),Q(-24,5)]]
    weights = [Q(5749,11542),Q(1,2),Q(11,5771)]
    assert all(w>0 for w in weights) and sum(weights)==1
    assert all(sum(w*x[j] for w,x in zip(weights,increments))==0 for j in range(4))
    assert sum(w*det(x) for w,x in zip(weights,increments))==0
    atoms = [[u+v for u,v in zip(A,x)] for x in increments]
    assert sum(w*det(B) for w,B in zip(weights,atoms))==det(A)
    defect = sum(w*quartic(B) for w,B in zip(weights,atoms))-quartic(A)
    assert defect == Q(-13534664264487807,296890944920312500)

    # Quantitative QC constants use the actual certificate nu, not a float.
    pointwise = Q(1,12000)
    norm_coefficient = 24*(1+abs(Q(c["nu"])))
    kappa = Q(1,300000)
    assert pointwise-kappa*norm_coefficient > 0
    direct_jensen = pointwise/(3*norm_coefficient)
    assert direct_jensen > Q(1,900000)
    # Literal quartic uniform-convexity remainder, all vector dimensions.
    A2, X2, AX = sp.symbols("A2 X2 AX")
    remainder = sp.expand((A2+2*AX+X2)**2-A2**2-4*A2*AX-X2**2/sp.Integer(3))
    assert sp.expand(remainder - (2*(A2*X2-AX**2)+6*(AX+X2/3)**2)) == 0
    result = {"status":"PASS exact original certificate/source consumer; analytical whole review is separate",
              "certificate_path":str(certificate_path), "certificate_sha256":hashlib.sha256(raw).hexdigest(),
              "identity_nonzero_coefficients":len(target_dict), "gram_dimension":120,"primitive_count":224,
              "compatible_hessian_variables":6,"exact_identity":True,"whole_monomial_basis":True,
              "gram_shift":str(shift),"exact_residual_row_bound":str(error),"strict_gram_lower":str(shift-error),
              "consumed_gram_lower":"1/2000","pointwise_dissipation_lower":"T*|h|^2/12000",
              "actual_nu":c["nu"],"norm_dissipation_upper_coefficient":str(norm_coefficient),
              "kappa":"1/300000","positive_compensated_margin":str(pointwise-kappa*norm_coefficient),
              "direct_stronger_jensen_constant":str(direct_jensen),"consumed_jensen_constant":"1/900000",
              "original_finite_nonpc_defect":str(defect),"identity_seconds":identity_seconds,
              "total_seconds":time.perf_counter()-started,
              "producer_modules_imported":[],"optimizer_runs":0,"new_scientific_fixtures":0}
    (HERE/"EXACT_CONSUMER.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
