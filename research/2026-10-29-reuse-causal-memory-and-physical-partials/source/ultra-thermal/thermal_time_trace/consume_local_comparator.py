"""Exact local SAME-noisy-record efficiency bound; consumes frozen scalars.

This is a Fisher information statement at the stationary a0 reference,
NOT a fixed-Delta classification run or a new ideal-readout fixture.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import json,time,hashlib

HERE=Path(__file__).resolve().parent
p=HERE/'INTERFACE.json';r=json.loads(p.read_text());start=time.perf_counter()
def take(k):return F(r[k]['exact'])
theta=F(r['theta']);d=take('b_equals_d');g=take('g')
rho2=take('rho_squared_upper');rho8=rho2**4
psd=F(r['access']['noise_psd']);spacing=F(4,3);b0=F(8,11)
s0=theta*d+3*psd
per_read_lower=theta**4*d*d*g**4*b0*b0/(s0*s0)
rate_lower=per_read_lower/spacing
fraction_upper=rho8*(F(3,2)*theta**2*d**4+3*theta**2*d**3*spacing)/per_read_lower
asymptotic_fraction_upper=take('local_stationary_at_a0_Fisher_rate_chaos4_upper')/rate_lower
def enc(x):
 with localcontext() as ctx:
  ctx.prec=18
  return {'exact':str(x),'display':str(Decimal(x.numerator)/Decimal(x.denominator))}
out={'status':'EXACT_LOCAL_GAUSSIAN_COMPARATOR_QUALIFIED','scope':'Stationary one-sided derivative at a0, fixed Gaussian rectangular exposure record delta1/3,spacing4/3,Sdet1/100. All Q>=1. No finiteDelta efficiency transfer.','ordinary_operation':'Full Gaussian covariance likelihood for linear shunt, multiplied by3theta*d; this equals the quartic second-chaos score.','lower_covariance_likelihood_Fisher_per_read':enc(per_read_lower),'lower_covariance_likelihood_Fisher_rate':enc(rate_lower),'additional_fourth_chaos_fraction_upper_every_Q':enc(fraction_upper),'additional_fourth_chaos_fraction_upper_asymptotic':enc(asymptotic_fraction_upper),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'new_continuant_queries':0,'data_readouts':0,'seconds_after_imports':time.perf_counter()-start}
(HERE/'LOCAL_COMPARATOR.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
