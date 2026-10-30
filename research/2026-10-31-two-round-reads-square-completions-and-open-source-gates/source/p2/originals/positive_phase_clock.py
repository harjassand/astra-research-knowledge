"""Forward-only simultaneous diagonal phase closure from screened geometry.

Four conserved spinful occupations, common onsite U, six density pairs.
Seven real parking configurations supply a full-rank phase matrix. Every
out-and-back transfer's charge phase is integrated before solving waits.
No zero coupling or negative wait is used. Orbital projection and actual
compensating-force hardware remain qualifications.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre,j0,j1,i0,k0
from scipy.integrate import quad_vec


def run():
    a=.2;D=14.;r=1.;H=8.;leg=40.
    pairs=list(itertools.combinations(range(4),2))
    x,w=roots_legendre(160);rr=a*(x+1)/2
    weights=a*w/2*2*rr/a**2/j1(2.404825557695773)**2*j0(2.404825557695773*rr/a)**2
    qs=(2*np.arange(60)+1)*np.pi/2;fm=i0(np.outer(qs,rr))@weights
    def V(R):return float(2*np.dot(k0(qs*R),fm*fm))
    U=12.2895916094
    base=np.array([[D*(k+1),0.] for k in range(4)])
    configs=[base.copy()]
    for i,j in pairs:
        p=base.copy();p[i]=[0.,r/2];p[j]=[0.,-r/2];configs.append(p)
    def energy(positions):
        return np.r_[U,[V(np.linalg.norm(positions[i]-positions[j])) for i,j in pairs]]
    A=np.column_stack([energy(p) for p in configs])
    Ainv=np.linalg.inv(A)
    path_phase=np.zeros(7);minimum=math.inf
    # Every parking configuration is reached and left from all-far.
    # Three axis-aligned smooth stages give a proved clearance:
    # vertical +/-H, horizontal at +/-H, vertical to +/-r/2.
    # The moving-pair distance is >=r; other-port distances are >=min(D,H).
    def path(s,i,j,p):
        pos=base.copy()
        stage=min(int(3*s),2);u=3*s-stage
        v=10*u**3-15*u**4+6*u**5
        if stage==0:
            pos[i,1]=H*v;pos[j,1]=-H*v
        elif stage==1:
            pos[i]=[base[i,0]*(1-v),H];pos[j]=[base[j,0]*(1-v),-H]
        else:
            pos[i]=[0,H*(1-v)+v*r/2];pos[j]=[0,-H*(1-v)-v*r/2]
        return pos
    for (i,j),p in zip(pairs,configs[1:]):
        average,_=quad_vec(lambda s:energy(path(s,i,j,p)),0,1,points=[1/3,2/3],epsabs=1e-10,epsrel=1e-10)
        path_phase+=2*leg*average
        for s in np.linspace(0,1,1001):
            q=path(s,i,j,p)
            minimum=min(minimum,*[np.linalg.norm(q[k]-q[l]) for k,l in pairs])
    target=np.zeros(7);target[1+pairs.index((1,3))]=np.pi
    theta=target-path_phase
    # Constructive positive solution: round phase lattice around a
    # strictly interior positive-time point.
    center=np.pi*np.sum(abs(Ainv),axis=1)+1.
    z=np.rint((A@center-theta)/(2*np.pi)).astype(np.int64)
    waits=Ainv@(theta+2*np.pi*z)
    assert min(waits)>0
    residual=A@waits+path_phase-target-2*np.pi*z
    endpoint=0.
    for occupation in itertools.product(range(3),repeat=4):
        features=np.array([sum(n*(n-1)/2 for n in occupation)]
                          +[occupation[i]*occupation[j] for i,j in pairs])
        actual=np.exp(-1j*(A@waits+path_phase)@features)
        desired=np.exp(-1j*target@features)
        endpoint=max(endpoint,float(abs(actual-desired)))
    total_travel=2*leg*len(pairs);total=total_travel+sum(waits)
    result=dict(occupation_domain='0,1,2 independently at all four ports; 81 joint charge patterns',
                energy_unit='K/h',time_unit='hbar h/K',a_over_h=a,
                far_port_pitch_over_h=D,near_pair_separation_over_h=r,
                transport_lane_height_over_h=H,one_leg_duration=leg,
                proved_center_clearance=min(r,H,D),
                phase_matrix=A.tolist(),phase_matrix_condition=float(np.linalg.cond(A)),
                inverse_row_one_norms=np.sum(abs(Ainv),axis=1).tolist(),
                row_order=['common doublon phase']+[str(p) for p in pairs],
                path_phase=path_phase.tolist(),total_travel_time=total_travel,
                wait_times=waits.tolist(),total_wait_time=float(sum(waits)),total_time=float(total),
                phase_integer_vector=z.tolist(),max_phase_residual=float(max(abs(residual))),
                all_charge_pattern_operator_error=endpoint,
                sampled_minimum_center_distance=minimum,
                worst_four_onsite_fractional_error_for_action_1e3=float(1e-3/(2*U*total)),
                caveats=['The motion path is geometric; its forces and orbital excitation domain must be supplied.',
                         'All charges participating in these phase rows are conserved during the diagonal stage.',
                         'Other orbitals and source cells require the full incident norm bound.',
                         'Exact phase-closure lemma is analytic; electrostatic integrals and waits are ordinary floating point.',
                         'A full routed gate uses this closure at the required sides of noncommuting sorting stages; its cost is additional.'])
    Path(__file__).with_name('positive_phase_clock_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':run()
