#!/usr/bin/env python3
"""Independent dimension-sensitive challenge; separate paid 300-state clock."""
from verify_nonlinear import *
import time

def main():
    n=5;sp=['A','E','B','D','C'];zero=(0,)*n
    def unit(i,a=1):return tuple(a*int(j==i) for j in range(n))
    raw=[(zero,unit(0),F(1,10)),(unit(0),unit(1),F(1)),(unit(1),unit(0),F(1)),
         (unit(0),unit(2),F(1)),(unit(1),unit(3),F(1)),
         (unit(0),zero,F(1)),(unit(1),zero,F(1)),(unit(2),zero,F(1)),(unit(3),zero,F(1))]
    for i in [0,1]:raw += [(unit(i,2),unit(i,3),F(1,10)),(unit(i,3),unit(i,2),F(10))]
    for h,a in [(2,F(1)),(3,F(2))]:
        pair=tuple(int(j==h)+int(j==4) for j in range(n));raw += [(unit(h,2),pair,a),(pair,unit(h,2),F(1))]
    started=time.monotonic();rec,cert,result=run_case('two_inactive_phases_dimension_sensitive_clock',sp,raw)
    elapsed=time.monotonic()-started
    assert len(rec['inactive'])==2 and cert['activation_clock']['clock_radius']==24
    assert cert['activation_clock']['clock_linear_system_dimension']==300
    # Independently challenge Jensen/falling-factorial inequality across every composition
    # at and beyond its dimension-dependent threshold, including maximally balanced counts.
    minimum_slack=None;radial_checks=0
    for r in range(24,73):
        for y in comps(r,2):
            falling=sum(a*(a-1)*(a-2) for a in y)
            slack=F(falling)-F(r**3,8)
            assert slack>=0
            actual=(F(1,10)+F(1,10)*sum(a*(a-1) for a in y))/((r+1)*(r+2))-(r+10*falling)/(F(r)*(r+1))
            assert actual<=-1
            minimum_slack=slack if minimum_slack is None else min(minimum_slack,slack);radial_checks+=1
    bad=p.construct(rec,max_clock_states=299)
    assert not bad['accepted'] and bad['required_clock_states']==300
    output={'case':result,'raw_species':sp,'raw_reactions':raw,'acquired_service':rec['service'],
      'acquired_inactive':rec['inactive'],'clock_radius':24,'clock_dimension':300,
      'clock_fraction_bits':cert['activation_clock']['largest_clock_fraction_bits'],
      'activation_mean_bound':cert['activation_clock']['uniform_activation_mean_upper'],
      'clock_tmax':cert['activation_clock']['clock_exit_mean_max'],'clock_pmin':cert['activation_clock']['clock_activation_probability_min'],
      'nonlinear_tail_bounds':cert['restoring_pair_bounds'],'head_search_trials':cert['search_trials'],
      'radial_exact_compositions_checked':radial_checks,'minimum_jensen_slack':minimum_slack,
      'dimension_specific_clock_budget_UNKNOWN':bad,'elapsed_seconds_observed':elapsed,
      'candidate_source_sha256':hashlib.sha256((HERE/'frozen_nonlinear_boundary.py').read_bytes()).hexdigest(),
      'full_certificate_independently_verified':True}
    print(json.dumps(output,default=p.encode,indent=2))

if __name__=='__main__':main()
