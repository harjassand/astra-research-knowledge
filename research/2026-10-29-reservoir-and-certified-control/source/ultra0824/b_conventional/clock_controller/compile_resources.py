#!/usr/bin/env python3
"""Exact scalar resource receiver for PROOF.md.

Default execution acquires only the fixed Bose-filter majorant and universal
error budget. --input accepts a JSON scalar contract (n,L,b,epsilon,E); it does
not qualify the native lambda_B/T_B promises, generate a Jacobi table, prepare
a quantum state or execute dynamics. Huge exact values use a hex JSON codec.
No producer code, system spectra, Hamiltonian instances or random data are read.
"""

from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse
import json
import time


def poly_derivative(p):
    return {j-1: j*c for j, c in p.items() if j}


def flat_derivative_majorants(order=4):
    # exp(-1/x), then the smooth step quotient, then its two scaled factors.
    B, S, filters = [], [], []
    p = {0: 1}
    for k in range(order+1):
        B.append(sum(abs(c)*factorial(j) for j, c in p.items()))
        if k == 0:
            S.append(1)
        else:
            S.append(8*(B[k]+2*sum(comb(k,j)*B[j]*S[k-j]
                                   for j in range(1,k+1))))
        filters.append(4**k*sum(comb(k,j)*S[j]*S[k-j]
                                for j in range(k+1)))
        # p_next=x^2(p-p'), so (d/dx)^k exp(-1/x)=p_k(1/x)exp(-1/x).
        d = poly_derivative(p)
        terms = dict(p)
        for j, c in d.items():
            terms[j] = terms.get(j,0)-c
        p = {j+2: c for j,c in terms.items() if c}
    return filters


def bose_majorant():
    filt = flat_derivative_majorants()
    assert filt == [1,384,199680,136396800,116570456064]
    T = [sum(comb(k,a)*factorial(k-a)*3**(k-a+1)
             for a in range(k+1)) for k in range(5)]
    B = [sum(comb(k,j)*filt[j]*T[k-j] for j in range(k+1))
         for k in range(5)]
    C_B = 64*(1+max(B))
    return filt, T, B, C_B


def ceil_fraction(x):
    x = F(x)
    return (x.numerator+x.denominator-1)//x.denominator


def ceil_log2(x):
    x = F(x)
    if x <= 1:
        return 0
    k = max(0,x.numerator.bit_length()-x.denominator.bit_length())
    if F(1 << k) < x:
        k += 1
    assert F(1 << k) >= x
    assert k == 0 or F(1 << (k-1)) < x
    return k


def schedule(n,L,b,epsilon,E,C_B):
    n,L = int(n),int(L)
    b,epsilon,E = map(F,(b,epsilon,E))
    assert n>=1 and L>=2 and b>=1 and 0<epsilon<1 and E>=0
    m=n*(L-1)
    A=C_B*(1+ceil_fraction(b))**4
    C=4*A
    G=16*m*A*A
    Mbar=32*m*A*A
    Kbar=64*m*A*A
    taubar=32*A*A
    R0=2+3*Mbar
    g=F(1,16)
    U=32*(ceil_fraction(b*(E+1))+L*n+ceil_log2(16/epsilon))
    Kgap=m*C*C*G*(8+2*b+8*R0)
    K11=2*R0+2*G*U*(2*R0+3*Mbar)+2*G*(1+Mbar)*(1+G*U)
    K13=G*U*(4*G*R0+2*Mbar+2*G*G*R0*R0
              +4*G*G*Mbar*R0+G*Kbar)
    K17=G*G*U*(8*taubar+2*b+8*Kbar)
    Ktot=K11+K13+K17+b*G
    alpha=min(F(1),1/(2*b*G),g/(4*Kgap),epsilon/(16*(1+Ktot)))
    tau=U/(alpha*alpha)
    eps_B=epsilon/8
    eta=epsilon/16
    # The first R modes are the common comparison; M is the implemented chain.
    k=ceil_fraction(32*(1+tau))+4*ceil_log2(128*m*(1+tau)/eps_B)
    R=k-1
    ell=ceil_log2(128*m*(R+1)/eps_B)
    M=R+1+4*ell
    B=m*M
    rz=ceil_fraction(64*(B+1)/eta)
    drive_l1=B*rz
    root4_moment=4*(B+1+drive_l1+m*tau)
    sqrt_moment=root4_moment*root4_moment
    cutoff_root=1024*(1+drive_l1+m*tau)*sqrt_moment/eps_B
    K=max(1,ceil_fraction(cutoff_root*cutoff_root)-1)
    local_dim=2*K+2
    tolerance=(epsilon/16)/(4096*(1+tau)*(n+B)*(1+K))

    # Integer/log inequalities pay factorial and covariance errors without
    # constructing 2^(astronomical chain length) or any mode matrix.
    assert k>=12*F(3,2)*tau
    ell0=ceil_log2(128*m*(1+tau)/eps_B)
    assert k>=4*ell0
    assert F(128*m)*(1+tau)/eps_B>1
    assert M-R-1==4*ell
    assert (K+1)>=cutoff_root*cutoff_root
    assert alpha*Ktot<=epsilon/16
    assert alpha*Kgap<=g/4
    assert 1/(2*alpha*G)>=b
    # Elementary denominator bit bound for the explicit moment-Gram floor.
    # Internal precision counts grow with M, not merely log(M).
    d=M+1
    gram_lower_exponent=5+3*ceil_log2(d)+10*(d-1)
    gram_condition_exponent=gram_lower_exponent+ceil_log2(d)+2*(d-1)
    return {
        'kind':'SCALAR_RESOURCE_CONTRACT_NOT_NATIVE_ADMISSION',
        'input':dict(n=n,L=L,b=b,epsilon=epsilon,E=E),
        'm_seeds':m,'A_B':A,'Gamma_upper':G,'moment_upper':Mbar,
        'second_moment_upper':Kbar,'observation_R_upper':R0,
        'U_rescaled':U,'alpha':alpha,'tau_clock_units':tau,
        'Kgap':Kgap,'K11':K11,'K13':K13,'K17':K17,'Ktot':Ktot,
        'comparison_modes_R':R,'implemented_modes_per_chain_M':M,
        'total_bath_modes_B':B,'clipped_amplitude_radius':rz,
        'integrated_force_l1_upper':drive_l1,
        'number_moment_upper':sqrt_moment*sqrt_moment,
        'global_occupation_K':K,'local_level_dimension':local_dim,
        'absolute_coefficient_tolerance':tolerance,
        'calibration_prefactor_4096_requires_native_table_density':True,
        'moment_Gram_lower_bound':'2^(-gram_lower_exponent)',
        'gram_lower_exponent':gram_lower_exponent,
        'gram_condition_upper_bound':'2^(gram_condition_exponent)',
        'gram_condition_exponent':gram_condition_exponent,
        'native_lambda_B_T_B_qualified':False,
        'Jacobi_coefficient_table_generated':False,
        'quantum_state_or_dynamics_executed':False,
    }


def exact_codec(x):
    if isinstance(x,bool) or x is None or isinstance(x,(str,float)):
        return x
    if isinstance(x,F):
        return {'rational':{'numerator':exact_codec(x.numerator),
                            'denominator':exact_codec(x.denominator)}}
    if isinstance(x,int):
        return x if x.bit_length()<=512 else {'integer_hex':hex(x)}
    if isinstance(x,dict):
        return {k:exact_codec(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):
        return [exact_codec(v) for v in x]
    raise TypeError(type(x))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    start=time.perf_counter()
    filt,T,B,C_B=bose_majorant()
    error_budget=F(1,8)+5*F(1,16)
    assert error_budget==F(7,16)<1
    receipt={
        'status':'EXACT_SCALAR_RECURRENCE_AND_RESOURCE_PROGRAM',
        'flat_derivatives_0_through_4':filt,
        'Bose_thermal_derivative_majorants':T,
        'Bose_filter_derivative_majorants':B,
        'C_B':C_B,'C_B_bits':C_B.bit_length(),
        'total_error_over_epsilon_upper':error_budget,
        'physical_time_polynomial_numeric_inputs':['n','b','1/epsilon','E'],
        'claimed_effective_alpha_inverse_coarse_degree':
            'O(epsilon^-1 m^5 (1+b)^40 U)',
        'claimed_cooling_time_coarse_degree':
            'O(epsilon^-2 m^10 (1+b)^80 U^3)',
        'source_lambda_fixed_in_volume':True,
        'microscopic_alpha_fixed_in_volume':False,
        'many_body_minimum_Bohr_gap_input':False,
        'Hamiltonian_spectral_oracle_input':False,
        'native_clock_gate_qualified':False,
        'Jacobi_table_executed':False,'quantum_states_executed':0,
        'Hamiltonian_fixtures_or_trajectories_executed':0,
        'physical_calibration_or_3D_layout_acquired':False,
        'calibration_4096_native_source_term_density_upper_per_clock':256,
        'long_storage_or_multitime_fault_budget_acquired':False,
    }
    if args.input:
        data=json.loads(args.input.read_text())
        receipt['scalar_contract']=schedule(**data,C_B=C_B)
    receipt['wall_seconds_after_imports']=time.perf_counter()-start
    output=args.output or Path(__file__).with_name('RESOURCE_RECURRENCE.json')
    output.write_text(json.dumps(exact_codec(receipt),indent=2)+'\n')
    print(json.dumps({k:exact_codec(receipt[k]) for k in
                     ('status','C_B','C_B_bits',
                      'total_error_over_epsilon_upper',
                      'wall_seconds_after_imports')},indent=2))


if __name__=='__main__':
    main()
