"""High-precision numerical sanity checks of the exact enclosure implementation.
These tests are not the mathematical proof of the enclosure, given separately.
"""
import json
from fractions import Fraction
from pathlib import Path
import mpmath as mp
import certify_finite_expression as c
mp.mp.dps=110
assert mp.mpf(c.PI_LO)/c.EQ<mp.pi<mp.mpf(c.PI_HI)/c.EQ
records=[]
for value in (Fraction(0),Fraction(1,3),Fraction(-12345,7),Fraction(2)**40,-(Fraction(2)**40)):
 x=round(value*c.Q);(re,im),err=c.exp_minus_i(x)
 observed=abs(mp.mpc(mp.mpf(re)/c.EQ,mp.mpf(im)/c.EQ)-mp.exp(-1j*mp.mpf(x)/c.Q))
 bound=mp.mpf(err.numerator)/err.denominator
 assert observed<=bound
 records.append({'phase':str(value),'error_upper':str(bound),'observed_error_at_110_digits':str(observed),'passed':True})
p=Path(__file__).with_name('PHASE_ENCLOSURE_SANITY.json');p.write_text(json.dumps({'pi_interval_contains_110_digit_reference':True,'cases':records},indent=2)+'\n');print('Five phase enclosure sanity checks passed.')
