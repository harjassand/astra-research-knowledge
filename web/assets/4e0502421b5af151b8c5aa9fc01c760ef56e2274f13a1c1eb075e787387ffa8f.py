#!/usr/bin/env python3
"""Exact integer checks for squared-hafnian cardinality coefficients."""
import random, json, itertools

def coefficients(B):
    n = len(B)
    h = [0] * (1 << n)
    h[0] = 1
    a = [0] * (n // 2 + 1)
    for mask in range(1 << n):
        size = mask.bit_count()
        if size & 1: continue
        if mask:
            ibit = mask & -mask
            i = ibit.bit_length() - 1
            rest = mask ^ ibit
            avail = rest
            while avail:
                jbit = avail & -avail
                j = jbit.bit_length() - 1
                h[mask] += B[i][j] * h[rest ^ jbit]
                avail ^= jbit
        a[size // 2] += h[mask] ** 2
    return a

def graph(n, weights):
    B = [[0] * n for _ in range(n)]
    for (i,j),w in zip(itertools.combinations(range(n),2),weights):
        B[i][j] = B[j][i] = w
    return B

def violation(a):
    for k in range(1,len(a)-1):
        if a[k] ** 2 < a[k-1] * a[k+1]:
            return k

def main():
    rng = random.Random(20261007)
    results = []
    for n,trials in [(6,32768),(8,20000),(10,20000),(12,2000)]:
        best = None
        for t in range(trials):
            if n == 6:
                w = [(t >> i) & 1 for i in range(n*(n-1)//2)]
            else:
                w = [rng.choice([0,0,0,1,1,2,3,10,100]) for _ in range(n*(n-1)//2)]
            B = graph(n,w)
            a = coefficients(B)
            k = violation(a)
            if k is not None:
                results.append({'n':n,'trial':t,'k':k,'a':a,'B':B})
                print(json.dumps(results[-1]), flush=True)
                break
        else:
            results.append({'n':n,'trials':trials,'no_logconcavity_violation':True})
            print(json.dumps(results[-1]), flush=True)
    with open(__file__.replace('.py','_results.json'),'w') as f:
        json.dump(results,f,indent=2)

if __name__ == '__main__': main()
