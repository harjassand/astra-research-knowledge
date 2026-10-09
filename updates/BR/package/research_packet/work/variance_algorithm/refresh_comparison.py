#!/usr/bin/env python3
"""Recompute final secant witnesses and exact comparison counts on frozen cases."""
import csv
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
from variance_fptas import read_coordinates
from secant_baseline import secant_bounds

ROOT=Path(__file__).resolve().parent
EXPECTED_SECANT='eb31e955138eb007019e34233cd3e3a8b5322528fc5815b3bce786c6a28a3484'
assert sha256((ROOT/'secant_baseline.py').read_bytes()).hexdigest()==EXPECTED_SECANT
rows=[]
for p in sorted((ROOT/'benchmark_cases').glob('case_*.json')):
    case=json.loads(p.read_text())
    cs=read_coordinates(case['coordinates'])
    sb=secant_bounds([(c.a,c.b,c.c) for c in cs])
    dp=case['result']
    witness=sb['witness']
    assert all(x in (c.a,c.b) for c,x in zip(cs,witness))
    S=sum(witness,F(0))
    assert S>0
    value=sum((c.c*x*x for c,x in zip(cs,witness)),F(0))/S**2
    assert value==sb['lower']<=sb['upper']
    assert sb['upper']==F(case['secant_upper'])
    if case['exact_optimum'] is not None:
        assert sb['lower']<=F(case['exact_optimum'])<=sb['upper']
    rows.append(dict(case=case['case_index'],family=case['family'],dimension=case['dimension'],
        secant_lower=str(sb['lower']),secant_upper=str(sb['upper']),
        secant_exact=sb['lower']==sb['upper'],
        secant_witness=[str(x) for x in witness],
        secant_lower_ge_dp=sb['lower']>=F(dp['lower_bound']),
        secant_lower_gt_dp=sb['lower']>F(dp['lower_bound']),
        secant_upper_lt_dp=sb['upper']<F(dp['upper_bound_dp']),
        secant_upper_lt_combined_dp=sb['upper']<F(dp['upper_bound']),
        secant_upper_eq_combined_dp=sb['upper']==F(dp['upper_bound']),
        witness_arithmetic_pass=True,secant_source_sha256=EXPECTED_SECANT))
(ROOT/'secant_witness_comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
summary=list(csv.DictReader((ROOT/'benchmark_summary.csv').open()))
large=[r for r in summary if int(r['d'])>=64]
ratios=[float(r['solve_seconds'])/float(r['secant_seconds']) for r in large]
metrics=dict(cases=len(rows),secant_source_sha256=EXPECTED_SECANT,
    secant_upper_beats_raw_dp=sum(r['secant_upper_lt_dp'] for r in rows),
    secant_upper_beats_clipped_dp=sum(r['secant_upper_lt_combined_dp'] for r in rows),
    secant_upper_ties_clipped_dp=sum(r['secant_upper_eq_combined_dp'] for r in rows),
    secant_exact_count=sum(r['secant_exact'] for r in rows),
    secant_witness_at_least_dp=sum(r['secant_lower_ge_dp'] for r in rows),
    secant_witness_better_dp=sum(r['secant_lower_gt_dp'] for r in rows),
    secant_speedup_larger_min=min(ratios),secant_speedup_larger_max=max(ratios),
    large_secant_seconds_min=min(float(r['secant_seconds']) for r in large),
    large_secant_seconds_max=max(float(r['secant_seconds']) for r in large),
    all_witness_arithmetic_pass=True)
(ROOT/'FINAL_METRICS.json').write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps(metrics,indent=2))
