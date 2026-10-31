"""Complete six-site Hubbard implementation of the composite singlet filter.

All intermediate charge sectors at N_up=N_down=3 are retained (400 states).
No spin-model replacement is made during propagation. The optional real
rest-edge hopping is also present during helper phase pulses and ramps.
"""
from pathlib import Path
from itertools import combinations, product
from math import acos, pi, sqrt
import json
import argparse
import numpy as np
from scipy.linalg import eigh, norm, expm
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import expm_multiply

ROOT = Path(__file__).resolve().parent


def fock_basis(sites, n_up, n_down):
    ans = []
    for ups in combinations(range(sites), n_up):
        for dns in combinations(range(sites), n_down):
            ans.append(sum(1 << (2*i) for i in ups) + sum(1 << (2*i+1) for i in dns))
    return ans


def hop(word, p, q):
    if not (word >> q) & 1 or (word >> p) & 1:
        return None
    sign = (-1)**((word & ((1 << q)-1)).bit_count())
    word ^= 1 << q
    sign *= (-1)**((word & ((1 << p)-1)).bit_count())
    return word | (1 << p), sign


def hopping_matrix(basis, edges):
    lookup = {a:i for i,a in enumerate(basis)}
    rows, cols, vals = [], [], []
    for col, word in enumerate(basis):
        for i, j in edges:
            for spin in range(2):
                for p,q in [(2*i+spin, 2*j+spin), (2*j+spin, 2*i+spin)]:
                    result = hop(word, p, q)
                    if result is not None:
                        new, sign = result
                        rows.append(lookup[new]); cols.append(col); vals.append(-sign)
    return csr_matrix((vals, (rows, cols)), shape=(len(basis), len(basis)), dtype=complex)


def spin_states(sites, ups):
    return [sum(1 << i for i in c) for c in combinations(range(sites), ups)]


def spin_dot_matrix(states, i, j):
    lookup = {a:k for k,a in enumerate(states)}
    out = np.zeros((len(states), len(states)), complex)
    for col, word in enumerate(states):
        if ((word >> i) & 1) == ((word >> j) & 1):
            out[col, col] = .25
        else:
            out[col, col] = -.25
            out[lookup[word ^ (1<<i) ^ (1<<j)], col] = .5
    return out


def setup():
    basis = fock_basis(6, 3, 3)
    lookup = {a:i for i,a in enumerate(basis)}
    doubles = np.array([sum(((a >> (2*i)) & 3) == 3 for i in range(6)) for a in basis])
    h_u = diags(doubles, dtype=complex).tocsr()
    h_star = hopping_matrix(basis, [(0,4), (1,4), (2,4), (3,5)])
    h_phase = hopping_matrix(basis, [(4,5)])
    h_rest = hopping_matrix(basis, [(0,1)])
    data = spin_states(4, 2)
    load = np.zeros((len(basis), len(data)), complex)
    for k, word in enumerate(data):
        for up_helper, sign in [(4,1), (5,-1)]:
            full = sum(1 << (2*i + (0 if (word >> i)&1 else 1)) for i in range(4))
            full |= 1 << (2*up_helper)
            full |= 1 << (2*(9-up_helper)+1)
            load[lookup[full], k] = sign/sqrt(2)
    s2 = 3*np.eye(6, dtype=complex) + 2*sum(spin_dot_matrix(data, i, j) for i,j in combinations(range(4),2))
    r2 = 2.25*np.eye(6, dtype=complex) + 2*sum(spin_dot_matrix(data, i, j) for i,j in combinations(range(3),2))
    eye = np.eye(6, dtype=complex)
    p0 = (s2-2*eye)@(s2-6*eye)/12
    p1 = s2@(6*eye-s2)/8
    p2 = s2@(s2-2*eye)/24
    prhalf = (3.75*eye-r2)/3
    projectors = dict(code=p0, j1_rest_half=p1@prhalf, j1_rest_threehalf=p1@(eye-prhalf), j2=p2)
    h_rest_spin = spin_dot_matrix(data,0,1)-.25*eye
    return dict(basis=basis, h_u=h_u, h_star=h_star, h_phase=h_phase, h_rest=h_rest,
                load=load, single_mask=doubles==0, projectors=projectors,
                h_rest_spin=h_rest_spin)


def pulse_shape_propagate(state, static, hopping, duration, ramp_time, ramp_steps, spectrum=None):
    """sin^2 turn-on, plateau, sin^2 turn-off; duration is plateau time.

    Fourth-order two-exponential commutator-free propagation on ramps.
    Plateau propagation is exact eigendecomposition of the full Hamiltonian.
    """
    if ramp_time:
        state = ramp(state, static, hopping, ramp_time, ramp_steps, False)
    if duration > 0:
        if spectrum is None:
            spectrum = eigh((static+hopping).toarray(), check_finite=False)
        vals, vecs = spectrum
        state = vecs @ (np.exp(-1j*duration*vals)[:,None] * (vecs.conj().T @ state))
    if ramp_time:
        state = ramp(state, static, hopping, ramp_time, ramp_steps, True)
    return state


def ramp(state, static, hopping, duration, steps, down):
    a1 = (3-2*sqrt(3))/12
    a2 = (3+2*sqrt(3))/12
    c1 = .5-sqrt(3)/6
    c2 = .5+sqrt(3)/6
    dt = duration/steps
    for i in range(steps):
        def shape(c):
            s = (i+c)/steps
            return np.cos(pi*s/2)**2 if down else np.sin(pi*s/2)**2
        g1,g2 = shape(c1),shape(c2)
        state = expm_multiply(-1j*dt*(.5*static+(a2*g1+a1*g2)*hopping), state)
        state = expm_multiply(-1j*dt*(.5*static+(a1*g1+a2*g2)*hopping), state)
    return state


def max_on(p, effect):
    return float(max(0., np.linalg.eigvalsh((p@effect@p + (p@effect@p).conj().T)/2)[-1]))


def analyze(state, m, total_time, j_rest):
    load=m['load']; ps=m['projectors']; p0=ps['code']
    k=load.conj().T@state
    clean=state[m['single_mask'],:]
    q_charge=np.eye(6)-clean.conj().T@clean
    accept=k.conj().T@k
    target=expm(-1j*j_rest*total_time*m['h_rest_spin'])@p0
    alpha=np.trace(target.conj().T@k@p0)/2
    accepted_error=float(norm(k@p0-alpha*target,2))
    out=dict(total_duration_U_units=float(total_time),
             norm_preservation_error=float(norm(state.conj().T@state-np.eye(6))),
             accepted_code_scalar=[float(alpha.real),float(alpha.imag)],
             accepted_code_target_operator_error=accepted_error,
             code_reject_probability=max_on(p0,np.eye(6)-accept),
             code_final_charge_probability=max_on(p0,q_charge),
             worst_final_charge_probability=float(max(0.,np.linalg.eigvalsh(q_charge)[-1])),
             worst_false_accept_probability=max_on(np.eye(6)-p0,accept),
             sector_stats={})
    for name,p in ps.items():
        rank=int(round(np.trace(p).real))
        beta=np.trace(p@k@p)/rank
        out['sector_stats'][name]=dict(rank_m0=rank,
            accepted_amplitude=[float(beta.real),float(beta.imag)],
            scalar_residual=float(norm(k@p-beta*p,2)),
            maximum_accept_probability=max_on(p,accept),
            charge_probability=max_on(p,q_charge))
    return out,k


def run_case(m, ratio, ramp_time=0., ramp_steps=40, calibrated=False, rest_fraction=0.):
    # Units U=1, J_nom=1/ratio. All contact edges have the same hopping.
    j=1/ratio
    t=.5*sqrt(j)
    j_pair=(sqrt(1+16*t*t)-1)/2
    clock=j_pair if calibrated else j
    # A physical rest edge with exactly calibrated isolated-pair exchange.
    j_rest=rest_fraction*j
    t_rest=.5*sqrt(j_rest*(1+j_rest))
    static=m['h_u']+t_rest*m['h_rest']
    hops=[t*m['h_star'],t*m['h_phase']]
    spectra=[eigh((static+h).toarray(), check_finite=False) for h in hops]
    # Integrate the actual isolated-pair gap on a ramp for pair-calibrated
    # clocks. This is a pulse-area calibration, not a projection in propagation.
    grid=np.linspace(0,1,2001)
    gs=np.sin(pi*grid/2)**2
    jg=(np.sqrt(1+16*(t*gs)**2)-1)/2 if calibrated else j*gs**2
    ramp_angle=float(2*ramp_time*np.trapezoid(jg,grid))
    phi=acos(1/3)
    sequence=[(0,pi),(1,2*pi-phi),(0,3*pi),(1,phi),(0,pi)]
    state=m['load'].copy(); total=0.; lengths=[]
    for kind,angle in sequence:
        plateau=(angle-ramp_angle)/clock
        if plateau < 0: raise ValueError('Ramp exceeds pulse angle')
        state=pulse_shape_propagate(state,static,hops[kind],plateau,ramp_time,ramp_steps,spectra[kind])
        total+=plateau+2*ramp_time
        lengths.append(plateau+2*ramp_time)
    answer,k=analyze(state,m,total,j_rest)
    answer.update(U_over_J_nominal=ratio,t_over_U=t,J_pair_over_J_nominal=j_pair/j,
                  ramp_time_U_units=ramp_time,ramp_steps=ramp_steps,
                  isolated_pair_phase_calibration=calibrated,
                  concurrent_rest_exchange_fraction=rest_fraction,
                  pulse_durations_U_units=lengths)
    return answer,k


def star_spectrum(ratio):
    basis=fock_basis(4,2,2); t=.5/sqrt(ratio)
    ds=np.array([sum(((a>>(2*i))&3)==3 for i in range(4)) for a in basis])
    h=diags(ds,dtype=complex)+t*hopping_matrix(basis,[(0,3),(1,3),(2,3)])
    vals=eigh(h.toarray(),eigvals_only=True)
    low=vals[:6]
    # Low m=0 multiplets ordered at small t: symmetric triplet, two
    # standard singlets, two standard triplets, fully polarized quintet.
    e1sym=float(low[0]); e0=float(np.mean(low[1:3])); e1std=float(np.mean(low[3:5])); e2=float(low[5])
    delta=e1std-e0
    return dict(U_over_J_nominal=ratio, low_m0_eigenvalues=list(map(float,low)),
                J_standard=delta,J_standard_over_J_nominal=delta*ratio,
                symmetric_gap=e2-e1sym,
                symmetric_to_standard_gap_ratio=(e2-e1sym)/delta,
                pair_gap_over_standard_gap=((sqrt(1+4/ratio)-1)/2)/delta)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--quick',action='store_true')
    args=parser.parse_args()
    m=setup(); rows=[]
    ratios=[10.,20.,50.,100.] if not args.quick else [20.]
    for ratio in ratios:
        for ramp_time,calibrated,rest in [(0.,False,0.),(10.,False,0.),(10.,True,0.),(10.,True,.2)]:
            answer,k=run_case(m,ratio,ramp_time,40,calibrated,rest)
            rows.append(answer)
            print(json.dumps({key:answer[key] for key in ['U_over_J_nominal','ramp_time_U_units','isolated_pair_phase_calibration','concurrent_rest_exchange_fraction','code_reject_probability','worst_false_accept_probability','code_final_charge_probability','accepted_code_target_operator_error','total_duration_U_units']}),flush=True)
    # One concrete numerical-risk resolution: repeat the most demanding
    # chosen ramp example with twice the integration resolution.
    a,k1=run_case(m,20.,10.,40,True,.2)
    b,k2=run_case(m,20.,10.,80,True,.2)
    convergence=dict(case_U_over_J=20.,steps=[40,80],accepted_operator_difference=float(norm(k1-k2,2)),
                     coarse_code_charge=a['code_final_charge_probability'],fine_code_charge=b['code_final_charge_probability'])
    data=dict(model='six-site single-orbital Hubbard; exact 400-state Sz=0 propagation',
              cases=rows,ramp_convergence=convergence,
              four_site_star_spectra=[star_spectrum(r) for r in [10.,20.,50.,100.,200.,1000.]])
    (ROOT/'finite_hubbard_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(convergence),flush=True)


if __name__=='__main__': main()
