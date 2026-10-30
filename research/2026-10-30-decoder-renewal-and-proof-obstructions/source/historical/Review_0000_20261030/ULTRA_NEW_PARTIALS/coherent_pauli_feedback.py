"""Literal coherent Pauli-sector feedback; exact rational all-r moment state.

Two physical N queries, one after coupling an already encoded payload.
The proposed final CPTP decoder is found numerically, then RATIONALLY
REPAIRED; positivity/trace normalization/fidelity are checked exactly.
This is circuit algebra and controller acquisition, NOT a quantum run.
"""

from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import argparse,hashlib,json,time
import numpy as np
import cvxpy as cp
from relative_swap_feedback import PERMS,compose,inverse,cycle,pmove


def vectors():
    # E=(I,X,Z,-iY), refs(T,E); logical(payload,input1,input2=oldref1).
    vv=[]
    for aa,bb in ((F(11,14),F(5,14)),(F(1,97),F(56,97))):
        assert aa*aa+3*bb*bb==1
        v=np.empty((8,8),dtype=object);v[:]=F(0)
        for T in range(2):
            for oldref in range(2):
                for E in range(4):
                    amp=aa if E==3 else bb
                    out=oldref if E in(0,2) else 1-oldref
                    sg=-1 if E in(2,3) and oldref else 1
                    v[4*T+E,4*T+2*oldref+out]+=sg*amp/2
        vv.append(v)
    a=(vv[0]+vv[1])/2;d=(vv[0]-vv[1])/2
    b=np.empty_like(a);b[:]=F(0)
    for i in range(8):
        for j in range(8):b[i,pmove(j,(1,0,2))]=d[i,j]
    return a,b


def exact_state_coefficients():
    v=vectors();mom={};flip=(1,0,2)
    for pi in PERMS:
        m=[[[F(0) for _ in range(8)] for _ in range(8)] for _ in range(3)]
        for s in range(2):
            for t in range(2):
                power=3-cycle(compose(flip,pi) if s!=t else pi)
                for i in range(8):
                    for j in range(8):
                        m[power][i][j]+=sum(v[s][i,l]*v[t][j,pmove(l,pi)] for l in range(8))
        mom[pi]=m
    z=[[[F(0) for _ in range(48)] for _ in range(48)] for _ in range(3)]
    for pi in PERMS:
        inv=inverse(pi);m=mom[pi]
        for h,g in enumerate(PERMS):
            gh=PERMS.index(compose(inv,g))
            for power in range(3):
                for i in range(8):
                    for j in range(8):z[power][6*i+gh][6*j+h]+=m[power][i][j]/6
    assert [sum(zz[i][i] for i in range(48)) for zz in z]==[1,0,0]
    for power,zz in enumerate(z):
        for a in range(2):
            for b in range(2):
                assert sum(zz[24*a+i][24*b+i] for i in range(24))==(F(a==b,2) if power==0 else 0)
    return z


def exact_state(r):
    coeff=exact_state_coefficients()
    z=[[sum(coeff[h][i][j]/r**h for h in range(3)) for j in range(48)] for i in range(48)]
    assert all(z[i][j]==z[j][i] for i in range(48) for j in range(48))
    assert sum(z[i][i] for i in range(48))==1
    target=[[z[24*b+j][24*a+i]/2 for j in range(24) for b in range(2)]
            for i in range(24) for a in range(2)]
    return z,target


def strict_ldl(a):
    n=len(a);L=[[F(0)]*n for _ in range(n)];diag=[]
    for j in range(n):
        L[j][j]=F(1)
        d=a[j][j]-sum(L[j][h]**2*diag[h] for h in range(j))
        if d<=0:raise ValueError(('not strictly positive',j,str(d)))
        diag.append(d)
        for i in range(j+1,n):
            L[i][j]=(a[i][j]-sum(L[i][h]*L[j][h]*diag[h] for h in range(j)))/d
    return min(diag)


def repair(raw,target,bits=28,noise=F(1,1<<18)):
    n=48;den=1<<bits
    z=[[F(round(float((raw[i,j]+raw[j,i])/2)*den),den)+(noise if i==j else 0)
        for j in range(n)] for i in range(n)]
    pivot=strict_ldl(z)
    tr=[[z[2*i][2*j]+z[2*i+1][2*j+1] for j in range(24)] for i in range(24)]
    err=max(sum(abs(tr[i][j]-int(i==j)) for j in range(24)) for i in range(24))
    scale=1+err
    z=[[x/scale for x in row] for row in z]
    # Known |0><0| fallback completes the trace deficit, PSD by row norm.
    residual=[[int(i==j)-tr[i][j]/scale for j in range(24)] for i in range(24)]
    assert all(residual[i][i]>=sum(abs(residual[i][j]) for j in range(24) if j!=i) for i in range(24))
    for i in range(24):
        for j in range(24):z[2*i][2*j]+=residual[i][j]
    assert all(z[2*i][2*j]+z[2*i+1][2*j+1]==int(i==j) for i in range(24) for j in range(24))
    value=sum(z[i][j]*target[j][i] for i in range(n) for j in range(n))
    return z,value,{'dyadic_rounding_bits':bits,'positive_noise_added':str(noise),
                    'strict_LDL_pivots_all_positive':True,'minimum_pivot':str(pivot),
                    'partial_trace_row_norm_error':str(err),'normalizing_scale':str(scale),
                    'fallback_trace_deficit_PSD_by_diagonal_dominance':True,
                    'all_576_trace_preserving_entries_exact':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--r',type=int,default=2)
    a=ap.parse_args();assert a.r>=1;start=time.perf_counter()
    state,target=exact_state(a.r);objective=np.array(target,dtype=float)
    C=cp.Variable((48,48),symmetric=True)
    problem=cp.Problem(cp.Maximize(cp.trace(C@objective)),[C>>0,C[0::2,0::2]+C[1::2,1::2]==np.eye(24)])
    result=problem.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,tol_feas=1e-10,max_iter=150)
    repaired,value,receipt=repair(C.value,target)
    base=Path(__file__).parent
    certificate={'r':a.r,'input_dimension':24,'output_dimension':2,
                 'repaired_CPTP_Choi':[[str(v) for v in row] for row in repaired]}
    (base/'COHERENT_FEEDBACK_DECODER.json').write_text(json.dumps(certificate,indent=2)+'\n')
    out={'scope':'exact two-query coherent Pauli feedback circuit and rational CPTP final-decoder certificate; no quantum/source run',
         'r':a.r,'coherent_Kraus_amplitudes':{'physical_symmetric':{'Y':'11/14','I_X_Z_each':'5/14'},'physical_antisymmetric':{'Y':'1/97','I_X_Z_each':'56/97'}},
         'Y_label_operator':'-i*Y, real matrix [[0,-1],[1,0]]; relative phase is part of the coherent controller',
         'transpose_depolarizing_coefficients':{'physical_symmetric':str(4*F(5,14)**2-1),'physical_antisymmetric':str(4*F(56,97)**2-1)},
         'required_new_forward_source_calls':2,'online_source_calls_after_unknown_payload':1,
         'actual_source_or_circuit_calls':0,'final_decoder_input_dimension':24,
         'physical_branch_not_classically_measured':True,'Kraus_index_retained_coherently':True,
         'no_unknown_inverse_controlled_source_or_environment':True,
         'floating_discovery_optimum':float(result),'solver_status':problem.status,
         'qualified_feasible_Bell_fidelity':str(value),'qualified_feasible_Bell_fidelity_decimal':float(value),
         'physical_Pauli_twirl_halfdiamond_upper':str(1-value),
         'physical_Pauli_twirl_halfdiamond_upper_decimal':float(1-value),
         'Pauli_twirl_seed':'two internal fair bits, discarded after final correction; fresh for each payload',
         'rational_CPTP_repair':receipt,'seconds_after_imports':time.perf_counter()-start}
    (base/'COHERENT_FEEDBACK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rational_CPTP_repair'},indent=2))


if __name__=='__main__':main()
