"""Bounded arithmetic/quadrature diagnostics; not interval certification."""
import json
from pathlib import Path
import mpmath as mp

mp.mp.dps=50
p=lambda r: 1/mp.gamma(2+r/2)
breaks=[0,1,2,4,8,16,32,64,128]
mass=mp.quad(lambda r:r*r*p(r),breaks)
variance=mp.quad(lambda r:r**4*p(r),breaks)/(3*mass)
gap=64/(27*mp.pi**4)
# Independent numerical integration of the maximally mixed output radius.
def u(r):
    f=lambda s:s*p(s)
    return (f(r+1)+(f(r-1) if r>1 else -f(1-r)))/(2*r)
outmass=mp.quad(lambda r:r*r*u(r),breaks)
outsecond=mp.quad(lambda r:r**4*u(r),breaks)/outmass
discrepancy=abs(outsecond/3-(1+variance))
assert discrepancy<mp.mpf('1e-40')
assert abs(outmass/mass-1)<mp.mpf('1e-40')
result={'schema':'astra.genesis2.pauli-variance-check.v1',
        'decimal_precision':50,'integration_breaks':breaks,
        'gamma_noise_variance_per_coordinate':str(variance),
        'analytic_variance_gap':str(gap),
        'analytic_variance_lower_bound':str(2+gap),
        'gamma_raw_coordinate_second_moment':str(outsecond/3),
        'ordinary_covariant_raw_coordinate_second_moment':3,
        'moment_identity_discrepancy':str(discrepancy),
        'all_assertions_passed':True,
        'scope':'bounded quadrature and arithmetic; finite cutoff; no interval error or physical validation'}
out=Path(__file__).with_name('PAULI_VARIANCE_CHECK.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
