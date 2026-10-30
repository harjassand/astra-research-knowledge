"""One-shot certificates at the same chemical-accuracy target.

Corrects the cost comparison made by root-searching much tighter intervals.
Also gives the retaining incumbent the computed FCI vector for choosing P.
"""
import time
START=time.perf_counter()
import json
from pathlib import Path
import numpy as np
from scipy import linalg
from strong_audit import rayleigh_upper,safe_diag,certify_schur,residual_factor_bound,down

BASE=Path(__file__).resolve().parent
TARGET=0.00159360143764
MARGIN=0.0015


def main():
    load_start=time.perf_counter()
    data=np.load(BASE/'hamiltonian.npz');H=data['H'];addr=data['addresses']
    vfull=np.load(BASE/'reference_vector.npy').ravel()[addr]
    output={'scope':'exact matrix of saved binary64 entries with rounding model in strong_audit.py; exact-FCIDUMP bridge available separately from s05_energy_certificates','target_width_hartree':TARGET,'precommitted_trial_margin':MARGIN,'matrix_load_seconds':time.perf_counter()-load_start,'rows':[],'root_search':'none'}
    # Shared upper bound for retaining baseline variants. FCI vector cost charged.
    t=time.perf_counter();upper,detail=rayleigh_upper(H,vfull)
    output['shared_rayleigh_upper_seconds']=time.perf_counter()-t
    output['shared_rayleigh_upper']=upper
    output['rayleigh_detail']=detail
    t=time.perf_counter()
    shift=upper-MARGIN
    F=np.tril(linalg.cholesky(H-shift*np.eye(len(H)),lower=True,check_finite=False))
    delta,detail=residual_factor_bound(H,shift,F)
    lower=down(shift-delta)
    output['full_factor']=dict(lower=lower,upper=upper,width=upper-lower,wall_seconds=time.perf_counter()-t,detail=detail)
    ids=np.arange(len(H))
    # The strongest retaining baseline can choose P using its already paid vector.
    for size in [128,256,512]:
        t=time.perf_counter();p=np.argsort(np.abs(vfull))[::-1][:size];selection_seconds=time.perf_counter()-t
        q=np.setdiff1d(ids,p);A=H[np.ix_(p,p)];B=H[np.ix_(p,q)];C=H[np.ix_(q,q)]
        D=safe_diag(C,np.ones(len(C)))
        try:
            lower,detail=certify_schur(A,B,D,upper-MARGIN)
            row=dict(method='retaining_FCI_vector_top_coefficients',size=size,status='CHECKED',lower=lower,upper=upper,width=upper-lower,selection_seconds=selection_seconds,wall_seconds=time.perf_counter()-t,detail=detail)
        except (ValueError,linalg.LinAlgError) as e:
            row=dict(method='retaining_FCI_vector_top_coefficients',size=size,status='FAIL_CLOSED',reason=str(e),selection_seconds=selection_seconds,wall_seconds=time.perf_counter()-t)
        output['rows'].append(row)
    # Candidate acquires determinants from PT2/residual scores, without FCI v.
    t=time.perf_counter();P=np.argsort(np.diag(H))[:1].tolist();selection_seconds=0
    while len(P)<512:
        p=np.asarray(P);q=np.setdiff1d(ids,p)
        e,v=linalg.eigh(H[np.ix_(p,p)],subset_by_index=[0,0])
        r=H[np.ix_(q,p)]@v[:,0]
        score=r*r/np.maximum(np.diag(H)[q]-e[0],1e-8)
        P.extend(q[np.argsort(score)[::-1][:min(512-len(P),max(1,len(P)))]].tolist())
    selection_seconds=time.perf_counter()-t
    p=np.asarray(P);q=np.setdiff1d(ids,p);A=H[np.ix_(p,p)];B=H[np.ix_(p,q)];C=H[np.ix_(q,q)]
    e,v=linalg.eigh(A,subset_by_index=[0,0]);vec=np.zeros(len(H));vec[p]=v[:,0]
    upper,rd=rayleigh_upper(H,vec);D=safe_diag(C,np.ones(len(C)))
    try:
        lower,detail=certify_schur(A,B,D,upper-MARGIN)
        row=dict(method='candidate_native_PT2_selection',size=512,status='CHECKED',lower=lower,upper=upper,width=upper-lower,selection_seconds=selection_seconds,wall_seconds=time.perf_counter()-t,detail=detail,rayleigh_detail=rd)
    except (ValueError,linalg.LinAlgError) as e:
        row=dict(method='candidate_native_PT2_selection',size=512,status='FAIL_CLOSED',reason=str(e),selection_seconds=selection_seconds,wall_seconds=time.perf_counter()-t)
    output['rows'].append(row)
    output['decision']='No new comparative capability: equally informed retaining incumbent can use same one-shot Schur certificate and acquires determinants from its already computed vector. Root-search costs cannot be used as matched-target performance.'
    output['elapsed_seconds']=time.perf_counter()-START
    (BASE/'MATCHED_TARGET.json').write_text(json.dumps(output,indent=2))
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
