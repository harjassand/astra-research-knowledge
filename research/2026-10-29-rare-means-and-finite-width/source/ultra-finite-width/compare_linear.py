"""Same-source exact two-particle LINEAR response (strong primary baseline).

The unilateral vacuum-to-pair block generates the Duhamel first derivative
in epsilon exactly; number-preserving Hc in the two-particle sector is kept
to all orders in U and J. No spectral gap or zero-eigenvalue division.
"""
import hashlib
import json
import time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from native import compile_hubbard,evolve,numerical_bound,exp_upper,fraction_record,quantities

HERE=Path(__file__).resolve().parent


def main():
    H,pairs,ms,off,r=compile_hubbard(4,4,1)
    # Delete only the source's pair-to-vacuum feedback. The triangular
    # evolution is the exact first-order response, not a cutoff solution.
    H=H.tolil()
    for src,dst in pairs:
        for x,y in zip(src,dst):H[x,y]=0
    H=H.tocsr();H.eliminate_zeros()
    r['integer_row_norm']=max(int(np.max(np.asarray(abs(H).sum(axis=1)))),
                              int(np.max(np.asarray(abs(H).sum(axis=0)))))
    r['max_row_nonzeros']=max(int(np.max(np.diff(H.indptr))),
                              int(np.max(np.diff(H.tocsc().indptr))))
    nb=numerical_bound(r,F(10),60,36)
    # Logarithmic norm of -i G is epsilon/2. Unlike a Hermitian
    # propagator, its norm is <=exp(epsilon*t/2). Charge both input
    # and error propagation by exp(z/2); exp(z) is a safe product.
    correction=exp_upper(F(1,2))
    for k in ['state','reduction','observable']:nb[k]*=correction
    vec,sec=evolve(H)
    obs=quantities(vec,pairs,ms,off)
    prediction=json.loads((HERE/'PREDICTION.json').read_text())
    target=prediction['observables']['density_excess_at_source']
    err=prediction['qualification']['density_total_error_upper']['upper_float']
    linear=obs['density_excess_at_source']
    # Reductions on the nonnormalized first-order vector need its norm^2.
    linerr=float(nb['observable'])*float(exp_upper(F(1,2)))
    out=dict(source='SAME 4x4 open Hubbard U8,J1,epsilon1/20,t10,eta-coherent theta pi/2',
             exact_operation='two-particle first-order source response with all U/J dynamics retained',
             dimension=r['dimension'],matrix_nnz=int(H.nnz),compile_seconds=r['compile_seconds'],
             propagation_seconds=sec,integer_matvecs=2160,
             linear_density_excess=linear,linear_numerical_error_upper=linerr,
             nonlinear_density_excess=target,nonlinear_total_error_upper=err,
             difference_nonlinear_minus_linear=target-linear,
             separated_by_at_least=abs(target-linear)-err-linerr,
             linear_eta_y=obs['eta_y_at_source'],
             same_information_ordinary_comparator='Yang eta symmetry + bounded-source Dyson/Fock cutoff reproduces our nonlinear operation exactly; no superiority over that comparator is established',
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'LINEAR_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
