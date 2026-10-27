"""Exact finite-support Galerkin bounds for an actual reversible pair chain.

The graph is not enumerated. Integer-scaled powers of the full BACKWARD
operator include every neighbor, including those outside the trial support.
This is an ordinary Galerkin certificate, not a new rarity complexity claim.
"""
from fractions import Fraction as F
from pathlib import Path
import sys, math, time, json, resource, platform
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] /
    'missing_scientific_operation_20261027' / '_deps'))
from flint import fmpq, fmpq_mat


def product(xs):
    ans = 1
    for x in xs:
        ans *= x
    return ans


def fixture(m):
    return ([F(17 + (7*i % 13), 100) for i in range(m)],
            [F(11 + (3*i % 7), 10) for i in range(m-1)])


def rational_box(x):
    x = F(x)
    return {'num_hex': hex(x.numerator), 'den_hex': hex(x.denominator),
            'num_bits': abs(x.numerator).bit_length(),
            'den_bits': x.denominator.bit_length(), 'approx': float(x)}


def decode(box):
    return F(int(box['num_hex'], 16), int(box['den_hex'], 16))


def exact_fraction(v):
    if type(v) not in (int, F):
        raise TypeError('Exact int or Fraction inputs are required')
    return F(v)


class ActualOperator:
    def __init__(self, theta, clocks, delta=F(0)):
        self.theta = list(map(exact_fraction, theta))
        self.clocks = list(map(exact_fraction, clocks))
        self.delta = exact_fraction(delta)
        self.m = len(self.theta)
        if self.m < 4 or self.m % 2 or len(self.clocks) != self.m-1:
            raise ValueError('Even M >= 4 and M-1 clocks are required')
        if not all(0 < t < 1 for t in self.theta):
            raise ValueError('0 < theta < 1 required')
        if not all(a > 0 for a in self.clocks) or self.delta < 0:
            raise ValueError('Positive clocks and nonnegative delta required')
        self.a, self.b = 0, (1 << self.m)-1
        self.nums = [t.numerator for t in self.theta]
        self.dens = [t.denominator for t in self.theta]
        self.W, self.N = product(self.dens), product(self.nums)
        self.rho = F(self.N, self.W)
        rational_table = []
        creation = []
        for i, alpha in enumerate(self.clocks):
            t, s = self.theta[i:i+2]
            c, an = alpha*t*s/(1+t*s), alpha/(1+t*s)
            right, left = alpha*s/(t+s), alpha*t/(t+s)
            creation.append(c)
            rational_table.append([[q*(1+self.delta*z)
                for q in (c, right, left, an)] for z in (0, 1)])
        self.D = math.lcm(*(q.denominator for tab in rational_table
                               for row in tab for q in row))
        self.table = [[[int(q*self.D) for q in row] for row in tab]
                      for tab in rational_table]
        assert all(q*self.D == v for tab, itab in zip(rational_table,self.table)
                   for row, irow in zip(tab,itab) for q,v in zip(row,irow))
        self.Ra = sum(creation, F(0))
        self.Rstar = (1+self.delta)*sum(self.clocks, F(0))
        # Ordered heatbath coupling gives this reference gap; the one-sided
        # same-Gibbs conductance perturbation cannot reduce it.
        self.gap = 2*min(creation)
        self.weight_cache = {self.a:self.W, self.b:self.N}
        self.transition_cache = {}
        self.edge_evaluations = 0

    def weight(self, x):
        if x not in self.weight_cache:
            ans = self.W
            for i in range(self.m):
                if x >> i & 1:
                    ans = ans // self.dens[i] * self.nums[i]
            self.weight_cache[x] = ans
        return self.weight_cache[x]

    def transitions(self, x):
        if x not in self.transition_cache:
            rows = []
            for i in range(self.m-1):
                j = i-1 if i else 2
                outside, pair = x >> j & 1, x >> i & 3
                rows.append((x ^ (3 << i), self.table[i][outside][pair],
                             self.table[i][outside][pair ^ 3]))
            self.transition_cache[x] = tuple(rows)
            self.edge_evaluations += self.m-1
        return self.transition_cache[x]

    def apply_A(self, vector):
        """Apply A=D*(-Q_backward) to finite support; include all neighbors."""
        out = {}
        for x, value in vector.items():
            if not value:
                continue
            wx = self.weight(x)
            rows = self.transitions(x)
            out[x] = out.get(x, 0) + sum(q for _,q,_ in rows)*value
            for y, forward, reverse in rows:
                wy, rem = divmod(wx*forward, reverse)
                assert rem == 0
                old = self.weight_cache.setdefault(y, wy)
                assert old == wy
                out[y] = out.get(y, 0) - reverse*value
        out = {x:v for x,v in out.items() if v}
        assert sum(self.weight(x)*v for x,v in out.items()) == 0
        return out

    def inner(self, x, y):
        if len(x) > len(y):
            x,y = y,x
        return sum(self.weight(s)*v*y.get(s,0) for s,v in x.items())

    def spin_mask(self, occupation):
        parity = out = 0
        for i in range(self.m-1):
            parity ^= occupation >> i & 1
            out |= parity << i
        return out

    def support_receipt(self, vector, degree):
        center_b = self.spin_mask(self.b)
        in_a = in_b = overlap = 0
        for x in vector:
            z = self.spin_mask(x)
            da, db = z.bit_count(), (z ^ center_b).bit_count()
            assert min(da,db) <= degree
            in_a += da <= degree
            in_b += db <= degree
            overlap += da <= degree and db <= degree
        return {'degree':degree, 'nonzeros':len(vector), 'within_a':in_a,
                'within_b':in_b, 'overlap':overlap,
                'max_value_bits':max(abs(v).bit_length() for v in vector.values())}


def solve_fraction_matrix(matrix, rhs):
    n = len(rhs)
    mat = fmpq_mat([[fmpq(x) for x in row] for row in matrix])
    vec = fmpq_mat([[fmpq(x)] for x in rhs])
    sol = mat.solve(vec)
    assert mat*sol == vec
    return [F(int(sol[i,0].p), int(sol[i,0].q)) for i in range(n)]


def galerkin_at_degree(op, vectors, k, gram):
    S = [[gram[i][j+1] for j in range(k)] for i in range(k)]
    assert all(S[i][j] == S[j][i] for i in range(k) for j in range(k))
    t = [gram[i][0] for i in range(k)]
    alpha = solve_fraction_matrix(S, t)
    energy = sum((a*t0 for a,t0 in zip(alpha,t)), F(0))
    assert energy > 0
    beta = [F(1)] + [-a for a in alpha]
    residual_norm = sum((beta[i]*beta[j]*gram[i][j]
                        for i in range(k+1) for j in range(k+1)), F(0))
    assert residual_norm >= 0
    scale = op.W**2 * op.N
    lower = op.D*energy/scale
    error = residual_norm/(scale*op.gap)
    return lower, lower+error, alpha, residual_norm


def certify(theta, clocks, delta=F(0), eps=F(1,1000), max_degree=3,
            progress=False, return_internal=False):
    start = time.perf_counter()
    eps = exact_fraction(eps)
    if not 0 < eps < 1 or type(max_degree) is not int or max_degree < 1:
        raise ValueError('0 < eps < 1 and positive integer max_degree required')
    op = ActualOperator(theta, clocks, delta)
    vectors = [{op.a:op.N, op.b:-op.W}]
    assert sum(op.weight(x)*v for x,v in vectors[0].items()) == 0
    lower = (1+op.rho)/(2*op.Rstar)
    upper = (1+op.rho)/op.gap
    records = []
    for k in range(1,max_degree+1):
        vectors.append(op.apply_A(vectors[-1]))
        gram = [[op.inner(x,y) for y in vectors] for x in vectors]
        lo,hi,alpha,residual = galerkin_at_degree(op,vectors,k,gram)
        lower,upper = max(lower,lo),min(upper,hi)
        assert 0 < lower <= upper
        plo,phi = op.rho/(op.Ra*upper),op.rho/(op.Ra*lower)
        records.append({'degree':k,'I_lower':rational_box(lower),
            'I_upper':rational_box(upper), 'raw_Galerkin_lower':rational_box(lo),
            'raw_residual_upper':rational_box(hi),'p_lower':rational_box(plo),
            'p_upper':rational_box(phi),'relative_width':float(upper/lower-1),
            'support':op.support_receipt(vectors[-1],k),
            'moment_max_bits':max(abs(g).bit_length() for row in gram for g in row),
            'coefficient_max_num_bits':max(abs(a.numerator).bit_length() for a in alpha),
            'coefficient_max_den_bits':max(a.denominator.bit_length() for a in alpha),
            'residual_norm_scaled':rational_box(residual),
            'edge_evaluations':op.edge_evaluations,
            'seconds':time.perf_counter()-start})
        if progress:
            print('degree',k,'relative_width',records[-1]['relative_width'],
                  'support',len(vectors[-1]),'seconds',records[-1]['seconds'],
                  flush=True)
        if upper/lower <= 1+eps:
            break
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes = rss if platform.system() == 'Darwin' else 1024*rss
    result = {'status':'TARGET_MET' if upper/lower <= 1+eps else
              'CERTIFIED_BUT_TARGET_NOT_MET',
        'method':'ordinary exact Galerkin with full backward residual',
        'M':op.m,'delta':str(op.delta),'epsilon':str(eps),
        'degree_cap':max_degree,'degree':k,'p_lower':rational_box(plo),
        'p_upper':rational_box(phi),'I_lower':rational_box(lower),
        'I_upper':rational_box(upper),'relative_width':float(upper/lower-1),
        'degrees':records,'rho':rational_box(op.rho),'R_a':rational_box(op.Ra),
        'gap_lower':rational_box(op.gap),'rate_denominator_bits':op.D.bit_length(),
        'weight_scale_bits':op.W.bit_length(),
        'visited_weight_states':len(op.weight_cache),
        'transition_rows_materialized':len(op.transition_cache),
        'full_even_state_count':1 << (op.m-1),'peak_process_RSS_bytes':rss_bytes,
        'seconds':time.perf_counter()-start,'theta':list(map(str,op.theta)),
        'clocks':list(map(str,op.clocks)),
        'scope':'Supplied exact reversible model and analytic gap; no physical acquisition, novelty, uniform low degree, or new rarity complexity claim.'}
    return (result,(op,vectors,gram,alpha)) if return_internal else result


if __name__ == '__main__':
    out = certify(*fixture(24), delta=F(1,20), max_degree=3, progress=True)
    Path('DIRECT_INITIAL_M24.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['p_lower']['approx'],out['p_upper']['approx'],flush=True)
