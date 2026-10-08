"""Bounded exact audit of two displayed examples, not theorem certification."""
from pathlib import Path
import json
import sympy as s

R = s.Rational
I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
paulis = [I, X, Y, Z]
kron = s.kronecker_product


def partial_a(mat):
    return s.Matrix(2, 2, lambda b, c: sum(mat[2*i+b, 2*i+c] for i in range(2)))


def partial_b(mat):
    return s.Matrix(2, 2, lambda a, c: sum(mat[2*a+i, 2*c+i] for i in range(2)))


def clone_product(mat):
    return (R(4, 9)*mat
            + R(1, 9)*(kron(partial_b(mat), I)+kron(I, partial_a(mat)))
            + R(1, 36)*mat.trace()*s.eye(4))


# Exact rectangular-code trace and identity failure, followed by the
# tempting common trace normalization. The normalized marginal violates
# the proved three-Pauli broadcaster star inequality.
V = s.Matrix([[1, 0], [0, 0], [0, 0], [0, 1]])
compressed = lambda a: V.H*clone_product(V*a*V.H)*V
assert compressed(s.diag(1, 0)).trace() == R(13, 18)
assert compressed(I) == R(13, 18)*I
normalized = lambda a: R(18, 13)*compressed(a)
normalized_eigenvalues = [R(8, 13), R(8, 13), R(12, 13)]
for a, value in zip(paulis[1:], normalized_eigenvalues):
    assert normalized(a) == value*a
assert sum(normalized_eigenvalues) == R(28, 13) > 2

# One-edge graph instance: both channels are Pauli diagonal. This audits
# the graph-weight formula and full quadratic-form comparison, while
# showing that the displayed channel is not a product of local maps.
U = s.diag(1, 1, 1, -1)
eta, mu = R(2, 3), R(1, 3)
graph = []
for ai, a in enumerate(paulis):
    for bi, b in enumerate(paulis):
        P = kron(a, b)
        transformed = U.H*P*U
        hits = []
        for ci, c in enumerate(paulis):
            for di, d in enumerate(paulis):
                q = kron(c, d)
                if transformed == q or transformed == -q:
                    hits.append(int(ci != 0)+int(di != 0))
        assert len(hits) == 1
        wt, wt_encoded = int(ai != 0)+int(bi != 0), hits[0]
        ph = (eta**wt+eta**wt_encoded)/2
        ps = (mu**wt+mu**wt_encoded)/2
        residual = 2*(1-ph)-(1-ps)
        assert residual >= 0
        graph.append({"pauli_indices": [ai, bi], "weights": [wt, wt_encoded],
                      "phi_eigenvalue": str(ph), "psi_eigenvalue": str(ps),
                      "C2_residual": str(residual)})
values = {tuple(item["pauli_indices"]): s.sympify(item["phi_eigenvalue"])
          for item in graph}
assert values[(1, 0)] == values[(0, 1)] == R(5, 9)
assert values[(1, 1)] == R(4, 9) != values[(1, 0)]*values[(0, 1)]

result = {
    "status": "PASS",
    "scope": "two exact displayed-example audits; not quantified theorem certification",
    "rectangular_code": {
        "retained_trace": "13/18", "image_of_identity": "(13/18)I2",
        "normalized_Pauli_eigenvalues": [str(a) for a in normalized_eigenvalues],
        "normalized_Pauli_sum": "28/13",
        "normalized_marginal_self_compatible": False,
        "reason": "three-Pauli star bound requires eigenvalue sum <= 2"
    },
    "one_edge_graph": graph
}
Path(__file__).with_name("EXTRA_FORMULA_AUDIT.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": "PASS", "graph_basis_directions": len(graph),
                  "code_normalized_Pauli_sum": "28/13"}, indent=2))
