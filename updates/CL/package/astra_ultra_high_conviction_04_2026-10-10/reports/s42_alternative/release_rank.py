"""Exact finite-field rank of strong-clamp release sensitivity functions.

Uses formal time power series, not simulated hidden access. This checks only
the candidate function map's rank; it does not acquire coefficients physically.
"""
import json

P = 1000000007

def inv(a):
    return pow(int(a) % P, P - 2, P)

def power_series(d, exponent_num, exponent_den, order):
    ans = [1]
    exponent = exponent_num * inv(exponent_den) % P
    for k in range(1, order + 1):
        ans.append(ans[-1] * (exponent - (k - 1)) * inv(k) * d % P)
    return ans

def conv(a, b, order):
    return [sum(a[j] * b[k-j] for j in range(k+1)) % P
            for k in range(order+1)]

def rank(rows):
    a = [row[:] for row in rows]
    pivots = []
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row,len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        s = inv(a[row][col])
        a[row] = [x*s % P for x in a[row]]
        for i in range(row+1, len(a)):
            s = a[i][col]
            if s:
                a[i] = [(x-s*y) % P for x,y in zip(a[i],a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return len(pivots)

def matrix(c, order):
    m = len(c)
    h = [power_series(2*x*x, -3, 2, order) for x in c]
    up = [power_series(2*x*x, 3, 2, order) for x in c]
    down = [power_series(2*x*x, -1, 2, order) for x in c]
    oriented = {}
    for i in range(m):
        for j in range(m):
            integrand = conv(up[i],down[j],order)
            integral = [0]+[integrand[k-1]*inv(k)%P for k in range(1,order+1)]
            term = conv(h[i],integral,order)
            # q_1=-b.w_1; b_i=-c_i^3. Positive sign is immaterial to rank.
            oriented[i,j] = [(c[i]*c[j]*inv(3)*h[i][k]
                              +c[i]**3*c[j]*term[k]) % P
                             for k in range(order+1)]
    cols=[]
    for i in range(m):
        for j in range(i,m):
            cols.append([(oriented[i,j][k]+(oriented[j,i][k] if i!=j else 0))%P
                         for k in range(order+1)])
    return list(map(list, zip(*cols)))

results=[]
for m in range(1,13):
    unknowns=m*(m+1)//2
    order=2*unknowns+5
    mat=matrix(list(range(1,m+1)),order)
    r=rank(mat)
    first=next((j+1 for j in range(len(mat)) if rank(mat[:j+1])==unknowns),None)
    results.append(dict(hidden_nodes=m,unknowns=unknowns,rank=r,
                        checked_order=order,first_full_rank_rows=first))
print(json.dumps(results,indent=2))
