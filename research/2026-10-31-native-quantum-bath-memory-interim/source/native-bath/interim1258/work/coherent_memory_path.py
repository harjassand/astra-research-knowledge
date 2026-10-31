#!/usr/bin/env python3
"""Finite coherent-fault receiver and a certified failed global-scan transfer."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/autonomous_memory'
sys.path.insert(0,str(ROOT/'work'))
from native_bath_memory import code_basis,bath_projection,choi
sys.path.insert(0,str(ROOT/'outputs/reversible_currents'))
from currents import log_bounds


def exact_matrix(A):
    return s.SparseMatrix(A.shape[0],A.shape[1],{
        (i,j):int(A[i,j].real)+s.I*int(A[i,j].imag)
        for i in range(A.shape[0]) for j in range(A.shape[1]) if A[i,j]!=0})


def main():
    start=time.perf_counter();frame,algebra=code_basis()
    I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
    words=['IYIII','IIYII','IIIIX'];bath=[Z,Z,X]
    t=F(1,100);den=10001
    partial=s.SparseMatrix(64,4,{(i,i):1 for i in range(4)})
    for word,B in zip(words,bath):
        K=s.kronecker_product(exact_matrix(frame(word)),B)
        assert K*K==s.eye(64)
        U=(9999*s.eye(64)+200*s.I*K)/den
        partial=U*partial
    Kraus=[partial[4*j:4*j+4,:] for j in range(16)]
    assert sum((K.conjugate().T*K for K in Kraus),s.zeros(4))==s.eye(4)
    channel=sum((s.kronecker_product(K.conjugate(),K) for K in Kraus),s.zeros(16))
    eta=4*t/(1+t*t)
    W=3*eta*eta
    total=np.array(channel,dtype=complex)
    comparison,_=bath_projection(total)
    witness=float(sum(abs(np.linalg.eigvalsh(choi(total-comparison,4)))))
    assert 0<witness<float(2*W)+1e-12
    # The same fixed physical noise locations make all one-fault histories
    # correctable by the previously checked code. The first-two-fault tree
    # has leaves 11*,101,011, each with weight eta^2.
    # Certified asymptotic diagnostic of the much weaker global scan:
    L=512;N=L*L;k=L;e=F(1,50);m=(N-k)//2
    le=log_bounds(e,64);lp=log_bounds(1+e,64)
    scan_log_lower=k*le[0]+m*lp[0]
    classical_log_upper=log_bounds(N-k+1,64)[1]+k*le[1]
    assert scan_log_lower>580 and classical_log_upper<-1990
    def compact(x):
        scale=2**112;q=x*scale
        return F(q.numerator//q.denominator,scale)
    result={'status':'FINITE_COHERENT_PATH_RECEIVER_PASSED_GLOBAL_SCAN_TRANSFER_FAILED',
        'finite_pure_coherent_control':{'code':'[[5,1,3]]','one_shared_bath_qubit':True,
            'unitaries':'(9999 I+200 i K_j)/10001','memory_Paulis':words,
            'bath_Paulis':['Z','Z','X'],'exact_channel_Kraus_TP':True,
            'fault_norm_bound_each':str(eta),'bad_leaves':['11*','101','011'],
            'decision_weight_W':str(W),'joint_diamond_bound':str(2*W),
            'joint_diamond_bound_preview':float(2*W),
            'normalized_Choi_trace_error_to_bath_projection_preview':witness,
            'comparison_channel':'Id_L tensor Tr_L Phi(I_L/2 tensor .)',
            'no_native_dissipative_floor_required_for_this_finite_circuit':True,
            'same_information_incumbent':'ordinary local coherent-fault-path methods; no algorithmic advantage'},
        'global_scan_failure':{'eta':str(e),'linear_scale_L':L,'N':N,'k':k,
            'scan_tree_weight_lower':'eta^k * (1+eta)^floor((N-k)/2)',
            'scan_weight_log_lower_certified':str(compact(scan_log_lower)),
            'scan_weight_log_lower_preview':float(scan_log_lower),
            'classical_run_union_bound_log_upper_certified':str(-compact(-classical_log_upper)),
            'classical_run_union_bound_log_upper_preview':float(classical_log_upper),
            'receiving_norm_bound_trivial_despite_excellent_stochastic_bound':True,
            'not_a_no_go':'other trees, local cuts or cluster resummations remain possible'},
        'remaining_consequential_gap':'uniform local norm resummation for the actual asynchronous memory and a stable low-dimensional local clock',
        'new_random_draws':0,'physical_experiments':0,'independent_audit':'NOT_PERFORMED',
        'CPU_wall_seconds':time.perf_counter()-start,
        'code_SHA256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'coherent_path_control.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['CPU_wall_seconds'],
        'finite_joint_bound':float(2*W),'finite_Choi_trace_witness':witness,
        'scan_log_lower':float(scan_log_lower),'classical_log_upper':float(classical_log_upper),
        'new_random_draws':0},indent=2))


if __name__=='__main__':main()
