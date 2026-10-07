#!/usr/bin/env python3
"""Finite-bit local compiler for an explicitly admitted N=2 critical-spin family.

No float participates in interval endpoints, acceptance, rounding, or certificates.
Rationals and outward dyadic intervals suffice. Runtime measurements are floats.
The emitted object is a local preparation description; no hardware is controlled.
"""
from __future__ import annotations

import argparse
import datetime
from fractions import Fraction as F
import json
from math import isqrt
from pathlib import Path
import resource
import secrets
import time


class Ledger:
    def __init__(self):
        self.counts = {}
        self.max_integer_bits = 0

    def add(self, key, n=1):
        self.counts[key] = self.counts.get(key, 0) + n

    def see(self, *values):
        for x in values:
            if isinstance(x, F):
                self.max_integer_bits = max(self.max_integer_bits,
                    abs(x.numerator).bit_length(), x.denominator.bit_length())
            elif isinstance(x, int):
                self.max_integer_bits = max(self.max_integer_bits, abs(x).bit_length())

    def op(self, symbol, x, y):
        self.add('fraction_' + symbol)
        z = {'add': lambda: x+y, 'sub': lambda: x-y,
             'mul': lambda: x*y, 'div': lambda: x/y}[symbol]()
        self.see(x, y, z)
        return z

    def snapshot(self):
        return {'explicit_operation_counts': dict(self.counts),
                'max_observed_integer_bits': self.max_integer_bits,
                'scope': 'Explicit arithmetic calls, not Python/Fraction internal GCD or CPU bit-operation counts.'}


ledger = Ledger()


def fa(x, y): return ledger.op('add', x, y)
def fs(x, y): return ledger.op('sub', x, y)
def fm(x, y): return ledger.op('mul', x, y)
def fd(x, y): return ledger.op('div', x, y)


class IV:
    P = 0
    Q = 1

    @classmethod
    def precision(cls, p):
        cls.P, cls.Q = p, 1 << p

    def __init__(self, lo, hi=None, raw=False):
        lo, hi = F(lo), F(lo if hi is None else hi)
        assert lo <= hi
        ledger.see(lo, hi)
        if raw:
            self.lo, self.hi = lo, hi
        else:
            ledger.add('outward_dyadic_endpoint_roundings', 2)
            a, b = fm(lo, F(self.Q)), fm(hi, F(self.Q))
            self.lo = F(a.numerator // a.denominator, self.Q)
            self.hi = F(-((-b.numerator) // b.denominator), self.Q)
            ledger.see(self.lo, self.hi)

    def __add__(self, other):
        other = iv(other)
        return IV(fa(self.lo, other.lo), fa(self.hi, other.hi))

    __radd__ = __add__

    def __neg__(self):
        ledger.add('interval_negations')
        return IV(-self.hi, -self.lo, raw=True)

    def __sub__(self, other): return self + (-iv(other))
    def __rsub__(self, other): return iv(other) + (-self)

    def __mul__(self, other):
        other = iv(other)
        products = [fm(a, b) for a in (self.lo, self.hi)
                    for b in (other.lo, other.hi)]
        ledger.add('interval_endpoint_extrema', 2)
        return IV(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ArithmeticError('Certified division denominator includes zero')
        return IV(fd(F(1), self.hi), fd(F(1), self.lo))

    def __truediv__(self, other): return self * iv(other).reciprocal()
    def __rtruediv__(self, other): return iv(other) * self.reciprocal()

    def json(self):
        return {'lo': str(self.lo), 'hi': str(self.hi),
                'width': str(fs(self.hi, self.lo))}


def iv(x): return x if isinstance(x, IV) else IV(x)


def sqrt_iv(x):
    x = iv(x)
    assert x.lo >= 0
    def endpoint(y, upper):
        z = fm(y, F(IV.Q * IV.Q))
        n = z.numerator // z.denominator
        ledger.add('integer_square_roots')
        k = isqrt(n)
        if upper and F(k*k) != z:
            k += 1
        ledger.see(n, k)
        return F(k, IV.Q)
    return IV(endpoint(x.lo, False), endpoint(x.hi, True), raw=True)


def exp_scalar(x):
    """For |x|<=2, enclose exp(x) by range reduction and exact Taylor sums.

    On 0<=z<=1, Lagrange's remainder is <=3/(n+1)! since e<=3.
    For negative x use reciprocal; square after each halving.
    """
    ledger.add('exp_scalar_calls')
    if x < 0:
        return exp_scalar(-x).reciprocal()
    assert x <= 2
    halves = 0
    while x > 1:
        x = fd(x, F(2))
        halves += 1
    tol = F(1, 1 << (IV.P + 8))
    total, term, factorial = F(1), F(1), 1
    n = 0
    while True:
        rem = F(3, factorial * (n+1))
        ledger.see(rem, factorial)
        if rem <= tol:
            break
        n += 1
        term = fd(fm(term, x), F(n))
        total = fa(total, term)
        factorial *= n
        ledger.add('exp_taylor_terms')
        ledger.see(factorial)
    out = IV(total, fa(total, rem))
    for _ in range(halves):
        out = out * out
    return out


def exp_iv(x):
    x = iv(x)
    return IV(exp_scalar(x.lo).lo, exp_scalar(x.hi).hi, raw=True)


def even_series_scalar(x, kind):
    """Enclose cosh(x), or sinh(x)/x with its removable value at x=0.

    For |x|<=1 the omitted positive tail after k terms is bounded by
    3/(2k+2)! for cosh and 3/(2k+3)! for sinch. This follows from
    Lagrange's exponential remainder and, for sinch, integration of cosh.
    """
    assert 0 <= x <= 1
    ledger.add(kind + '_scalar_calls')
    offset = 0 if kind == 'cosh' else 1
    tol = F(1, 1 << (IV.P + 8))
    total, term, k, factorial = F(1), F(1), 0, 1
    x2 = fm(x, x)
    while True:
        d1, d2 = 2*k+1+offset, 2*k+2+offset
        next_factorial = factorial*d1*d2
        rem = F(3, next_factorial)
        ledger.see(next_factorial, rem)
        if rem <= tol:
            break
        term = fd(fm(term, x2), F(d1*d2))
        total = fa(total, term)
        factorial = next_factorial
        k += 1
        ledger.add(kind + '_taylor_terms')
    return IV(total, fa(total, rem))


def even_series_iv(x, kind):
    x = iv(x)
    assert x.lo >= 0
    return IV(even_series_scalar(x.lo, kind).lo,
              even_series_scalar(x.hi, kind).hi, raw=True)


def moments(a_input, b_input):
    """N=2, A=diag(a,-a,0), b=(0,0,b). Drop the scalar 3I/2 in K."""
    root2 = sqrt_iv(iv(2))
    s = root2 * sqrt_iv(root2)   # 2^(3/4)
    a = iv(a_input) / (2*root2) # even-block X coefficient
    h = iv(b_input) / s        # even-block Z coefficient
    # A signed interval times itself need not have a nonnegative lower bound.
    def square(x):
        hi = max(fm(x.lo, x.lo), fm(x.hi, x.hi))
        lo = F(0) if x.lo <= 0 <= x.hi else min(fm(x.lo,x.lo),fm(x.hi,x.hi))
        return IV(lo,hi)
    d = sqrt_iv(square(a) + square(h))
    E, O = exp_iv(F(1,2)), exp_iv(F(-1,2))
    cd, sd = even_series_iv(d,'cosh'), even_series_iv(d,'sinch')
    c1, s1 = even_series_iv(iv(1),'cosh'), even_series_iv(iv(1),'sinch')
    denom = 2*(E*cd + O*c1)
    mz = 2*E*h*sd/denom
    cx = 2*(E*a*sd+O*s1)/denom
    cy = 2*(O*s1-E*a*sd)/denom
    cz = 2*(E*cd-O*c1)/denom
    weights = [cx/2,cx/2,cy/2,cy/2,(cz+mz)/2,(cz-mz)/2,
               4*O*(c1-s1)/denom]
    H = [[iv(0) for _ in range(4)] for _ in range(4)]
    H[0][0],H[3][3] = iv(F(1,2))+h,iv(F(1,2))-h
    H[0][3]=H[3][0]=a
    H[1][1]=H[2][2]=iv(F(-1,2))
    H[1][2]=H[2][1]=iv(1)
    return weights, H, {'a':a,'h':h,'d':d,'partition_without_scalar':denom,
                        'mean_z':mz,'corr_x':cx,'corr_y':cy,'corr_z':cz}


def quantize(weights, k):
    W, D = k+8, 1 << (k+8)
    ns = []
    for w in weights[:6]:
        mid = fd(fa(w.lo,w.hi),F(2))
        x = fm(mid,F(D))
        ns.append(x.numerator // x.denominator)
    ns.append(D-sum(ns))
    qs = [F(n,D) for n in ns]
    assert all(n>=0 for n in ns) and sum(ns)==D
    errors = [max(abs(fs(q,w.lo)),abs(fs(q,w.hi))) for q,w in zip(qs,weights)]
    tv_upper = fd(sum(errors,F(0)),F(2))
    assert tv_upper <= F(1,1<<k)
    return ns,qs,W,tv_upper,errors


def mixture_matrix(q):
    """Exact rational matrix of seven axis/mixed iid-product branches."""
    cx,cy,cz,mz = q[0]+q[1],q[2]+q[3],q[4]+q[5],q[4]-q[5]
    return [[(1+2*mz+cz)/4, F(0), F(0), (cx-cy)/4],
            [F(0),(1-cz)/4,(cx+cy)/4,F(0)],
            [F(0),(cx+cy)/4,(1-cz)/4,F(0)],
            [(cx-cy)/4,F(0),F(0),(1-2*mz+cz)/4]]


def mm(A,B):
    return [[sum((A[i][t]*B[t][j] for t in range(4)),iv(0))
             for j in range(4)] for i in range(4)]


def independent_exp_audit(H, target, k):
    """Direct 4x4 Taylor enclosure, independent of the two-block formulas.

    The admitted family has ||H||_infinity<=2. Remainder <=
    9*2^(n+1)/(n+1)! since e^2<=9. Outward intervals carry all arithmetic.
    T(rho,target)<=||rho-target||_F<=sum entrywise absolute bounds.
    """
    rowbound = max(sum(max(abs(x.lo),abs(x.hi)) for x in row) for row in H)
    assert rowbound <= 2
    identity = [[iv(int(i==j)) for j in range(4)] for i in range(4)]
    S,term,n = identity,identity,0
    factorial, power = 1,2
    tol=F(1,1<<(k+16))
    while True:
        rem=F(9*power,factorial*(n+1))
        ledger.see(rem,factorial,power)
        if rem<=tol:
            break
        n+=1
        term=mm(term,H)
        term=[[x/n for x in row] for row in term]
        S=[[S[i][j]+term[i][j] for j in range(4)] for i in range(4)]
        factorial*=n
        power*=2
        ledger.add('direct_matrix_taylor_terms')
    S=[[x+IV(-rem,rem) for x in row] for row in S]
    Z=sum((S[i][i] for i in range(4)),iv(0))
    assert Z.lo>0
    rho=[[x/Z for x in row] for row in S]
    eb=[[max(abs(fs(target[i][j],rho[i][j].lo)),
             abs(fs(target[i][j],rho[i][j].hi))) for j in range(4)] for i in range(4)]
    bound=sum((sum(row,F(0)) for row in eb),F(0))
    assert bound<=F(1,1<<k)
    return {'matrix_taylor_degree':n,'matrix_remainder_infinity_bound':str(rem),
            'matrix_input_infinity_norm_upper':str(rowbound),
            'direct_trace_distance_upper':str(bound),
            'normalized_gibbs_entry_intervals':[[x.json() for x in row] for row in rho]}


BRANCHES=['+X','-X','+Y','-Y','+Z','-Z','mixed']
GATES={'+X':['H'],'-X':['X','H'],'+Y':['H','S'],'-Y':['H','Sdg'],
       '+Z':[],'-Z':['X']}
BLOCH={'+X':[1,0,0],'-X':[-1,0,0],'+Y':[0,1,0],'-Y':[0,-1,0],
       '+Z':[0,0,1],'-Z':[0,0,-1],'mixed':[0,0,0]}


def emit(ns,W,uniform_integer=None,mixed_bits=None):
    D=1<<W
    if uniform_integer is None:
        u=secrets.randbits(W)
        entropy='OS secrets.randbits; correctness theorem assumes ideal fair bits'
    else:
        u=uniform_integer
        entropy='supplied deterministic transcript; not evidence of random-source fairness'
    assert 0<=u<D
    cumul=0
    for j,n in enumerate(ns):
        cumul+=n
        if u<cumul:
            break
    branch=BRANCHES[j]
    if branch=='mixed':
        bits=[secrets.randbits(1),secrets.randbits(1)] if mixed_bits is None else mixed_bits
        assert len(bits)==2 and all(x in [0,1] for x in bits)
        gates=[['X'] if bit else [] for bit in bits]
    else:
        bits=[]
        gates=[GATES[branch],GATES[branch]]
    return {'uniform_integer':u,'selection_random_bits':W,'branch_index':j,
            'branch_label':branch,'local_bloch_vector':BLOCH[branch],
            'identical_local_density_copies':2,
            'mixed_emission_independent_bits':bits,
            'emission_random_bits':len(bits),
            'single_qubit_gate_lists_from_zero':gates,
            'single_qubit_gate_count':sum(map(len,gates)),
            'random_source':entropy,'hardware_executed':False}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--a',default='1/4')
    ap.add_argument('--b',default='1/8')
    ap.add_argument('--error-bits',type=int,default=32)
    ap.add_argument('--uniform-integer',type=int)
    ap.add_argument('--mixed-bits',default='0,1')
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    a,b,k=F(args.a),F(args.b),args.error_bits
    assert abs(a)<=1 and abs(b)<=F(1,2) and 8<=k<=128
    t0,c0=time.perf_counter(),time.process_time()
    IV.precision(k+32)
    weights,H,intermediates=moments(a,b)
    assert all(w.lo>0 for w in weights)
    ns,qs,W,tv,errors=quantize(weights,k)
    compiled_matrix=mixture_matrix(qs)
    compile_cost=ledger.snapshot()
    compile_wall,compile_cpu=time.perf_counter()-t0,time.process_time()-c0
    t1,c1=time.perf_counter(),time.process_time()
    audit=independent_exp_audit(H,compiled_matrix,k)
    audit_wall,audit_cpu=time.perf_counter()-t1,time.process_time()-c1
    t2,c2=time.perf_counter(),time.process_time()
    emission=emit(ns,W,args.uniform_integer,[int(x) for x in args.mixed_bits.split(',')])
    emission_wall,emission_cpu=time.perf_counter()-t2,time.process_time()-c2
    expected_gates=sum(q*2*len(GATES[label]) for q,label in zip(qs[:6],BRANCHES[:6]))+qs[6]
    result={'worker_id':'c07_s03','status':'CERTIFIED_ADMITTED_N2_CLASSICAL_DESCRIPTION',
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'input':{'N':2,'A_diagonal':[str(a),str(-a),'0'],'b_vector':['0','0',str(b)],
                 'public_domain':'|a|<=1, |b|<=1/2; known rational parameters',
                 'requested_trace_error':str(F(1,1<<k))},
        'precision':{'working_fraction_bits':IV.P,'weight_denominator_bits':W,
                     'taylor_internal_absolute_tolerance':str(F(1,1<<(IV.P+8))),
                     'guard_bits':32,'rounding':'outward exact dyadic rational'},
        'exact_weight_intervals':[w.json() for w in weights],
        'dyadic_integer_weights':ns,'dyadic_weight_denominator':1<<W,
        'dyadic_rational_weights':[str(q) for q in qs],
        'per_weight_absolute_error_upper':[str(e) for e in errors],
        'mixture_trace_distance_upper':str(tv),
        'intermediate_enclosures':{key:value.json() for key,value in intermediates.items()},
        'compiled_density_matrix':[[str(x) for x in row] for row in compiled_matrix],
        'independent_direct_matrix_certificate':audit,
        'sample_local_preparation':emission,
        'costs':{'compile':{**compile_cost,'wall_seconds':compile_wall,'cpu_seconds':compile_cpu},
                 'audit_including_cumulative_arithmetic':{**ledger.snapshot(),
                    'wall_seconds':audit_wall,'cpu_seconds':audit_cpu},
                 'sample_emission_description':{'wall_seconds':emission_wall,'cpu_seconds':emission_cpu},
                 'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'worst_case_fair_random_bits_per_output':W+2,
                 'expected_fair_random_bits_per_output':str(F(W)+2*qs[6]),
                 'worst_case_single_qubit_clifford_gates':4,
                 'expected_single_qubit_clifford_gates':str(expected_gates),
                 'physical_initializations':2,'physical_output_qubits':2,
                 'retained_mixture_weights':7,'physical_energy':'UNKNOWN: no hardware run',
                 'backend_token_and_gpu_cost':'UNKNOWN',
                 'guard_strategy':'Every numerical operation is enclosed, then final rational error inequalities are checked. Fixed guard failure raises, never silently certifies.'},
        'limits':['N=2 only; no growing-N finite-Trotter sampler implementation',
                  'rational parameter acquisition is supplied, not inferred',
                  'ideal Clifford-gate action is the physical interface; no noise or reset energy certified',
                  'fair bits are an explicit source assumption; a recorded sample does not validate that source',
                  'no claim of historical novelty, external validation, or field-breaking science']}
    out=Path(args.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(out),'status':result['status'],
                      'mixture_error_upper':str(tv),'direct_matrix_error_upper':audit['direct_trace_distance_upper'],
                      'requested_error':str(F(1,1<<k)),'working_bits':IV.P,
                      'compile_wall_seconds':compile_wall,'audit_wall_seconds':audit_wall,
                      'max_integer_bits':ledger.max_integer_bits,'selected_branch':emission['branch_label']}))


if __name__=='__main__':
    main()
