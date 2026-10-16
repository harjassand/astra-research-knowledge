"""Exact finite-state closure replay for path-map correctability.

This is a finite algebraic verification aid.  It does not prove a threshold,
scalable controller, physical implementation, or almost-sure termination from
the closure computation itself.  See REPORT.md for the model and scope.
"""

from __future__ import annotations

import json
import platform
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import sympy as sp


I2 = sp.eye(2)
I32 = sp.eye(32)
PAULI = {
    "I": I2,
    "X": sp.Matrix([[0, 1], [1, 0]]),
    "Y": sp.Matrix([[0, -sp.I], [sp.I, 0]]),
    "Z": sp.Matrix([[1, 0], [0, -1]]),
}
PHASE = sp.diag(1, sp.I)


def kron_all(mats: Iterable[sp.Matrix]) -> sp.Matrix:
    mats = list(mats)
    out = mats[0]
    for item in mats[1:]:
        out = sp.kronecker_product(out, item)
    return out


def pauli_string(word: str) -> sp.Matrix:
    return kron_all(PAULI[c] for c in word)


def five_qubit_code() -> tuple[sp.Matrix, sp.Matrix, list[sp.Matrix]]:
    """Return an exact [[5,1,3]] encoding isometry, logical X, and stabilizers."""
    stabilizer_words = ("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ")
    stabilizers = [pauli_string(w) for w in stabilizer_words]
    projector = I32
    for g in stabilizers:
        projector = projector * (I32 + g) / 2

    # The stabilizer projector has probability 1/16 on |00000>, so multiplying
    # by four gives a normalized +1 stabilizer state with rational entries.
    zero = sp.zeros(32, 1)
    zero[0, 0] = 1
    ket0 = 4 * projector * zero
    logical_x = pauli_string("XXXXX")
    ket1 = logical_x * ket0
    V = sp.Matrix.hstack(ket0, ket1)

    assert V.H * V == sp.eye(2)
    assert all(g * V == V for g in stabilizers)
    assert logical_x * V == V * sp.Matrix([[0, 1], [1, 0]])
    return V, logical_x, stabilizers


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    kraus: sp.Matrix
    fault_cost: int
    label: str


@dataclass
class Graph:
    states: tuple[str, ...]
    initial: str
    accepting_flags: dict[str, str]
    edges: tuple[Edge, ...]

    def outgoing(self, state: str) -> tuple[Edge, ...]:
        return tuple(e for e in self.edges if e.src == state)


def state_graph_one_site(V: sp.Matrix, *, include_logical_x: bool) -> Graph:
    """A TP graph with cold/hot latch states and accepting terminal flag.

    Cold has two noncommuting zero-cost gate loops, one primitive X_1 fault
    edge that sets a persistent hot latch, and one exit.  Hot has the same
    repeated zero-cost gates and two equivalent exit Kraus outcomes.  The
    hot latch can therefore enable arbitrarily many later gates for one
    primitive fault.  Every local instrument is trace preserving.
    """
    del V  # Dimensions are fixed by the five-qubit example.
    X1 = sp.kronecker_product(PAULI["X"], sp.eye(16))
    S1 = sp.kronecker_product(PHASE, sp.eye(16))
    LX = pauli_string("XXXXX")
    cold, hot, accept = "cold", "hot", "accept"
    edges: list[Edge] = []

    if include_logical_x:
        # Nine Kraus outcomes of norm 1/3 give an exact TP instrument with
        # three loop/fault branches and six parallel accepting outcomes.
        scale = sp.Rational(1, 3)
        for q in (cold, hot):
            edges.extend([
                Edge(q, q, scale * X1, 0, "X1-loop"),
                Edge(q, q, scale * S1, 0, "S1-loop"),
                Edge(q, q, scale * LX, 0, "logical-X-loop"),
            ])
        edges.append(Edge(cold, hot, scale * X1, 1, "primitive-X1-fault; latch-on"))
        for q in (cold, hot):
            exit_count = 5 if q == cold else 6
            for j in range(exit_count):
                edges.append(Edge(q, accept, scale * I32, 0, f"accept-{j + 1}"))
    else:
        scale = sp.Rational(1, 2)
        edges.extend([
            Edge(cold, cold, scale * X1, 0, "X1-loop"),
            Edge(cold, cold, scale * S1, 0, "S1-loop"),
            Edge(cold, hot, scale * X1, 1, "primitive-X1-fault; latch-on"),
            Edge(cold, accept, scale * I32, 0, "accept"),
            Edge(hot, hot, scale * X1, 0, "X1-loop-after-latch"),
            Edge(hot, hot, scale * S1, 0, "S1-loop-after-latch"),
            Edge(hot, accept, scale * I32, 0, "accept-1"),
            Edge(hot, accept, scale * I32, 0, "accept-2"),
        ])
    return Graph((cold, hot, accept), cold, {accept: "accepted"}, tuple(edges))


def flag_graph() -> Graph:
    """Two trusted terminal flags record whether logical X was applied."""
    LX = pauli_string("XXXXX")
    i0, f0, f1 = "initial", "flag0", "flag1"
    half = sp.Rational(1, 2)
    # Four outcomes at amplitude 1/2 make the initial instrument TP.  The
    # duplicate same-flag Kraus operators are ordinary distinct outcomes.
    edges = (
        Edge(i0, f0, half * I32, 0, "flag0-identity-a"),
        Edge(i0, f0, half * I32, 0, "flag0-identity-b"),
        Edge(i0, f1, half * LX, 0, "flag1-logical-X-a"),
        Edge(i0, f1, half * LX, 0, "flag1-logical-X-b"),
    )
    return Graph((i0, f0, f1), i0, {f0: "parity-0", f1: "parity-1"}, edges)


def flat(M: sp.Matrix) -> list[sp.Expr]:
    return [sp.simplify(M[i, j]) for i in range(M.rows) for j in range(M.cols)]


def unflat(v: list[sp.Expr], rows: int, cols: int) -> sp.Matrix:
    return sp.Matrix(rows, cols, v)


def is_zero(x: sp.Expr) -> bool:
    return sp.simplify(x) == 0


def insert_exact(basis: dict[int, list[sp.Expr]], vector: list[sp.Expr]) -> list[sp.Expr] | None:
    """Insert a vector into a forward-echelon basis over Q(i), if independent."""
    v = [sp.simplify(x) for x in vector]
    for pivot in sorted(basis):
        coefficient = v[pivot]
        if not is_zero(coefficient):
            row = basis[pivot]
            v = [sp.simplify(x - coefficient * y) for x, y in zip(v, row)]
    pivot = next((j for j, value in enumerate(v) if not is_zero(value)), None)
    if pivot is None:
        return None
    scale = v[pivot]
    v = [sp.simplify(x / scale) for x in v]
    basis[pivot] = v
    return v


def reachable_spaces(graph: Graph, V: sp.Matrix, fault_budget: int) -> tuple[dict[tuple[str, int], dict[int, list[sp.Expr]]], int]:
    """Compute least linear spaces closed under every budget-respecting edge."""
    spaces: dict[tuple[str, int], dict[int, list[sp.Expr]]] = {}
    work: deque[tuple[str, int, list[sp.Expr]]] = deque()

    def add(state: str, budget: int, vector: list[sp.Expr]) -> None:
        loc = (state, budget)
        basis = spaces.setdefault(loc, {})
        new_vector = insert_exact(basis, vector)
        if new_vector is not None:
            work.append((state, budget, new_vector))

    add(graph.initial, 0, flat(V))
    while work:
        state, budget, vector = work.popleft()
        source = unflat(vector, V.rows, V.cols)
        for edge in graph.outgoing(state):
            next_budget = budget + edge.fault_cost
            if next_budget > fault_budget:
                continue
            image = edge.kraus * source
            add(edge.dst, next_budget, flat(image))

    # The ambient bound is |Q|*(f+1)*D*k scalar dimensions.  Every successful
    # insertion consumes one dimension, so worklist saturation must stop.
    inserted = sum(len(basis) for basis in spaces.values())
    assert inserted <= len(graph.states) * (fault_budget + 1) * V.rows * V.cols
    return spaces, inserted


def location_matrices(spaces: dict[tuple[str, int], dict[int, list[sp.Expr]]],
                      V: sp.Matrix, locations: Iterable[tuple[str, int]]) -> list[sp.Matrix]:
    out: list[sp.Matrix] = []
    for loc in locations:
        for vector in spaces.get(loc, {}).values():
            out.append(unflat(vector, V.rows, V.cols))
    return out


def independent_union(matrices: Iterable[sp.Matrix], D: int, k: int) -> list[sp.Matrix]:
    basis: dict[int, list[sp.Expr]] = {}
    for M in matrices:
        insert_exact(basis, flat(M))
    return [unflat(v, D, k) for _, v in sorted(basis.items())]


def scalar_identity_witness(G: sp.Matrix) -> bool:
    if G.rows != G.cols:
        return False
    return all(is_zero(G[i, j]) for i in range(G.rows) for j in range(G.cols) if i != j) and all(
        is_zero(G[i, i] - G[0, 0]) for i in range(1, G.rows)
    )


def kl_check(maps: list[sp.Matrix]) -> tuple[bool, dict | None]:
    for i, A in enumerate(maps):
        for j, B in enumerate(maps):
            gram = sp.simplify(A.H * B)
            if not scalar_identity_witness(gram):
                return False, {"left_basis_index": i, "right_basis_index": j,
                               "gram": matrix_json(gram)}
    return True, None


def scalar_multiple(G: sp.Matrix, U: sp.Matrix) -> tuple[bool, sp.Expr | None]:
    alpha = None
    for i in range(G.rows):
        for j in range(G.cols):
            if not is_zero(U[i, j]):
                alpha = sp.simplify(G[i, j] / U[i, j])
                break
        if alpha is not None:
            break
    if alpha is None:
        return G == sp.zeros(*G.shape), sp.Integer(0)
    return all(is_zero(G[i, j] - alpha * U[i, j])
               for i in range(G.rows) for j in range(G.cols)), alpha


def fixed_decoder_check(maps: list[sp.Matrix], decoder_kraus: list[sp.Matrix],
                        intended_U: sp.Matrix) -> tuple[bool, dict | None]:
    """Each prescribed branch D_r A must be alpha U for every span basis A."""
    for r, D in enumerate(decoder_kraus):
        for a, A in enumerate(maps):
            ok, alpha = scalar_multiple(D * A, intended_U)
            if not ok:
                return False, {"decoder_kraus_index": r, "terminal_basis_index": a,
                               "product": matrix_json(D * A),
                               "intended_U": matrix_json(intended_U)}
    return True, None


def decoder_5qubit(V: sp.Matrix, stabilizers: list[sp.Matrix]) -> tuple[list[sp.Matrix], dict]:
    """Build and verify the standard 16-syndrome single-qubit decoder."""
    errors = [sp.eye(32)]
    labels = ["IIIII"]
    for site in range(5):
        for p in "XYZ":
            word = ["I"] * 5
            word[site] = p
            labels.append("".join(word))
            errors.append(pauli_string(labels[-1]))

    Pcode = V * V.H
    syndrome_projectors = [sp.simplify(E * Pcode * E.H) for E in errors]
    projectors_orthogonal = all(
        sp.simplify(syndrome_projectors[i] * syndrome_projectors[j]) == sp.zeros(32)
        for i in range(len(errors)) for j in range(i)
    )
    projectors_sum_to_identity = sp.simplify(sum(syndrome_projectors, sp.zeros(32))) == I32
    decoders = [sp.simplify(V.H * E.H * P) for E, P in zip(errors, syndrome_projectors)]
    decoder_tp = sp.simplify(sum((D.H * D for D in decoders), sp.zeros(32))) == I32
    report = {
        "error_representatives": labels,
        "syndrome_count": len(errors),
        "projectors_pairwise_orthogonal": projectors_orthogonal,
        "projectors_sum_to_identity": projectors_sum_to_identity,
        "decoder_kraus_sum_DdaggerD_is_identity": decoder_tp,
    }
    assert len(errors) == 16 and projectors_orthogonal and projectors_sum_to_identity and decoder_tp
    return decoders, report


def matrix_json(M: sp.Matrix) -> list[list[str]]:
    return [[str(sp.simplify(M[i, j])) for j in range(M.cols)] for i in range(M.rows)]


def graph_tp_check(graph: Graph, D: int) -> dict:
    rows: dict[str, dict] = {}
    for state in graph.states:
        outgoing = graph.outgoing(state)
        if not outgoing:
            continue
        total = sp.simplify(sum((edge.kraus.H * edge.kraus for edge in outgoing), sp.zeros(D)))
        rows[state] = {
            "outgoing_edge_count": len(outgoing),
            "sum_KdaggerK_is_identity": total == sp.eye(D),
            "edge_labels": [edge.label for edge in outgoing],
        }
    return {"states": rows, "all_nonterminal_local_instruments_TP": all(
        r["sum_KdaggerK_is_identity"] for r in rows.values()
    )}


def one_site_absorption_probabilities(graph: Graph) -> dict[str, str]:
    """Solve the exact controller-only hitting equations for test-one graph."""
    # All edge Kraus operators are scalar times unitaries, so each branch has
    # input-independent probability |scalar|^2.  Solve p=q_exit+Qp exactly.
    transient = [q for q in graph.states if q not in graph.accepting_flags]
    Q = sp.zeros(len(transient))
    r = sp.zeros(len(transient), 1)
    for i, q in enumerate(transient):
        for edge in graph.outgoing(q):
            # Verify Kdagger K = p I, avoiding a state-dependent probability.
            M = sp.simplify(edge.kraus.H * edge.kraus)
            if M != M[0, 0] * sp.eye(M.rows):
                raise ValueError("controller transition probability depends on data")
            probability = sp.simplify(M[0, 0])
            if edge.dst in graph.accepting_flags:
                r[i, 0] += probability
            else:
                Q[i, transient.index(edge.dst)] += probability
    probabilities = (sp.eye(len(transient)) - Q).inv() * r
    return {q: str(sp.simplify(probabilities[i, 0])) for i, q in enumerate(transient)}


def run_replay() -> dict:
    V, logical_x, stabilizers = five_qubit_code()
    X1 = sp.kronecker_product(PAULI["X"], sp.eye(16))
    S1 = sp.kronecker_product(PHASE, sp.eye(16))
    assert X1 * S1 != S1 * X1

    decoder, decoder_report = decoder_5qubit(V, stabilizers)
    identity2 = sp.eye(2)

    # Test 1: arbitrarily long, noncommuting histories (plus one bounded fault)
    # remain within the single-qubit operator algebra on physical qubit one.
    graph1 = state_graph_one_site(V, include_logical_x=False)
    spaces1, insertions1 = reachable_spaces(graph1, V, fault_budget=1)
    accepted1 = independent_union(
        location_matrices(spaces1, V, [("accept", 0), ("accept", 1)]), V.rows, V.cols
    )
    kl1, kl_witness1 = kl_check(accepted1)
    fixed1_ok, fixed1_witness = fixed_decoder_check(accepted1, decoder, identity2)
    graph1_tp = graph_tp_check(graph1, V.rows)
    absorption1 = one_site_absorption_probabilities(graph1)

    # Reachable operator spaces at cold/hot/accept are all 4-dimensional copies
    # of the full 2x2 single-qubit algebra acting on the code.
    dims1 = {f"{q}|faults={b}": len(basis) for (q, b), basis in sorted(spaces1.items())}
    assert kl1 and fixed1_ok and graph1_tp["all_nonterminal_local_instruments_TP"]
    assert absorption1 == {"cold": "1", "hot": "1"}
    assert all(dim == 4 for dim in dims1.values())

    # Test 2: add an unrecorded logical-X loop.  The terminal span now contains
    # V and X_L V, whose Gram is X_L|code = logical X, a nonscalar witness.
    graph2 = state_graph_one_site(V, include_logical_x=True)
    graph2_tp = graph_tp_check(graph2, V.rows)
    spaces2, insertions2 = reachable_spaces(graph2, V, fault_budget=1)
    accepted2 = independent_union(
        location_matrices(spaces2, V, [("accept", 0), ("accept", 1)]), V.rows, V.cols
    )
    kl2, kl_witness2 = kl_check(accepted2)
    decoder2, decoder_witness2 = fixed_decoder_check(accepted2, decoder, identity2)
    absorption2 = one_site_absorption_probabilities(graph2)
    explicit_logical_witness = sp.simplify(V.H * logical_x * V)
    assert logical_x == logical_x.H and not scalar_identity_witness(explicit_logical_witness)
    assert not kl2 and not decoder2
    assert absorption2 == {"cold": "1", "hot": "1"}
    assert graph2_tp["all_nonterminal_local_instruments_TP"]

    # Test 3: a trusted classical parity flag separates I from logical X.  Each
    # output flag alone is correctable; erasing/forgetting the flag is not.
    graph3 = flag_graph()
    spaces3, insertions3 = reachable_spaces(graph3, V, fault_budget=0)
    by_flag = {}
    for state, flag in graph3.accepting_flags.items():
        maps = independent_union(location_matrices(spaces3, V, [(state, 0)]), V.rows, V.cols)
        ok, witness = kl_check(maps)
        by_flag[flag] = {"correctable": ok, "dimension": len(maps), "witness": witness}
        assert ok
    forgotten = independent_union(
        location_matrices(spaces3, V, [("flag0", 0), ("flag1", 0)]), V.rows, V.cols
    )
    forgotten_ok, forgotten_witness = kl_check(forgotten)
    decoder0 = [V.H]
    flag_decoder1 = [V.H * logical_x.H]
    flag0_fixed, flag0_witness = fixed_decoder_check(
        independent_union(location_matrices(spaces3, V, [("flag0", 0)]), V.rows, V.cols),
        decoder0, identity2,
    )
    flag1_fixed, flag1_fixed_witness = fixed_decoder_check(
        independent_union(location_matrices(spaces3, V, [("flag1", 0)]), V.rows, V.cols),
        flag_decoder1, identity2,
    )
    flag_tp = graph_tp_check(graph3, V.rows)
    flag_accept_probability = sp.simplify(sum(
        (edge.kraus.H * edge.kraus)[0, 0] for edge in graph3.edges
        if edge.dst in graph3.accepting_flags
    ))
    assert not forgotten_ok and flag0_fixed and flag1_fixed
    assert flag_tp["all_nonterminal_local_instruments_TP"]
    assert flag_accept_probability == 1

    # A model-independent invariant: total inserted dimension cannot exceed
    # |Q|(f+1)Dk, regardless of history length or noncommutativity.
    bound1 = len(graph1.states) * 2 * V.rows * V.cols
    bound2 = len(graph2.states) * 2 * V.rows * V.cols
    bound3 = len(graph3.states) * 1 * V.rows * V.cols
    assert insertions1 <= bound1 and insertions2 <= bound2 and insertions3 <= bound3

    return {
        "schema": "finite-history-kraus-closure-replay-v1",
        "field": "Gaussian rationals Q(i)",
        "runtime": {"python": platform.python_version(), "sympy": sp.__version__},
        "initial_code": {
            "name": "five-qubit perfect stabilizer code [[5,1,3]]",
            "physical_dimension_D": V.rows,
            "logical_dimension_k": V.cols,
            "encoding_isometry_V": matrix_json(V),
            "logical_X": matrix_json(sp.Matrix([[0, 1], [1, 0]])),
            "stabilizer_words": ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"],
        },
        "closure_rule": "least spaces L_(q,b) seeded by V and closed under K_e left multiplication; positive fault_cost increments b; retain only b<=f",
        "dimension_bound": "at most |Q|*(f+1)*D*k independent insertions",
        "tests": {
            "one_site_unbounded_history": {
                "description": "Noncommuting X1 and S1 loops run for unbounded history length; a single X1 fault sets a persistent latch that permits further zero-cost gate loops; all accepted maps stay on physical qubit 1.",
                "fault_budget": 1,
                "graph_states": list(graph1.states),
                "edge_labels": [e.label for e in graph1.edges],
                "noncommuting_loop_check": X1 * S1 != S1 * X1,
                "reachable_layer_dimensions": dims1,
                "total_independent_insertions": insertions1,
                "dimension_bound": bound1,
                "accepted_span_dimension": len(accepted1),
                "knill_laflamme": kl1,
                "fixed_5qubit_syndrome_decoder_intended_identity": fixed1_ok,
                "fixed_decoder_failure": fixed1_witness,
                "local_tp_check": graph1_tp,
                "controller_acceptance_probability_by_transient_state": absorption1,
                "decoder_construction": decoder_report,
            },
            "unrecorded_logical_x_loop": {
                "description": "The same bounded-latch controller additionally permits an unrecorded logical X_L loop at zero primitive-fault cost.",
                "fault_budget": 1,
                "reachable_layer_dimensions": {f"{q}|faults={b}": len(basis) for (q, b), basis in sorted(spaces2.items())},
                "total_independent_insertions": insertions2,
                "dimension_bound": bound2,
                "accepted_span_dimension": len(accepted2),
                "knill_laflamme": kl2,
                "fixed_5qubit_syndrome_decoder_intended_identity": decoder2,
                "kl_failure_witness": kl_witness2,
                "fixed_decoder_failure": decoder_witness2,
                "controller_acceptance_probability_by_transient_state": absorption2,
                "explicit_path_pair_witness": {
                    "left_path_map": "V",
                    "right_path_map": "X_L V",
                    "Vdagger_XLV": matrix_json(explicit_logical_witness),
                    "is_scalar_identity": scalar_identity_witness(explicit_logical_witness),
                },
                "local_tp_check": graph2_tp,
            },
            "trusted_flag_then_forgetting": {
                "description": "Initial controller records parity in terminal output: flag 0 applies I; flag 1 applies X_L. Separate trusted flags are decoded separately; erasing the flag combines the two path-map families.",
                "per_flag": by_flag,
                "per_flag_fixed_decoders_intended_identity": {
                    "parity-0": {"correct": flag0_fixed, "failure": flag0_witness,
                                  "decoder": matrix_json(decoder0[0])},
                    "parity-1": {"correct": flag1_fixed, "failure": flag1_fixed_witness,
                                  "decoder": matrix_json(flag_decoder1[0])},
                },
                "forgotten_flag_correctable": forgotten_ok,
                "forgotten_flag_failure_witness": forgotten_witness,
                "one_step_total_acceptance_probability": str(flag_accept_probability),
                "local_tp_check": flag_tp,
            },
        },
        "scope": {
            "established": [
                "exact finite-state saturation over Q(i) for the supplied graphs",
                "the standard Knill-Laflamme pairwise Gram condition on accepted path-map spans",
                "exact fixed-decoder branch checks for the supplied decoder Kraus maps",
                "separate exact local-instrument completeness and controller absorption checks",
            ],
            "not_established": [
                "novelty of the finite-dimensional saturation argument",
                "scalable or asymptotic fault tolerance, a threshold, or physical implementation",
                "controller correctness beyond the stated graph, allowed edges, budget, and output flags",
                "any termination or acceptance fact from the vector-space closure calculation alone",
            ],
            "literature_position": "This is a finite-algebra verification instance of standard reachable-subspace saturation plus the Knill-Laflamme criterion. No novelty claim is made; distinguish this exact computation from a literature-priority review.",
        },
    }


def main() -> None:
    result = run_replay()
    here = Path(__file__).resolve().parent
    out = here / "replay.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "replay": str(out),
        "test1_KL": result["tests"]["one_site_unbounded_history"]["knill_laflamme"],
        "test1_fixed_decoder": result["tests"]["one_site_unbounded_history"]["fixed_5qubit_syndrome_decoder_intended_identity"],
        "test2_KL": result["tests"]["unrecorded_logical_x_loop"]["knill_laflamme"],
        "test3_flags": {k: v["correctable"] for k, v in result["tests"]["trusted_flag_then_forgetting"]["per_flag"].items()},
        "test3_forgotten_flag": result["tests"]["trusted_flag_then_forgetting"]["forgotten_flag_correctable"],
    }, indent=2))


if __name__ == "__main__":
    main()
