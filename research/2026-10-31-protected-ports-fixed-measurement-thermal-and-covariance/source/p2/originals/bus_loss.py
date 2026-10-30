"""Exact vacuum-loss coherence witness for an ideal harmonic force loop.

This supplies a necessary resource check, not a complete gate fidelity.
The two branches are Z_A+Z_B=+2,-2. Their force difference is 4G.
The bus and loss input start in vacuum; adding an energy-qualified dirty
bus does not remove this physical loss channel.
"""
import json
import math
from pathlib import Path


def witness(G,omega,Q):
    Delta=4*abs(G); T=2*math.pi/Delta; kappa=omega/Q
    a=kappa/2; D=a*a+Delta*Delta; Fdiff=4*abs(G)
    end=Fdiff*Fdiff/D*(-math.expm1(-a*T))**2
    integral=T-math.expm1(-kappa*T)/kappa-2*a*(-math.expm1(-a*T))/D
    bath=kappa*Fdiff*Fdiff/D*integral
    exponent=(end+bath)/2
    coherence=math.exp(-exponent)
    return dict(Q=Q,gate_time_U=T,kappa_time=kappa*T,
                coherence_exponent=exponent,remaining_coherence=coherence,
                half_trace_distance_witness=(1-coherence)/2,
                final_bus_displacement_difference_squared=end)


if __name__=='__main__':
    G=1.5330926657103854e-5; omega=.05
    r=dict(model='Harmonic force, Markov vacuum loss, calibrated effective frequency; no charge counterterm or nonlinear corrections.',
           G_over_U=G,omega_over_U=omega,
           rows=[witness(G,omega,q) for q in [1e5,1e6,1e7]])
    Path(__file__).with_name('bus_loss_results.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
