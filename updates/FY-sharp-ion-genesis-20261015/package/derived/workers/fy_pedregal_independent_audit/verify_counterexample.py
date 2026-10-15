"""Exact, standard-library verification of an empty T image in arXiv v5.

This verifies a counterexample to the paper's permitted-mold/nonempty-image
claim. It does not test or refute rank-one convexity => quasiconvexity.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


U_NODES = [[0, 4], [2, 3]]
V_NODES = [[1, 0], [0, 2]]


def gradient_table(z):
    n = len(z)
    answer = []
    for j in range(n):
        for i in range(n):
            a, b = z[j][i], z[j][(i+1) % n]
            c, d = z[(j+1) % n][i], z[(j+1) % n][(i+1) % n]
            answer.extend([(n*(b-a), n*(c-a)), (n*(d-c), n*(d-b))])
    return answer


def interface_groups(n):
    tri = lambda i, j, k: 2*((j % n)*n+(i % n))+k
    groups = {"V": [], "H": [], "D": []}
    for j in range(n):
        for i in range(n):
            groups["V"].append((tri(i,j,0), tri(i-1,j,1)))
            groups["H"].append((tri(i,j,0), tri(i,j-1,1)))
            groups["D"].append((tri(i,j,0), tri(i,j,1)))
    return groups


def convex(a, b, x):
    return tuple(x*aa+(1-x)*bb for aa, bb in zip(a,b))


def sub(a, b):
    return tuple(aa-bb for aa, bb in zip(a,b))


def det(a, b):
    return a[0]*b[1]-a[1]*b[0]


def main():
    n, m = 2, 8
    gu, gv = gradient_table(U_NODES), gradient_table(V_NODES)
    assert all(sum(g[k] for g in gu) == 0 for k in (0,1))
    assert all(sum(g[k] for g in gv) == 0 for k in (0,1))
    groups = interface_groups(n)
    normals = {"V": (1,0), "H": (0,1), "D": (1,1)}
    # Local compatibility follows from shared nodal values; check exactly.
    for z in (gu,gv):
        for tag, es in groups.items():
            for left, right in es:
                assert det(sub(z[left],z[right]), normals[tag]) == 0
    molds = [groups[a]+groups[b] for a,b in [("V","H"),("V","D"),("H","D")]]
    for es in molds:
        assert Counter(k for edge in es for k in edge) == Counter({k: 2 for k in range(m)})
    counts = Counter(k for es in molds for edge in es for k in edge)
    assert counts == Counter({k: 6 for k in range(m)})
    uniform_leaf = F(1,48)
    assert 2*uniform_leaf == F(1,24) == F(1, 3*m)
    assert all(counts[k]*uniform_leaf == F(1,8) for k in range(m))
    assert len(set(gu)) == len(set(gv)) == 8
    # In j=1, the seventh and eighth interface pairs are combined at the
    # next dyadic level: leaves [[13,14],[15,16]] in one-based notation.
    h1,h2 = molds[0][6:8]
    assert h1 == (4,1) and h2 == (6,3)
    corners = []
    for alpha,beta,gamma,delta in product((F(0),F(1)), repeat=4):
        du = sub(convex(gu[h1[0]],gu[h1[1]],alpha),
                 convex(gu[h2[0]],gu[h2[1]],beta))
        dv = sub(convex(gv[h1[0]],gv[h1[1]],gamma),
                 convex(gv[h2[0]],gv[h2[1]],delta))
        value = det(du,dv)
        expected = 72+16*alpha-16*beta-8*gamma+8*delta
        assert value == expected
        corners.append(value)
    # The determinant is affine in the four fractions, so its extrema on
    # their full [0,1]^4 box occur at the checked vertices. The true Theta
    # fractions form a subset; no triangle mass constraint can help.
    assert min(corners) == 48 and max(corners) == 96
    # Analytic stability bound for independent nodal sup errors <= 1/10.
    # Each gradient coordinate moves <= 4 eps; each paired difference
    # coordinate moves <= 8 eps, uniformly over all convex fractions.
    eps = F(1,10)
    robust_lower_bound = (4-8*eps)*(4-8*eps)+(4-8*eps)*(8-8*eps)
    assert robust_lower_bound == F(832,25) > 0
    summary = {
        "status": "EXACT_COUNTEREXAMPLE_TO_NONEMPTY_IMAGE_FOR_PERMITTED_MOLD",
        "scope": "Corollary 7.2 and the arbitrary-labeling proof route; not the main planar ROC=>QC statement",
        "grid_n": n,
        "l": 1,
        "u_nodes_rows_y_columns_x": U_NODES,
        "v_nodes_rows_y_columns_x": V_NODES,
        "u_gradients_T0_through_T7": gu,
        "v_gradients_T0_through_T7": gv,
        "molds_interface_pairs_zero_based_triangles": molds,
        "uniform_input_leaf_weight": str(uniform_leaf),
        "critical_interface_pairs": [h1,h2],
        "U_difference": ["4", "-6-2*alpha+2*beta"],
        "V_difference": ["8", "6-2*gamma+2*delta"],
        "determinant": "72+16*alpha-16*beta-8*gamma+8*delta",
        "all_four_fractions_in": "[0,1]",
        "determinant_exact_minimum_on_full_box": 48,
        "determinant_exact_maximum_on_full_box": 96,
        "robust_nodal_sup_error_each_component": str(eps),
        "robust_determinant_exact_lower_bound": str(robust_lower_bound),
        "conclusion": "T(t) is empty for every t in Theta_1 for this permitted mold.",
        "verification": "Exact integer/Fraction arithmetic; no numerical solver required."
    }
    out = Path(__file__).with_name("counterexample_certificate.json")
    out.write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
