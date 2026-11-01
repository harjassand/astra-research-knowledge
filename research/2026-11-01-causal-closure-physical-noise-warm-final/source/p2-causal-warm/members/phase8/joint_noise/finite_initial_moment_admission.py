"""Finite conditioning FROM an explicit initially admitted number cap.
This computes the consequence of that physical admission; it does not measure
or assume that a laboratory device has acquired such a cap.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent
src=json.loads((HERE/'robust_complete_meter_tail_results.json').read_text())
cfg=src['model'];T=1.2;Ninit=100
rows=[]
for case in src['cases']:
    theta=case['theta_ceiling'];nb=cfg['thermal_nmax'];eps=1.;u=cfg['force_error_cap'];r=cfg['ramp']
    def w(t):
        if t<r:return math.sin(math.pi*t/(2*r))**2
        if t>T-r:return math.sin(math.pi*(T-t)/(2*r))**2
        return 1.
    d=(1-math.exp(-theta))*(1-nb*math.expm1(theta));sh=2*math.sinh(theta/2)
    def rhs(t,y):
        kl=cfg['k0_lower']+cfg['read_rate_lower']*w(t)
        ku=cfg['k0_upper']+cfg['read_rate_upper']*w(t)
        a=kl*d-u*eps*sh;b=ku*nb*math.expm1(theta)+u/eps*sh
        return [-a/theta*y[0]+b]
    sol=solve_ivp(rhs,[0,T],[theta*Ninit],rtol=1e-11,atol=1e-12,max_step=.005)
    end=float(sol.y[0,-1]);bound=case['log_M_boundary']
    assert end<=bound
    rows.append(dict(theta=theta,initial_number_cap=Ninit,initial_log_moment=theta*Ninit,
                     final_log_moment_upper=end,required_boundary_log_moment=bound,
                     conditioning_duration=T,conditioning_ramp=.1,force_error_envelope=u,
                     comparison='Finite moment admission is sufficient; no vacuum target is imposed.'))
out=dict(physical_model=cfg,initial_admission='n<=100 is an explicit prior hardware energy admission; it has NOT been inferred from mean energy or acquired by this script.',
         initialization_before_data_encoding=True,rows=rows,
         costs='The1.2/g conditioning interval, its two0.1/g ramps, thermal flux, residual force, and all control errors must be charged separately from the10.984/g repeated meter.')
(HERE/'finite_initial_moment_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
