"""Independent Q54 stage2 checks in original force coordinates."""
from collections import defaultdict, Counter
from pathlib import Path
import csv
import json
import math

import numpy as np
from scipy.optimize import linprog
from scipy.special import ndtr

HERE = Path(__file__).resolve().parent
DATA = HERE/'replay/Q54_stage2'


def read_rows(name):
    with (DATA/name).open() as inp:
        return list(csv.DictReader(inp))


def main():
    grouped = defaultdict(list)
    for row in read_rows('withheld_measurements.csv'):
        grouped[int(row['case'])].append(row)
    cases = read_rows('withheld_cases.csv')
    max_discrepancy = 0.
    calibration_covered = 0
    for row in cases:
        cid = int(row['case'])
        rec = grouped[cid]
        positions = [float(r['x']) for r in rec] + [1.]
        bounds = [(float(r['measurement'])-float(r['radius']),
                   float(r['measurement'])+float(r['radius'])) for r in rec] + [(None,None)]
        n = len(positions)
        # Direct force increments; no transformed monotone-cone formula is used.
        constraints, values = [], []
        for j in range(n-1):
            dx = positions[j+1]-positions[j]
            v = np.zeros(n)
            v[j+1],v[j] = 1,-1
            constraints.extend([v,-v])
            values.extend([5*dx,-dx])
        objective = np.zeros(n)
        objective[-1] = 1
        low = linprog(objective,A_ub=constraints,b_ub=values,bounds=bounds,method='highs')
        high = linprog(-objective,A_ub=constraints,b_ub=values,bounds=bounds,method='highs')
        assert low.success and high.success
        discrepancy = max(abs(low.x[-1]-float(row['target_lower'])),
                          abs(high.x[-1]-float(row['target_upper'])))
        assert discrepancy < 1e-8
        max_discrepancy = max(max_discrepancy,discrepancy)
        calibration_covered += int(all(abs(float(r['measurement'])-float(r['true_force']))
                                      <= float(r['radius'])+1e-15 for r in rec))
    tasks = read_rows('withheld_tasks.csv')
    incorrect = 0
    for row in tasks:
        cap, truth = float(row['force_ceiling']),float(row['true_target'])
        incorrect += int((row['verdict']=='SAFE' and truth>cap) or
                         (row['verdict']=='UNSAFE' and truth<=cap))

    functions = json.loads((DATA/'analytic_witness_functions.json').read_text())
    worst_interval_miss, largest_slopedelta = 0., 0.
    for entry in functions:
        cid = entry['case']
        knots = np.array(entry['knots'])
        vals = np.array(entry['unsmoothed_values'])
        slopes = np.diff(vals)/np.diff(knots)
        assert slopes.min() >= -1e-10 and slopes.max() <= 4+1e-10
        largest_slopedelta = max(largest_slopedelta,float(slopes.max()))
        jumps = np.diff(np.r_[0.,slopes,0.])
        width = entry['gaussian_width']
        def convolution(x):
            delta = x-knots
            z = delta/width
            return float(np.sum(jumps*(delta*ndtr(z)+width*np.exp(-z*z/2)/math.sqrt(2*math.pi))))
        zero = convolution(0)
        for r in grouped[cid]:
            x = float(r['x'])
            force = x+convolution(x)-zero
            miss = abs(force-float(r['measurement']))-float(r['radius'])
            worst_interval_miss = max(worst_interval_miss,miss)
        assert worst_interval_miss < 2e-9

    # Fresh independent scalar-force SPRT, not sampled LLR increments.
    rng = np.random.default_rng(54210626)
    m0 = .5
    delta,c,sigma = .025,.65,.001
    eps = 4*delta*(math.log1p(math.exp((.5-c)/delta))-math.log1p(math.exp(-c/delta)))
    threshold = math.log(19)
    sprt = []
    for h in (0,1):
        count = np.zeros(20000,dtype=int)
        llr = np.zeros(20000)
        active = np.ones(20000,dtype=bool)
        while active.any():
            ids = np.flatnonzero(active)
            y = m0+h*eps+sigma*rng.standard_normal(len(ids))
            llr[ids] += eps*(y-m0-eps/2)/sigma**2
            count[ids] += 1
            active[ids[np.abs(llr[ids])>=threshold]] = False
            assert count.max() < 5000
        error = float(np.mean((llr>0) != bool(h)))
        assert error < .06
        sprt.append({'hypothesis':h,'trials':20000,'error':error,
                     'mean_readings':float(count.mean()),'max_realized_count':int(count.max())})
    result = {'case_count':len(cases),'original_force_LP_max_discrepancy':max_discrepancy,
              'calibration_covered_cases':calibration_covered,'task_count':len(tasks),
              'verdict_counts':dict(Counter(r['verdict'] for r in tasks)),
              'incorrect_certificates':incorrect,'analytic_witnesses_checked':len(functions),
              'largest_preconvolution_g_slope':largest_slopedelta,
              'largest_interval_violation':worst_interval_miss,'fresh_scalar_SPRT':sprt,
              'SPRT_expected_count_lower_bound':2*sigma**2*.9*math.log(19)/eps**2}
    (HERE/'independent_stage2_q54_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
