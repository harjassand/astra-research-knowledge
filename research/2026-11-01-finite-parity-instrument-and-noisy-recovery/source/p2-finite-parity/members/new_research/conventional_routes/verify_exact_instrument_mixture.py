"""Check the CP good/bad mixture on the actual optimized 4x4 outcome Grams.

This targets the full finite-strength instrument, including the nonzero
auxiliary K phase; no two-dimensional-only or single-coherence surrogate.
"""
from pathlib import Path
import sys
import json
import numpy as np
from scipy.special import ndtr

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'root'
sys.path.insert(0,str(ROOT))
from finite_mediator_parity import instrument_gram


def main():
    source=json.loads((ROOT/'optimized_cnot_results.json').read_text())
    r=source['integrals'];m=r['model'];N=r['N']
    q=float(ndtr(-2*np.sqrt(m['eta']*N)))
    gamma=float(np.exp(-2*N)/2)
    pZ=float(-np.expm1(-2*(m['kb']+m['kc'])*r['IB'])/2)
    e=q+gamma*gamma/q;p=1-e;good=p*(1-pZ);bad=1-good
    z1=np.array([1.,1.,-1.,-1.]);z2=np.array([1.,-1.,1.,-1.]);S=z1*z2
    aux_parity=m['kb']*r['IU']+m['kc']*r['IV']
    aux_local=(m['kb']+m['kc'])*r['IB']
    H=np.exp(-aux_parity*(S[:,None]-S[None,:])**2/2
             -aux_local*(z2[:,None]-z2[None,:])**2/2
             +1j*r['K']*((z1[:,None]-z1[None,:])
                         +S[:,None]*z2[None,:]-S[None,:]*z2[:,None]))
    rows=[];total_residual_diagonal=np.zeros(4,complex)
    for report in (1,-1):
        G=instrument_gram(r,report)
        mask=(S==report).astype(float)
        ideal=np.outer(mask,mask)
        residual=G-good*ideal
        total_residual_diagonal+=np.diag(residual)
        kbad=np.where(S==report,gamma/np.sqrt(q),np.sqrt(q))
        phase_error_vector=z2*mask
        predicted=good*ideal+p*pZ*np.outer(phase_error_vector,phase_error_vector)+H*np.outer(kbad,kbad)
        rows.append({'report':report,
                     'full_gram_min_eigenvalue':float(np.linalg.eigvalsh(G).min()),
                     'residual_eigenvalues':np.linalg.eigvalsh(residual).tolist(),
                     'normalized_bad_gram_min_eigenvalue':float(np.linalg.eigvalsh(residual/bad).min()),
                     'explicit_mixture_reconstruction_max_error':float(np.max(abs(G-predicted))),
                     'residual_hermiticity_error':float(np.max(abs(residual-residual.conj().T)))})
    out={'scope':'Actual optimized physical 4x4 outcome Grams, with all auxiliary phases.',
         'N':N,'q':q,'gamma':gamma,'pZ':pZ,'auxiliary_K':r['K'],
         'main_bad_weight':e,'ideal_good_weight':good,'full_bad_weight':bad,
         'auxiliary_channel_min_eigenvalue':float(np.linalg.eigvalsh(H).min()),
         'residual_effect_diagonal':total_residual_diagonal.real.tolist(),
         'state_independent_bad_weight_max_error':float(np.max(abs(total_residual_diagonal-bad))),
         'outcomes':rows}
    (HERE/'exact_instrument_mixture_check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
