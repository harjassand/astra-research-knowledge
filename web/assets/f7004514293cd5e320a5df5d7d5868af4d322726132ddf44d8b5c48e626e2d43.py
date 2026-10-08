#!/usr/bin/env python3
"""Exact finite controls for the groups/operator cycle-2 audit.

This checks (i) the local residual-p and trace examples, and (ii) two small
planar band diagrams that exercise the N129 same-edge disk surgeries.  The
K4 diagrams are local surgery controls; they do not satisfy or test the
large closed-system exclusion needed by the full N129 theorem.
"""
from collections import deque
from itertools import combinations
import json
from pathlib import Path


INV = {"a": "A", "A": "a", "b": "B", "B": "b",
       "c": "C", "C": "c"}


def inv_word(word):
    return "".join(INV[x] for x in reversed(word))


def cyclically_reduced(word):
    return all(word[(i + 1) % len(word)] != INV[word[i]]
               for i in range(len(word))) if word else True


def free_reduce(word):
    out = []
    for x in word:
        if out and out[-1] == INV[x]:
            out.pop()
        else:
            out.append(x)
    return "".join(out)


def ribbon_faces(rotations, paired_darts):
    """Return face cycles of an orientable ribbon map.

    Darts are (vertex, position).  `rotations[v]` is a cyclic order of
    positions; paired_darts is a list of unordered pairs of darts.
    Face successor is sigma after edge reversal.
    """
    alpha = {}
    for x, y in paired_darts:
        assert x not in alpha and y not in alpha
        alpha[x] = y
        alpha[y] = x
    sigma = {}
    for v, positions in rotations.items():
        for i, pos in enumerate(positions):
            sigma[(v, pos)] = (v, positions[(i + 1) % len(positions)])
    assert set(alpha) == set(sigma)
    phi = {dart: sigma[alpha[dart]] for dart in sigma}
    seen, faces = set(), []
    for dart in phi:
        if dart in seen:
            continue
        face, x = [], dart
        while x not in seen:
            seen.add(x)
            face.append(x)
            x = phi[x]
        assert x == dart
        faces.append(face)
    return faces


def rotation_component(rotations, pairs, labels):
    """Check inverse labels, complete pairing, no monogon, and Euler genus."""
    for x, y in pairs:
        assert labels[x] == INV[labels[y]], (x, y, labels[x], labels[y])
    faces = ribbon_faces(rotations, pairs)
    assert all(len(face) >= 2 for face in faces), faces
    vertices = len(rotations)
    edges = len(pairs)
    chi = vertices - edges + len(faces)
    assert chi == 2, (vertices, edges, len(faces), faces)
    return {"V": vertices, "E": edges, "F": len(faces),
            "chi": chi, "face_lengths": sorted(map(len, faces)),
            "face_cycles": [[f"{v}:{i}" for v, i in face] for face in faces]}


def k4_graph():
    # Proper 3-edge-colouring of K4; low-to-high orientation has label a,b,c.
    edges = [(0, 1, "a"), (2, 3, "a"), (0, 2, "b"),
             (1, 3, "b"), (0, 3, "c"), (1, 2, "c")]
    oriented = []
    for eid, (u, v, label) in enumerate(edges):
        oriented.append((u, v, label, eid))
        oriented.append((v, u, INV[label], eid))
    return edges, oriented


def edge_path(oriented, vertices):
    out = []
    for u, v in zip(vertices, vertices[1:]):
        matches = [x for x in oriented if x[0] == u and x[1] == v]
        assert len(matches) == 1
        out.append(matches[0])
    return out


def closure_bound(oriented):
    """Exact BFS for every first/last directed-edge state in K4."""
    starts = {}
    for i, (u, v, _, _) in enumerate(oriented):
        starts.setdefault(u, []).append(i)
    reverse = {i: i ^ 1 for i in range(len(oriented))}
    max_len = 0
    witness = None
    for first in range(len(oriented)):
        p = oriented[first][0]
        for last in range(len(oriented)):
            end = oriented[last][1]
            # Empty closure is allowed exactly when the segment was already
            # cyclically closed and its last/first edges do not cancel.
            if end == p and last != reverse[first]:
                continue
            queue = deque([(end, last, ())])
            seen = {(end, last)}
            found = None
            while queue:
                vertex, previous, path = queue.popleft()
                for nxt in starts[vertex]:
                    if nxt == reverse[previous]:
                        continue
                    next_path = path + (nxt,)
                    target = oriented[nxt][1]
                    if target == p and nxt != reverse[first]:
                        found = next_path
                        break
                    state = (target, nxt)
                    if state not in seen:
                        seen.add(state)
                        queue.append((target, nxt, next_path))
                if found is not None:
                    break
            assert found is not None
            if len(found) > max_len:
                max_len = len(found)
                witness = (first, last, found)
    return max_len, witness


def finite_group_algebra_controls():
    # F_2[C_3]: e=x+x^2 is a proper idempotent with augmentation and
    # identity coefficient both zero.  C3 fails the no p-power-conjugacy
    # condition, so this only refutes the generic trace-faithfulness step.
    e = {1, 2}  # coefficients are 1; exponents are modulo 3.
    product = {}
    for i in e:
        for j in e:
            k = (i + j) % 3
            product[k] = product.get(k, 0) ^ 1
    product = {k for k, c in product.items() if c}
    assert product == e
    augmentation = len(e) % 2
    identity_coefficient = int(0 in e)
    assert augmentation == identity_coefficient == 0
    assert e != set() and e != {0}

    # Exhaustively verify that F2[P] has only 0,1 idempotents for P=C2 and
    # P=C2 x C2 (the induction basis/control cases of the local-ring proof).
    local_counts = {}
    for rank in (1, 2):
        n = 1 << rank
        elements = range(1 << n)

        def mul(x, y):
            out = 0
            for i in range(n):
                if (x >> i) & 1:
                    for j in range(n):
                        if (y >> j) & 1:
                            out ^= 1 << (i ^ j)
            return out

        idempotents = [x for x in elements if mul(x, x) == x]
        assert idempotents == [0, 1]
        local_counts[f"C2^{rank}"] = len(idempotents)
    return {"F2C3_control": {"idempotent": "x+x^2", "square": "x+x^2",
                             "augmentation": 0, "identity_coefficient": 0,
                             "scope": "generic trace control only; C3 violates the hypotheses"},
            "finite_p_group_checks": local_counts}


def disk_controls():
    edges, oriented = k4_graph()
    # The proper edge-colouring makes the map K4 -> rose(a,b,c) immersive.
    for vertex in range(4):
        outgoing = [label for u, _, label, _ in oriented if u == vertex]
        assert len(outgoing) == 3 and len(set(outgoing)) == 3
    assert {tuple(sorted((u, v))) for u, v, _ in edges} == set(combinations(range(4), 2))
    girth = 3  # K4 contains triangles and is simple.
    max_closure, closure_witness = closure_bound(oriented)
    assert max_closure == girth

    # Distinct-inner-disk same-edge surgery.
    e = edge_path(oriented, [0, 1])
    P = edge_path(oriented, [1, 2, 3, 0])
    Q = edge_path(oriented, [0, 3, 2, 1])
    assert P[0][0] == e[0][1] and P[-1][1] == e[0][0]
    assert Q[0][0] == e[0][0] and Q[-1][1] == e[0][1]
    assert [(x[3]) for x in Q] == [x[3] for x in reversed(P)]
    word1 = "".join(x[2] for x in e + P)
    word2 = "".join(x[2] for x in [(e[0][1], e[0][0], INV[e[0][2]], e[0][3])] + Q)
    assert cyclically_reduced(word1) and cyclically_reduced(word2)
    assert word1 == "acaC" and word2 == "AcAC"  # exact rose words
    spliced = "".join(x[2] for x in P + Q)
    assert free_reduce(spliced) == ""

    # Four parallel comparison bands: e/e^-1 plus the three reverse-path
    # pairs.  Rotations are in boundary-position order.
    xlabels = [x[2] for x in e + P]
    ypath = [(e[0][1], e[0][0], INV[e[0][2]], e[0][3])] + Q
    ylabels = [x[2] for x in ypath]
    x_pos_to_y_pos = {0: 0, 1: 3, 2: 2, 3: 1}
    xrot = {("X", i): xlabels[i] for i in range(4)}
    yrot = {("Y", i): ylabels[i] for i in range(4)}
    xpairs = [(('X', i), ('Y', j)) for i, j in x_pos_to_y_pos.items()]
    distinct_map = rotation_component({"X": list(range(4)), "Y": list(range(4))},
                                      xpairs, {**xrot, **yrot})

    # Nonempty outer boundary component: inner cycle is inverse to w=acB.
    wpath = edge_path(oriented, [0, 1, 2, 0])
    cpath = edge_path(oriented, [0, 2, 1, 0])
    w = "".join(x[2] for x in wpath)
    cword = "".join(x[2] for x in cpath)
    assert w == "acB" and cword == "bCA" and cword == inv_word(w)
    copairs = [(('C', 0), ('O', 2)), (('C', 1), ('O', 1)),
               (('C', 2), ('O', 0))]
    co_map = rotation_component({"C": [0, 1, 2], "O": [0, 1, 2]}, copairs,
                                {("C", i): cword[i] for i in range(3)} |
                                {("O", i): w[i] for i in range(3)})
    distinct_combined = {"V": 4, "E": 7,
                         "F": distinct_map["F"] + co_map["F"] - 1}
    assert distinct_combined["V"] - distinct_combined["E"] + distinct_combined["F"] == 3
    assert distinct_combined["F"] == 6  # two planar components, one nested
    h_before_distinct = len(e + P) + len([(e[0][1], e[0][0], INV[e[0][2]], e[0][3])] + Q) + len(cpath)
    h_after_distinct = len(cpath)
    assert (h_before_distinct, h_after_distinct, w) == (11, 3, "acB")

    # Self-paired same-edge surgery, with the two path blocks supported by
    # their inverse triangular caps U,V.  This gives a planar ribbon map.
    D = edge_path(oriented, [0, 1]) + edge_path(oriented, [1, 2, 3, 1]) + \
        edge_path(oriented, [1, 0]) + edge_path(oriented, [0, 3, 2, 0])
    U = edge_path(oriented, [1, 3, 2, 1])
    V = edge_path(oriented, [0, 2, 3, 0])
    dword, uword, vword = ("".join(x[2] for x in path) for path in (D, U, V))
    assert dword == "ac aBAcAB".replace(" ", "")
    assert uword == "bAC" and vword == "baC"
    assert all(cyclically_reduced(word) for word in (dword, uword, vword, w))
    assert D[0][3] == D[4][3] and D[0][2] == INV[D[4][2]]

    dlabels = list(dword)
    ulabels = list(uword)
    vlabels = list(vword)
    self_pairs = [(('D', 0), ('D', 4)),
                  (('D', 1), ('U', 2)), (('D', 2), ('U', 1)),
                  (('D', 3), ('U', 0)),
                  (('D', 5), ('V', 2)), (('D', 6), ('V', 1)),
                  (('D', 7), ('V', 0))]
    self_labels = ({("D", i): dlabels[i] for i in range(8)} |
                   {("U", i): ulabels[i] for i in range(3)} |
                   {("V", i): vlabels[i] for i in range(3)})
    self_map = rotation_component({"D": list(range(8)), "U": [0, 1, 2],
                                   "V": [0, 1, 2]}, self_pairs, self_labels)
    face_cycles = [[tuple(item.split(":")) for item in face]
                   for face in self_map["face_cycles"]]
    q_side = next(face for face in face_cycles
                  if ("D", "0") in face and ("D", "5") in face)
    assert ("V", "0") in q_side

    # The outer component is nested in the face adjacent to D's Q side;
    # then the formal exterior remains on that side through surgery.
    self_combined = {"V": 5, "E": 10,
                     "F": self_map["F"] + co_map["F"] - 1}
    assert self_combined["V"] - self_combined["E"] + self_combined["F"] == 3
    assert self_combined["F"] == 8
    h_before_self = len(D) + len(U) + len(V) + len(cpath)
    # The outer side retains Q as the new cap, V, and the C cap.
    h_after_self = 3 + len(V) + len(cpath)
    assert (h_before_self, h_after_self, w) == (17, 9, "acB")

    return {"graph": {"type": "K4 with proper 3-edge-colouring",
                      "vertices": 4, "edges": 6, "girth_L": girth,
                      "immersion": True, "closure_D0": 1,
                      "max_added_closure_edges": max_closure,
                      "closure_pair_states": 144},
            "distinct_disk_surgery": {"inner_words": [word1, word2],
                                      "P": "".join(x[2] for x in P),
                                      "Q": "".join(x[2] for x in Q),
                                      "P_Q_before_tightening": spliced,
                                      "P_Q_after_tightening": free_reduce(spliced),
                                      "outer_w": w,
                                      "H_before": h_before_distinct,
                                      "H_after": h_after_distinct,
                                      "planar_pair_component": distinct_map,
                                      "outer_component": co_map,
                                      "combined_VEF": distinct_combined},
            "self_disk_surgery": {"inner_word": dword,
                                  "P": "c a B", "Q": "c A B",
                                  "other_caps": [uword, vword],
                                  "outer_w": w,
                                  "outer_side": [f"{v}:{i}" for v, i in q_side],
                                  "H_before": h_before_self,
                                  "H_after": h_after_self,
                                  "planar_pair_component": self_map,
                                  "outer_component": co_map,
                                  "combined_VEF": self_combined},
            "scope": "Local exact disk controls only; full bounded-exclusion hypothesis not checked."}


def main():
    result = {"status": "FINITE-LOCAL-CONTROLS-PASS",
              "residual_p_and_trace": finite_group_algebra_controls(),
              "N129_local_disk_controls": disk_controls()}
    out = Path(__file__).with_name("CHECKS.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks": "passed", "closure_D0L": 3,
                      "disk_cases": 2, "outer_word_preserved": True,
                      "output": str(out)}))


if __name__ == "__main__":
    main()
