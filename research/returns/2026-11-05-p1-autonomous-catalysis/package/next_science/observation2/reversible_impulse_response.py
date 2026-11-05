"""Exact complete-current pulse response, including subsequent relaxation.

Synthetic two-state, parallel-channel reversible counterexample. The pulse
protocol is prescribed externally; this does NOT claim a thermodynamically
free autonomous pulse or fit the PtCo catalyst. The invention constructor
separately supplies a closed chemical/gate model.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parent
KB=8.617333262e-5; TEMP=298.; TAU=41e-9
c=1000.;d=1e6
a=2.3e9*np.exp(-.375/(KB*TEMP))
affinity=1.2/(KB*TEMP)
b=c*a*np.exp(-affinity)/d
lam=a+b+c+d
J0=(c*a-d*b)/lam
piI=(c+b)/lam
hI=(a+b)/lam
w=1-hI
C=.192/(KB*TEMP);g=np.exp(C)

def rectangle(pI0):
    lam1=c+d+g*(a+b)
    pi1=(c+g*b)/lam1
    occupation=pi1*TAU+(pI0-pi1)*(-np.expm1(-lam1*TAU))/lam1
    return (g-1)*w*((a+b)*occupation-b*TAU)

def exponential(pI0):
    # Dimensionless time x=t/tau resolves the fast pulse waveform.
    def rhs(x,y):
        gg=np.exp(C*np.exp(-x))
        pI=y[0]
        return [TAU*((c+gg*b)*(1-pI)-(d+gg*a)*pI),
                TAU*(gg-1)*w*((a+b)*pI-b)]
    z=solve_ivp(rhs,(0,45),[pI0,0.],rtol=2e-11,atol=[1e-13,1e-16])
    assert z.success
    return z.y[1,-1]

currents=[]
for r in [1.,3.3,float(g)]:
    J=(c*r*a-d*r*b)/(r*(a+b)+c+d)
    currents.append(dict(barrier_multiplier=r,current=J,gain=J/J0))
responses=[]
for p,name in [(piI,'unconditioned_stationary'),(1.,'conditioned_on_rare_reactive_state')]:
    responses.append(dict(initial_condition=name,p_reactive=p,
       rectangle_net_additional_turnovers=rectangle(p),
       exponential_net_additional_turnovers=exponential(p)))
out=dict(scope=__doc__,parameters=dict(T_K=TEMP,tau_s=TAU,
    precursor_forward=c,precursor_reverse=d,product_forward=a,
    product_reverse=b,total_cycle_affinity_eV=1.2,
    J0=J0,reactive_state_probability=piI,
    product_barrier_degree_of_control=w,
    naive_irreversible_waiting_fraction=J0/a,
    Poisson_h=[0.,hI],product_corrected_reward=w,
    conditioning_relative_entropy_nats=-np.log(piI),
    kBT_times_conditioning_relative_entropy_eV=-KB*TEMP*np.log(piI),
    conditioning_caveat='The reference is a nonequilibrium steady state. kBT times its relative entropy is reported as an energy scale, not asserted to be an unconditional thermodynamic work cost; that identification needs an acquired equilibrium free-energy reference and preparation protocol.'),
    steady_cases=currents,pulse_responses=responses)
(ROOT/'reversible_impulse_response.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
