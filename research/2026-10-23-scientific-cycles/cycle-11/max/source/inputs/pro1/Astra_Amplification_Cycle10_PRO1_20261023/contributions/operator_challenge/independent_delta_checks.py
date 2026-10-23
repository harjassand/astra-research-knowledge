"""Bounded final-delta verification; no channel simulation or old-suite replay."""
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib, json, time

ROOT = Path(__file__).resolve().parents[2]

def direct_v(k):
    """Evaluate the defining finite random-walk return sum, without closed form."""
    D = Decimal
    probability = D(1)
    collision = D(k-1)
    for j in range(1, (k-2)//2+1):
        probability *= D(2*j-1)/D(2*j)
        collision += D(k-1-2*j)*probability
    return (D(k*(k-1))-collision)/8

def run():
    started = time.perf_counter()
    source = ROOT/'representation/capacity_comparison.json'
    data = source.read_bytes()
    record = json.loads(data)
    checks = []
    with localcontext() as ctx:
        ctx.prec = 120
        D = Decimal
        ell = D(2).ln()
        for row in record['observations']:
            denominator = row['beta_denominator']
            b = D(1)/D(denominator)**2
            floors = {}
            for cycle, divisor in ((8, 32), (9, 64), (10, 64)):
                key = f'cycle{cycle}_k'
                if key not in row:
                    continue
                k = row[key]
                expected = ell*direct_v(k)*b*b/(divisor*k)
                supplied = D(row[f'cycle{cycle}_exact_floor'])
                relative = abs(expected-supplied)/expected
                assert relative < D('1e-90'), (denominator, cycle, relative)
                floors[f'cycle{cycle}'] = expected
            floors['pair'] = D(row['pair_actual_entropy_excess'])
            floors['four_call'] = D(row['nonscalar_four_call_actual_entropy_excess'])
            assert max(floors, key=floors.get) == row['best_retained_certificate']
            check = {'beta_denominator':denominator, 'direct_random_walk_sum_floors_match':True,
                     'strongest_retained_certificate':row['best_retained_certificate']}
            if denominator == 512:
                k = row['cycle10_k']; v = direct_v(k)
                kappa = (1-b)*ell*v*b*b/128
                t = kappa/(2*k*k)
                gap = kappa*kappa/(4*k*k)
                for name, value in [('kappa',kappa),('lyapunov_t',t),('one_minus_lambda',gap)]:
                    assert abs(value-D(row[name]))/value < D('1e-90')
                check['new_resource_values_match'] = True
            checks.append(check)
    return {'source_json_sha256':hashlib.sha256(data).hexdigest(),
            'status':'PASS', 'checks':checks,
            'wall_seconds':time.perf_counter()-started,
            'scope':'New manuscript comparison/resource delta only. Replays verify evaluated formulas, not the analytic theorem, discovery cost or physical performance.'}

if __name__=='__main__':
    result = run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
