from fractions import Fraction as F
from pathlib import Path
import json, time, sys
sys.dont_write_bytecode = True
from sparse_galerkin import certify,fixture,decode,rational_box,product


def dyadic(d):
    # Probability endpoints are compact mantissas; no huge decimal-int parse.
    mantissa,exponent = int(d['mantissa']),int(d['exponent2'])
    return F(mantissa)*(F(2)**exponent)


if __name__ == '__main__':
    prior = json.loads((Path(__file__).resolve().parent.parent /
                        'LARGE_NONFREE_EXCURSION.json').read_text())
    theta,clocks = fixture(24)
    assert list(map(str,theta)) == prior['theta']
    assert list(map(str,clocks)) == prior['clocks']
    prior_lo,prior_hi = map(dyadic,(prior['probability']['lower'],
                                  prior['probability']['upper']))
    Z = (product(1+t for t in theta)+product(1-t for t in theta))/2
    results = []
    for delta in (F(0),F(1,20),F(1,2)):
        print('BEGIN delta',str(delta),flush=True)
        result = certify(theta,clocks,delta,max_degree=3,progress=True)
        lo,hi = decode(result['p_lower']),decode(result['p_upper'])
        # The earlier Gaussian proof plus one-sided conductance transfer
        # contains the actual output; the new interval must be compatible.
        envelope_lo,envelope_hi = prior_lo,(1+delta)*prior_hi
        assert max(lo,envelope_lo) <= min(hi,envelope_hi)
        result['prior_Gaussian_transferred_envelope'] = {
            'lower':rational_box(envelope_lo),'upper':rational_box(envelope_hi),
            'relative_width':float(envelope_hi/envelope_lo-1),
            'compatible':'PASS','new_interval_subset':envelope_lo <= lo <= hi <= envelope_hi}
        if delta == 0:
            assert max(lo,prior_lo) <= min(hi,prior_hi)
            result['reference_Gaussian_overlap'] = 'PASS'
        ra = decode(result['R_a'])
        result['capacity_normalized'] = {'lower':rational_box(lo*ra/Z),
                                         'upper':rational_box(hi*ra/Z)}
        result['Z_even'] = rational_box(Z)
        results.append(result)
        print('END',str(delta),result['status'],lo.__float__(),hi.__float__(),
              result['seconds'],flush=True)
    out = {'status':'ALL_TARGETS_MET' if all(x['status']=='TARGET_MET' for x in results)
              else 'SOME_TARGETS_NOT_MET','cases':results,
           'ordinary_comparator':'Identical sparse Galerkin/CG receives the same model, gap, preprocessing and construction.',
           'statistical_comparator':'Finite-horizon potential-kernel Monte Carlo also has no inverse-global-rarity factor under the same gap/source promises.',
           'scope':'Executed deterministic actual-nonquadratic certificates. No physical model acquisition, priority or new complexity class claimed.'}
    Path('ACTUAL_M24_CASES.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],flush=True)
