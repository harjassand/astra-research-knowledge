"""Exact hard BCS counting/sampling for acquired gauged Green kernels.

Off diagonal F_ij=a_i*b_j*x_min(i,j). x may be complex and nonmonotone.
The min denotes the smaller INDEX. Diagonal entries are irrelevant at hard
projection. Dense nonzero off-diagonal input parameters are acquired exactly.
All canonical counts and prefix counts use O(n^2) rational arithmetic.
"""
from cutrank_bcs import *
from dataclasses import dataclass


@dataclass
class GreenParameters:
    x: list
    a: list
    b: list


def green_matrix(params):
    n = len(params.x)
    return [[params.a[i]*params.b[j]*params.x[min(i,j)]
             for j in range(n)] for i in range(n)]


def verify_green(F, params):
    n = len(F)
    if not all(len(v) == n for v in (params.x, params.a, params.b)):
        raise ValueError('parameter dimensions')
    if not all(len(row) == n for row in F):
        raise ValueError('square F required')
    for i in range(n):
        for j in range(n):
            if i != j and C.of(F[i][j]) != params.a[i]*params.b[j]*params.x[min(i,j)]:
                raise ValueError({'failed_offdiagonal_entry': [i,j]})
    return params


def acquire_dense_green(F):
    """Exact recognizer and parameter acquisition; no supplied factorization.

    Input off-diagonal entries must be nonzero. Rejects any failed symmetry
    gauge or upper Green identity, with a specific offending entry.
    """
    F = [[C.of(v) for v in row] for row in F]
    n = len(F)
    if not n or not all(len(row) == n for row in F):
        raise ValueError('nonempty square F required')
    if n == 1:
        return GreenParameters([ONE], [ONE], [ONE])
    for i in range(n):
        for j in range(n):
            if i != j and not F[i][j]:
                raise ValueError({'dense_admission_zero_entry': [i,j]})
    # F=diag(s) H, with H symmetric. The first site fixes the diagonal gauge.
    s = [ONE]+[F[i][0]/F[0][i] for i in range(1,n)]
    H = [[F[i][j]/s[i] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if H[i][j] != H[j][i]:
                raise ValueError({'failed_symmetrization': [i,j]})
    # H_ij=p_i*q_j for i<j. p_0=q_0=1 is an exact harmless gauge;
    # p_(n-1) has no off-diagonal use and is chosen equal to q_(n-1).
    q = [ONE]+[H[0][j] for j in range(1,n)]
    p = [ONE]+[H[i][n-1]/q[n-1] for i in range(1,n-1)]+[q[n-1]]
    for i in range(n):
        for j in range(i+1,n):
            if H[i][j] != p[i]*q[j]:
                raise ValueError({'failed_upper_Green_identity': [i,j]})
    params = GreenParameters([p[i]/q[i] for i in range(n)],
                             [s[i]*q[i] for i in range(n)], q)
    return verify_green(F, params)


class GreenCounter:
    """Count tables and exact independent samples under hard local tables.

    weights[i]=(empty,up,down), all nonnegative rational. Physical hard prefix
    constraints set disallowed local weights to zero; no inverse event cost.
    """
    def __init__(self, params, weights=None):
        self.params = params
        self.n = len(params.x)
        n = self.n
        weights = [(Q(1),Q(1),Q(1)) for _ in range(n)] if weights is None else weights
        if len(weights) != n or any(len(w) != 3 for w in weights):
            raise ValueError('one empty/up/down table per site')
        weights = [[Q(z) for z in w] for w in weights]
        if any(z < 0 for w in weights for z in w):
            raise ValueError('nonnegative local weights required')
        self.x = [ZERO]+list(params.x)
        self.A = [Q(0)]+[params.a[i].abs2()*weights[i][1] for i in range(n)]
        self.B = [Q(0)]+[params.b[i].abs2()*weights[i][2] for i in range(n)]
        self.E = [Q(1)]+[w[0] for w in weights]
        base = [Q(1)]*(n+1)
        for r in range(n-1,-1,-1):
            base[r] = self.E[r+1]*base[r+1]
        self.DP = [base]
        self.R = [[Q(0)]*(n+1)]
        for m in range(1,n//2+1):
            prev = self.DP[m-1]
            qa, qb = [Q(0)]*(n+1), [Q(0)]*(n+1)
            for r in range(n-1,-1,-1):
                q = r+1
                qa[r] = self.A[q]*prev[q]+self.E[q]*qa[q]
                qb[r] = self.B[q]*prev[q]+self.E[q]*qb[q]
            R = [self.A[p]*qb[p]+self.B[p]*qa[p] for p in range(n+1)]
            s0, s1, s2 = [Q(0)]*(n+1), [ZERO]*(n+1), [Q(0)]*(n+1)
            for r in range(n-1,-1,-1):
                p = r+1
                s0[r] = R[p]+self.E[p]*s0[p]
                s1[r] = R[p]*self.x[p]+self.E[p]*s1[p]
                s2[r] = R[p]*self.x[p].abs2()+self.E[p]*s2[p]
            cur = [Q(0)]*(n+1)
            for r in range(n+1):
                cross = (self.x[r].conj()*s1[r]).re
                cur[r] = s2[r]-2*cross+self.x[r].abs2()*s0[r]
                if cur[r] < 0:
                    raise AssertionError('exact DP positivity invariant failed')
            self.DP.append(cur)
            self.R.append(R)

    def counts(self):
        return [v[0] for v in self.DP]+[Q(0)]*(self.n-len(self.DP)+1)

    def sample(self, k, rng=None):
        rng = random.SystemRandom() if rng is None else rng
        if not isinstance(k, int) or not 0 <= k <= self.n//2 or not self.DP[k][0]:
            raise ValueError('zero or invalid requested sector')
        states, r, m = [0]*self.n, 0, k
        while m:
            ws, empty = [], Q(1)
            for p in range(r+1,self.n+1):
                ws.append(empty*(self.x[p]-self.x[r]).abs2()*self.R[m][p])
                empty *= self.E[p]
            p = r+1+integer_choice(ws,rng)
            ws, empty = [], Q(1)
            for q in range(p+1,self.n+1):
                h = self.A[p]*self.B[q]+self.B[p]*self.A[q]
                ws.append(empty*h*self.DP[m-1][q])
                empty *= self.E[q]
            q = p+1+integer_choice(ws,rng)
            orientation = integer_choice([self.A[p]*self.B[q],self.B[p]*self.A[q]],rng)
            states[p-1], states[q-1] = (1,2) if orientation == 0 else (2,1)
            r, m = q, m-1
        assert self.DP[0][r] > 0
        return states


def green_counts(F, allowed=None):
    params = acquire_dense_green(F)
    n = len(F)
    allowed = [set(range(4)) for _ in range(n)] if allowed is None else allowed
    weights = [[Q(int(x in allowed[i])) for x in (0,1,2)] for i in range(n)]
    return GreenCounter(params,weights).counts()
