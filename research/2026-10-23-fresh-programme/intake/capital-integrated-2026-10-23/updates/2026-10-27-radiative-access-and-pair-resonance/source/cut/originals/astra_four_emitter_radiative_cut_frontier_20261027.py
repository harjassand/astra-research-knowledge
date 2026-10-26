#!/usr/bin/env python3
"""Independent four-emitter source-compatibility and no-bypass transfer bounds.

Hamiltonian: H=H_L(t) directsum H_R(t) directsum omega + W+W^dagger.
Initial one excitation is in L. The 'no-bypass' theorem is an operator-
norm bound independent of H_L,H_R and their control slew.

This is NOT a device simulation, nor a claim about microscopic relativity.
"""
import json, math
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import roots_legendre
from scipy.linalg import expm
from scipy.optimize import brentq
from sympy import symbols, integrate, cos, simplify, sin

eta=.01; cutoff=12.; tau=.5; T=12.; quadN=40
x=np.arange(4,dtype=float)*tau
wgrid,weights=roots_legendre(quadN)
w=.5*cutoff*(wgrid+1)
weights=.5*cutoff*weights
v=eta*np.sqrt(w)*(1-w/cutoff)**2
W4=np.vstack([np.sqrt(weights)[:,None]*v[:,None]*np.exp(1j*sign*w[:,None]*x[None,:]) for sign in [1,-1]])
W_L=W4[:,:2]; W_R=W4[:,2:]
wL=np.linalg.norm(W_L,2); wR=np.linalg.norm(W_R,2)
cut_upper=(wL/wR)*(np.cosh(wR*T)-1)
T_min=math.acosh(1+wR/wL)/wR
eta_min=eta*T_min/T

# Analytic two-emitter Gram calculation. x4-x2=2*tau=1.
z=symbols('z',real=True)
expr=simplify(integrate(z*(1-z/12)**4*cos(z),(z,0,12)))
K42_exact=f'2 eta^2 * ({expr})'
K42=2*eta**2*float(expr.evalf(20))

# For t<tau, the earlier A-source has q2(t)=-[4t(1-t)]^3, and q3=q4=0.
# The e4 equation cannot then be satisfied by on-site controls or nearest-
# neighbor e3-e4 coupling when the latter is bounded, as the source returns
# nonzero bath forcing. Compute the exact convolution in spectral quadrature.
def q2_initial(t):
    return -(4*t*(1-t))**3 if 0<t<tau else 0.

def memory_kernel(dt):
    return 2*np.sum(weights*(v**2)*np.cos(w*(x[3]-x[1]))*np.exp(-1j*w*dt))

def forced_emitter4(t):
    real=quad(lambda s: (memory_kernel(t-s)*q2_initial(s)).real,0,t,epsabs=2e-16)[0]
    imag=quad(lambda s: (memory_kernel(t-s)*q2_initial(s)).imag,0,t,epsabs=2e-16)[0]
    return -1j*(real+1j*imag)

onset=[]
for t in [.1,.05,.02,.01]:
    f=forced_emitter4(t)
    leading=1j*K42*16*t**4
    onset.append({'t':t,'actual_real':float(f.real),'actual_imag':float(f.imag),
                  'leading_imag':float(leading.imag), 'ratio':float((f/leading).real),
                  'relative_complex_remainder':float(abs(f/leading-1))})

# A completely independent full one-photon unitary check:
# internal basis (a,e1,e2,b,e3,e4), bath 2*quadN modes.
n=6+2*quadN
C=np.zeros((n,n),complex)
C[6:,6:]=np.diag(np.tile(w,2))
for emitter_index, internal_index in enumerate([1,2,4,5]):
    C[6:,internal_index]=W4[:,emitter_index]
    C[internal_index,6:]=W4[:,emitter_index].conj()

# Perturbatively small waveguide-mediated transfer, with locally engineered
# emitter/storage couplings but absolutely no term across the L/R cut.
base=C.copy()
base[:6,:6]=np.diag([3.,2.,3.,3.,2.,3.])
for i,j,coupling in [(0,2,.6),(1,2,.4),(3,4,.6),(4,5,.4)]:
    base[i,j]=base[j,i]=coupling
initial=np.zeros(n,complex);initial[0]=1.
final=expm(-1j*base*T)@initial
normR=float(np.linalg.norm(final[3:6]))
bathnorm=float(np.linalg.norm(final[6:]))

# Explicit direct-bypass control graph; now the cut theorem must NOT apply.
# Length-four perfect-transfer chain: a--e2--e3--b (other emitters passive).
bypass=C.copy()
bypass[:6,:6]=np.diag([3.,3.,3.,3.,3.,3.])
for i,j,hopping in [(0,2,math.sqrt(3)),(2,4,2.),(4,3,math.sqrt(3))]:
    bypass[i,j]=bypass[j,i]=math.pi*hopping/(2*T)
final_bypass=expm(-1j*bypass*T)@initial
normR_bypass=float(np.linalg.norm(final_bypass[3:6]))

# Trivial analytic bound avoids any oscillatory quadrature: two-emitter
# port Gram lambda_max<=Tr Gram = 2*G00, with G00=9.6 eta^2.
trivial_w=math.sqrt(19.2)*eta
trivial_bound=np.cosh(trivial_w*T)-1

# A numerical root of zero-time cross coupling, for a possible bath-geometry
# alternative (only eliminates the LEADING forcing coefficient).
def gram_at_sep(sep):
    return 2*eta**2*quad(lambda z:z*(1-z/12)**4*np.cos(z*sep),0,12,epsabs=5e-13)[0]
sep0=brentq(gram_at_sep,.4,.6,xtol=1e-13)
M1_at_zero=2*eta**2*quad(lambda z:z**2*(1-z/12)**4*np.cos(z*sep0),0,12,epsabs=5e-13)[0]
# At the tuned zero, K'(0)=-i M1. For q2=-64t^3+O(t^4),
# W4^dag xi(t)=+3.2*M1*t^5+O(t^6). This is still not identically zero.
port_trace=9.6*eta**2
required_ports=math.ceil((math.acosh(2)/(T*math.sqrt(port_trace)))**2)
bath_exposure_min=1/(wR**2*T)
bath_exposure_at_eta_threshold=1/((wR*eta_min/eta)**2*T)

result={
 'setup': {'eta':eta,'cutoff':cutoff,'tau':tau,'T':T,'quadrature_nodes_per_direction':quadN,'emitter_positions':x.tolist()},
 'bath_norms':{'W_L':wL,'W_R':wR,'full_gram_diagonal':float((W4.conj().T@W4)[0,0].real),
               'gram_nearest_offdiag':float((W4.conj().T@W4)[0,1].real),
               'gram_2tau':float((W4.conj().T@W4)[1,3].real)},
 'no_bypass_theorem':{'formula':'norm(P_R U(T) P_L) <= (wL/wR)*(cosh(wR*T)-1)',
                      'max_right_amplitude':float(cut_upper),
                      'minimum_time_for_perfect_transfer':float(T_min),
                      'minimum_eta_at_T12_necessary':float(eta_min),
                      'minimum_radiation_exposure_integral':float(bath_exposure_min),
                      'radiation_exposure_if_coupling_at_necessary_threshold':float(bath_exposure_at_eta_threshold),
                      'necessary_emitters_per_region_same_per_site_coupling_trace_bound':int(required_ports),
                      'elementary_gram_free_bound':float(trivial_bound)},
 'early_source_obstruction':{'K42_exact_expression':K42_exact,
                            'K42_value':K42,'leading':'W_4^dag xi(t)=i*16*K42*t^4+O(t^5)',
                            't_samples':onset},
 'full_hamiltonian_validation':{'local_controls_right_norm':normR,'local_controls_bath_norm':bathnorm,
                                 'no_bypass_bound':float(cut_upper),
                                 'bypass_right_norm':normR_bypass,
                                 'bypass_does_not_obey_no_bypass_bound':bool(normR_bypass>cut_upper)},
 'geometry_alternative':{'separation_for_zero_K42':sep0,'tau_for_same_2tau_spacing':sep0/2,
  'next_spectral_moment_M1':float(M1_at_zero),
  'residual_after_M0_orthogonalization':'W4^dag xi(t)=3.2*M1*t^5+O(t^6); nonzero even when K42(0)=0',
  'scope':'Cancels only zeroth cross Gram; higher spectral moments remain and local dynamics not constructed'},
 'claims_scope':'Analytic no-bypass amplitude bound for arbitrary local Hermitian time-dependent controls; explicit source-incompatibility for original early histories. Numerical expm tests illustrate but do not prove theorem.'
}
assert normR<cut_upper+1e-12
assert normR_bypass>cut_upper
assert all(o['relative_complex_remainder'] < 0.4 for o in onset)
with open('/mnt/data/astra_four_emitter_radiative_cut_frontier_20261027.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
