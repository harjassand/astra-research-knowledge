"""An exact scope counterexample, not a norm or state-preparation algorithm."""
import importlib.util
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

source = Path(__file__).resolve().parents[1] / "cycle3" / "paired_fermion_checks.py"
spec = importlib.util.spec_from_file_location("paired_checks", source)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

n = 4
A = {0, 1}
B = {2, 3}
X = [[Q(1), Q(1)], [Q(1), Q(1, 2)]]
F = [[Q(0) for _ in range(n)] for _ in range(n)]
for i in range(2):
    for j in range(2):
        F[i][2 + j] = X[i][j]
        F[2 + j][i] = X[i][j]
assert F == list(map(list, zip(*F)))
assert all(F[i][j] == 0 for C in (A, B) for i in C for j in C)

state = base.exp_pair(F)
rows = []
for U in itertools.combinations(range(n), 2):
    U = set(U)
    D = set(range(n)) - U
    mask = sum(1 << i for i in U) + sum(1 << (n + j) for j in D)
    # Occupation order is (all up, all down). The tensor spin basis creates
    # the occupied mode of each site in increasing site order.
    sequence = [i if i in U else n + i for i in range(n)]
    inversions = sum(sequence[i] > sequence[j] for i in range(n)
                     for j in range(i + 1, n))
    amp = state.get(mask, Q(0)) * (-1) ** inversions
    corrected = amp * (-1) ** len(A & D)
    rows.append({"spins": "".join("u" if i in U else "d" for i in range(n)),
                 "spin_basis_amplitude": str(amp),
                 "Marshall_corrected_amplitude": str(corrected)})

corrected = {x["spins"]: Q(x["Marshall_corrected_amplitude"]) for x in rows}
assert corrected["uudd"] == Q(1, 2)
assert corrected["udud"] == Q(1)
assert corrected["uddu"] == Q(-1, 2)
assert any(x > 0 for x in corrected.values()) and any(x < 0 for x in corrected.values())
result = {"F_AB": [[str(x) for x in row] for row in X],
          "symmetric_bipartite_pair_matrix": True,
          "hard_projection_k": 2,
          "spin_basis": "site-ordered creation operators",
          "Marshall_correction": "(-1)^(number of down spins on sites 0,1)",
          "amplitudes": rows,
          "fails_Marshall_sign_up_to_global_phase": True,
          "pass": True}
target = Path(__file__).with_name("bipartite_scope_checks.json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
