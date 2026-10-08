"""Duplicated d=3 control only; not a C8 advance beyond the prime-d line theorem."""
import numpy as np
from weyl3_search import d, Id, obs, reps

Hlines = []
for p in range(4):
    H = np.zeros((d**3, d**3), complex)
    for A in obs[2*p:2*p+2]:
        H += np.kron(np.kron(A.T, A), Id) + np.kron(np.kron(A.T, Id), A)
    Hlines.append(H)
D = [H - 2*np.eye(d**3) for H in Hlines]
print("line_spectra", [np.round(np.linalg.eigvalsh(H), 10).tolist() for H in Hlines])
print("shifted_square_spectra", [np.round(np.linalg.eigvalsh(M@M), 10).tolist() for M in D])
print("anticommutator_norms", [[float(np.linalg.norm(D[i]@D[j]+D[j]@D[i], 2)) for j in range(4)] for i in range(4)])
import itertools
for size in range(1, 5):
    tops = []
    for subset in itertools.combinations(range(4), size):
        HH = sum((Hlines[i] for i in subset), np.zeros_like(Hlines[0]))
        tops.append(float(np.linalg.eigvalsh(HH)[-1]))
    print("subset_size", size, "max_star", max(tops), "all_top_values", sorted(set(round(x, 10) for x in tops)))
print("commutator_full_line", [float(np.linalg.norm(sum(Hlines)-Hlines[i] if False else sum(Hlines)-Hlines[i] for i in []) ) if False else float(np.linalg.norm((sum(Hlines))@Hlines[i]-Hlines[i]@(sum(Hlines)), 2)) for i in range(4)])
