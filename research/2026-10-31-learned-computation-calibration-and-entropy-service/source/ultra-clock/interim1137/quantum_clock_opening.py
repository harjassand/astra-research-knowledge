#!/usr/bin/env python3
"""Different-family attack: geometric gates and autonomous heralded quantum clocks.

Exact symbolic construction. This supplies no engineered quantum reservoir,
calibrated gate, physical detector or quantum-computing advantage.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time
import sympy as s

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/quantum_clock_opening'
sys.path.insert(0,str(ROOT/'work'))
from coherent_generator_control import inverse,mv


def zero(A):return all(s.simplify(x)==0 for x in A)


def main():
    start=time.perf_counter();OUT.mkdir(parents=True,exist_ok=True)
    ket0=s.Matrix([1,0,0]);ket1=s.Matrix([0,1,0]);exc=s.Matrix([0,0,1]);bright=(ket0-ket1)/s.sqrt(2)
    H=exc*bright.T+bright*exc.T;P=ket0*ket0.T+ket1*ket1.T
    assert zero(P*H*P) and zero(H**3-H)
    a=s.symbols('a',real=True);U=s.eye(3)+(s.cos(a)-1)*H**2-s.I*s.sin(a)*H
    assert zero(s.simplify(U.conjugate().T*U-s.eye(3)))
    assert zero(U*H-H*U)
    assert zero(U.subs(a,s.pi)[:2,:2]-s.Matrix([[0,1],[1,0]]))
    area_controls=[]
    for scale in [s.Rational(1),s.Rational(1,2),s.Rational(1,3),s.Rational(1,10),s.Rational(2)]:
        state=s.simplify(U.subs(a,s.pi*scale)*ket0)
        fidelity=s.simplify(abs((ket1.T*state)[0])**2)
        leakage=s.simplify(abs((exc.T*state)[0])**2)
        area_controls.append({'unknown_coupling_scale':str(scale),'nominal_pulse_area':'pi',
                              'target_X_fidelity_exact':str(fidelity),'fidelity_preview':float(fidelity),
                              'auxiliary_leakage_exact':str(leakage)})
    # Autonomous clock with noncommuting unitary-dressed hops. It needs
    # no external completion time for conditional correctness, but every
    # unitary is already supplied in the coherent jump interaction.
    Had=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);phase=s.diag(1,s.I)
    gates=[Had,phase,Had];frames=[s.eye(2)]
    for gate in gates:frames.append(s.simplify(gate*frames[-1]))
    L=len(gates);p=F(2);q=F(1);n=L+1;checks=0
    G=s.diag(*frames)
    for j,gate in enumerate(gates):
        edge=s.zeros(n);edge[j+1,j]=1
        dressed=s.kronecker_product(edge,gate)
        bare=s.kronecker_product(edge,s.eye(2))
        assert zero(G.conjugate().T*dressed*G-bare);checks+=1
        assert zero(G.conjugate().T*dressed.conjugate().T*G-bare.conjugate().T);checks+=1
    # First-hit backwards equations hold as CHANNEL identities for every
    # logical input, because each forward/backward composition telescopes.
    final=frames[-1]
    for j in range(L):
        to_final=s.simplify(final*frames[j].conjugate().T)
        forward=s.simplify(final*frames[j+1].conjugate().T*gates[j])
        assert zero(forward-to_final);checks+=1
        if j:
            backward=s.simplify(final*frames[j-1].conjugate().T*gates[j-1].conjugate().T)
            assert zero(backward-to_final);checks+=1
    Q=[[F(0)]*L for _ in range(L)]
    for j in range(L):
        Q[j][j]=-p-(q if j else 0)
        if j+1<L:Q[j][j+1]=p
        if j:Q[j][j-1]=q
    times=mv(inverse([[-x for x in row] for row in Q]),[F(1)]*L)
    assert times[0]==F(17,8)
    # A bath resolving the logical computational index has the SAME clock
    # rates but dephases the first hop. Paired reverse jumps use adjoints.
    plus=s.Matrix([1,1])/s.sqrt(2);rho=plus*plus.T;projectors=[s.diag(1,0),s.diag(0,1)]
    split=sum((gate0*rho*gate0.conjugate().T for gate0 in [gates[0]*D for D in projectors]),s.zeros(2))
    assert split==s.eye(2)/2
    target=s.simplify(final*rho*final.conjugate().T)
    fidelity=s.simplify(s.trace(target*split));assert fidelity==s.Rational(1,2)
    data={'status':'QUANTUM_GEOMETRIC_AND_HERALDED_CLOCK_CONTROLS_PASSED',
          'geometric_gate':{'parallel_transport_logical_Hamiltonian_zero_exact':True,
                            'ideal_pi_area_is_X_exact':True,'unknown_source_scale_controls':area_controls,
                            'finite_deadline_bound':'||U_lambda-I|| <= lambda * integral ||H_nominal(t)|| dt',
                            'scope':'actual path closure/pulse area not acquired by specifying a geometric target'},
          'autonomous_heralded_clock':{'clock_states':n,'supplied_logical_gates':['H','S','H'],
              'coherent_hop_gauge_identities_and_first_hit_channel_checks':checks,
              'completion_channel':'Ad_(H S H), exactly, for any positive common clock-rate scale',
              'mean_completion_time_at_unit_scale':str(times[0]),
              'mean_completion_time_at_scale_lambda':'17/(8 lambda)',
              'deadline_success_upper':'min(1,(3 lambda T)^3/6)',
              'clock_bath_entropy_flow_per_completion':'3 log(2)',
              'thermal_gradient_clock_reset_work_floor':'3 kBT log(2)',
              'not_total_instrument_entropy':'detector, halt and controller record costs remain unacquired'},
          'bath_coherence_negative_control':{'same_classical_clock_rates':True,
              'logical_plus_input_final_state':'I/2','target_fidelity_exact':str(fidelity),
              'missing_physical_primitive':'coherent unitary-dressed bath jumps, not logical-state-resolving jump channels'},
          'ordinary_incumbent':'same supplied unitary-dressed quantum clock; gauge equivalent to bare clock carrying identity',
          'decision':'not selected for sustained depth: correctness can be heralded, but gates/bath coherence are supplied and kinetic deadline burden remains',
          'physical_experiments':0,'new_observations':0,'elapsed_wall_seconds':time.perf_counter()-start}
    (OUT/'receipt.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))


if __name__=='__main__':main()
