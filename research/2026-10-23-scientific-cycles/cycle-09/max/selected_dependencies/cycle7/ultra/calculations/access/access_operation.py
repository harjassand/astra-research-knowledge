#!/usr/bin/env python3
"""Exact finite receiving operation: access thresholds, score, resource and spectrum.

Fraction arithmetic throughout; no EF/POVM optimization or scientific search.
Small brute enumeration is an independent check against ALL label assignments,
not just interval partitions already assumed by the dynamic programme.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,time


def score(D,L,a):
    return F(a)+sum((F(1,D**h) for h in range(1,L-a+1)),F(0))


def original(D,L):
    return sum((F(k)+sum((F(1,D**(2*h)) for h in range(1,L-k+1)),F(0))
                for k in range(1,L+1)),F(0))/L


def optimize(D,L,J):
    q=min(L,J); dp={(0,0):(F(0),[])}
    for j in range(1,q+1):
        for b in range(j,L+1):
            best=None
            for a in range(j,b+1):
                prev=dp.get((j-1,a-1))
                if prev is None: continue
                candidate=(prev[0]+(b-a+1)*score(D,L,a),prev[1]+[(a,b)])
                if best is None or candidate[0]>best[0]: best=candidate
            dp[j,b]=best
    value,bins=dp[q,L]
    mean_gap=sum((F((b-a+1)*(b-a),2*L) for a,b in bins),F(0))
    direct=sum((F(b-a+1,L)*score(D,L,a) for a,b in bins),F(0))
    assert direct==value/L
    return direct,bins,mean_gap


def brute(D,L,J):
    best=F(-1)
    for assignment in product(range(J),repeat=L):
        groups={z:[] for z in range(J)}
        for k,z in enumerate(assignment,1): groups[z].append(k)
        value=sum((F(len(ks),L)*score(D,L,min(ks))
                   for ks in groups.values() if ks),F(0))
        best=max(best,value)
    return best


def kyfan_spectrum(D,L,R):
    budget=R;mass=F(0)
    for j in range(L,0,-1):
        count=1 if j==L else D**(2*(L-j))-D**(2*(L-j-1))
        eigen=sum((F(1,L*D**(2*(L-k))) for k in range(1,j+1)),F(0))
        n=min(count,budget);mass+=n*eigen;budget-=n
    return mass


def main():
    wall,cpu=time.perf_counter(),time.process_time()
    rows=[]
    specs=[(2,2,1),(2,2,2),(2,3,2),(2,4,2),(2,4,3),
           (2,5,2),(2,5,3),(2,6,2),(2,6,3),(2,7,3),(3,5,2)]
    for D,L,J in specs:
        value,bins,gap=optimize(D,L,J)
        assert value==brute(D,L,J)
        q=min(L,J);h,t=divmod(L,q)
        minimum=F(q*h*(h-1)+2*t*h,2*L)
        assert gap>=minimum
        loss=original(D,L)-value
        assert gap-F(1,D-1)<=loss<=gap+F(1,D*D-1)
        if J==1: assert value==score(D,L,1)
        if J>=L: assert value>=original(D,L)
        rows.append(dict(D=D,L=L,J=J,optimum_score_units_lnD=str(value),
                         bins=bins,actual_score_loss_units_lnD=str(loss),
                         achieved_mean_gap=str(gap),minimum_possible_mean_gap=str(minimum),
                         all_label_assignment_count=J**L,independent_brute='PASS'))
    large=[]
    for J in [1,2,4,8,32]:
        value,bins,gap=optimize(2,32,J)
        large.append(dict(D=2,L=32,J=J,score_units_lnD=str(value),bins=bins,
                          score_loss_units_lnD=str(original(2,32)-value)))
    spectra=[]
    for D,L in [(2,1),(2,2),(2,5),(2,16),(3,4),(4,7)]:
        for R in sorted({1,D**L,max(1,D**L-1),D**L+1,D**(2*L)}):
            explicit=kyfan_spectrum(D,L,R)
            formula=sum((min(F(1),F(R,D**(2*(L-k)))) for k in range(1,L+1)),F(0))/L
            assert explicit==formula
            spectra.append(dict(D=D,L=L,R=R,kyfan_mass=str(explicit),
                                exact_spectrum_vs_support_formula='PASS'))
    replacements=[]
    for D,L in [(2,2),(2,7),(3,5),(4,16)]:
        for i in range(1,L+1):
            old=(F(L-i+1)+sum((F(1,D**(2*(i-k))) for k in range(1,i)),F(0)))/L
            new=(F(L-i+1)+sum((F(1,D**(i-k)) for k in range(1,i)),F(0)))/L
            assert new>=old
        replacements.append(dict(D=D,L=L,extra_expected_Bell_D_pairs=str(F(L-1,2)),
                                 every_prefix_dominates=True,source_selector='independent'))
    result=dict(status='PASS',exact_DP_vs_all_labels=rows,larger_exact_DP=large,
                spectrum_checks=spectra,ordinary_replacements=replacements,
                scope='Exact classical operation/certificate admissions. No generic formation solution, acquired output data or EF optimizer.')
    Path(__file__).with_name('RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    timing=dict(jobs=1,wall_seconds=time.perf_counter()-wall,process_cpu_seconds=time.process_time()-cpu,
                DP_brute_cases=len(rows),larger_DP_cases=len(large),
                spectrum_cases=len(spectra),replacement_cases=len(replacements))
    Path(__file__).with_name('TIMING.json').write_text(json.dumps(timing,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',**timing)))


if __name__=='__main__':main()
