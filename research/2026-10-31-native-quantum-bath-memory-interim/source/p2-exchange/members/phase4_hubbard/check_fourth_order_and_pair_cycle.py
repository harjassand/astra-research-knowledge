"""Algebraic Hubbard expansion and same-parameter helper load/read cycle."""
from pathlib import Path
from itertools import combinations
from math import pi,sqrt,ceil,acos
import json
import numpy as np
from scipy.linalg import eigh,norm,expm
from scipy.integrate import solve_ivp
from check_finite_hubbard import fock_basis,hopping_matrix,spin_states,spin_dot_matrix

ROOT=Path(__file__).resolve().parent


def fourth_order_star():
    basis=fock_basis(4,2,2); lookup={a:i for i,a in enumerate(basis)}
    doubles=np.array([sum(((a>>(2*i))&3)==3 for i in range(4)) for a in basis])
    # t=U=1 only for extraction of formal homogeneous expansion coefficients.
    v=hopping_matrix(basis,[(0,3),(1,3),(2,3)]).toarray()
    states=spin_states(4,2)
    p=np.zeros((len(basis),len(states)),complex)
    for k,word in enumerate(states):
        f=sum(1<<(2*i+(0 if (word>>i)&1 else 1)) for i in range(4))
        p[lookup[f],k]=1
    r=np.diag([1/d if d else 0 for d in doubles])
    a=p.conj().T@v@r@v@p
    c=p.conj().T@v@r@r@v@p
    b=p.conj().T@v@r@v@r@v@r@v@p
    h2=-a
    h4=-b+(a@c+c@a)/2
    star=sum(spin_dot_matrix(states,i,3)-.25*np.eye(6) for i in range(3))
    leaves=sum(spin_dot_matrix(states,i,j)-.25*np.eye(6) for i,j in combinations(range(3),2))
    want2=4*star
    want4=-16*star+4*leaves
    r2=2.25*np.eye(6)+2*sum(spin_dot_matrix(states,i,j) for i,j in combinations(range(3),2))
    # All matrices have dyadic-rational entries; the zero residual is an
    # exact arithmetic identity in this basis, not a small fitted difference.
    return dict(second_order_max_entry_error=float(np.max(abs(h2-want2))),
                fourth_order_max_entry_error=float(np.max(abs(h4-want4))),
                extra_leaf_term_commutator_with_star=float(norm(leaves@star-star@leaves)),
                extra_leaf_term_as_rest_spin_error=float(norm(leaves-(r2-3.75*np.eye(6))/2)),
                H2_coefficient=h2.real.tolist(),H4_coefficient=h4.real.tolist(),
                canonical_SW_formula='H2=-PVRVP; H4=-PVRVRVRVP+{PVRVP,PVR^2VP}/2; R=Q/H_U')


def pair_hamiltonian(delta,t):
    # Basis D_L, S_11, D_R. The triplet manifold has H=0 identically.
    return np.array([[1+delta,-sqrt(2)*t,0],[-sqrt(2)*t,0,-sqrt(2)*t],[0,-sqrt(2)*t,1-delta]],complex)


def evolve_segment(state,duration,delta,tfun):
    if duration==0:return state
    def rhs(time,y):
        s=time/duration
        return -1j*pair_hamiltonian(delta(s),tfun(s))@y
    sol=solve_ivp(rhs,[0,duration],state,rtol=2e-11,atol=2e-13,method='DOP853')
    assert sol.success
    return sol.y[:,-1]


def pair_read_cycle(ratio=50.,ramp=40.,sweep=400.,delta_final=1.5):
    t=.5/sqrt(ratio)
    state=np.array([0,1,0],complex)
    state=evolve_segment(state,ramp,lambda s:0.,lambda s:t*np.sin(pi*s/2)**2)
    state=evolve_segment(state,sweep,lambda s:delta_final*s,lambda s:t)
    state=evolve_segment(state,ramp,lambda s:delta_final,lambda s:t*np.cos(pi*s/2)**2)
    read_state=state.copy()
    prep=np.array([0,0,1],complex)
    prep=evolve_segment(prep,ramp,lambda s:delta_final,lambda s:t*np.sin(pi*s/2)**2)
    prep=evolve_segment(prep,sweep,lambda s:delta_final*(1-s),lambda s:t)
    prep=evolve_segment(prep,ramp,lambda s:0.,lambda s:t*np.cos(pi*s/2)**2)
    vals=[eigh(pair_hamiltonian(d,t),eigvals_only=True) for d in np.linspace(0,delta_final,501)]
    gap=min(v[1]-v[0] for v in vals)
    return dict(U_over_J_nominal=ratio,t_over_U=t,ramp_duration_U_units=ramp,
                sweep_duration_U_units=sweep,delta_final_over_U=delta_final,
                per_direction_duration_U_units=2*ramp+sweep,
                read_final_probabilities_DL_S_DR=list(map(float,abs(read_state)**2)),
                read_singlet_false_triplet_probability=float(1-abs(read_state[2])**2),
                prep_final_probabilities_DL_S_DR=list(map(float,abs(prep)**2)),
                preparation_error_probability=float(1-abs(prep[1])**2),
                minimum_singlet_adiabatic_gap_over_U=float(gap),
                norm_errors=[float(abs(norm(read_state)**2-1)),float(abs(norm(prep)**2-1))],
                triplet_response='identity in all three triplet states in the one-orbital model')


def low_band_gaps():
    # The complete six-site star is a disconnected four-site star and pair,
    # but electrons may distribute among them in the full N=6 Hilbert space.
    # The 400-dimensional check retains all those charge distributions.
    from check_finite_hubbard import setup
    m=setup(); t=.5/sqrt(50.)
    ans=[]
    for kind in ['h_star','h_phase']:
        for scale in [0.,.25,.5,.75,1.]:
            vals=eigh((m['h_u']+scale*t*m[kind]).toarray(),eigvals_only=True)
            ans.append(dict(pulse=kind,amplitude_fraction=scale,
                            spin_band_top=float(vals[19]),
                            next_charge_eigenvalue=float(vals[20]),
                            low_band_gap=float(vals[20]-vals[19])))
    return ans


def exact_pair_controls():
    tmax=.5/sqrt(50.)
    phimax=pi*(1-1/sqrt(1+16*tmax*tmax))
    rows=[]
    for theta in [pi/4,pi/2,pi,acos(1/3),2*pi-acos(1/3)]:
        m=ceil(theta/phimax)
        omega=1/(1-theta/(pi*m))
        t=.25*sqrt(omega*omega-1)
        duration=2*pi*m/omega
        out=expm(-1j*pair_hamiltonian(0.,t)*duration)@np.array([0,1,0],complex)
        rows.append(dict(theta=theta,revivals=m,t_over_U=t,duration_U_units=duration,
                         singlet_return_error=float(norm(out-np.array([0,np.exp(1j*theta),0]))),
                         charge_leak_probability=float(abs(out[0])**2+abs(out[2])**2)))
    return rows


def main():
    data=dict(fourth_order=fourth_order_star(),
              helper_pair_cycle=pair_read_cycle(),
              finite_hubbard_band_gaps=low_band_gaps(),
              exact_finite_U_pair_controls=exact_pair_controls())
    (ROOT/'fourth_order_and_pair_cycle_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data['fourth_order'].items() if 'coefficient' not in k},indent=2))
    print(json.dumps(data['helper_pair_cycle'],indent=2))
    print('Minimum sampled full charge-band gap:',min(x['low_band_gap'] for x in data['finite_hubbard_band_gaps']))


if __name__=='__main__':main()
