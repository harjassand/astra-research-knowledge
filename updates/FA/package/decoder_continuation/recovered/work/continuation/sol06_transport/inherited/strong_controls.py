#!/usr/bin/env python3
"""Matched nonlinear passive controls; no assumed uniform500Pa.s baseline."""
from dataclasses import replace
from pathlib import Path
import json
import math

import numpy as np
from scipy.integrate import simpson
from scipy.optimize import brentq

import nonlinear_transport as model


def wall_film(target,delta,p,carrier=.084):
    a=p.radius-delta
    r=np.linspace(0,a,1025)
    def mean(G):
        core=simpson(r*r*model.unactuated_rate(G*r/2,p),x=r)
        film=G*(p.radius**4-a**4)/(8*carrier)
        return (core+film)/p.radius**2
    gradient=brentq(lambda G:mean(G)-target,1e-10,1e7,xtol=1e-10)
    power=gradient*p.length*math.pi*p.radius**2*target/p.pump_efficiency
    return {'film_thickness_m':delta,'carrier_viscosity_Pa_s':carrier,
      'pressure_gradient_Pa_m':gradient,'electric_W':power,
      'gate':'Ideal stable same-carrier layer; its physical availability, migration and concentration changes are not supplied.'}


def main():
    p=model.Parameters();target=.003125;rows=[]
    active=json.loads(Path(__file__).with_name('nonlinear_transport.json').read_text())['rows']
    for factor in (1.,1.5,2.,3.):
        flow=math.pi*p.radius**2*target*factor
        candidates=[r for r in active if r['throughput_factor']==factor and
                    not r['outside_OSP_chi_data'] and not r['outside_unactuated_stress_data']
                    and r['material_strain_max']<=.05]
        best=min(candidates,key=lambda r:r['rigid_resonator']['total_electric_before_idle_and_seal'])
        power=best['rigid_resonator']['total_electric_before_idle_and_seal']
        def passive(radius):
            mean=flow/(math.pi*radius**2)
            return model.unactuated_matched(mean,replace(p,radius=radius))[1]
        baseline=passive(p.radius)
        radius_match=brentq(lambda r:passive(r)-power,p.radius,p.radius*2) if power<baseline else None
        films=[wall_film(target*factor,d,p) for d in (2e-6,5e-6,10e-6,20e-6)]
        rows.append({'throughput_factor':factor,'flow_L_min':flow*60000,
          'same125mm_pipe_unactuated_W':baseline,
          'conditional_rigid_active_before_missing_costs_W':power,
          'active_wall_velocity':best['wall_velocity'],
          'unactuated161mm_pipe_W':passive(.0805),
          '161mm_holdup_factor':(.0805/p.radius)**2,
          'minimum_passive_ID_matching_active_power_m':None if radius_match is None else 2*radius_match,
          'passive_holdup_factor_matching_active':None if radius_match is None else (radius_match/p.radius)**2,
          'ideal_carrier_film_controls':films})
    data={'status':'strong matched passive controls against explicitly conditional active cases',
      'rows':rows,'passive_geometry_gate':'Larger-pipe control changes envelope and inventory; fixed-envelope benefit requires a real constraint forbidding this change.',
      'source_caveat':'Unactuated curve is SI figure-digitised; OSP raw curve and its off-rate multiplicative extension are separate evidence.'}
    Path(__file__).with_name('strong_controls.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))


if __name__=='__main__':
    main()
