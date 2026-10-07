"""Exact adversarial checks for the completed bounded thermal algorithm.

Finite checks of implementation identities, not validation by agreement.
Imports only the owned bounded_thermal.py; no peer files are imported.
"""
from fractions import Fraction as F
from itertools import combinations
from types import SimpleNamespace
from pathlib import Path
import json
import time

from bounded_thermal import (ceil_sqrt_q, ComponentInput, Limits, DyadicCDF,
                             PauliObservable, BoundedThermal,
                             FiniteRatioCompiler, quantize_clip)


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def add(A, B):
    return [[x + y for x, y in zip(a, b)] for a, b in zip(A, B)]


def scale(c, A):
    return [[c * x for x in row] for row in A]


def transpose(A):
    return list(map(list, zip(*A)))


def determinant(A):
    a = [list(map(F, row)) for row in A]
    out = F(1)
    for k in range(len(a)):
        pivot = next((j for j in range(k, len(a)) if a[j][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]; out = -out
        out *= a[k][k]
        for j in range(k + 1, len(a)):
            ratio = a[j][k] / a[k][k]
            for l in range(k + 1, len(a)):
                a[j][l] -= ratio * a[k][l]
    return out


def inverse(A):
    n = len(A)
    a = [list(map(F, row)) + e for row, e in zip(A, eye(n))]
    for k in range(n):
        pivot = next(j for j in range(k, n) if a[j][k])
        a[k], a[pivot] = a[pivot], a[k]
        divisor = a[k][k]
        a[k] = [x / divisor for x in a[k]]
        for j in range(n):
            if j != k:
                ratio = a[j][k]
                a[j] = [x - ratio * y for x, y in zip(a[j], a[k])]
    return [row[n:] for row in a]


def principal_minors(A):
    n = len(A)
    return [determinant([[A[i][j] for j in inds] for i in inds])
            for size in range(1, n + 1) for inds in combinations(range(n), size)]


def check_cdf():
    cases = [([2, 1, 4], F(1, 4)), ([0, 3, 0, 4], F(1, 4)), ([5], F(1, 10))]
    records = []
    for weights, delta in cases:
        cdf = DyadicCDF(weights, delta)
        frequencies = [0] * len(weights)
        for j in range(cdf.grid):
            frequencies[cdf.from_bits(j)] += 1
        assert tuple(F(x, cdf.grid) for x in frequencies) == cdf.mu
        for p, q in zip(cdf.pi, cdf.mu):
            assert p or not q  # zero exact masses stay absent
        records.append({"weights": weights, "bits": cdf.bits,
                        "exact_law": list(map(str, cdf.mu)), "tv": str(cdf.actual_tv)})
    return records


def direct_two_qubit_component(comp, data, beta):
    """Independent Fraction matrix polynomial and sequential power."""
    I = eye(4)
    X0 = [[F((i ^ j) == 1) for j in range(4)] for i in range(4)]
    X1 = [[F((i ^ j) == 2) for j in range(4)] for i in range(4)]
    Z0 = [[F((1 if i % 2 == 0 else -1) if i == j else 0) for j in range(4)] for i in range(4)]
    Z1 = [[F((1 if i < 2 else -1) if i == j else 0) for j in range(4)] for i in range(4)]
    _, _, a, g = data.edges[0]
    E = [[3*a+g, F(0), F(0), F(0)],
         [F(0), 3*a-g, 2*a, F(0)],
         [F(0), 2*a, 3*a-g, F(0)],
         [F(0), F(0), F(0), 3*a+g]]
    terms = [E]
    for (b, c), X, Z in zip(data.fields, [X0, X1], [Z0, Z1]):
        terms.append(add(add(scale(b+abs(c), I), scale(b, X)), scale(c, Z)))
    h = beta/(2*comp.m)
    W = I
    for A in terms:
        P = add(add(I, scale(h, A)), scale(h*h/2, mm(A, A)))
        W = mm(W, P)
    B = mm(W, transpose(W))
    K = I
    for _ in range(comp.m):
        K = mm(K, B)
    acquired = [[F(x, comp.Kden) for x in row] for row in comp.K]
    assert K == acquired
    return {"dimension": 4, "layers": comp.m, "all_16_rational_entries_match": True}


def check_global_dense():
    first = ComponentInput(2, ((0, 1, F(1,8), -F(1,16)),),
                           ((F(1,12), F(1,24)), (F(1,12), -F(1,24))))
    second = ComponentInput(1, (), ((F(1,8), F(1,10)),))
    obs = PauliObservable([(F(1,2), "XXI"), (F(1,3), "XZX"), (-F(1,6), "ZZZ")], [2,1])
    engine = BoundedThermal([first,second], F(1,4), obs, F(1,2), F(1,5))
    direct = direct_two_qubit_component(engine.components[0], first, F(1,4))
    left, right = engine.components
    K = [[left.K[a&3][b&3] * right.K[a>>2][b>>2] for b in range(8)] for a in range(8)]
    Z = sum(K[i][i] for i in range(8))
    O = [[F(0) for _ in range(8)] for _ in range(8)]
    for coefficient, word, _ in obs.terms:
        flip = sum((x == "X") << j for j,x in enumerate(word))
        signs = sum((x == "Z") << j for j,x in enumerate(word))
        for b in range(8):
            O[b^flip][b] += coefficient * (-1 if (b&signs).bit_count()&1 else 1)
    theta = sum((O[b][a]*K[a][b] for a in range(8) for b in range(8)), F(0))/Z
    first_moment, second_moment = F(0), F(0)
    max_table_error = F(0)
    for b in range(8):
        state = (b&3,b>>2)
        ratio = obs.ratio(engine.components,state,engine.limits)
        dense_ratio = sum((O[b][a]*K[a][b] for a in range(8)), F(0))/K[b][b]
        assert ratio == dense_ratio
        approx = engine.ratio_compiler.ratio(state)
        max_table_error = max(max_table_error,abs(approx-ratio))
        assert abs(approx-ratio) <= engine.ratio_compiler.uniform_error
        p = F(K[b][b], Z)
        first_moment += p*ratio; second_moment += p*ratio*ratio
    assert first_moment == theta == engine.pi_mean
    assert second_moment == engine.pi_second <= 1
    return {"global_qubits":3,"all_8_global_ratios_match_dense":True,
            "exact_first_moment":str(theta),"exact_second_moment":str(second_moment),
            "maximum_actual_table_error":str(max_table_error),
            "table_error_bound":str(engine.ratio_compiler.uniform_error),
            "independent_P2_matrix_check":direct}


def check_rare_psd():
    q = 1 << 40
    K = [[1,q],[q,q*q+1]]
    assert determinant(K) == 1
    epsilon = F(1,5)
    delta = epsilon*epsilon/1000
    comp = SimpleNamespace(n=1, dim=2, K=K, trace=q*q+2,
                           cdf=DyadicCDF([1,q*q+1],delta))
    obs = PauliObservable([(F(1),"X")],[1])
    compiler = FiniteRatioCompiler([comp],obs,epsilon/4000,Limits())
    ratios = obs.local_values(comp,(1,0))
    mean = sum((p*x for p,x in zip(comp.cdf.pi,ratios)), F(0))
    moment = sum((p*x*x for p,x in zip(comp.cdf.pi,ratios)), F(0))
    assert moment == F(q*q,q*q+1) < 1
    assert ratios[0] == q and comp.cdf.pi[0] < F(1,1<<80)
    T = 10/epsilon
    outbits = 15
    quantized = []
    for b in range(2):
        approx = compiler.ratio((b,))
        assert abs(approx-ratios[b]) <= compiler.uniform_error
        quantized.append(F(quantize_clip(approx,T,outbits),1<<outbits))
    implemented_mean = sum((p*x for p,x in zip(comp.cdf.mu,quantized)), F(0))
    implemented_second = sum((p*x*x for p,x in zip(comp.cdf.mu,quantized)), F(0))
    assert abs(implemented_mean-mean) <= epsilon/5
    assert implemented_second <= F(6,5)
    try:
        FiniteRatioCompiler([comp],obs,epsilon/4000,Limits(max_global_ratio_bits=8))
    except ValueError:
        pass
    else:
        raise AssertionError("rare-ratio precision cap not enforced before table construction")
    return {"rare_diagonal_mass":str(comp.cdf.pi[0]),"rare_ratio":str(ratios[0]),
            "PSD_determinant":"1","exact_variance_bound":str(moment),
            "CDF_tv":str(comp.cdf.actual_tv),"table_bits":compiler.bits,
            "maximum_table_operand_bits":compiler.max_operand_bits,
            "implemented_mean":str(implemented_mean),
            "implemented_second_moment":str(implemented_second),
            "absolute_bias":str(abs(implemented_mean-mean)),
            "no_inverse_probability_sample_schedule":True,
            "finite_ratio_operand_cap_rejection":True}


def check_gaussian_schur():
    I = eye(4)
    J = [[F(0),F(0),F(1),F(0)], [F(0),F(0),F(0),F(1)],
         [-F(1),F(0),F(0),F(0)], [F(0),-F(1),F(0),F(0)]]
    S = [[F(1),F(0),F(1),F(1,2)], [F(0),F(1),F(1,2),-F(1)],
         [F(0),F(0),F(1),F(0)], [F(0),F(0),F(0),F(1)]]
    assert mm(mm(S,J),transpose(S)) == J
    diag = [F(3,5),F(4,5),F(3,5),F(4,5)]
    V = mm(mm(S,[[diag[i] if i==j else F(0) for j in range(4)] for i in range(4)]),transpose(S))
    # Thermal diagonal covariance has symplectic eigenvalues 3/5,4/5>1/2;
    # real symplectic congruence certifies strict Gaussian physicality.
    K = add(V,scale(-F(1,2),I))
    R = scale(F(1,2),add(K,mm(mm(J,K),transpose(J))))
    X = add(K,scale(-1,R))
    assert mm(mm(J,R),transpose(J)) == R
    assert mm(mm(J,X),transpose(J)) == scale(-1,X)
    assert mm(R,X) != mm(X,R)  # the claimed algebra is genuinely noncommuting
    assert min(principal_minors(R)) > 0
    D = add(mm(mm(X,inverse(R)),X),scale(-1,R))
    deficits = principal_minors(add(I,scale(-1,D)))
    assert min(deficits) > 0
    eta = F(1,1000)
    Dloss = add(mm(mm(scale(eta,X),inverse(scale(eta,R))),scale(eta,X)),scale(-eta,R))
    assert Dloss == scale(eta,D)
    return {"modes":2,"R_X_noncommute":True,"strict_physicality":"symplectic image of diag(3/5,4/5,3/5,4/5)",
            "minimum_principal_minor_of_I_minus_D":str(min(deficits)),
            "D_loss_equals_eta_D":True}


def check_schedules_and_rejections():
    tests = [F(0),F(1),F(4),F(17,4),F(999999999999999999999999,1000000000000000000000000),
             F(1000000000000000000000001,1000000000000000000000000)]
    for x in tests:
        c = ceil_sqrt_q(x)
        assert c*c >= x and (c==0 or (c-1)*(c-1)<x)
    obs = PauliObservable([(F(1),"X")],[1])
    cases = [
        (ComponentInput(1,(),((-F(1),F(0)),)),F(1),Limits()),
        (ComponentInput(1,(),((F(1),F(0)),)),F(1000),Limits(max_layers=1)),
        (ComponentInput(1,(),((F(1),F(0)),)),F(1),Limits(max_entry_bits=8)),
    ]
    reasons=[]
    for data,beta,limits in cases:
        try:
            BoundedThermal([data],beta,obs,F(1,5),F(1,10),limits)
        except ValueError as e:
            reasons.append(str(e))
        else:
            raise AssertionError("invalid/cost-capped input accepted")
    outside=ComponentInput(2,((0,1,F(1),F(2)),),((F(0),F(0)),)*2)
    try:
        BoundedThermal([outside],F(1),PauliObservable([(F(1),"XX")],[2]),F(1,5),F(1,10))
    except ValueError as e:
        reasons.append(str(e))
    else:
        raise AssertionError("outside-cone input accepted")
    zero=ComponentInput(1,(),((F(0),F(0)),))
    trivial=BoundedThermal([zero],F(0),obs,F(1,5),F(1,10))
    assert trivial.components[0].K == [[1,0],[0,1]]
    assert trivial.generator_bound==0 and trivial.components[0].cdf.actual_tv==0
    return {"exact_square_root_cases":len(tests),"explicit_rejection_reasons":reasons,
            "zero_inverse_temperature_identity_case":True}


def main():
    start=time.monotonic()
    result={"scope":"implementation identities and adversarial finite inputs; uniform guarantees are in BOUNDED_THERMAL_PROOF.txt",
            "CDF_full_fixed_tape_laws":check_cdf(),
            "global_same_state_and_matrix_checks":check_global_dense(),
            "exponentially_rare_PSD_ratio":check_rare_psd(),
            "noncommuting_Gaussian_Schur_bridge":check_gaussian_schur(),
            "schedules_and_admission":check_schedules_and_rejections()}
    result["seconds"]=time.monotonic()-start
    result["status"]="PASS_EXACT_IMPLEMENTATION_AND_ADVERSARIAL_CHECKS"
    Path(__file__).with_suffix(".json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"seconds":result["seconds"],
                      "checks":[k for k in result if k not in ["scope","seconds","status"]]},indent=2))


if __name__=="__main__":
    main()
