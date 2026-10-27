"""Exact covariance/positivity checks and a value-only nonlinear gauge test.

No empirical moment calculation is used to certify total variation. The
full-law theorem follows from exact joint Gaussian seed algebra. The floating
test verifies the corresponding pathwise query identity for a nonseparable
conservative Lipschitz source; it does not prove a general mean factory.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import numpy as np


def tr(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in tr(b)] for row in a]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def sub(a, b):
    return [[x-y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def det(a):
    a = [row[:] for row in a]
    out = F(1)
    for j in range(len(a)):
        piv = next((i for i in range(j, len(a)) if a[i][j]), None)
        if piv is None:
            return F(0)
        if piv != j:
            a[piv], a[j] = a[j], a[piv]
            out = -out
        q = a[j][j]
        out *= q
        for i in range(j+1, len(a)):
            c = a[i][j]/q
            for k in range(j+1, len(a)):
                a[i][k] -= c*a[j][k]
    return out


def numeric(a):
    return np.array([[float(x) for x in row] for row in a])


def run():
    # Two retained means and three fresh nonlinear children. Each child has
    # position and output-noise slots; v=(-1,0), r=1.
    A = [[F(1,4), F(1,8)], [F(-1,8), F(1,4)],
         [F(1,8), F(-1,8)]]
    D = [[F(-1,2), F(0)], [F(0), F(-1,2)]]
    for row in A:
        D.extend([[-x for x in row], [F(0), F(0)]])
    K = sub(eye(8), mm(D, tr(D)))
    J = sub([[F(3,4),F(0)], [F(0),F(3,4)]], mm(tr(A),A))
    # Exact rational certificate: C=I, Cnew=4I, strict slack J.
    assert mm(tr(D),D) == sub(eye(2),J)
    minors = [det([row[:i] for row in K[:i]]) for i in range(1,9)]
    assert all(x > 0 for x in minors)
    assert all(det([row[:i] for row in J[:i]]) > 0 for i in (1,2))
    exact_sum = [[x+y for x,y in zip(ra,rb)]
                 for ra,rb in zip(K,mm(D,tr(D)))]
    assert exact_sum == eye(8)

    # This source is a gradient of b.x + ell sum log cosh(U^T x), so it
    # is globally ell-Lipschitz and nonseparable in the supplied coordinates.
    rng = np.random.default_rng(27102026)
    d = 17
    U, _ = np.linalg.qr(rng.standard_normal((d,d)))
    offset = rng.standard_normal(d)
    ell = 0.7
    query_count = 0
    def g(x):
        nonlocal query_count
        query_count += 1
        return offset+ell*(U @ np.tanh(U.T @ x))
    Kf, Df, Af = numeric(K), numeric(D), numeric(A)
    P = np.linalg.cholesky(Kf)
    T = 2*np.eye(2)
    means = rng.standard_normal((2,d))
    b = rng.standard_normal((3,d))
    centers = b+Af@means
    worst_query_error = 0.0
    worst_output_error = 0.0
    worst_retention_error = 0.0
    repetitions = 100
    for _ in range(repetitions):
        Z = rng.standard_normal((2,d))
        G = rng.standard_normal((8,d))
        R = means+Z
        xi = P@G
        eta = xi-Df@Z
        retained = R+T@xi[:2]
        retained_reference = means+T@eta[:2]
        worst_retention_error = max(worst_retention_error,
            float(np.max(np.abs(retained-retained_reference))))
        for i in range(3):
            pos_slot, noise_slot = 2+2*i, 3+2*i
            actual_query = b[i]+Af[i]@R+xi[pos_slot]
            reference_query = centers[i]+eta[pos_slot]
            worst_query_error = max(worst_query_error,
                float(np.max(np.abs(actual_query-reference_query))))
            actual = g(actual_query)+(1.0+0.2*i)*xi[noise_slot]
            reference = g(reference_query)+(1.0+0.2*i)*eta[noise_slot]
            worst_output_error = max(worst_output_error,
                float(np.max(np.abs(actual-reference))))
    assert query_count == repetitions*6
    assert worst_query_error < 1e-12
    assert worst_output_error < 1e-12
    assert worst_retention_error < 1e-12

    # Exact zero-slack projector and reserve-response closure, rho=1/4.
    # A2^T A2=(3/4)I, hence Cnew=4I and D2^T D2=I exactly.
    A2 = [[F(1,2),F(1,2)], [F(1,2),F(-1,2)],
          [F(1,2),F(0)], [F(0),F(1,2)]]
    D2 = [[F(-1,2),F(0)], [F(0),F(-1,2)]]
    for row in A2:
        D2.extend([[-x for x in row], [F(0),F(0)]])
    assert mm(tr(D2),D2) == eye(2)
    P2 = sub(eye(10),mm(D2,tr(D2)))
    assert mm(P2,P2) == P2
    assert mm(tr(D2),P2) == [[F(0)]*10 for _ in range(2)]
    # Old raw slots alternate position/noise. Their output response is 2
    # in the noise slot, giving a literal reserve of covariance I/4.
    Wold = [[F(0),F(0)], [F(2),F(0)],
            [F(0),F(0)], [F(0),F(2)]]
    Wnew = [[F(0)]*6 for _ in range(14)]
    for j in range(4):
        for i in range(2):
            Wnew[j][i] = Wold[j][i]/4
    for i in range(2):
        Wnew[4+i][i] = F(3,8)
    for j,row in enumerate(A2):
        for i in range(2):
            Wnew[6+2*j][i] = -row[i]/4
        Wnew[7+2*j][2+j] = 1
    expected_gram = [[F(0)]*6 for _ in range(6)]
    for i in range(6):
        expected_gram[i][i] = F(7,16) if i<2 else F(1)
    assert mm(tr(Wnew),Wnew) == expected_gram
    # Required upper bound is I, because rho^{-1} C_out^{-1}=4*(I/4).
    assert all(expected_gram[i][i] <= 1 for i in range(6))

    kap = [[F(1)], [F(-2)], [F(1,2)], [F(3,2)]]
    avec = mm(tr(A2),kap)
    rr = [[-row[0]] for row in avec]
    fresh_gauge = [[-rr[0][0]/2],[-rr[1][0]/2]]
    Ar = mm(A2,rr)
    for i in range(4):
        fresh_gauge.extend([[-kap[i][0]-Ar[i][0]],[F(0)]])
    assert mm(tr(D2),fresh_gauge) == [[F(0)],[F(0)]]
    Vold = [[F(-1)],[F(0)],[F(-1)],[F(0)]]
    old_shift = mm(Wold,rr)
    Vnew = [[Vold[i][0]+old_shift[i][0]] for i in range(4)] + fresh_gauge
    cross = mm(tr(Vnew),Wnew)
    # Orthogonality indeed fails before the unused-seed repair.
    assert any(c != 0 for c in cross[0])
    Vnorm2 = mm(tr(Vnew),Vnew)[0][0]
    repaired_gram = [[expected_gram[i][j]+cross[0][i]*cross[0][j]/Vnorm2
                     for j in range(6)] for i in range(6)]
    # The repair's exact covariance statement is the rank-one Cauchy bound;
    # all principal minors of 2*Gram - repairedGram are nonnegative.
    repair_margin = [[2*expected_gram[i][j]-repaired_gram[i][j]
                      for j in range(6)] for i in range(6)]
    assert all(det([[repair_margin[i][j] for j in ix] for i in ix]) >= 0
               for size in range(1,7) for ix in combinations(range(6),size))

    # Pathwise test of the complete projector program and its acquired gauge.
    Af2, Pf2 = numeric(A2), numeric(P2)
    Vnf = numeric(Vnew)[:,0]
    kappaf = numeric(kap)[:,0]
    b2 = rng.standard_normal((4,d))
    projector_queries_before = query_count
    projector_worst_query = 0.0
    projector_worst_output = 0.0
    def program2(x, seeds):
        old = np.stack([g(x+seeds[0])+0.5*seeds[1],
                        g(x+seeds[2])+0.5*seeds[3]])
        xi2 = Pf2@seeds[4:]
        queries = [x+seeds[0],x+seeds[2]]
        output = [old[0]+2*xi2[0], old[1]+2*xi2[1]]
        for i in range(4):
            query = b2[i]+kappaf[i]*x+Af2[i]@old+xi2[2+2*i]
            queries.append(query)
            output.append(g(query)+xi2[3+2*i])
        return np.stack(queries),np.stack(output)
    for _ in range(20):
        x = rng.standard_normal(d)
        delta = rng.standard_normal(d)
        seeds = rng.standard_normal((14,d))
        queries0,out0 = program2(x,seeds)
        queries1,out1 = program2(x+delta,seeds+Vnf[:,None]*delta)
        projector_worst_query = max(projector_worst_query,
            float(np.max(np.abs(queries0-queries1))))
        projector_worst_output = max(projector_worst_output,
            float(np.max(np.abs(out0-out1))))
    projector_query_count = query_count-projector_queries_before
    assert projector_query_count == 240
    assert projector_worst_query < 1e-12
    assert projector_worst_output < 1e-12

    # The strict capacity for k equal reads h=1/8 is 1/t^2+k/64<1.
    # This is exact algebra about the lift, not a target lower bound.
    capacity = {str(k):str(F(64,64-k)) for k in (1,8,16,32,48,60)}
    result = {
        "exact_rational_covariance_identity": True,
        "exact_strict_positivity_leading_minors": [str(x) for x in minors],
        "nonseparable_gradient_dimension": d,
        "source_lipschitz_bound": ell,
        "first_test_actual_algorithm_queries": repetitions*3,
        "first_test_separate_reference_queries": repetitions*3,
        "total_source_value_calls": query_count,
        "max_pathwise_query_difference_float": worst_query_error,
        "max_pathwise_output_difference_float": worst_output_error,
        "max_retained_record_difference_float": worst_retention_error,
        "cholesky_covariance_roundoff": float(np.max(np.abs(P@P.T-Kf))),
        "read_count_to_infimum_retained_variance": capacity,
        "projector_covariance_and_idempotence_exact": True,
        "constructed_response_gram_diagonal_exact": [str(expected_gram[i][i]) for i in range(6)],
        "external_gauge_response_cross_exact": [str(c) for c in cross[0]],
        "unused_seed_orthogonality_repair_bound_exact": True,
        "projector_gauge_test_calls_including_reference": projector_query_count,
        "projector_gauge_max_query_difference_float": projector_worst_query,
        "projector_gauge_max_output_difference_float": projector_worst_output,
        "full_law_basis": "Exact jointly Gaussian effective-seed identity; no empirical TV inference",
        "target_status": "No general Gaussian-mean acquisition algorithm is claimed",
    }
    root = Path(__file__).resolve().parent
    (root/"CHECK_RESULTS.txt").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    run()
