#!/usr/bin/env python3
"""Exact native-bath distinctions and excluded-case controls."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
import sympy as s

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/autonomous_memory'
sys.path.insert(0,str(ROOT/'work'))
from native_bath_memory import probability_bad


def vec(A):return s.Matrix([A[i,j] for j in range(A.cols) for i in range(A.rows)])
def dissipator(A):
    d=A.rows;I=s.eye(d);G=A.conjugate().T*A
    return s.kronecker_product(A.conjugate(),A)-(s.kronecker_product(I,G)+s.kronecker_product(G.T,I))/2


def choi(S,d):
    J=s.zeros(d*d)
    for i in range(d):
        for j in range(d):
            for a in range(d):
                for b in range(d):J[a*d+i,b*d+j]=S[a+d*b,i+d*j]/d
    return J


def main():
    start=time.perf_counter();I=s.eye(2);X=s.Matrix([[0,1],[1,0]])
    Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    gamma=s.Rational(1,100);h=s.Rational(1,2000)
    B=(I+Z)/2;K=s.kronecker_product(X,B)
    J=K/10+s.I*s.eye(4)/200
    Hsuper=-s.I*h*(s.kronecker_product(s.eye(4),K)-s.kronecker_product(K.T,s.eye(4)))
    native=gamma*dissipator(K)+Hsuper
    assert dissipator(J)==native
    effect=J.conjugate().T*J
    assert effect==gamma*s.kronecker_product(I,B)+h*h/gamma*s.eye(4)
    r=s.symbols('r',positive=True)
    u=vec(s.eye(4))/2;v=vec(s.kronecker_product(I,Z))/2
    W=u.row_join(v);compression=s.simplify(W.conjugate().T*choi(s.eye(16)+native/r,4)*W)
    expected=s.Matrix([[1-gamma/(2*r),-gamma/(4*r)],[-gamma/(4*r),0]])
    assert s.simplify(compression-expected)==s.zeros(2)
    assert s.simplify(compression.det()+gamma**2/(16*r**2))==0
    k=vec(K)/2
    Q=s.eye(16)-u*u.conjugate().T
    assert s.simplify(Q*choi(native,4)*Q-gamma*k*k.conjugate().T)==s.zeros(16)
    for P in (X,Y,Z):
        vb=vec(s.kronecker_product(I,P))/2
        assert (k.conjugate().T*vb)[0]==0
    z=s.symbols('z',real=True)
    bathH=s.kronecker_product(I,z*Z)
    bathcomm=-s.I*(s.kronecker_product(s.eye(4),bathH)-s.kronecker_product(bathH.T,s.eye(4)))
    residual=s.simplify(W.conjugate().T*choi(s.eye(16)+(native-bathcomm)/r,4)*W)
    assert s.simplify(residual.det()+(gamma**2/16+z*z)/r**2)==0
    # Counterexample to replacing conditional operator rates by an average.
    p=F(1,100);conditional=probability_bad(F(1),F(1),F(1))
    actual=(p*conditional[0],p*conditional[1])
    mean_only=probability_bad(p,F(1),F(1))
    assert actual[0]>mean_only[1]
    # Exact all-good bath completion remains TP even though its individual
    # branches steer an L-B entangled input. This is not postselected memory.
    Bell=s.Matrix([1,0,0,1])/s.sqrt(2);rho=Bell*Bell.T
    M0=s.diag(1,s.Rational(3,5));M1=s.Matrix([[0,s.Rational(4,5)],[0,0]])
    assert M0.T*M0+M1.T*M1==I
    A=s.kronecker_product(I,M1)
    post=A*rho*A.T
    assert s.trace(post)==s.Rational(8,25)
    # An uncharged continuous H creates a logical error with no jumps:
    # exp[-i(pi/2)Y_1] exp[-i(pi/2)Y_2] exp[-i(pi/2)X_4]
    # is i IYYIX, a logical X up to phase in the [[5,1,3]] code.
    # The exact Gaussian code proof in native_bath_memory.py establishes this.
    result={'status':'EXACT_NATIVE_BATH_INTERFACE_AND_COUNTERMODELS_PASSED',
        'displaced_jump_same_native_generator_exact':True,
        'escape_effect_exact':str(effect),
        'finite_rate_CPTP_uniformization_impossible':{'dimension_memory_bath':4,
            'operator_K':'X_M tensor |0><0|_B',
            'normalized_Choi_compression':str(compression),
            'determinant_exact':str(s.factor(compression.det())),
            'negative_for_every_finite_positive_rate':True,
            'conditional_Choi_rank_one_and_bath_subspace_orthogonal_exact':True,
            'after_arbitrary_bath_Hamiltonian_reallocation_determinant':str(s.factor(residual.det())),
            'scope':'Id+native_generator/r is not CP; no claim excluding larger-state dilations or other analysis'},
        'conditional_rates_are_state_dependent':{
            'bath_zero':str(gamma+h*h/gamma),'bath_one':str(h*h/gamma),
            'ratio_exact':str((gamma+h*h/gamma)/(h*h/gamma))},
        'mean_rate_countermodel':{'rare_active_bath_probability':str(p),
            'active_conditional_rate':'1','unconditional_average_rate':str(p),
            'correction_rate':'1','duration':'1',
            'actual_bad_geometry_probability_enclosure':list(map(str,actual)),
            'incorrect_Poisson_mean_rate_enclosure':list(map(str,mean_only)),
            'strict_separation_exact':True,
            'scope':'bad-record domination fails under a mean-only rate; not a theorem counterexample'},
        'postselected_bath_outcome':{'initial_state':'logical-bath Bell pair',
            'selected_outcome_probability':'8/25','logical_marginal_after_selection':'|1><1|',
            'averaged_bath_channel_preserves_logical_marginal':True,
            'postselected_preservation_not_claimed':True},
        'uncharged_Hamiltonian_counterexample':{'local_terms':['Y_1','Y_2','X_4'],
            'integrated_angle_each':'pi/2','counted_fault_jumps':0,
            'final_logical_channel':'Ad_X exactly','diamond_distance_from_identity':'2',
            'excluded_hypothesis':'quiet Hamiltonian syndrome-scalar',
            'scope':'one correction-free finite interval; disproves jump-only support accounting'},
        'new_random_draws':0,'physical_experiments':0,
        'CPU_wall_seconds':time.perf_counter()-start,
        'code_SHA256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'exact_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['CPU_wall_seconds'],
        'Choi_determinant':result['finite_rate_CPTP_uniformization_impossible']['determinant_exact'],
        'hazard_ratio':result['conditional_rates_are_state_dependent']['ratio_exact'],
        'actual_bad_preview':[float(x) for x in actual],
        'incorrect_mean_only_preview':[float(x) for x in mean_only],'new_random_draws':0},indent=2))


if __name__=='__main__':main()
