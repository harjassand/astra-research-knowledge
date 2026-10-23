"""Exact rational constrained-flow witness on K_s join P_m.

The universal proof uses the first 2s+1 sine modes. This executable uses
2s+1 disjoint integer tents, which gives the separately stated rational bound
C_2^4 >= h^2/[3(m-1)], h=floor(m/(2(2s+1))). It needs no floating eigensolver.
All input and witness entries are exact Fraction values. Bit costs are not
claimed constant; at fixed s the arithmetic operation count is O(m).
"""
from fractions import Fraction as F


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def transpose(A):
    return [list(row) for row in zip(*A)]


def rref(A, ncols=None):
    A = [list(map(F, row)) for row in A]
    n = len(A[0]) if A else (0 if ncols is None else ncols)
    pivots = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        a = A[r][c]
        A[r] = [x/a for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                a = A[i][c]
                A[i] = [x-a*y for x, y in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
        if r == len(A):
            break
    return A, pivots


def null_vector(A, ncols):
    R, pivots = rref(A, ncols)
    free = next((j for j in range(ncols) if j not in pivots), None)
    if free is None:
        raise ValueError("no nonzero null vector")
    z = [F(0)]*ncols
    z[free] = F(1)
    for row, col in zip(R, pivots):
        z[col] = -row[free]
    return z, len(pivots)


def inverse(A):
    n = len(A)
    aug = [list(row) + [F(i == j) for j in range(n)] for i, row in enumerate(A)]
    R, pivots = rref(aug)
    if pivots[:n] != list(range(n)):
        raise ValueError("singular")
    return [row[n:] for row in R]


def sparse_action(n, q, entries, X):
    out = [[F(0) for _ in range(q)] for _ in range(n)]
    for (i, j), a in entries.items():
        for k in range(q):
            out[i][k] += a*X[j][k]
            if i != j:
                out[j][k] += a*X[i][k]
    return out


def outer_sparse(w):
    active = [i for i, a in enumerate(w) if a]
    return {(i, j): w[i]*w[j] for i in active for j in active if i <= j}


def support(s, m):
    n = s+m
    return ([(i, i) for i in range(n)] + [(i, j) for i in range(s) for j in range(i+1, n)]
            + [(s+i, s+i+1) for i in range(m-1)])


def build(X, s):
    X = [list(map(F, row)) for row in X]
    n, q, m = len(X), s+2, len(X)-s
    if s < 0 or m < 2*(2*s+1) or any(len(row) != q for row in X):
        raise ValueError("need q=s+2 and m>=2(2s+1) for integer tents")
    if any(dot(x, x) > 1 for x in X):
        raise ValueError("row energy cap violated")
    T, V = X[:s], X[s:]
    if s and len(rref(T)[1]) < s:
        a, rank = null_vector(transpose(T), s)
        w = a + [F(0)]*m
        return {"kind":"apex_kernel", "X":X, "s":s, "m":m, "w":w,
                "kernel_entries":outer_sparse(w), "constraint_rank":rank}
    if s:
        Ginv = inverse([[dot(a, b) for b in T] for a in T])
        R = [[dot([dot(x, t) for t in T], col) for col in transpose(Ginv)] for x in V]
        Z = [[x[k]-sum((r[a]*T[a][k] for a in range(s)), F(0)) for k in range(q)] for x, r in zip(V, R)]
    else:
        R, Z = [[] for _ in V], [row[:] for row in V]
    for i in range(m-1):
        local = T + [V[i], V[i+1]]
        if len(rref(local)[1]) < q:
            a, rank = null_vector(transpose(local), q)
            w = a[:s] + [F(0)]*m
            w[s+i], w[s+i+1] = a[s:]
            return {"kind":"clique_kernel", "X":X, "s":s, "m":m, "w":w,
                    "kernel_entries":outer_sparse(w), "constraint_rank":rank}
    u, v = Z[0], Z[1]
    kappa = dot(u, u)*dot(v, v)-dot(u, v)**2
    assert kappa > 0
    def J(z):
        return [v[k]*dot(u,z)-u[k]*dot(v,z) for k in range(q)]
    JZ = [J(z) for z in Z]
    r2 = [dot(z,z) for z in Z]
    omega = [dot(JZ[i],Z[i+1]) for i in range(m-1)]
    assert all(omega)
    K = 2*s+1
    h = m//(2*K)
    tents = [[F(max(0,h-abs(i-(2*j+1)*h))) for i in range(m+1)] for j in range(K)]
    d_tents = [[f[i+1]-f[i] for i in range(m)] for f in tents]
    M = []
    for a in range(s):
        for basis in (u,v):
            M.append([sum((R[i][a]*df[i]*dot(JZ[i],basis)/r2[i] for i in range(m)),F(0)) for df in d_tents])
    alpha, rank = null_vector(M, K)
    c = [sum((alpha[j]*tents[j][i] for j in range(K)),F(0)) for i in range(m+1)]
    assert c[0] == c[-1] == 0 and any(c)
    energy = sum((c[i+1]-c[i])**2 for i in range(m))
    mass = sum(a*a for a in c)
    assert energy*h*h <= 3*mass
    b = [c[i+1]/omega[i] for i in range(m-1)]
    a = [-((b[i-1]*dot(Z[i],Z[i-1]) if i else 0) +
           (b[i]*dot(Z[i],Z[i+1]) if i<m-1 else 0))/r2[i] for i in range(m)]
    BR = [[a[i]*R[i][j] + (b[i-1]*R[i-1][j] if i else 0) +
           (b[i]*R[i+1][j] if i<m-1 else 0) for j in range(s)] for i in range(m)]
    entries = {(s+i,s+i):a[i] for i in range(m)}
    entries.update({(s+i,s+i+1):b[i] for i in range(m-1)})
    entries.update({(j,s+i):-BR[i][j] for i in range(m) for j in range(s)})
    entries.update({(j,k):sum((R[i][j]*BR[i][k] for i in range(m)),F(0)) for j in range(s) for k in range(j,s)})
    DX = sparse_action(n,q,entries,X)
    expected = [[F(0)]*q for _ in range(s)] + [[(c[i+1]-c[i])*JZ[i][k]/(kappa*r2[i]) for k in range(q)] for i in range(m)]
    assert DX == expected
    action2 = sum(dot(row,row) for row in DX)
    assert action2 > 0
    flow_ratio2 = max(x*x for x in b)/action2
    imin = min(range(m), key=lambda i:r2[i])
    w = [-x for x in R[imin]] + [F(i==imin) for i in range(m)]
    local_entries = outer_sparse(w)
    local_action = sparse_action(n,q,local_entries,X)
    w2 = dot(w,w)
    local_action2 = sum(dot(row,row) for row in local_action)
    assert local_action2 == w2*r2[imin]
    local_ratio2 = w2/r2[imin]
    lower_fourth = F(h*h,3*(m-1))
    assert max(flow_ratio2,local_ratio2)**2 >= lower_fourth
    return {"kind":"flow", "X":X, "s":s, "m":m, "h":h,
            "constraint_rank":rank,"alpha":alpha,"flow":c,
            "flow_entries":entries,"local_entries":local_entries,"local_w":w,
            "flow_action_squared":action2,"local_action_squared":local_action2,
            "flow_operator_lower_squared":max(x*x for x in b),
            "local_operator_squared":w2*w2,"flow_ratio_squared":flow_ratio2,
            "local_ratio_squared":local_ratio2,"guaranteed_ratio_fourth":lower_fourth,
            "tent_energy":energy,"tent_mass":mass,"kappa":kappa}


def unit_fixture(s, m):
    """Predetermined rational unit-row data, followed by rational rotations."""
    q=s+2
    X=[[F(i==j) for j in range(q)] for i in range(s)]
    for i in range(m):
        if s == 0:
            X.append(([F(1),F(0)],[F(0),F(1)],[F(3,5),F(4,5)])[i%3][:])
        else:
            t=[F(1)] + [F((i+j)%3-1) for j in range(1,s)] + [F((-1)**i*(1+(i%3==0)))]
            tt=dot(t,t)
            X.append([2*x/(1+tt) for x in t]+[(1-tt)/(1+tt)])
    for a in range(q-1):
        for row in X:
            x,y=row[a],row[a+1]
            row[a],row[a+1]=F(3,5)*x-F(4,5)*y,F(4,5)*x+F(3,5)*y
    assert all(dot(x,x)==1 for x in X)
    return X


def serializable(result):
    def rec(v):
        if isinstance(v,F): return str(v)
        if isinstance(v,dict):
            if v and all(isinstance(k,tuple) for k in v):
                return [[i,j,str(a)] for (i,j),a in sorted(v.items())]
            return {k:rec(a) for k,a in v.items()}
        if isinstance(v,(list,tuple)): return [rec(a) for a in v]
        return v
    return {"schema":"astra.separator_flow.v1",**rec(result)}
