"""Conservative dimensionless budgets; no values are device measurements."""
from __future__ import annotations
import json
import math
from pathlib import Path


def geometric_amplitude(a, err, n):
    return min(1., a**n + err * (1-a**n)/(1-a))


def budget(a, e_contact, nc, nr, charge_error, prep_error,
           tau, switch_and_supply, charge_time, spin_strength=0.):
    # Two selective contacts per return macrostep, no extra ramp error in this
    # illustrative account; any actual ramp error must be added to 2*e_contact.
    qc = geometric_amplitude(a, e_contact, nc)
    qr = geometric_amplitude(a, 2*e_contact, nr)
    helpers = nc + 2*nr
    wall = helpers * (tau + switch_and_supply) + 2*charge_time
    epsilon = qc + qc*qc + qr*qr + 2*charge_error + helpers*prep_error + spin_strength*wall
    return dict(a=a, coherent_error_per_contact=e_contact, capture_contacts=nc,
                return_macrosteps=nr, cold_helpers=helpers, complete_charge_reads=2,
                capture_miss_probability_bound=qc*qc,
                return_failure_probability_bound=qr*qr,
                charge_instrument_error_per_read=charge_error,
                helper_preparation_error_per_use=prep_error,
                full_wall_time=wall, spin_strength=spin_strength,
                total_error_bound=epsilon)


def main():
    rows=[]
    for target in [1e-2, 1e-3, 1e-4]:
        # These are simultaneous dimensionless certificate requirements, not a
        # claim that a fabricated device achieves them. e_contact is an amplitude.
        e_contact=target/32
        delta_q=target/16
        prep=target/100000
        candidates=[]
        for nc in range(1,25):
            for nr in range(1,25):
                z=budget(.2,e_contact,nc,nr,delta_q,prep,math.pi/2,.5,4.)
                if z['total_error_bound']<=target:
                    candidates.append(z)
        best=min(candidates,key=lambda z:z['full_wall_time'])
        best['target']=target
        # Sufficient first-order gap budget using block row bounds s<=s0/Delta,
        # c<=c0/Delta, with w,v fixed. This is just equation (2) solved numerically.
        # Constants have intentionally simple values and are not tied to the
        # separate Coulomb quadrature's geometry.
        s0,c0,w,v=.4,.08,1.15,.5
        def contact_bound(gap):
            s=s0/gap
            return 2*s+(math.pi/2)*math.exp(2*s)*(c0/gap+2*s*w+s*v)
        lo,hi=1.,1.
        while contact_bound(hi)>e_contact:
            hi*=2
        for _ in range(80):
            mid=(lo+hi)/2
            if contact_bound(mid)>e_contact:lo=mid
            else:hi=mid
        best['illustrative_sufficient_energy_gap']=hi
        best['computed_contact_bound']=contact_bound(hi)
        best['gap_constants']=dict(s0=s0,c0=c0,w=w,v=v)
        rows.append(best)
    # Show why more contacts at fixed imperfection do not imply unbounded gain.
    exposure=[budget(.2,2e-4,n,max(1,(n+1)//2),1e-5,2e-7,
                     math.pi/2,.5,4.,spin_strength=2e-6)
              for n in range(1,21)]
    result=dict(scope="Dimensionless model budgets only; no material parameter or practical advantage is inferred.",
                scenarios=rows, fixed_hardware_exposure_scan=exposure,
                minimum_exposure_scan=min(exposure,key=lambda z:z['total_error_bound']))
    path=Path(__file__).resolve().parent/'cold_carrier_resource_results.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(scenarios=rows, fixed_hardware_best=result['minimum_exposure_scan']),indent=2))


if __name__=='__main__':
    main()
