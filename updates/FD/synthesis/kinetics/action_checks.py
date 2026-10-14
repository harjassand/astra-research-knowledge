#!/usr/bin/env python3
"""Independent exact finite checks for the conditional-action synthesis.

These diagnostics are not molecular benchmarks, asymptotic proofs, or novelty
evidence. No producer code is imported.
"""
from pathlib import Path
import argparse
import json
import random
import sympy as s

ROOT = Path(__file__).resolve().parent


def graph_fixture(rng, n):
    edges = [(i, rng.randrange(i + 1, n)) for i in range(n - 1)]
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in edges and rng.random() < 0.4:
                edges.append((i, j))
    B = s.zeros(n, len(edges))
    for e, (i, j) in enumerate(edges):
        B[i, e], B[j, e] = 1, -1
    c = [s.Rational(rng.randrange(1, 8), rng.randrange(1, 8)) for _ in edges]
    C = s.diag(*c)
    A = B * C * B.T
    weights = [rng.randrange(1, 8) for _ in range(n)]
    p = s.Matrix([s.Rational(w, sum(weights)) for w in weights])
    tangent = [s.Rational(rng.randrange(-5, 6), 7) for _ in range(n - 1)]
    dotp = s.Matrix(tangent + [-sum(tangent)])
    psi = s.Matrix(list(A[:-1, :-1].inv() * dotp[:-1, :]) + [0])
    psi -= s.ones(n, 1) * (p.T * psi)[0]
    current = C * B.T * psi
    h = s.diag(*[1 / pi for pi in p]) * dotp
    Q = -s.diag(*[1 / pi for pi in p]) * A
    K = (current.T * C.inv() * current)[0]
    assert B * current == dotp
    assert -Q * psi == h
    assert (p.T * psi)[0] == 0
    assert K == (dotp.T * psi)[0]
    assert K == (h.T * s.diag(*p) * psi)[0]
    assert K >= 0
    cycles = B.nullspace()
    if cycles:
        cycle = sum((rng.randrange(-3, 4) * z for z in cycles), s.zeros(len(edges), 1))
        competitor = current + cycle
        assert B * competitor == dotp
        extra = (competitor.T * C.inv() * competitor)[0] - K
        assert s.factor(extra - (cycle.T * C.inv() * cycle)[0]) == 0
        assert extra >= 0
    return {"vertices": n, "edges": len(edges), "action": str(K),
            "cycle_space_dimension": len(cycles), "assertions": 9 if cycles else 6}


def two_state():
    p, dp, r = s.symbols("p dp r", positive=True)
    pi = s.Matrix([1-p, p])
    Q = s.Matrix([[-2*r*p, 2*r*p], [2*r*(1-p), -2*r*(1-p)]])
    h = s.Matrix([-dp/(1-p), dp/p])
    psi = h/(2*r)
    c = 2*r*p*(1-p)
    K = s.factor((h.T*s.diag(*pi)*psi)[0])
    assert s.simplify(-Q*psi-h) == s.zeros(2, 1)
    assert s.simplify(K-dp**2/c) == 0
    assert s.simplify(K.subs({p:s.Rational(1,2),dp:s.Rational(1,4)})-1/(8*r)) == 0
    assert s.simplify(K.subs(r,2*r)-K/2) == 0
    # At s=0, the score is (-1/2,+1/2); autocovariance is exp(-2rt)/4.
    t = s.symbols("t", nonnegative=True)
    covariance_integral = s.integrate(s.exp(-2*r*t)/4, (t, 0, s.oo))
    assert covariance_integral == 1/(8*r)
    return {"action": str(K), "conductance": str(c), "at_logistic_midpoint": "1/(8*r)",
            "midpoint_score_covariance": "exp(-2*r*t)/4", "assertions": 5}


def orthogonal_slow_mode():
    eps = s.symbols("eps", positive=True)
    # States (slow,fast)=(0,0),(0,1),(1,0),(1,1); uniform equilibrium.
    Q = s.Matrix([[-1-eps,1,eps,0], [1,-1-eps,0,eps],
                  [eps,0,-1-eps,1], [0,eps,1,-1-eps]])
    hf = s.Matrix([-1,1,-1,1])
    hs = s.Matrix([-1,-1,1,1])
    assert -Q*hf == 2*hf
    assert -Q*hs == 2*eps*hs
    assert (hf.T*hs)[0] == 0
    Kf = (hf.T*(hf/2))[0]/4
    Ks = (hs.T*(hs/(2*eps)))[0]/4
    assert Kf == s.Rational(1,2)
    assert Ks == 1/(2*eps)
    return {"fast_score_action": str(Kf), "slow_score_action": str(Ks),
            "scope": "exact four-state product diagnostic; not an acquired molecular representation", "assertions": 5}


def mobility_and_preparation():
    # Even full equilibrium masses and energies do not determine mobility.
    m = s.Matrix([1, 1])
    A = s.Matrix([[2,-1],[-1,1]])
    r = s.symbols("r", positive=True)
    tau = (m.T*A.inv()*m)[0]/2
    taur = (m.T*(r*A).inv()*m)[0]/2
    assert s.simplify(taur-tau/r) == 0
    # Increasing a physical internal conductance can increase a point-start MFPT.
    c = s.symbols("c", positive=True)
    Aa = s.Matrix([[1+c,-c],[-c,s.Rational(1,100)+c]])
    u = Aa.inv()*m
    before, after = u.subs(c,s.Rational(1,10000)),u.subs(c,100)
    assert after[0] > before[0]
    assert (m.T*after)[0] < (m.T*before)[0]
    return {"equilibrium_mfpt":str(tau), "mobility_scaled_mfpt":str(taur),
            "point_start_before":str(before[0]),"point_start_after":str(after[0]),
            "equilibrium_mean_before":str((m.T*before)[0]/2),
            "equilibrium_mean_after":str((m.T*after)[0]/2), "assertions":3}


def hidden_gate_family():
    records = []
    assertions = 0
    for nbits in range(1, 7):
        N = 2**nbits
        mass = s.Matrix([s.Rational(N+i,N) for i in range(1,N+1)])
        Z = sum(mass)
        H = [sum(mass[i:]) for i in range(N)]
        baseline = sum(x*x for x in H)/Z
        hidden_c = s.Rational(1,100*N**3)
        assert Z <= 2*N; assertions += 1
        assert baseline <= 4*N*N; assertions += 1
        values = []
        for j in range(N):
            hidden = baseline+H[j]*H[j]*(1/hidden_c-1)/Z
            assert hidden >= 50*N*N; assertions += 1
            assert hidden > 4*baseline; assertions += 1
            values.append(hidden)
            if N <= 8:
                # Definition-first inverse check independent of cumulative formula.
                B = s.zeros(N,N)
                for e in range(N):
                    B[e,e] = 1
                    if e: B[e-1,e] = -1
                cs = [s.Integer(1)]*N
                cs[j] = hidden_c
                A = B*s.diag(*cs)*B.T
                direct = (mass.T*A.inv()*mass)[0]/Z
                assert direct == hidden; assertions += 1
        records.append({"bits":nbits,"states":N,"baseline":str(baseline),
                        "minimum_hidden_gate_mean":str(min(values)),
                        "minimum_ratio":str(min(values)/baseline),
                        "hidden_conductance":str(hidden_c)})
    return {"records":records,"assertions":assertions,
            "scope":"Every hidden position checked at n=1..6; direct grounded inverse checked at n<=3. Lower-bound proof is separate."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261014)
    rows = [graph_fixture(rng,2+i%6) for i in range(48)]
    result = {"scope":"Exact rational/symbolic finite diagnostics; universal claims require written proofs.",
              "random_graphs":rows,"two_state":two_state(),
              "slow_mode":orthogonal_slow_mode(),"mobility_and_preparation":mobility_and_preparation(),
              "hidden_gate":hidden_gate_family()}
    result["exact_assertions"] = sum(x["assertions"] for x in rows)+sum(result[k]["assertions"] for k in ["two_state","slow_mode","mobility_and_preparation","hidden_gate"])
    (args.output_dir/"action_check_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"graphs":len(rows),"exact_assertions":result["exact_assertions"],
                      "two_state":result["two_state"],"slow_mode":result["slow_mode"],
                      "mobility_and_preparation":result["mobility_and_preparation"],
                      "hidden_gate":result["hidden_gate"]},indent=2))


if __name__ == "__main__":
    main()
