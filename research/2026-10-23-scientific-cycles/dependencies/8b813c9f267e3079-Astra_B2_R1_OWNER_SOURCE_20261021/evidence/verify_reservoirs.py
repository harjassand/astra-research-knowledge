#!/usr/bin/env python3
"""Finite diagonal checks only; analytic proofs are in CONSTRUCTIONS.md."""
import json
import math

LN2 = math.log(2)

def entropy(ps):
    return -sum(p * math.log(p) for p in ps if p)

def eigprobs(N, low, high):
    out = []
    for x in range(2**N):
        r = N if not x else N - x.bit_length()
        out.append(sum(2.0 ** (k-N) for k in range(low, min(high, r)+1)) / (high-low+1))
    return out

def close(a, b, tol=2e-12):
    assert abs(a-b) < tol, (a, b)

rows = []
for J in range(1, 5):
    for L in range(J, 8):
        N = J+L-1
        p = eigprobs(N, J, N)
        close(sum(p), 1)
        resource = N*LN2-entropy(p)
        mean = J+(L-1)/2
        h = resource-mean*LN2+math.log(L)
        assert -1e-12 <= h <= 2*LN2+1e-12
        for j in range(1, J+1):
            q = eigprobs(N, J-j, N-j)
            close(sum(q), 1)
            tv = sum(abs(a-b) for a,b in zip(p,q))/2
            expected_tv = (j-(2**j-1)*2.0**(-L))/L
            close(tv, expected_tv)
            close(N*LN2-entropy(q), resource-j*LN2)
            # The claimed positive eigenspace: first N-j+1 signs are plus.
            for x, (a,b) in enumerate(zip(p,q)):
                r = N if not x else N-x.bit_length()
                assert (a-b >= -2e-12) if r >= N-j+1 else (a-b <= 2e-12)
        # Coherent-ladder exact overlap formula.
        theta = math.pi/(L+1)
        amps = [math.sqrt(2/(L+1))*math.sin((r+1)*theta) for r in range(L)]
        close(sum(a*a for a in amps), 1)
        for j in range(1, J+1):
            direct = sum(amps[r]*amps[r+j] for r in range(L-j))
            formula = ((L-j)*math.cos(j*theta)+math.sin((j+1)*theta)/math.sin(theta))/(L+1)
            close(direct, formula)
        rows.append({"J":J,"L":L,"N":N,"return_terminal":(J-(2**J-1)*2.0**(-L))/L,"E_R":resource,"h":h})

# Exact terminal-only ladder optimizer.
for delta in [1, .7, .5, .3, .2, .125, .1, .075, .01]:
    n = math.ceil(1/delta)
    p = [delta]*(n-1)+[1-(n-1)*delta]
    tv = (p[0]+sum(abs(p[k]-(p[k+1] if k+1<n else 0)) for k in range(n)))/2
    close(tv, delta)
    mean = sum((k+1)*a for k,a in enumerate(p))
    close(mean, n-delta*n*(n-1)/2)
    assert 1/(2*delta)+.5-1e-12 <= mean <= 1/(2*delta)+.5+delta/8+1e-12

print(json.dumps({"status":"PASS","finite_unflagged_cases":len(rows),"all_prefix_distances":True,"ER_formula_and_exact_drop":True,"coherent_overlap_formula":True,"terminal_ladder_optimizer_formula":True,"rows":rows},indent=2))
