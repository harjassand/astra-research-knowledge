#!/usr/bin/env python3
"""Exact rational certificates for the manuscript's fixed numerical margins."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
Elo=sum((F(1,factorial(k)) for k in range(11)), F(0))
Ehi=Elo+F(1,factorial(11))*F(12,11)
Xlo=Elo**6
qlo=((Xlo-1)/(Xlo+1))**2
assert qlo>F(99,100)
alphahi=3*(1-qlo)
assert alphahi<F(3,100)
rhi=3/Xlo
epsilonhi=4*rhi**4*(4/(1-rhi)+rhi/(1-rhi)**2)
assert epsilonhi<F(247,5000000000)
rhohi=16*Ehi**2/10000
assert rhohi<F(3,250)
assert rhohi/(1-rhohi)<1
# Universal tail: beta=.03. R=0,1 checked exactly. For R>=2:
# 4 beta^(2R)[2R/(1-beta)+beta/(1-beta)^2] <= 9R beta^(2R).
# R beta^R decreases for R>=2 since beta*(R+1)/R <= 3beta/2 <1.
beta=F(3,100)
tail4=4*beta**4*(4/(1-beta)+beta/(1-beta)**2)
assert tail4<=10 and tail4<=10*beta
assert 8/(1-beta)+2*beta/(1-beta)**2<=9
assert F(3,2)*beta<1
assert 9*2*beta**2<=10
result={
 'status':'all exact rational inequalities passed',
 'exp1_lower':str(Elo),'exp1_upper':str(Ehi),
 'q_lower_approx':float(qlo),'alpha_upper_approx':float(alphahi),
 'peierls_epsilon_upper_approx':float(epsilonhi),
 'kp_rho_upper_approx':float(rhohi),
 'uniform_correlation_bound':{'C':10,'c':'log(100/3)','scope':'all integer distances R>=0'},
 'method':'factorial-series rational brackets; analytic monotonicity for all R>=2'
}
p=Path(__file__).with_name('final_constants_results.json')
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
