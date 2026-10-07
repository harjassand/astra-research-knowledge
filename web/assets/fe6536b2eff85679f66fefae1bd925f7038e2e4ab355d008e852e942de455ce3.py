"""Exact parity-softening counterexamples; no FPRAS is implemented."""
import importlib.util
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

_path = Path(__file__).resolve().parents[1] / "cycle3" / "paired_fermion_checks.py"
_spec = importlib.util.spec_from_file_location("parity_gate_gq", _path)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
GQ, det, abs2 = _base.GQ, _base.det, _base.abs2


def mix_cycles(u):
    c, s = (1-u*u)/(1+u*u), 2*u/(1+u*u)
    F = [[GQ(0) for _ in range(6)] for _ in range(6)]
    for j in range(3):
        nxt = (j+1) % 3
        F[j][nxt] = GQ(c)
        F[j][3+nxt] = GQ(-s)
        F[3+j][nxt] = GQ(s)
        F[3+j][3+nxt] = GQ(c)
    return F, c, s


def minor(F, rows, cols):
    return det([[F[i][j] for j in cols] for i in rows])


def check_soft_case(u, eps):
    F, c, s = mix_cycles(u)
    assert c*c+s*s == 1
    for i in range(6):
        assert not F[i][i]
        for j in range(6):
            assert sum(F[i][a]*F[j][a] for a in range(6)) == GQ(i == j)
    allsites = set(range(6))
    norm = Q(0)
    hard = Q(0)
    marginals = [Q(0)]*12
    bases = 0
    for ne in range(7):
        for E in itertools.combinations(range(6), ne):
            Ec = sorted(allsites.difference(E))
            for J in itertools.combinations(range(6), 6-ne):
                value = abs2(minor(F,J,Ec))
                if not value:
                    continue
                bases += 1
                broken = len(set(E).symmetric_difference(J))
                weighted = value*eps**broken
                norm += weighted
                if broken == 0:
                    hard += weighted
                for i in E:
                    marginals[i] += weighted
                for i in J:
                    marginals[6+i] += weighted
    a = c**6+3*c**2*s**4
    b = 3*c**4*s**2+s**6
    assert a+b == 1
    predicted = a*(6*eps+2*eps**3)**2 + b*((1+eps)**6+(eps-1)**6)
    assert norm == predicted
    assert hard == 2*b
    assert all(2*x == norm for x in marginals)
    supports = {}
    active_entries = set()
    for I in itertools.combinations(range(6),3):
        J = sorted(allsites.difference(I))
        amp = minor(F,I,J)
        if not amp:
            continue
        supports[I] = abs2(amp)
        for ri,i in enumerate(I):
            for cj,j in enumerate(J):
                cofactor = minor(F,[x for x in I if x != i],[x for x in J if x != j])
                if F[i][j] and cofactor:
                    active_entries.add((i,j))
    assert len(supports) == 8
    assert sorted(supports.values()) == sorted([c**4*s**2]*6+[s**6]*2)
    nonzero_entries = {(i,j) for i in range(6) for j in range(6) if F[i][j]}
    assert active_entries == nonzero_entries
    return {"u":str(u),"epsilon":str(eps),"supported_dpp_bases":bases,
            "hard_supports":len(supports),"participating_nonzero_entries":len(active_entries),
            "all_coordinate_marginals":"1/2","hard_norm":str(hard),
            "hard_probability":str(hard/norm),"hard_probability_float":float(hard/norm)}


def cycle_counterexamples():
    result=[]
    for q in range(2,7):
        n=2*q
        supports=[]
        for I in itertools.combinations(range(n),q):
            si=set(I)
            if not si.intersection({(i+1)%n for i in I}):
                supports.append(I)
        assert len(supports)==2
        assert set(supports[0]).isdisjoint(supports[1])
        # For every update resampling fewer than q selectors the two supports
        # have no common retained selector, so no transition is possible.
        result.append({"q":q,"hard_supports":2,"support_symmetric_difference":2*q,
                       "maximum_fractional_lc_alpha":str(Q(1,q)),
                       "minimum_resampled_pairs_to_move":q})
    return result


def curvature_checks():
    result=[]
    for eps in [Q(1,2),Q(1,4),Q(1,16)]:
        eigenvalue=2*eps*eps-1
        assert eigenvalue < 0
        kappa_upper_bound=(2*eps*eps-1)/eps
        result.append({"epsilon":str(eps),"zero_curvature_bad_eigenvalue":str(eigenvalue),
                       "max_admissible_kappa_upper_bound":str(kappa_upper_bound)})
    return result


if __name__ == "__main__":
    result={"status":"PASS","orthogonal_zero_diagonal_balancing_cases":[
        check_soft_case(Q(1,2),Q(1,3)),
        check_soft_case(Q(1,8),Q(1,4)),
        check_soft_case(Q(1,2**20),Q(1,64))],
        "directed_cycle_cases":cycle_counterexamples(),
        "local_curvature_cases":curvature_checks(),"fpras_executed":False}
    target=Path(__file__).with_name("parity_counting_gate_checks_result.json")
    target.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
