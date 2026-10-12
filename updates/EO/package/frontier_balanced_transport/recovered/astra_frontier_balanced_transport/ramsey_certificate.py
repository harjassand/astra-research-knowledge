"""Exact certificate arithmetic for a local Ramsey decision rule.
The optional synthetic outcomes are clearly NOT laboratory measurements.
"""
from fractions import Fraction as Q
from math import factorial, exp, cos
from pathlib import Path
import numpy as np, json

N=100000
h=Q(1,90)
tau=Q(1,4)
d=Q(2)
Lambda=Q(4)
# Hoeffding: failure <=2 exp(-N h^2/2)<1/100, certified without log/float.
y=Q(N)*h*h/2
lower_exp_y=sum((y**k/factorial(k) for k in range(18)),Q(0))
assert lower_exp_y>200
# e^(1/2) >= 1+1/2+(1/2)^2/2+(1/2)^3/6 =79/48.
E_lower=sum(((d*tau)**k/factorial(k) for k in range(4)),Q(0))
assert E_lower==Q(79,48)
c=1-Lambda**2*tau**2/12
assert c==Q(11,12)
accept=Q(51,100)
Xi_upper=2*(1-E_lower*(accept-h))/(c*tau**2)
D_lower=4/(4+Xi_upper)
ratio=D_lower/Q(1,8)
assert ratio>3
# Synthetic fixture only; the conditional certificate is valid for any outcomes
# satisfying the threshold under the specified physical/statistical assumptions.
mu=exp(-float(d*tau))*cos(3*float(tau)/2)**2*cos(float(tau)/2)**2
rng=np.random.default_rng(261012)
plus=int(rng.binomial(N,(1+mu)/2))
sample_mean=Q(2*plus-N,N)
record={'status':'Exact rational decision certificate; floating synthetic fixture is not an experiment',
        'N':N,'tau':str(tau),'d':str(d),'detuning_bound':str(Lambda),
        'acceptance_rule':'sample mean >= 51/100',
        'statistical_radius':str(h),'conditional_confidence_at_least':'99/100',
        'Hoeffding_exponent_exact':str(y),'exp_lower_exceeds_200':True,
        'Xi_upper_exact':str(Xi_upper),'Xi_upper':float(Xi_upper),
        'target_D_lower_exact':str(D_lower),'target_D_lower':float(D_lower),
        'baseline_D_upper':'1/8','ratio_lower_exact':str(ratio),'ratio_lower':float(ratio),
        'evolution_time_total':'25000 time units plus preparation, control, readout and calibration',
        'synthetic_fixture':{'seed':261012,'mean_model_float':mu,'plus_outcomes':plus,
           'sample_mean_exact':str(sample_mean),'accepts':sample_mean>=accept},
        'missing_physical_resources':'No device, preparation/measurement calibration, real Ramsey shots, Markovianity or model validation supplied.'}
Path(__file__).with_name('ramsey_checks.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
