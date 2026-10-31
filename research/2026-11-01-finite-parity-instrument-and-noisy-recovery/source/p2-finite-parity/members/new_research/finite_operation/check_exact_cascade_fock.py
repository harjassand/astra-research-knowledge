"""Independent finite-Fock Lindblad check of the exact cascade derivation.

This deliberately uses weak pulses so convergence is cheap. It is a check of
signs, phases, cascade Hamiltonian, all six logical coherences and bypass/loss
terms, not a hardware validation or a truncation certificate at high power.
"""
from pathlib import Path
from dataclasses import asdict
import json
import itertools
import numpy as np
from scipy.integrate import solve_ivp
from exact_cascade_parity import Model, solve, waveforms, Z1, Z2, S


def annihilator(n):
    return np.diag(np.sqrt(np.arange(1,n)),1).astype(complex)


def fock_check(ncut, model):
    n=ncut*ncut
    b=np.kron(annihilator(ncut),np.eye(ncut))
    c=np.kron(np.eye(ncut),annihilator(ncut))
    Xb=b+b.conj().T; Xc=c+c.conj().T
    nc=c.conj().T@c
    Hcas=0.5j*np.sqrt(model.ke*model.kc)*(b.conj().T@c-c.conj().T@b)
    Ls=[np.sqrt(model.ke)*b+np.sqrt(model.kc)*c,
        np.sqrt(model.kb)*b,np.sqrt(model.ki)*c]
    G=sum(L.conj().T@L for L in Ls)
    Hfixed=[Hcas+q*model.chi*nc for q in Z1]
    rho0=np.zeros((n,n),complex);rho0[0,0]=1
    r,_,_=solve(model)
    N=r['target_photons_N'];NB=r['source_output_photons_NB'];C=r['AB_integral_C']
    ri2=model.ki/model.kc;rb2=model.kb/model.ke;phi=r['dynamical_local_z1_phase']
    outputs=[]
    for i,j in [(0,0)]+list(itertools.combinations(range(4),2)):
        def rhs(t,flat):
            rho=flat.reshape(n,n)
            f=waveforms(model,t)
            Hdrive=f['u']*Xb+f['w']*Xc
            Hl=Hfixed[i]+Z2[i]*Hdrive
            Hr=Hfixed[j]+Z2[j]*Hdrive
            dr=-1j*(Hl@rho-rho@Hr)-0.5*(G@rho+rho@G)
            for L in Ls:
                dr+=L@rho@L.conj().T
            return dr.ravel()
        sol=solve_ivp(rhs,[0,model.T],rho0.ravel(),method='DOP853',rtol=3e-11,atol=1e-12)
        final=sol.y[:,-1].reshape(n,n)
        actual=np.trace(final)
        expo=-0.5*((1+ri2)*(S[i]-S[j])**2*N+(ri2+rb2)*(Z2[i]-Z2[j])**2*NB)
        expo+=1j*(phi*(Z1[i]-Z1[j])+ri2*C*(S[i]*Z2[j]-S[j]*Z2[i]))
        expected=np.exp(expo)
        outputs.append({'i':i,'j':j,'fock_trace':[actual.real,actual.imag],
                        'analytic_trace':[expected.real,expected.imag],
                        'abs_error':float(abs(actual-expected)),
                        'final_nonvacuum_weight_diagonal':float(1-final[0,0].real) if i==j else None,
                        'solver_success':bool(sol.success),'nfev':sol.nfev})
    return {'model':asdict(model),'cutoff_per_mode':ncut,'comparisons':outputs,
            'maximum_coherence_error':max(v['abs_error'] for v in outputs)}


if __name__=='__main__':
    all_results=[]
    for loss in (0.0,0.02):
        m=Model(T=4,kc=5,chi=2.5,kb=loss,ki=5*loss,photons=0.02)
        for ncut in (3,4,5):
            r=fock_check(ncut,m)
            all_results.append(r)
            print('loss',loss,'cut',ncut,'max_error',r['maximum_coherence_error'],flush=True)
    Path(__file__).with_name('exact_cascade_fock_check.json').write_text(json.dumps(all_results,indent=2))
