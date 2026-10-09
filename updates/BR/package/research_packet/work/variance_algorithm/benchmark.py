#!/usr/bin/env python3
"""Reproducible heldout diagnostics; see benchmark_plan.txt."""
from fractions import Fraction as F
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
import random
import resource
import subprocess
import sys
import time
from variance_fptas import Coordinate, solve, exhaustive, objective, analytic_upper_bounds

ROOT = Path(__file__).resolve().parent
FAMILIES = ('heterogeneous', 'zero_lower', 'narrow', 'common', 'dynamic')


def generate(d, family, seed):
    r = random.Random(seed)
    pw = [r.randint(1,11) for _ in range(d)]
    qw = [r.randint(1,11) for _ in range(d)]
    if family == 'dynamic':
        pw = [F(2)**r.randint(-12,0) for _ in range(d)]
    P = [F(x)/sum(pw) for x in pw]
    q = [F(x)/sum(qw) for x in qw]
    rows = []
    for i in range(d):
        lo = r.randint(1,8)
        hi = r.randint(lo+1,16)
        B = F(r.randint(2,8),2)
        if family == 'narrow':
            lo = r.randint(8,14)
            hi = lo+1
        elif family == 'zero_lower' and i%2 == 0:
            lo = 0
        if family == 'common':
            rows.append(Coordinate(q[i],q[i],F(1),F(1,3),F(1)))
        else:
            rows.append(Coordinate(P[i],q[i],B,F(lo,16),F(hi,16)))
    return tuple(rows)


def run_case(index, d, family, seed, epsilon, exact):
    started = time.perf_counter()
    coords = generate(d, family, seed)
    construction = time.perf_counter()-started
    t = time.perf_counter()
    cheap = analytic_upper_bounds(coords)
    cheap_seconds = time.perf_counter()-t
    result = solve(coords, F(epsilon))
    L,U = F(result['lower_bound']),F(result['upper_bound'])
    exact_value = None
    interior_checks = 0
    exact_seconds = None
    if exact:
        t = time.perf_counter()
        exact_value = objective(exhaustive(coords))
        exact_seconds = time.perf_counter()-t
        assert L <= exact_value <= U, (index,L,exact_value,U)
        r = random.Random(seed+991)
        for _ in range(20):
            xs = [c.a+F(r.randint(0,32),32)*(c.b-c.a) for c in coords]
            S = sum(xs,F(0))
            if S:
                V = sum((c.c*x*x for c,x in zip(coords,xs)),F(0))
                assert V/S**2 <= exact_value
                interior_checks += 1
    assert L<=U<=(1+F(epsilon))*L
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak if sys.platform == 'darwin' else peak*1024
    out = dict(case_index=index, dimension=d, family=family, seed=seed,
               epsilon=epsilon, coordinates=[{key:str(getattr(c,key))
               for key in ('P','q','B','lower','upper')} for c in coords],
               result=result, exact_optimum=None if exact_value is None else str(exact_value),
               exact_seconds=exact_seconds, interior_checks=interior_checks,
               construction_seconds=construction, analytic_seconds=cheap_seconds,
               peak_process_rss_bytes=peak_bytes,
               all_assertions_pass=True,
               implementation_sha256=hashlib.sha256((ROOT/'variance_fptas.py').read_bytes()).hexdigest())
    return out


def add_secant(out):
    try:
        from secant_baseline import secant_upper
    except ImportError:
        return
    from variance_fptas import read_coordinates
    coords = read_coordinates(out['coordinates'])
    t = time.perf_counter()
    value = secant_upper([(c.a,c.b,c.c) for c in coords])
    elapsed = time.perf_counter()-t
    out['secant_upper'] = str(value)
    out['secant_seconds'] = elapsed
    if out['exact_optimum'] is not None:
        assert value >= F(out['exact_optimum'])
    assert value >= F(out['result']['lower_bound'])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--case', nargs=6)
    p.add_argument('--refresh-secants', action='store_true')
    args=p.parse_args()
    if args.case:
        index,d,family,seed,eps,ex=args.case
        out=run_case(int(index),int(d),family,int(seed),eps,ex=='1')
        add_secant(out)
        print(json.dumps(out))
        return
    result_dir=ROOT/'benchmark_cases'
    result_dir.mkdir(exist_ok=True)
    cases=[]
    for fi,family in enumerate(FAMILIES):
        for j,d in enumerate((4,6,8,10)):
            cases.append((d,family,730201+4*fi+j,'1/4',True))
    for fi,family in enumerate(FAMILIES):
        cases.append((64,family,730301+fi,'1/4',False))
    cases.append((128,'heterogeneous',730399,'1/2',False))
    rows=[]
    for index,(d,family,seed,eps,ex) in enumerate(cases):
        dest=result_dir/f'case_{index:02d}.json'
        if args.refresh_secants:
            out=json.loads(dest.read_text())
            add_secant(out)
        else:
            completed=subprocess.run([sys.executable,str(Path(__file__).resolve()),
                '--case',str(index),str(d),family,str(seed),eps,str(int(ex))],
                text=True,capture_output=True,check=True)
            out=json.loads(completed.stdout)
        dest.write_text(json.dumps(out,indent=2)+'\n')
        r=out['result']
        ab=r['analytic_upper_bounds']
        row={
            'case':index,'family':family,'d':d,'epsilon':eps,
            'L':float(F(r['lower_bound'])),'U_DP':float(F(r['upper_bound_dp'])),
            'U_combined':float(F(r['upper_bound'])),
            'exact':None if out['exact_optimum'] is None else float(F(out['exact_optimum'])),
            **{'analytic_'+k:None if v is None else float(F(v)) for k,v in ab.items()},
            'secant_upper':None if 'secant_upper' not in out else float(F(out['secant_upper'])),
            'secant_seconds':out.get('secant_seconds'),
            'solve_seconds':r['elapsed_seconds'],
            'analytic_seconds':out['analytic_seconds'],
            'exact_seconds':out['exact_seconds'],
            'peak_states':max(r['layer_counts']),
            'peak_expanded':r['peak_expanded_states'],
            'peak_rss_mib':out['peak_process_rss_bytes']/2**20,
            'pass':out['all_assertions_pass'],
        }
        rows.append(row)
        print(f"{index:02d} {family:14s} d={d:3d} DP={row['solve_seconds']:.4f}s states={row['peak_states']} L={row['L']:.6g} U_DP={row['U_DP']:.6g} analytic={row['analytic_best']:.6g}",flush=True)
    with (ROOT/'benchmark_summary.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    metadata={'python':sys.version,'platform':platform.platform(),
              'processor':platform.processor(),'case_count':len(cases),
              'all_assertions_pass':all(x['pass'] for x in rows)}
    (ROOT/'benchmark_environment.json').write_text(json.dumps(metadata,indent=2)+'\n')


if __name__=='__main__':
    main()
