#!/usr/bin/env python3
"""Independently execute key analytic checks for the radiative-rank / local bus continuation."""
import math,json,numpy as np
from scipy.integrate import solve_ivp
from scipy.special import roots_legendre

GAMMA=.2;X=12.5;TAU=2.5;E0=24
A=X/GAMMA

def gamL(t):
    return GAMMA/(1+math.exp(-GAMMA*t)) if -A<=t<=A else 0.
def gamR(t):
    u=t-TAU
    return GAMMA/(1+math.exp(GAMMA*u)) if -A<=u<=A else 0.
def left_amplitude(t):
    if t< -A:return 1.
    if t>A:return math.exp(-X/2)
    return math.sqrt((1+math.exp(-X))/(1+math.exp(GAMMA*t)))
def ode(t,y):
    source=0.
    if -A+TAU<=t<=A+TAU:
        z=t-TAU
        source=math.sqrt(gamL(z)*gamR(t))*left_amplitude(z)
    return [-0.5*gamR(t)*y[0]-source]
sol=solve_ivp(ode,(-A,A+TAU),[-0.],rtol=3e-12,atol=3e-13,max_step=.04)
b_numeric=float(sol.y[0,-1]);b_expected=-(1-math.exp(-X))

# Minimum radiative port rank: two spatially distinct emitters coupled to two directions.
sep=1.3; omega=np.linspace(.04,12,1001)
mindet=float(np.min(np.abs(2*np.sin(omega*sep))))
nonresonant=omega[np.abs(np.sin(omega*sep))>.15]
max_inverse_cond=0
for w in nonresonant[::25]:
    M=np.array([[1,np.exp(1j*w*sep)],[1,np.exp(-1j*w*sep)]])
    max_inverse_cond=max(max_inverse_cond,float(np.linalg.cond(M)))

# For finite band h(omega)=(1-((omega-E0)/E0)^2)^2,
# exactly int h(omega)/omega domega = 4/3.
w,quad=roots_legendre(300)
energy=E0*(1+w)
h=(1-w*w)**2
inverse_weight=float(np.dot(quad,h/(1+w))) # omega=E0(1+w); domega=E0 dw

# Rigorous truncation bound of an attached gapless Jacobi arm length m.
J=8.; eta=.05; K=2*J+eta;T=143.6875;M=7000
u=K*T
log_bound=math.log(J*T)+M*math.log(u)-math.lgamma(M+1)-math.log1p(-u/(M+1))

out={'markov_cascade':{'x':X,'gamma':GAMMA,'numerical_receiver_amplitude':b_numeric,
    'exact_receiver_amplitude':b_expected,'absolute_difference':abs(b_numeric-b_expected),
    'exact_full_state_error':math.sqrt(2*math.exp(-X)),
    'exact_sender_population':math.exp(-X),
    'minimum_total_emission_duration_for_target_error_1pct':2*math.log(1/.01)/GAMMA},
    'two_bidirectional_ports':{'determinant':'-2i sin(omega*(xR-xL)); full column rank on every open interval except isolated points',
    'tested_w_frequency_samples':len(omega),'max_matrix_condition_on_selected_nonzero_samples':max_inverse_cond,
    'logical_basis':'compact-time source Fourier transforms are entire; zeros over a nonempty spectral interval force zero sources'},
    'finite_positive_chiral_band':{'analytic_integral_h_over_omega':4/3,'quadrature':inverse_weight,
      'schur_margin_at_E0_24_gamma_0p3':24-4*.3/(3*np.pi)},
    'gapless_arm_completion':{'J':J,'eta':eta,'K_max_offdiag_row_sum':K,'T':T,'m':M,
     'u':u,'rigorous_log10_norm_difference_bound':log_bound/math.log(10),
     'formula':'J*T*sum_{n>=M} (K*T)^n/n! <= J*T*(K*T)^M/M! / (1-K*T/(M+1))',
     'proof_scope':'One-excitation, uniformly bounded local controls, initial state at sender; infinite auxiliary arm vs M-site truncation.'}}
assert abs(b_numeric-b_expected)<2e-9
assert abs(inverse_weight-4/3)<1e-12
assert log_bound/math.log(10)<-300
with open('/mnt/data/astra_radiative_rank_and_local_transfer_audit_20261027.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
