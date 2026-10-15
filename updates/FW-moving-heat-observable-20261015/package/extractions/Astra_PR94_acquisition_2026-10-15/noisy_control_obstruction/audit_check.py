"""Independent local numerical audit. No network or repository dependencies.
Constructs coefficients by closed-form products rather than stage elimination.
Numerics are sanity checks; AUDIT.md supplies the proof.
"""
import itertools
import numpy as np

rng = np.random.default_rng(854)
for m in range(1, 9):
    eps = m**-2
    delta = eps/(2*m*m)
    D = eps
    full_margin = eps/(4*(m+1)**2)
    lam = 1/full_margin
    P = np.zeros((m+2,m)); P[1:-1] = np.eye(m)
    b = np.zeros(m+2); b[0] = D
    c = np.zeros(m+2); c[-1] = 1
    max_error = energy_error = 0.
    min_ratio = float('inf')
    labels = list(itertools.product((0,1), repeat=m))
    test_u = [rng.random(m), np.zeros(m), np.ones(m)]
    sums = np.zeros(len(test_u))
    for s in labels:
        A = eps*np.eye(m)
        beta = np.array([eps*np.prod(s[:i]) for i in range(m)])
        gamma = np.array([(1-2*s[j])*np.prod(s[j+1:]) for j in range(m)])
        alpha = np.prod(s)
        for i in range(m):
            for j in range(i):
                A[i,j] = -eps*(1-2*s[j])*np.prod(s[j+1:i])
        B = np.zeros((m+2,m+2)); B[0,0] = B[-1,-1] = D
        B[1:-1,1:-1] = A; B[1:-1,0] = -beta
        B[-1,0] = -eps*alpha; B[-1,1:-1] = -eps*gamma
        ratio = np.linalg.eigvalsh((B+B.T)/2)[0]/full_margin
        min_ratio = min(min_ratio, ratio)
        assert ratio > .999
        x = rng.normal(size=m)
        y = [0.]
        for i, bit in enumerate(s):
            y.append(x[i] if bit == 0 else y[-1]-x[i])
        energy = eps/2*(y[-1]**2 + np.dot(np.diff(y),np.diff(y)))
        energy_error = max(energy_error, abs(x@A@x-energy))
        y0,zout = rng.normal(size=2)
        y = [y0]
        for i,bit in enumerate(s):
            y.append(x[i] if bit == 0 else y[-1]-x[i])
        vec = np.r_[y0,x,zout]
        full_energy = eps/2*(y0*y0+zout*zout+(y[-1]-zout)**2+np.dot(np.diff(y),np.diff(y)))
        energy_error = max(energy_error,abs(vec@B@vec-full_energy))
        for k,u in enumerate(test_u + [np.asarray(s)]):
            f = np.prod([eps/(eps+u[i]) if bit == 0 else u[i]/(eps+u[i]) for i,bit in enumerate(s)])
            M = B + P@np.diag(u)@P.T
            transfer = c@np.linalg.solve(M,b)
            scaled = (np.sqrt(lam)*c)@np.linalg.solve(lam*M,np.sqrt(lam)*b)
            max_error = max(max_error, abs(transfer-f), abs(scaled-f))
            if k < len(test_u): sums[k] += f
            else: assert f >= .5-1e-14
        # A vertex selected by a zero/one mismatch proves pairwise separation.
        if m <= 6:
            for t in labels:
                if t == s: continue
                r, other = (s,t) if any(a==0 and z==1 for a,z in zip(s,t)) else (t,s)
                other_at_r = np.prod([eps/(eps+r[i]) if bit == 0 else r[i]/(eps+r[i]) for i,bit in enumerate(other)])
                assert other_at_r == 0
    assert np.max(np.abs(sums-1)) < 1e-12
    assert max_error < 1e-11
    assert energy_error < 1e-11
    print(f'm={m} plants={len(labels)} full_coercivity_ratio={min_ratio:.6g} transfer_error={max_error:.3g} energy_error={energy_error:.3g}')

# Exact N854 triple witness, including rescaling to t3=1/2.
from fractions import Fraction as F

def solve_fraction(M, b):
    rows = [list(row)+[rhs] for row,rhs in zip(M,b)]
    n = len(rows)
    for i in range(n):
        pivot = next(j for j in range(i,n) if rows[j][i])
        rows[i],rows[pivot] = rows[pivot],rows[i]
        q = rows[i][i]; rows[i] = [v/q for v in rows[i]]
        for j in range(n):
            if j != i:
                q = rows[j][i]
                rows[j] = [v-q*w for v,w in zip(rows[j],rows[i])]
    return [row[-1] for row in rows]

a = [F(1),F(2),F(3)]
H = [[F(10),F(1,5),F(1,2)], [F(3,10),F(10),F(11,10)], [F(7,10),F(13,10),F(10)]]
values = []
for flips in itertools.product((0,1), repeat=2):
    C = [row.copy() for row in H]
    for flip,(i,j) in zip(flips,[(0,2),(1,2)]):
        if flip: C[i][j],C[j][i] = (a[j]/a[i])*C[j][i],(a[i]/a[j])*C[i][j]
    for t in (F(1),F(1,2)):
        scaled_H = [[v/t for v in row] for row in C]
        scaled_a = [v/t for v in a]
        M = [[F(i==j)+t*scaled_H[i][j] for j in range(3)] for i in range(3)]
        z = solve_fraction(M,[F(1)]*3)
        value = F(10)-sum(scaled_a[i]*t*z[i] for i in range(3))
        if t == 1: values.append(value)
        else: assert value == values[-1]
assert len(set(values)) == 4
print('Exact N854 triple candidate values:', ', '.join(map(str,values)))
