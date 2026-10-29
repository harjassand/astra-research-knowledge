#!/usr/bin/env python3
"""Exact finite checks for the energy-clock intervention obstruction.

Uses rational arithmetic only. These are algebraic controls, not acquired data.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent


def zeros(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def mm(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def transpose(A):
    return [list(row) for row in zip(*A)]


def inverse(A):
    n = len(A)
    aug = [row[:] + [F(i == j) for j in range(n)] for i, row in enumerate(A)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        scale = aug[j][j]
        aug[j] = [x/scale for x in aug[j]]
        for i in range(n):
            if i != j:
                scale = aug[i][j]
                aug[i] = [x-scale*y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def generator(w, flux):
    Q = [[flux[i][j]/w[i] for j in range(len(w))] for i in range(len(w))]
    for i in range(len(w)):
        Q[i][i] = -sum(Q[i])
    return Q


def adjoint(Q, w):
    return [[w[j]*Q[j][i]/w[i] for j in range(len(w))] for i in range(len(w))]


def stationary(Q, w):
    assert all(sum(row) == 0 for row in Q)
    assert all(sum(w[i]*Q[i][j] for i in range(len(w))) == 0 for j in range(len(w)))


def parity_balance(Q, w, theta):
    stationary(Q, w)
    assert all(theta[theta[i]] == i and w[i] == w[theta[i]] for i in range(len(w)))
    assert adjoint(Q, w) == [[Q[theta[i]][theta[j]] for j in range(len(w))]
                             for i in range(len(w))]


def source():
    # Two singleton ports, one hidden entrance state, and an asymmetric hidden cycle.
    w = list(map(F, [1, 1, 2, 3, 5]))
    flux = zeros(5)
    flux[0][2] = flux[2][0] = F(1)
    flux[1][2] = flux[2][1] = F(2)
    for i, j, forward, backward in [(2, 3, 2, 1), (3, 4, 3, 2), (4, 2, 4, 3)]:
        flux[i][j], flux[j][i] = F(forward), F(backward)
    return generator(w, flux), w


def complete(Q, w, ports):
    interior = [i for i in range(len(w)) if i not in ports]
    indices = [(b, 0) for b in ports] + [(i, s) for s in (1, -1) for i in interior]
    location = {v: i for i, v in enumerate(indices)}
    W = [w[i] if s == 0 else w[i]/2 for i, s in indices]
    Qstar = adjoint(Q, w)
    L = zeros(len(indices))
    for a, (x, sx) in enumerate(indices):
        for b, (y, sy) in enumerate(indices):
            if a == b:
                L[a][b] = Q[x][x]
            elif sx == 0 and sy == 0:
                L[a][b] = (Q[x][y] + Qstar[x][y])/2
            elif sx == 0:
                L[a][b] = (Q if sy == 1 else Qstar)[x][y]/2
            elif sy == 0 or sx == sy:
                L[a][b] = (Q if sx == 1 else Qstar)[x][y]
    theta = [location[(i, -s)] for i, s in indices]
    return L, W, theta, indices


def kernel_laplace(Q, w, ports, s):
    interior = [i for i in range(len(w)) if i not in ports]
    left = [[w[b]*Q[b][i] for i in interior] for b in ports]
    middle = [[F(i == j)*s-Q[i][j] for j in interior] for i in interior]
    right = [[Q[i][b] for b in ports] for i in interior]
    return mm(mm(left, inverse(middle)), right)


def clock(Q, w, speeds):
    return [[speeds[i]*x for x in row] for i, row in enumerate(Q)], [w[i]/speeds[i] for i in range(len(w))]


def force_derivative(Q, V):
    B = [[Q[i][j]*(V[j]-V[i])/2 if i != j else F(0)
          for j in range(len(Q))] for i in range(len(Q))]
    for i in range(len(Q)):
        B[i][i] = -sum(B[i])
    return B


def main():
    Q, w = source()
    stationary(Q, w)
    ports = [0, 1]
    L, W, theta, indices = complete(Q, w, ports)
    parity_balance(L, W, theta)
    assert sum(w) == sum(W) == 12
    assert adjoint(Q, w) != Q
    # Positive, distinct hidden weights imply that any weight-preserving involution
    # fixing the two native ports must be the identity on the original chain.
    assert len(set(w[2:])) == 3 and all(x not in w[:2] for x in w[2:])
    s_values = list(map(F, [1, 2, 3, 5])) + [F(1, 2), F(5, 7)]
    baseline_checks = 0
    for s in s_values:
        K = kernel_laplace(Q, w, ports, s)
        assert K == transpose(K)
        assert K == kernel_laplace(L, W, ports, s)
        baseline_checks += 1
    speed_pairs = [(F(1), F(1)), (F(1, 2), F(2)), (F(3, 2), F(4, 3)),
                   (F(2), F(3, 5)), (F(4, 5), F(7, 4))]
    controlled_kernel_checks = 0
    fdt_checks = 0
    for d0, d1 in speed_pairs:
        speeds = [d0, d1, F(1), F(1), F(1)]
        speeds_lift = [speeds[i] for i, _ in indices]
        Qd, wd = clock(Q, w, speeds)
        Ld, Wd = clock(L, W, speeds_lift)
        stationary(Qd, wd)
        parity_balance(Ld, Wd, theta)
        assert sum(wd) == sum(Wd)
        assert [-Qd[b][b] for b in ports] == [-Ld[b][b] for b in ports]
        for s in s_values:
            Kq, Kl = kernel_laplace(Qd, wd, ports, s), kernel_laplace(Ld, Wd, ports, s)
            assert Kq == Kl
            # Same full excursion transform after the native hold, for either port.
            for b in ports:
                rate = -Qd[b][b]
                for c in ports:
                    Aq = rate/(s+rate)*Kq[b][c]/(wd[b]*rate)
                    Al = rate/(s+rate)*Kl[b][c]/(Wd[b]*rate)
                    assert Aq == Al
            controlled_kernel_checks += 1
        # The FDT generator identity holds without reversibility, for every tested
        # potential and every basis terminal observable; powers verify all time jets.
        for M, weights in [(Qd, wd), (Ld, Wd)]:
            n = len(M)
            pi = [[x/sum(weights) for x in weights]]
            for port in ports:
                V = [F(i == port) for i in range(n)]
                B = [[-V[i]*x for x in row] for i, row in enumerate(M)]
                expected = mm([[pi[0][i]*V[i] for i in range(n)]], M)
                actual = mm(pi, B)
                assert actual == [[-x for x in expected[0]]]
                power = [[F(i == j) for j in range(n)] for i in range(n)]
                for _ in range(7):
                    assert mm(actual, power) == [[-x for x in mm(expected, power)[0]]]
                    power = mm(power, M)
                    fdt_checks += n
    # A four-state generalized-equilibrium chain shows why the symmetric edge
    # tilt need not be an equilibrium-compatible energy operation for odd states.
    flux = zeros(4)
    for i, j, a, b in [(0, 2, 2, 1), (0, 3, 1, 2), (1, 2, 1, 2), (1, 3, 2, 1)]:
        flux[i][j], flux[j][i] = F(a), F(b)
    G = generator([F(1)]*4, flux)
    parity_balance(G, [F(1)]*4, [0, 1, 3, 2])
    V = [F(1), F(0), F(0), F(0)]
    pi = [[F(1, 4)]*4]
    B = force_derivative(G, V)
    canonical_derivative = [[pi[0][i]*(V[i]-F(1, 4)) for i in range(4)]]
    equilibrium_residual = [a+b for a, b in zip(mm(pi, B)[0], mm(canonical_derivative, G)[0])]
    assert equilibrium_residual == [F(0), F(0), F(1, 8), F(-1, 8)]
    # Same energetic ratio derivative can coexist with unbounded symmetric rate
    # sensitivity. Fixed FDT discrepancy while baseline entropy tends to zero.
    kinetic_examples = []
    for delta in [F(1, 2), F(1, 4), F(1, 10), F(1, 100), F(1, 1000)]:
        H = zeros(3)
        for i in range(3):
            H[i][(i+1) % 3] = 1+delta
            H[i][(i-1) % 3] = 1-delta
            H[i][i] = F(-2)
        V = [F(1), F(0), F(0)]
        B = force_derivative(H, V)
        for i, j in [(0, 1), (1, 0)]:
            extra = H[i][j]/delta
            B[i][j] += extra
            B[i][i] -= extra
        pi = [[F(1, 3)]*3]
        actual = mm(pi, B)[0][0]
        predicted = -pi[0][0]*H[0][0]
        assert actual-predicted == F(-2, 3)
        kinetic_examples.append({"delta":str(delta), "symmetric_rate_sensitivity":str(1/delta),
            "fdt_discrepancy_t0":str(actual-predicted),
            "baseline_entropy_rate_float":2*float(delta)*math.log(float((1+delta)/(1-delta)))})
    result = {
        "status":"PASS", "arithmetic":"exact rational except displayed logarithms",
        "source_states":5, "completion_states":8, "source_weights":[str(x) for x in w],
        "completion_theta":theta, "native_singleton_ports":ports,
        "source_ordinary_entropy_rate":"log(4)/12 > 0",
        "source_ordinary_entropy_rate_float":math.log(4)/12,
        "source_admits_no_stationary_weight_preserving_involution_fixing_ports_other_than_identity":True,
        "completion_generalized_entropy_rate":"0 exactly, also under every tested clock field",
        "reciprocal_kernel_transform_checks":baseline_checks,
        "controlled_kernel_transform_checks":controlled_kernel_checks,
        "fdt_basis_time_jet_checks":fdt_checks,
        "symmetric_edge_tilt_canonical_stationarity_derivative_residual":[str(x) for x in equilibrium_residual],
        "unbounded_kinetic_sensitivity_controls":kinetic_examples,
        "source_observations":0, "physical_preparations":0, "physical_controls_executed":0,
        "arbitrary_protocol_scope":"Proved by observable causal time change, not established by these finite checks alone.",
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    (ROOT/"CLOCK_RESPONSE_CHECKS.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
