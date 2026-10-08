"""Exact seed-kernel diagnostics; finite fixtures do not replace the proof."""
import json
from pathlib import Path
import sympy as sp


def main():
    dim = 32
    phi = sp.zeros(dim, 1)
    psi = sp.zeros(dim, 1)
    # Big-endian five-wire convention, common clock suffix |10>.
    phi[2], phi[18] = 1/sp.sqrt(2), -1/sp.sqrt(2)
    for three, sign in [(0, 1), (3, -1), (5, -1), (6, -1)]:
        psi[4*three+2] = sp.Rational(sign, 2)
    cc = sp.simplify((phi.adjoint()*psi)[0])
    assert cc == 1/sp.sqrt(8)
    pphi, ppsi = phi*phi.adjoint(), psi*psi.adjoint()
    jj = sp.simplify((pphi+ppsi-cc*(phi*psi.adjoint()+psi*phi.adjoint()))/(1-cc**2))
    ss = sp.eye(dim)-jj
    assert jj == jj.adjoint() and ss == ss.adjoint()
    assert jj*jj == jj and ss*ss == ss
    assert jj.rank() == 2 and ss.rank() == 30
    assert all(v.is_Rational for v in ss)
    xx = sp.kronecker_product(sp.Matrix([[0, 1], [1, 0]]), sp.eye(16))
    zz = sp.kronecker_product(sp.diag(1, -1), sp.diag(1, -1),
                              sp.diag(1, -1), sp.eye(4))
    assert xx*zz == -zz*xx
    expected = [-1, 0, -cc, 0, 1, cc]
    observed = [sp.simplify((v.adjoint()*op*w)[0]) for v, op, w in
                [(phi, xx, phi), (psi, xx, psi), (psi, xx, phi),
                 (phi, zz, phi), (psi, zz, psi), (psi, zz, phi)]]
    assert observed == expected
    assert sp.trace(jj*xx) == -sp.Rational(6, 7)
    assert sp.trace(jj*zz) == sp.Rational(6, 7)
    assert sp.trace(ss*xx) == sp.Rational(6, 7)
    assert sp.trace(ss*zz) == -sp.Rational(6, 7)
    seed_zero = sp.zeros(dim, 1)
    seed_zero[0] = 1
    assert pphi*seed_zero == sp.zeros(dim, 1)
    assert ppsi*seed_zero == sp.zeros(dim, 1)
    assert ss*seed_zero == seed_zero
    pzero = sp.zeros(dim)
    pzero[0, 0] = 1
    data_zero = sp.zeros(dim, 1)
    data_zero[16] = 1  # |10000>
    assert pzero*data_zero == sp.zeros(dim, 1)
    full = []
    for tt in [1, 2, 4, 16]:
        coeff = sp.Rational(31, 32)**tt*sp.Rational(3, 112)*sp.Rational(15, 16)**(tt-1)
        assert coeff > 0
        full.append({"T": tt, "logical_qubits": 10*tt,
                     "full_kernel_rank": str(31**tt*30**tt),
                     "L_X_coefficient": str(coeff), "L_Z_coefficient": str(-coeff),
                     "method": "Proved tensor formulas; dense full matrix not allocated"})
    out = {"status": "EXACT_SEED_KERNEL_FIXTURE_PASSED",
           "seed_span_rank": 2, "seed_kernel_rank": 30,
           "overlap_square": "1/8", "Tr_S_X": "6/7", "Tr_S_ZZZ": "-6/7",
           "full_instance": "All three singleton colors, weights 1/2,1/4,1/4",
           "full_kernel_formula": "(I-P0)^tensor T tensor S^tensor T",
           "instances": full,
           "scope": "Finite exact diagnostics; theorem and generator membership are analytic"}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
