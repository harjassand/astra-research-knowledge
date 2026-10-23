"""Small independent algebra checks; no sampled-X claim of universality."""
from fractions import Fraction as F
from pathlib import Path
import json
import time

started = time.perf_counter()

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def trans(a):
    return list(map(list, zip(*a)))

def mul(a, b):
    return [[dot(row, col) for col in trans(b)] for row in a]

def fnorm2(a):
    return sum((dot(row, row) for row in a), F(0))

def det(a, b):
    return a[0]*b[1]-a[1]*b[0]

checks = {}

# Proof X: exact skew-field adjoint entries and Frobenius factor 1/2.
n = 8
X = [[F(1, 5), F(i+1, 20), F((-1)**i, 7)] for i in range(n)]
assert all(F(0) < dot(x, x) <= 1 for x in X)
A = [[F(0), F(-1), F(0)], [F(1), F(0), F(0)], [F(0), F(0), F(0)]]
f = [F(max(0, 2-abs(i-2))) for i in range(1, n+1)]
Y = [[f[i]*v for v in mul([X[i]], trans(A))[0]] for i in range(n)]
adj = [[F(0) for _ in range(n)] for _ in range(n)]
energy = F(0)
for i in range(n):
    adj[i][i] = dot(Y[i], X[i])
    assert adj[i][i] == 0
    for j in range(i+1, min(n, i+3)):
        adj[i][j] = adj[j][i] = (dot(Y[i], X[j])+dot(Y[j], X[i]))/2
        xAx = dot(X[i], [dot(row, X[j]) for row in A])
        assert adj[i][j] == (f[j]-f[i])*xAx/2
        energy += (f[j]-f[i])**2*xAx**2/2
assert fnorm2(adj) == energy
checks['proof_x_adjoint_identity_and_half_factor'] = True

rotations = [
    [[0,-1,0],[1,0,0],[0,0,0]],
    [[0,0,-1],[0,0,0],[1,0,0]],
    [[0,0,0],[0,0,-1],[0,1,0]],
]
for x in X:
    assert sum(dot([dot(row,x) for row in a], [dot(row,x) for row in a]) for a in rotations) == 2*dot(x,x)
checks['proof_x_rotation_energy'] = True

for m in range(1, 11):
    ff = lambda i: max(0, m-abs(i))
    assert sum(ff(i)**2 for i in range(-m-2,m+3)) == F(2*m**3+m,3)
    assert sum((ff(i+1)-ff(i))**2 for i in range(-m-2,m+3)) == 2*m
    assert sum((ff(i+2)-ff(i))**2 for i in range(-m-2,m+3)) <= 8*m
checks['proof_x_tent_sums_m_1_through_10'] = True

# Proof Y: m=4 makes the three sine modes span the entire flow space.
# Hence an exact rational null vector tests the same two-constraint lift.
m = 4
Z = [[F(1,5),F(i,10)] for i in range(1,m+1)]
t = [F((-1)**i,7) for i in range(1,m+1)]
r0 = F(1,2)
Xfan = [[F(0),F(0),r0]]+[z+[tt] for z,tt in zip(Z,t)]
assert all(dot(x,x)<=1 for x in Xfan)

def flow(c):
    cc = [F(0)] + c + [F(0)]
    b = [cc[i+1]/det(Z[i],Z[i+1]) for i in range(m-1)]
    B = [[F(0) for _ in range(m)] for _ in range(m)]
    for i in range(m-1):
        B[i][i+1] = B[i+1][i] = b[i]
    for i in range(m):
        B[i][i] = -sum(B[i][j]*dot(Z[i],Z[j]) for j in range(m) if j!=i)/dot(Z[i],Z[i])
    BZ = mul(B,Z)
    for i in range(m):
        assert BZ[i] == [(cc[i+1]-cc[i])*(-Z[i][1])/dot(Z[i],Z[i]), (cc[i+1]-cc[i])*Z[i][0]/dot(Z[i],Z[i])]
    assert fnorm2(BZ) == sum((cc[i+1]-cc[i])**2/dot(Z[i],Z[i]) for i in range(m))
    return B, BZ

basis = [[F(int(i==j)) for i in range(m-1)] for j in range(m-1)]
q = [mul([t],flow(c)[1])[0] for c in basis]
a, b = trans(q)
c = [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
assert any(c)
B, BZ = flow(c)
assert mul([t],BZ) == [[0,0]]
L = [[-tt/r0 for tt in t]] + [[F(int(i==j)) for j in range(m)] for i in range(m)]
D = mul(mul(L,B),trans(L))
DX = mul(D,Xfan)
assert DX == [[F(0),F(0),F(0)]] + [row+[F(0)] for row in BZ]
assert fnorm2(DX) == fnorm2(BZ) > 0
assert any(any(row) for row in D)
assert D == trans(D)
for i in range(1,m+1):
    for j in range(1,m+1):
        if abs(i-j)>1:
            assert D[i][j] == 0
checks['proof_y_flow_identity_and_energy'] = True
checks['proof_y_two_constraints_and_exact_lift'] = True
checks['proof_y_symmetric_fan_support_and_nonzero_action'] = True

results = {
    'all_checks_passed': all(checks.values()),
    'checks': checks,
    'calculation_seconds': time.perf_counter()-started,
    'scope': 'Exact rational identity checks on small examples only; verdict rests on the universal analytic arguments.',
}
Path(__file__).with_name('independent_exact_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
