#!/usr/bin/env python3
"""Exact degree-three hidden-clock countermodel for degree-two acquisition."""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations


def solve_exact(A, b):
    n=len(b)
    aug=[list(map(F,row))+[F(rhs)] for row,rhs in zip(A,b)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if aug[i][j]),None)
        if pivot is None: raise ArithmeticError('singular killed generator')
        aug[j],aug[pivot]=aug[pivot],aug[j]
        p=aug[j][j]
        aug[j]=[v/p for v in aug[j]]
        for i in range(n):
            if i==j or not aug[i][j]: continue
            q=aug[i][j]
            aug[i]=[x-q*y for x,y in zip(aug[i],aug[j])]
    return [aug[i][-1] for i in range(n)]


def mean(eps):
    N=16; K=[[F(0) for _ in range(N)] for _ in range(N)]
    for x in range(N):
        for i in range(4):
            if i==0:
                context=[j for j in range(4) if j!=i]
                rate=eps/F(2) if all((x>>j)&1 for j in context) else F(1,2)
            else: rate=F(1,2)
            y=x^(1<<i)
            K[x][x]+=rate
            K[x][y]-=rate
        K[x][x]+=F((x>>0)&1)
    u=solve_exact(K,[F(1)]*N)
    residual=[sum(K[x][y]*u[y] for y in range(N)) for x in range(N)]
    if any(value != 1 for value in residual): raise AssertionError('exact killed-system residual failed')
    if min(u) <= 0: raise AssertionError('mean-response witness not positive')
    return sum(u,F(0))/N,u


def main():
    eps=F(1,100)
    base,base_u=mean(F(1));slow,slow_u=mean(eps)
    records=[]
    for i in range(4):
        contexts=[sum(1<<j for j in S) for S in [()] + [(j,) for j in range(4) if j!=i] + list(combinations([j for j in range(4) if j!=i],2))]
        old=[F(1,2)]*len(contexts)
        new=[(eps/F(2) if i==0 and all((x>>j)&1 for j in [1,2,3]) else F(1,2)) for x in contexts]
        records.append({'coordinate':i,'queries':len(contexts),'exact_clock_query_vectors_equal':old==new})
    out={'n':4,'energy_weights':'W(x)=1 for all states in both laws','target':'k(x)=x_0, kappa=1','attempt_law_base':'a_i(y)=1 for every i,y','attempt_law_hidden':'a_0(y)=1-(99/100)y_1 y_2 y_3; a_i(y)=1 for i>0','hidden_clock_positive':eps>0,'max_degree_of_hidden_law':3,'degree_at_most_two_query_count':4*7,'energy_queries':1+4+6,'query_vectors_identical_for_every_coordinate':all(r['exact_clock_query_vectors_equal'] for r in records),'per_coordinate_query_checks':records,'base_uniform_source_mean_exact':str(base),'hidden_uniform_source_mean_exact':str(slow),'lifetime_difference_exact':str(slow-base),'lifetime_ratio_exact':str(slow/base),'lifetime_ratio_float':float(slow/base),'base_positive_response_exact':all(v>0 for v in base_u),'hidden_positive_response_exact':all(v>0 for v in slow_u),'both_exact_Ku_eq_one':True,'base_response_witness':list(map(str,base_u)),'hidden_response_witness':list(map(str,slow_u)),'exact_generator_solve':'16x16 Fraction Gaussian elimination with exact Ku=1 and positivity checks','scope':'finite exact countermodel: degree-three mobility is invisible to degree-two reverse-clock support acquisition; no molecular or general capability claim'}
    outpath=Path(__file__).with_name('degree3_countermodel_results.json')
    outpath.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['query_vectors_identical_for_every_coordinate','base_uniform_source_mean_exact','hidden_uniform_source_mean_exact','lifetime_difference_exact','lifetime_ratio_exact','lifetime_ratio_float']},indent=2))

if __name__=='__main__': main()
