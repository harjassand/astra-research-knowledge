"""Exact checks supporting the analytic counterexamples; Python standard library."""
from fractions import Fraction as F
from pathlib import Path
import json

e=F(1,10000); L=(1-e)**2/4; U=2*e
assert L-U>F(1,5)
assert L/U>1024
assert F(5,6)<F(3,2)
# Geometric moments at z=1/2 prove normalization of (k-1)^2/2^(k+2).
z=F(1,2)
s0=1/(1-z);s1=z/(1-z)**2;s2=z*(1+z)/(1-z)**3
assert (s2-2*s1+s0)/4==1
assert F((0-1)**2,2**(0+2))==F(1,4)
assert F((1-1)**2,2**(1+2))==0
# Common-squeezing scalar counterexample: cosh(2r)=3, N_A=N_B=1, G=2.
k_input=F(1,2)+1/(F(2)**3-1)
k_output=F(1,2)+1/(F(5,4)**3-1)
assert k_output-3*k_input==-F(162,427)
r={'epsilon':str(e),'L':str(L),'U':str(U),'L_minus_U':str(L-U),
   'L_over_U':str(L/U),'output_K_strict_upper':'5/6',
   'proposed_RHS_lower':'3/2','strict_failure_margin_lower':'2/3',
   'scalar_squeezing_gap':str(k_output-3*k_input),
   'fock_output_normalization_exact':True,
   'scope':'Exact arithmetic supports the written analytic proof; neither counterexample refutes EPnI.'}
Path(__file__).with_name('exact_results.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
