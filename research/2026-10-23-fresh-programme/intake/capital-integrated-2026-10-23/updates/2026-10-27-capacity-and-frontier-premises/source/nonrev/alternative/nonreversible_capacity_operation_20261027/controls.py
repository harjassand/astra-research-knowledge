"""Independent full-state and independent gather-residual controls.

The reference generator is assembled from literal semantic local cycles;
it does not use Operator's transition tables or scatter algorithm.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import math
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True
from nonreversible import Operator, box, unbox, certify

RING = ((0,0),(1,0),(1,1),(0,1))


def assemble(n, theta, gamma):
    size = 1 << n
    states = [tuple((x >> i) & 1 for i in range(n)) for x in range(size)]
    index = {s:i for i,s in enumerate(states)}
    q = [[F(0) for _ in states] for _ in states]
    base = [[F(0) for _ in states] for _ in states]
    weights = [theta**sum(s) for s in states]
    for x, s in enumerate(states):
        for i in range(n):
            v = list(s)
            v[i] = 1-v[i]
            y = index[tuple(v)]
            rate = theta/(1+theta) if s[i] == 0 else 1/(1+theta)
            q[x][y] += rate
            q[x][x] -= rate
            base[x][y] += rate
            base[x][x] -= rate
        for i in range(n-1):
            local = (s[i],s[i+1])
            new = RING[(RING.index(local)+1) % 4]
            v = list(s)
            v[i],v[i+1] = new
            y = index[tuple(v)]
            rate = gamma*theta**2 / theta**sum(local)
            q[x][y] += rate
            q[x][x] -= rate
    adjoint = [[weights[y]*q[y][x]/weights[x]
                for y in range(size)] for x in range(size)]
    return q,adjoint,base,weights


def mv(a, v):
    return [sum((x*y for x,y in zip(row,v)),F(0)) for row in a]


def inner(w, x, y):
    return sum((a*b*c for a,b,c in zip(w,x,y)),F(0))


def full_solve(matrix, rhs):
    # Independent FLINT exact solve rather than certificate's elimination.
    sys.path.insert(0,str(Path(__file__).resolve().parents[1] /
        'missing_scientific_operation_20261027' / '_deps'))
    from flint import fmpq, fmpq_mat
    a = fmpq_mat([[fmpq(x.numerator,x.denominator) for x in row] for row in matrix])
    b = fmpq_mat([[fmpq(x.numerator,x.denominator)] for x in rhs])
    v = a.solve(b)
    assert a*v == b
    return [F(int(v[i,0].p),int(v[i,0].q)) for i in range(len(rhs))]


def poisson(h, u, pin):
    a = [row[:] for row in h]
    rhs = u[:]
    a[pin] = [F(int(i==pin)) for i in range(len(a))]
    rhs[pin] = F(0)
    x = full_solve(a,rhs)
    assert mv(h,x) == u
    return x


def psd_ldl(a):
    """Exact symmetric semidefinite elimination, including zero pivots."""
    a = [row[:] for row in a]
    size = len(a)
    assert all(a[i][j] == a[j][i] for i in range(size) for j in range(size))
    rank = 0
    for k in range(size):
        d = a[k][k]
        assert d >= 0
        if d == 0:
            assert all(a[k][i] == 0 for i in range(k,size))
            continue
        rank += 1
        for i in range(k+1,size):
            for j in range(i,size):
                a[i][j] -= a[i][k]*a[k][j]/d
                a[j][i] = a[i][j]
    return rank


def small_control(n,theta,gamma):
    started = time.perf_counter()
    q,qa,q0,w = assemble(n,theta,gamma)
    size = len(q)
    h = [[-x for x in row] for row in q]
    ha = [[-x for x in row] for row in qa]
    assert all(sum(row,F(0)) == 0 for row in q)
    assert all(sum((w[x]*q[x][y] for x in range(size)),F(0)) == 0
               for y in range(size))
    assert all(q[x][y] >= 0 for x in range(size) for y in range(size) if x!=y)
    current = w[0]*q[0][1] - w[1]*q[1][0]
    assert current == gamma*theta**2
    op = Operator(n,theta,gamma)
    a,b = 0,size-1
    rho = w[b]/w[a]
    u = [F(0)]*size
    u[a],u[b] = rho,-1
    x = poisson(h,u,b)
    z = poisson(ha,u,b)
    I = inner(w,u,x)/rho
    assert I == x[a]-x[b] == inner(w,u,z)/rho
    interior = [i for i in range(size) if i not in (a,b)]
    killed = [[h[i][j] for j in interior] for i in interior]
    hit = full_solve(killed,[-h[i][b] for i in interior])
    hitprob = [F(0)]*size
    hitprob[b] = F(1)
    for i,v in zip(interior,hit):
        hitprob[i] = v
    assert all(0 <= v <= 1 for v in hitprob)
    assert all(v == 0 for i,v in enumerate(mv(h,hitprob)) if i in interior)
    Ra = -q[a][a]
    p = sum((q[a][j]*hitprob[j] for j in range(size) if j!=a),F(0))/Ra
    assert I == rho/(Ra*p)
    # All columns of both full operators versus independent sparse scatter.
    # This catches backward/forward orientation and omitted predecessor rows.
    for j in range(size):
        for adjoint,mat in ((False,h),(True,ha)):
            got = op.apply({j:1},adjoint)
            expected = {i:int(op.D*mat[i][j]) for i in range(size) if mat[i][j]}
            assert all(op.D*mat[i][j] == expected.get(i,0) for i in range(size))
            assert got == expected
    # Symmetric contribution beyond the independent base is PSD exactly.
    added = [[w[i]*((h[i][j]+ha[i][j])/2 + q0[i][j])
               for j in range(size)] for i in range(size)]
    added_rank = psd_ldl(added)
    # Every product eigenfunction of the independent heat-bath base has
    # eigenvalue equal to its subset size, proving the claimed base gap.
    pbit = theta/(1+theta)
    for mask in range(size):
        f = []
        for state in range(size):
            value = F(1)
            for i in range(n):
                if mask >> i & 1:
                    value *= ((state >> i)&1)-pbit
            f.append(value)
        assert mv(q0,f) == [-mask.bit_count()*v for v in f]
    result,internals = certify(n,theta,gamma,degree_cap=3,
                              progress=False,return_internal=True)
    op,primal,dual,data = internals
    k = result['degree']
    yf = [F(op.D,op.W)*sum((c*v.get(i,0) for c,v in
          zip(data['alpha'],primal[:-1])),F(0)) for i in range(size)]
    zf = [F(op.D,op.W)*sum((c*v.get(i,0) for c,v in
          zip(data['beta'],dual[:-1])),F(0)) for i in range(size)]
    r = [aa-bb for aa,bb in zip(u,mv(h,yf))]
    s = [aa-bb for aa,bb in zip(u,mv(ha,zf))]
    r2,s2 = inner(w,r,r),inner(w,s,s)
    assert r2 == data['r2']/op.W**3
    assert s2 == data['s2']/op.W**3
    estimate = (inner(w,u,yf)+inner(w,zf,r))/rho
    assert estimate == data['estimate']
    error_identity = inner(w,s,poisson(h,r,b))/rho
    assert I-estimate == error_identity
    assert (I-estimate)**2 <= r2*s2/(rho*op.gap)**2
    assert unbox(result['I_lower']) <= I <= unbox(result['I_upper'])
    assert unbox(result['p_lower']) <= p <= unbox(result['p_upper'])
    # Rational uniformisation kernels test the four-term identity directly.
    uniform = op.Rmax
    P = [[F(int(i==j)) + q[i][j]/uniform for j in range(size)] for i in range(size)]
    assert all(v>=0 for row in P for v in row)
    power = [[F(int(i==j)) for j in range(size)] for i in range(size)]
    for step in range(4):
        quartet = rho*power[a][a]+power[b][b]-power[a][b]-rho*power[b][a]
        assert quartet == inner(w,u,mv(power,u))/rho
        power = [[sum((power[i][k]*P[k][j] for k in range(size)),F(0))
                  for j in range(size)] for i in range(size)]
    return {'n':n,'theta':str(theta),'gamma':str(gamma),'states':size,
        'I_exact':box(I),'p_exact':box(p),'stationary_current_0_to_1':box(current),
        'added_symmetric_PSD_rank':added_rank,'all_primal_and_adjoint_columns_checked':2*size,
        'exact_product_base_eigenfunctions_checked':size,
        'killed_poisson_adjoint_and_error_identity':'PASS',
        'certificate_interval_contains_exact_answer':True,
        'sparse_primal_and_dual_first_powers_differ':primal[1] != dual[1],
        'quartet_kernel_powers_checked':4,'seconds':time.perf_counter()-started}


def lincomb_integer(coefficients,vectors):
    den = math.lcm(*(v.denominator for v in coefficients))
    out = {}
    for c,v in zip(coefficients,vectors):
        integer = int(c*den)
        for x,y in v.items():
            out[x] = out.get(x,0) + integer*y
    return {x:y for x,y in out.items() if y},den


def three_state_control():
    # Parent suggested this counterexample; assemble and execute independently.
    q = [[F(0) for _ in range(3)] for _ in range(3)]
    for x in range(3):
        q[x][(x+1)%3] = F(2)
        q[x][(x-1)%3] = F(1)
        q[x][x] = F(-3)
    h = [[-v for v in row] for row in q]
    ha = [list(row) for row in zip(*h)]
    w,u = [F(1)]*3,[F(1),F(0),F(-1)]
    x = poisson(h,u,2)
    I = inner(w,u,x)
    y = [F(3,14)*v for v in u]
    r = [a-b for a,b in zip(u,mv(h,y))]
    s = [a-b for a,b in zip(u,mv(ha,y))]
    estimate = inner(w,u,y)+inner(w,y,r)
    r2,s2 = inner(w,r,r),inner(w,s,s)
    gap = F(9,2)
    assert I == F(3,7)
    assert estimate == F(87,196) > I
    assert r2 == s2 == F(1,14)
    assert abs(I-estimate) <= F(1,63)
    assert (I-estimate)**2 <= r2*s2/gap**2
    P = [[F(int(i==j))+q[i][j]/6 for j in range(3)] for i in range(3)]
    quartet = P[0][0]+P[2][2]-P[0][2]-P[2][0]
    merged_wrong = P[0][0]+P[2][2]-2*P[2][0]
    assert quartet == inner(w,u,mv(P,u))
    assert quartet != merged_wrong
    return {'status':'PASS','I_exact':box(I),'p_exc_exact':box(F(7,9)),
            'symmetric_gap_exact':box(gap),'estimate':box(estimate),
            'two_sided_radius':box(F(1,63)),
            'both_residual_norms_squared':box(r2),
            'reversible_lower_bound_is_invalid':True,
            'merging_cross_terms_is_invalid':True,
            'origin':'Parent supplied example; independently assembled and executed here.'}


def gather_apply(n,theta,gamma,D,vector,adjoint=False):
    """Independent literal outgoing stencil, gathering at ALL possible rows."""
    candidates = set(vector)
    for x in vector:
        for i in range(n):
            candidates.add(x ^ (1 << i))
    base = {bit:int(D*(theta if bit==0 else 1)/(1+theta)) for bit in (0,1)}
    rates = {pair:int(D*gamma*theta**2/theta**sum(pair)) for pair in RING}
    assert all(F(rate,D) == gamma*theta**2/theta**sum(pair)
               for pair,rate in rates.items())
    out = {}
    direction = -1 if adjoint else 1
    for x in candidates:
        fx = vector.get(x,0)
        value = 0
        for i in range(n):
            bit = (x >> i)&1
            y = x ^ (1 << i)
            value += base[bit]*(fx-vector.get(y,0))
        for i in range(n-1):
            pair = ((x >> i)&1,(x >> (i+1))&1)
            new = RING[(RING.index(pair)+direction)%4]
            y = x ^ ((pair[0]^new[0]) << i) ^ ((pair[1]^new[1]) << (i+1))
            value += rates[pair]*(fx-vector.get(y,0))
        if value:
            out[x] = value
    return out,len(candidates),len(candidates)*(2*n-1)


def large_control(path):
    started = time.perf_counter()
    saved = json.loads(path.read_text())
    n,theta,gamma = saved['n'],F(saved['theta']),F(saved['gamma'])
    recomputed,internal = certify(n,theta,gamma,F(saved['epsilon']),
                      saved['degree_cap'],progress=False,return_internal=True)
    for field in ('I_lower','I_upper','p_lower','p_upper'):
        assert recomputed[field] == saved[field]
    op,primal,dual,data = internal
    # Independently form the actual finite-support trial vectors, then gather
    # their full backward/adjoint residuals. No Gram-matrix norm shortcut.
    y,dy = lincomb_integer(data['alpha'],primal[:-1])
    z,dz = lincomb_integer(data['beta'],dual[:-1])
    hy,cy,ey = gather_apply(n,theta,gamma,op.D,y,False)
    hz,cz,ez = gather_apply(n,theta,gamma,op.D,z,True)
    r = {x:dy*v for x,v in primal[0].items()}
    s = {x:dz*v for x,v in dual[0].items()}
    for x,v in hy.items():
        r[x] = r.get(x,0)-v
    for x,v in hz.items():
        s[x] = s.get(x,0)-v
    r = {x:v for x,v in r.items() if v}
    s = {x:v for x,v in s.items() if v}
    r2 = F(sum(theta.numerator**x.bit_count()*theta.denominator**(n-x.bit_count())
               *v*v for x,v in r.items()),dy**2)
    s2 = F(sum(theta.numerator**x.bit_count()*theta.denominator**(n-x.bit_count())
               *v*v for x,v in s.items()),dz**2)
    assert r2 == data['r2']
    assert s2 == data['s2']
    assert sum(op.weight(x)*v for x,v in r.items()) == 0
    assert sum(op.weight(x)*v for x,v in s.items()) == 0
    uy = F(sum(op.weight(x)*v*y.get(x,0) for x,v in primal[0].items()),dy)
    zr = F(sum(op.weight(x)*v*r.get(x,0) for x,v in z.items()),dy*dz)
    estimate = op.D*(uy+zr)/(op.W**2*op.N)
    assert estimate == data['estimate']
    assert data['radius']**2 >= r2*s2/(op.W**2*op.N*op.gap)**2
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes = rss if platform.system()=='Darwin' else 1024*rss
    return {'status':'PASS','n':n,'theta':str(theta),'gamma':str(gamma),
        'saved_certificate':path.name,'degree':saved['degree'],
        'regenerated_bounds_identical':True,
        'independent_reference':'literal outgoing-stencil gather on full neighbor closure',
        'primal_trial_support':len(y),'dual_trial_support':len(z),
        'primal_full_residual_support':len(r),'dual_full_residual_support':len(s),
        'primal_candidate_rows':cy,'dual_candidate_rows':cz,
        'reference_local_term_evaluations':ey+ez,
        'primal_residual_norm2_scaled':box(r2),'dual_residual_norm2_scaled':box(s2),
        'estimate_matches_Gram_computation':True,
        'residual_mean_zero':True,
        'trial_common_denominator_largest_bits':max(dy.bit_length(),dz.bit_length()),
        'residual_integer_largest_bits':max(abs(v).bit_length() for v in list(r.values())+list(s.values())),
        'seconds_including_certificate_regeneration':time.perf_counter()-started,
        'peak_process_RSS_bytes':rss_bytes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--large',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.large:
        result = large_control(args.large)
    else:
        start = time.perf_counter()
        controls = []
        for n,theta,gamma in [(2,F(1,4),F(1,2)),(3,F(1,4),F(1,2)),
                               (4,F(1,4),F(1,2)),(5,F(1,4),F(1,2)),
                               (4,F(2,5),F(3,7))]:
            item = small_control(n,theta,gamma)
            controls.append(item)
            print('full-state PASS',n,str(theta),str(gamma),flush=True)
        result = {'status':'PASS','controls':controls,
                  'three_state_counterexample':three_state_control(),
                  'seconds':time.perf_counter()-start,
                  'scope':'Independent assembly and exact arithmetic validate these models; they do not certify an arbitrary source or physical system.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('controls','primal_residual_norm2_scaled','dual_residual_norm2_scaled')}),flush=True)
