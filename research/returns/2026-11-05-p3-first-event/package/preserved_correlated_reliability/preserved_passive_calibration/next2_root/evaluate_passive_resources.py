"""Explicit sufficient resource arithmetic, not executed acquisition.

The contraction check uses rational lower bounds C_b(q)>=2(1-2*b*q),
so the displayed inverse certificate does not depend on numerical quadrature.
High-precision logarithms here evaluate upper-bound formulae; deployed integer
rounding must use directed arithmetic as specified in the accompanying proof.
"""
import json, math
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp

mp.mp.dps=90
n,M,k,d=2,15,2,12
r,w,J,kappa=F(4),F(3,500),F(57,50),F(3,5)
q=r*w; x=4*J*w
mu=kappa*q/4
slopes=[]; contracts=[]
for b in range(1,k+1):
    c_lb=2*(1-2*b*q)
    assert c_lb>0
    bracket=((1-x)**(-b-1)+(1+x)**(-b-1))/2-1
    rho=4*d*b*bracket/c_lb
    assert rho<=F(1,4)
    slopes.append(w*c_lb)
    contracts.append(dict(b=b,C_lower=str(c_lb),rho_exact=str(rho),rho_float=float(rho)))
def m(z):return mp.mpf(z.numerator)/z.denominator if isinstance(z,F) else mp.mpf(z)
lam=min(slopes)
capture_time=mp.log(80000)/mp.mpf('2.46')
eta=mp.mpf('.1')/(100*M*capture_time)
delta=m(lam)*eta/32
confidence=mp.mpf('.001')
V=(1+2/(m(kappa)*m(q)))**(k+1)
mean_count=m(mu)+m(kappa)*m(q)/4
K=max(1,int(mp.ceil(mean_count)))
# P(Poisson(v)>K)<=(3*v/(K+1))^(K+1), using e<3.
while (3*mean_count/(K+1))**(K+1)>delta**2/(128*V*(k+1)):
    K+=1
B=(K/mp.sqrt(m(kappa)*m(mu)*m(q)))**(k+1)
N=mp.ceil(128*(V/delta**2+B/delta)*mp.log(2*M/confidence))
burn=2/m(r)*mp.log(16*mp.sqrt(n*mp.log(2))/delta)
exposure=N*(burn+2*m(w))
# A conservative independent mean-bias budget for clock errors.
timing=delta*m(w)/(128*(k+1))
# Distinct-port Poisson domination gives the improved unclipped moment bound.
# Fixed response d0 is a chosen model-unit parameter, not a device claim.
d0=mp.mpf('0.000001'); intensity=m(mu)/m(w)+m(kappa)*m(r)/4
rails=mp.ceil(32*(k+1)*intensity*d0*(1+d0/m(w))/delta)
loglo=mp.log10(6*n*N*m(mu)/m(kappa))
cw_loglo=mp.log10(3*n*m(kappa)*m(r)*exposure/(4*m(kappa)))
out={
 'status':'Evaluated sufficient resource bounds; no theorem-scale acquisition executed.',
 'source':{'n':n,'M':M,'k':k,'d':d,'r':str(r),'J':str(J),'w':str(w),'q':str(q),'kappa':str(kappa),'mu':str(mu)},
 'rational_contraction_certificates':contracts,
 'lambda_star_lower':str(lam),'old_capture_time':str(capture_time),
 'coefficient_accuracy':str(eta),'total_response_accuracy':str(delta),
 'confidence_failure':str(confidence),'variance_bound':str(V),
 'counter_cap':K,'clipped_statistic_bound':str(B),
 'log10_raw_blocks':str(mp.log10(N)),
 'log10_source_exposure_in_model_units':str(mp.log10(exposure)),
 'burn_duration_per_block':str(burn),
 'clock_endpoint_tolerance_example':str(timing),
 'fixed_detector_deadtime_example':str(d0),'log10_detector_rails_per_port_example':str(mp.log10(rails)),
 'log10_incident_LO_photon_allocation':str(loglo),
 'log10_incident_CW_LO_photon_allocation_including_burn':str(cw_loglo),
 'LO_efficiency_assumption_for_incident_budgets':'LO transmission/detection efficiency equals kappa; divide detected budgets by the actual LO efficiency in general.',
 'inverse_iterations':int(mp.ceil(mp.log(4*m(J)/eta,2))),
 'cost_not_in_trial_count':'Classical connected-set response inversion, detector service/propagation, phase/gain/loss/port calibration, and any separate coherent archive.',
 'comparison':'Old 10^39.12 total-raw-trial schedule used different purifier/export observations and lossless collection. This count is a different sufficient protocol at the same coefficient target, allowing kappa=.6; it is not an optimality or laboratory comparison.',
 'rounding':'Values printed to 90 decimal digits; the rational rho comparisons are exact. Other constants are conservative high-precision resource evaluations, not machine-checked interval certificates.'
}
Path(__file__).with_name('passive_resource_bounds.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['rational_contraction_certificates','coefficient_accuracy','total_response_accuracy','counter_cap','log10_raw_blocks','log10_source_exposure_in_model_units','burn_duration_per_block','clock_endpoint_tolerance_example','log10_detector_rails_per_port_example','inverse_iterations']},indent=2))
