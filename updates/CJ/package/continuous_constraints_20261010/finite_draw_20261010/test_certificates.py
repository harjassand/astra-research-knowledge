#!/usr/bin/env python3
"""Small deterministic tests, including invalid-certificate rejection."""
import copy, json, random, time
from fractions import Fraction as Q
from pathlib import Path
from certified_draw import gaussian_seed, normal_cdf_interval, IV_SCALE
from verify_draw import verify_report
HERE=Path(__file__).resolve().parent


def main():
    t=time.perf_counter(); checks=[]
    report=json.loads((HERE/'CERTIFIED_DRAW.json').read_text())
    verify_report(report); checks.append('complete saved draw replay')
    for label,change in [
        ('reject overstated native r', lambda x:x['native_certificate'].__setitem__('r',100)),
        ('reject altered output coordinate', lambda x:x['draw']['output']['x_integer'].__setitem__(0,str(int(x['draw']['output']['x_integer'][0])+1))),
        ('reject altered acceptance bound', lambda x:x['draw']['acceptance']['squared_acceptance_lower'].__setitem__('num','1')),
    ]:
        bad=copy.deepcopy(report); change(bad)
        try: verify_report(bad)
        except AssertionError: checks.append(label)
        else: raise AssertionError(label+' was not rejected')
    for q in [Q(0),Q(1,1000),Q(1,2),Q(1),Q(3),Q(6),Q(8),Q(12)]:
        lo,hi=normal_cdf_interval(q); nl,nh=normal_cdf_interval(-q)
        assert lo<=hi and nl==IV_SCALE-hi and nh==IV_SCALE-lo
    checks.append('CDF symmetry and integer enclosure order at 8 points')
    for seed in [0,1,2,3]:
        z,c=gaussian_seed(random.Random(seed)); assert c['normal_interval_integer']
    checks.append('four additional certified normal cells')
    result={'passed':len(checks),'checks':checks,'wall_seconds':time.perf_counter()-t,
            'scope':'Small deterministic correctness/negative tests, no statistical benchmark or global distribution test'}
    (HERE/'TEST_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
