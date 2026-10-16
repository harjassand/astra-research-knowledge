#!/usr/bin/env python3
"""Independent standard-library exact audit of the all-r stress certificate.

Input matrices and basis strings are untrusted data. No producer verifier or
numeric optimizer is imported. The unmodified base audit supplies only our
own exact Fraction matrix routines. Polynomials below are reconstructed with
six-variable rational arithmetic after clearing the positive denominator r+2.
"""
from fractions import Fraction as F
from pathlib import Path
import ast
import hashlib
import json
import platform

from exact_audit import ldl, det, serial_matrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
INPUT = ROOT / "workers/ga_parametric_stress_genesis/ALL_R_STRESS_EXACT_CERTIFICATE.json"
N = 6
ZERO = (0,) * N
checks = []


def check(name, condition, detail=None):
    if not condition:
        raise RuntimeError("FAILED: " + name)
    checks.append({"name": name, "status": "PASS", "detail": detail})


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.co = value.co.copy()
        elif isinstance(value, dict):
            self.co = {tuple(k): F(v) for k, v in value.items() if v}
        else:
            self.co = {} if not value else {ZERO: F(value)}

    def __add__(self, other):
        out = self.co.copy()
        for k, v in P(other).co.items():
            out[k] = out.get(k, F(0)) + v
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.co.items()})

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) + (-self)

    def __mul__(self, other):
        out = {}
        for k, v in self.co.items():
            for ell, w in P(other).co.items():
                m = tuple(x + y for x, y in zip(k, ell))
                out[m] = out.get(m, F(0)) + v * w
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        p = P(other)
        if set(p.co) != {ZERO}:
            raise ValueError("Polynomial division is allowed only by a nonzero rational constant")
        return self * (1 / p.co[ZERO])

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("Expected nonnegative integer exponent")
        out = P(1)
        for _ in range(n):
            out = out * self
        return out

    def __eq__(self, other):
        return self.co == P(other).co

    def derivative(self, i):
        out = {}
        for k, v in self.co.items():
            if k[i]:
                ell = list(k)
                ell[i] -= 1
                out[tuple(ell)] = k[i] * v
        return P(out)

    def coefficient(self, i, n):
        return P({k[:i] + (0,) + k[i + 1:]: v
                  for k, v in self.co.items() if k[i] == n})

    def substitute(self, replacement):
        out = P(0)
        for k, v in self.co.items():
            term = P(v)
            for i, exponent in enumerate(k):
                term *= replacement.get(i, variable(i)) ** exponent
            out += term
        return out


def variable(i):
    k = [0] * N
    k[i] = 1
    return P({tuple(k): F(1)})


VARS = dict(zip(("r", "a", "b", "c", "d", "s"), [variable(i) for i in range(N)]))


def parse_basis(text):
    # A tiny explicit polynomial grammar, not eval or executable source.
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Name) and node.id in VARS:
            return VARS[node.id]
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return P(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            x = visit(node.left)
            if isinstance(node.op, ast.Pow):
                if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, int):
                    raise ValueError("Invalid power")
                return x ** node.right.value
            y = visit(node.right)
            if isinstance(node.op, ast.Add):
                return x + y
            if isinstance(node.op, ast.Sub):
                return x - y
            if isinstance(node.op, ast.Mult):
                return x * y
            if isinstance(node.op, ast.Div):
                return x / y
        raise ValueError("Unsupported basis syntax: " + ast.dump(node))
    return visit(ast.parse(text, mode="eval"))


def jnumerator(r, a, b, c, d):
    # Exactly (r+2) times the frozen original Jr, not a fitted polynomial.
    u = a * a + c * c
    v = b * b + d * d
    j = a * d - b * c
    return (3 * r / 8 * (u + v - 2 * j) ** 2
            + r * (r - 1) * (r + 2) / 6 * u ** 2
            + (r + 2) * j ** 2 + r * (r + 2) * u * j)


def serial_poly(p):
    return [{"exponent_r_a_b_c_d_s": list(k), "coefficient": str(v)}
            for k, v in sorted(p.co.items())]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    input_hash = sha(INPUT)
    data = json.loads(INPUT.read_text())
    r, a, b, c, d, s = [VARS[t] for t in ("r", "a", "b", "c", "d", "s")]
    den = r + 2
    j = a * d - b * c
    shifted_num = jnumerator(r, a + s, b, c, d + s)
    unshifted_num = jnumerator(r, a, b, c, d)
    constant_num = den ** 2 * (r + 3) * s ** 4 / 6
    first_num = den ** 2 * (2 * r + 3) * s ** 3 * a / 3
    second_tangent_num = den ** 2 * s ** 3 * d
    raw_quadratic_num = den * (((r + 1) * a + d) ** 2
                              + r * den * c ** 2 / 3 + den * j)
    cubic_num = den * (r * (d + (2 * r + 1) * a / 3) * (a ** 2 + c ** 2)
                       + 2 * j * ((r + 1) * a + d))
    check("frozen Jr full all-r Taylor polynomial identity",
          shifted_num == constant_num + first_num + second_tangent_num
          + s ** 2 * raw_quadratic_num + s * cubic_num + unshifted_num)
    check("original denominators cleared only by r+2",
          all(k[0] <= 3 for k in shifted_num.co), {"positive_on_claimed_domain": "r>0 implies r+2>0"})
    sigma1_num = -den ** 2 * s ** 2 * b + 7 * r * b ** 3 / 6
    sigma2_num = (den ** 2 * s ** 3 + den * (5 * r / 2 + 2) * s ** 2 * a
                  + den * 7 * r * s * a ** 2 / 4 + r * (4 * r + 3) * a ** 3 / 12)
    G_num = shifted_num - constant_num - first_num - sigma1_num * c - sigma2_num * d
    check("residual homogeneity in a b c d s", all(sum(k[1:]) == 4 for k in G_num.co))
    check("residual parameter degree at most three", all(k[0] <= 3 for k in G_num.co))
    check("no residual s3 or s4 terms", G_num.coefficient(5, 3) == 0 and G_num.coefficient(5, 4) == 0)
    check("all-r residual s2 coefficient", G_num.coefficient(5, 2) ==
          den * ((r + 1) ** 2 * a ** 2 + d ** 2 + r * den * c ** 2 / 3
                 + (r / 2 + 2) * a * d))

    z0 = [parse_basis(t) for t in data["z0"]]
    z1 = [parse_basis(t) for t in data["z1"]]
    expected0 = [j + s * (a + d), r * c * s, r * c * d, r * c ** 2,
                 r * b * c, r * a * s, r * a * d, r * a * c, r * a * b, r * a ** 2]
    expected1 = [d * s, d ** 2, c * s, c * d, c ** 2, b * d, b * c,
                 b ** 2, a * s, a * d, a * c, a * b, a ** 2,
                 r * (a ** 2 + 2 * a * s + c ** 2), r * a * s, r * c * s]
    check("certificate basis matches intended 10+16 polynomials", z0 == expected0 and z1 == expected1
          and data["block_split"] == 10)
    Q = [[F(t) for t in row] for row in data["gram"]]
    check("constant rational Gram dimension", len(Q) == 26 and all(len(row) == 26 for row in Q))
    check("exact Gram symmetry", Q == [list(t) for t in zip(*Q)])
    check("exact 10+16 Gram separation", all(Q[i][j0] == 0 for i in range(10) for j0 in range(10, 26)))
    reconstruction = P(0)
    for basis, start, weight in ((z0, 0, P(1)), (z1, 10, r)):
        for i, x in enumerate(basis):
            for j0, y in enumerate(basis):
                reconstruction += Q[start + i][start + j0] * weight * x * y
    check("independent exact all-r weighted Gram polynomial identity", reconstruction == G_num,
          {"nonzero_coefficients": len(G_num.co), "parameter_samples_used": 0})
    Q0 = [row[:10] for row in Q[:10]]
    Q1 = [row[10:] for row in Q[10:]]
    own_ldl = {}
    for label, matrix in (("Q0", Q0), ("Q1", Q1)):
        low, diag = ldl(matrix)
        check(label + " independent full exact LDL positivity and reconstruction", all(v > 0 for v in diag))
        own_ldl[label] = {"lower_triangular": serial_matrix(low), "pivots": [str(t) for t in diag]}
    blocks = data["positive_definite_blocks"]
    check("four exact blocks partition 26 coordinates",
          len(blocks) == 4 and [len(b) for b in blocks] == [6, 4, 10, 6]
          and sorted(sum(blocks, [])) == list(range(26)))
    check("four-block exact separation", all(Q[i][j0] == 0
          for bi, b0 in enumerate(blocks) for bj, b1 in enumerate(blocks)
          if bi != bj for i in b0 for j0 in b1))
    block_proofs = []
    for number, block in enumerate(blocks):
        B = [[Q[i][j0] for j0 in block] for i in block]
        minors = [det([row[:k] for row in B[:k]]) for k in range(1, len(block) + 1)]
        check("block " + str(number) + " independent exact Sylvester minors", all(v > 0 for v in minors))
        pivots = [minors[0]] + [minors[k] / minors[k - 1] for k in range(1, len(minors))]
        check("block " + str(number) + " declared pivots independently reproduced",
              [str(t) for t in pivots] == data["ldl_pivots"][number])
        block_proofs.append({"indices": block, "leading_minors": [str(t) for t in minors],
                             "pivots": [str(t) for t in pivots]})
    own_ldl["blocks"] = block_proofs
    # Independently audit the stronger floor from the final constructor proof.
    floor = F(1, 512)
    Q1_floor = [[Q1[i][j0] - (floor if i == j0 else F(0)) for j0 in range(16)] for i in range(16)]
    low, diag = ldl(Q1_floor)
    check("receiving-side Q1-I/512 exact floor", all(v > 0 for v in diag))
    own_ldl["Q1_minus_I_over_512"] = {"lower_triangular": serial_matrix(low), "pivots": [str(t) for t in diag]}

    check("r0 residual reduces to twice shifted determinant defect square",
          G_num.coefficient(0, 0) == 2 * (j + s * (a + d)) ** 2)
    check("Q1 includes all ten gradient quadratics and sa sc sd",
          z1[:13] == expected1[:13])
    gradients = [a, b, c, d]
    V2 = sum((x ** 2 for x in gradients), P(0))
    M4 = sum(((x * y) ** 2 for i, x in enumerate(gradients) for y in gradients[i:]), P(0))
    square_difference = sum(((x ** 2 - y ** 2) ** 2
                            for i, x in enumerate(gradients) for y in gradients[i + 1:]), P(0))
    check("exact improved M4 >= 5|A|4/8 square identity",
          M4 - 5 * V2 ** 2 / 8 == square_difference / 8)
    div_num = sigma1_num.derivative(2) + sigma2_num.derivative(1)
    expected_div_num = r / 4 * (6 * den * s ** 2 + 14 * den * s * a
                               + (4 * r + 3) * a ** 2 + 14 * b ** 2)
    check("all-r general-f divergence numerator", div_num == expected_div_num)
    check("stress entries depend only on opposite first-gradient coordinates",
          sigma1_num.derivative(1) == 0 and sigma2_num.derivative(2) == 0)
    # Audit the new nonsmooth nonseparated example. Here a is used as the
    # dummy t variable and b as the dummy radical variable in exact identities.
    t, radical = a, b
    wave_flux_num = 2 * sigma1_num.substitute({2: s * t}) + sigma2_num.substitute({1: 2 * s * t})
    normal_flux_num = den ** 2 + 3 * r * den * t + 7 * r * den * t ** 2 + r * (8 * r + 13) * t ** 3 / 3
    check("nonseparated wave exact normal-flux numerator", wave_flux_num == s ** 3 * normal_flux_num)
    Ar = 8 * r + 13
    Br = 92 * r + 181
    Cr = 236 * r + 469
    delta = 912 * r ** 2 + 6024 * r + 8373
    quadratic = 16 * Ar * t ** 2 + 4 * Br * t + Cr
    check("exact normal-flux factorization at tplus=1/4",
          normal_flux_num - normal_flux_num.substitute({1: P(F(1, 4))})
          == r / 48 * (t - F(1, 4)) * quadratic)
    check("nonseparated root discriminant polynomial", Br ** 2 - 4 * Ar * Cr == delta)
    check("nonseparated displayed root clears the quadratic",
          (-Br + radical) ** 2 + 2 * Br * (-Br + radical) + 4 * Ar * Cr == radical ** 2 - delta)
    check("nonseparated root sign identity", Br ** 2 - delta == 4 * Ar * Cr)
    check("nonseparated discriminant and sign factors positive on r>0",
          all(v > 0 for p in (Ar, Br, Cr, delta) for v in p.co.values()))
    check("input certificate unchanged", input_hash == sha(INPUT))
    receipt = {
        "schema": "independent-all-r-separated-stress-audit/1", "status": "PASS",
        "domain": "every real r>0; every real s; periodic W1,4 F,H and unrestricted periodic W1,4 g",
        "claim": "For each fixed r>0,s, if div(S1(f_y),S2(f_x))=0 distributionally: gap >=5r/[4096(r+2)] avg|Dphi|4 + r*s2/[512(r+2)] avg(f_x2+g_x2+g_y2). Includes every separated first potential and the stated nonseparated two-state wave.",
        "scope": "Exact all-r algebra and constant rational Gram positivity. Null pairing and Sobolev proof are written in ALL_R_AUDIT.md.",
        "excluded_claims": ["universal conformal quasiconvexity", "all matrix backgrounds", "historical priority", "external certification"],
        "checks": checks,
        "residual_numerator": serial_poly(G_num),
        "divergence_numerator": serial_poly(div_num),
        "positive_denominator": "r+2>0 for r>0",
        "positive_Gram_weight": "r>0",
        "independently_certified_Q1_floor": str(floor),
        "independently_certified_Jensen_bound": "5r/[4096(r+2)] avg|Dphi|^4 + r*s^2/[512(r+2)] avg(a^2+c^2+d^2)",
        "nonseparated_normal_flux_numerator": serial_poly(normal_flux_num),
        "nonseparated_equal_flux_quadratic": serial_poly(quadratic),
        "nonseparated_radical_discriminant": serial_poly(delta),
        "nonseparated_quantifier": "For each fixed r>0 and s!=0, choose its two-state F and f=sF(2x+y); arbitrary periodic W1,4 g. This does not imply a fixed-field all-s discriminant statement.",
        "certificate_sha256": input_hash,
        "original_source_sha256": sha(ROOT / "originals/conformal_packet/RESEARCH_REPORT.md"),
        "constructor_proof_sha256": sha(ROOT / "workers/ga_parametric_stress_genesis/ALL_R_THEOREM_PROOF.txt"),
        "self_sha256": sha(Path(__file__)), "own_matrix_library_sha256": sha(HERE / "exact_audit.py"),
        "python": platform.python_version(),
    }
    (HERE / "ALL_R_INDEPENDENT_LDL_CERTIFICATE.json").write_text(json.dumps(own_ldl, indent=2) + "\n")
    (HERE / "ALL_R_AUDIT_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "checks": len(checks),
                      "residual_coefficients": len(G_num.co), "input_sha256": input_hash,
                      "independently_certified_Q1_floor": receipt["independently_certified_Q1_floor"]}, indent=2))


if __name__ == "__main__":
    main()
