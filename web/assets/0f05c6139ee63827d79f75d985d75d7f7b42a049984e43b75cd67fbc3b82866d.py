"""Check the exact C5 table and finite biased-ring error margins from v2.txt."""
from math import log, sqrt

n = 5
c = 11.0 / 20.0
phi = (1.0 + sqrt(5.0)) / 2.0
row_normalizer = 5.0 * (1.0 + 2.0 * c)
H = [[0.0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    H[i][i] = 1.0 / row_normalizer
    H[i][(i + 1) % n] = c / row_normalizer
    H[i][(i - 1) % n] = c / row_normalizer

# Copositive Horn witness: -1 on C5 edges and +1 on nonedges.
W = [[0.0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    W[i][i] = 1.0
    for j in range(n):
        if i != j:
            W[i][j] = -1.0 if (j - i) % n in (1, 4) else 1.0
horn_pairing = sum(W[i][j] * H[i][j] for i in range(n) for j in range(n))
min_eigenvalue = (1.0 - phi * c) / row_normalizer
horn_margin = -horn_pairing

M = 50000
switch_rate = 0.0001
eta = sqrt(M + 2.0) / M + switch_rate
robust_horn_margin = horn_margin - 2.0 * eta
robust_min_eigenvalue = min_eigenvalue - 2.0 * eta
epr_lower_bound = 2.0 * robust_horn_margin ** 2
realized_epr = M * log(M + 1.0)

# Build an Euler circuit in the balanced rational multigraph that realizes H
# as the exact directed edge-frequency table of a cyclic word of length 210.
counts = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    counts[i][i] = 20
    counts[i][(i + 1) % n] = 11
    counts[i][(i - 1) % n] = 11
adjacency = [[j for j in range(n) for _ in range(counts[i][j])] for i in range(n)]
stack = [0]
circuit = []
while stack:
    v = stack[-1]
    if adjacency[v]:
        stack.append(adjacency[v].pop())
    else:
        circuit.append(stack.pop())
word = list(reversed(circuit[:-1]))
assert len(word) == 210
word_counts = [[0 for _ in range(n)] for _ in range(n)]
for k, u in enumerate(word):
    v = word[(k + 1) % len(word)]
    word_counts[u][v] += 1
assert word_counts == counts
assert all(sum(row) == 42 for row in counts)
assert all(sum(counts[i][j] for i in range(n)) == 42 for j in range(n))

print(f"c={c:g}; H row marginal={1/n:g}; table mass={sum(map(sum, H)):.12g}")
print(f"PSD margin lambda_min(H)={min_eigenvalue:.12g}")
print(f"Horn pairing <W,H>={horn_pairing:.12g}")
print(f"M={M}; switch rate={switch_rate:g}; TV error bound eta={eta:.12g}")
print(f"retained PSD margin >= {robust_min_eigenvalue:.12g}")
print(f"retained negative Horn margin >= {robust_horn_margin:.12g}")
print(f"EPR lower bound from Horn+Pinsker >= {epr_lower_bound:.12g} nats/time")
print(f"realized ring EPR={realized_epr:.12g} nats/time")
print(f"Euler circuit length={len(word)}; exact edge-count table verified")

assert abs(sum(map(sum, H)) - 1.0) < 1e-14
assert min_eigenvalue > 0.0
assert horn_pairing < 0.0
assert robust_min_eigenvalue > 0.0
assert robust_horn_margin > 0.0
assert 0.0 < epr_lower_bound < realized_epr
