#!/usr/bin/env python3
"""Exact new receiving use; no predecessor science replay or tuning."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time
import squared_path_decoder as dec


def polynomial(A):
    n = len(A)
    result = [F(0)]*(n+1)
    for perm in itertools.permutations(range(n)):
        sign = (-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1, n))
        p = [F(sign)]
        for i, j in enumerate(perm):
            q = [-F(A[i][j]), F(i == j)]
            product = [F(0)]*(len(p)+1)
            for a, x in enumerate(p):
                for b, y in enumerate(q):
                    product[a+b] += x*y
            p = product
        result = [x+y for x, y in zip(result, p)]
    return result


def check(n):
    started = time.perf_counter()
    Z = dec.seed_integer(n)
    assert all(sum(a*a for a in row) == 2 for row in Z)
    expected = {1:[-2,1], 2:[3,-4,1], 3:[-4,9,-6,1],
                4:[4,-16,19,-8,1], 5:[16,-40,32,-10,1]}
    seen = set()
    for i in range(n):
        M = [Z[j] for j in dec.neighborhood(n, i)]
        key = tuple(M)
        if key not in seen:
            gram = dec.mul(M, dec.transpose(M)) if len(M)<=4 else dec.mul(dec.transpose(M), M)
            assert polynomial(gram) == list(map(F, expected[len(M)]))
            seen.add(key)
        if len(M) == 5:
            k = [dec.kernel(i, j) for j in dec.neighborhood(n, i)]
            assert sum(x*x for x in k) == 1
            assert all(sum(k[j]*M[j][c] for j in range(5)) == 0 for c in range(4))
    m = max(0, n-4)
    t = [F((11*i)%17-8, 7) for i in range(m)]
    q2 = sum(sum(a*t[j] for j, a in row.items())**2
             for _, _, row in dec.scalar_rows(n))
    gauge = [1]*m
    for j in range(1, m):
        i = j+1
        g = 4*dec.kernel(i, i+1)*dec.kernel(i+1, i)
        assert g in (-1,1)
        gauge[j] = gauge[j-1]*g
    z = [a*b for a, b in zip(t, gauge)]
    def at(i):
        return z[i] if 0 <= i < m else F(0)
    sos = F(1,4)*sum((at(i-1)+at(i+1)-at(i)/2)**2 for i in range(-1,m+1))
    sos += F(7,16)*sum(a*a for a in t)
    assert sos == q2
    triangles = 0
    for i in range(2, n-4):
        gain = F(1)
        for u,v in ((i,i+1),(i+1,i+2),(i+2,i)):
            gain *= 4*dec.kernel(u,v)*dec.kernel(v,u)
        assert gain == -1
        triangles += 1
    D = {(i,i):F(i%7-3,7) for i in range(n)}
    D.update({(i,j):F((3*i+2*j)%13-6,11) for i,j in dec.edges(n)})
    W = dec.action_scaled(n,D)
    recovered, meta = dec.decode_scaled(W)
    assert recovered == D
    E0 = [[F((17*i+3*c)%19-9,13) for c in range(4)] for i in range(n)]
    noisy = [[a+b for a,b in zip(w,e)] for w,e in zip(W,E0)]
    estimate, _ = dec.decode_scaled(noisy)
    error2 = dec.norm_squared({ij:estimate[ij]-a for ij,a in D.items()})
    noise2 = sum(a*a for row in E0 for a in row)/2
    assert error2 <= 26*noise2
    return {'n':n,'queries':4,'row_energy_squared':'1',
            'local_Gram_polynomials_exact':True,'kernel_equations_exact':True,
            'unbalanced_triangles_checked':triangles,'scalar_SOS_exact':True,
            'exact_recovery':True,'noise_squared':str(noise2),
            'output_frobenius_error_squared':str(error2),
            'squared_error_ratio':float(error2/noise2),
            'proved_squared_bound_upper':'26',**meta,
            'case_wall_seconds':time.perf_counter()-started}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    args = p.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    wall,cpu = time.perf_counter(),time.process_time()
    cases = [check(n) for n in (1,2,3,4,5,6,7,17,64,257)]
    receipt = {'schema':'astra.cycle4.squared_path_four_query.v1','status':'passed',
               'cases':cases,'body_wall_seconds':time.perf_counter()-wall,
               'body_cpu_seconds':time.process_time()-cpu,
               'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
               'decoder_sha256':hashlib.sha256(Path(dec.__file__).read_bytes()).hexdigest(),
               'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'scope':'One exact new decoder test body; imports excluded. Universal bound is analytic, code tests finite instances. No predecessor replay.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__ == '__main__':
    main()
