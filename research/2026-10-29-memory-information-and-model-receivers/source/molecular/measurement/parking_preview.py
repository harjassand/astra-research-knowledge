"""Bounded native-control preview; no physical gate qualification.

Uses published Ca+/CaOH+ model parameters and exact oscillator matrix elements.
Compares a bare carrier and established BB1 universal composite rotation.
No imported author code is executed. Full one-mode Hamiltonian is retained.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.linalg import eigh,expm,svdvals
from scipy.special import eval_genlaguerre,eval_laguerre
from scipy.constants import hbar,atomic_mass
from scipy.optimize import minimize_scalar

HERE=Path(__file__).resolve().parent


def parameters():
    mu=40/57
    wt=2*np.pi*.444e6
    w=wt*np.sqrt(1+mu-np.sqrt(1-mu+mu*mu))
    e=(-1+mu+np.sqrt(1-mu+mu*mu))/np.sqrt((-1+mu+np.sqrt(1-mu+mu*mu))**2+mu)
    eta=2*np.pi/729.15e-9*np.sqrt(hbar/(2*40*atomic_mass*w))*e
    return w,eta


def model(N=120):
    w,eta=parameters()
    n=np.arange(N)
    a=np.diag(np.sqrt(np.arange(1,N)),1)
    ev,V=eigh(a+a.T)
    displacement=(V*np.exp(1j*eta*ev))@V.T
    g=np.exp(-eta*eta/2)*eval_laguerre(n,eta*eta)
    # Same finite, beyond-LD sideband model used in the published notebook.
    coupling=np.exp(-eta*eta/2)/np.sqrt(n[:-1]+1)*eval_genlaguerre(n[:-1],1,eta*eta)
    ad=np.diag(coupling,-1)
    p=1j*(ad-ad.T)
    ep,P=eigh(p)
    strength=(2*np.pi*.145e6)*eta*175e-6/2
    seed=np.zeros(N,dtype=complex);seed[0]=1
    packets=[P@(np.exp(-1j*sign*strength*ep)*(P.conj().T@seed)) for sign in (1,-1)]
    plus=np.array([1,1])/np.sqrt(2);minus=np.array([1,-1])/np.sqrt(2)
    code=np.column_stack([np.kron(plus,packets[0]),np.kron(minus,packets[1])])
    return w,eta,g,displacement,packets,code


def sequence(theta,bb1):
    if not bb1:return [(theta,0.)]
    phi=np.arccos(-theta/(4*np.pi))
    return [(theta/2,0.),(np.pi,phi),(2*np.pi,3*phi),(np.pi,phi),(theta/2,0.)]


def main():
    start=time.perf_counter()
    N=120
    w,eta,g,D,packets,code=model(N)
    sy=np.array([[0,-1j],[1j,0]])
    sx=np.array([[0,1],[1,0]])
    sp=np.array([[0,1],[0,0]])
    target=np.kron(expm(-1j*np.pi/4*sy),np.eye(N))@code
    gref=g[42]
    reports=[]
    for rate in (85e3,20e3):
        om=2*np.pi*rate
        H=np.kron(np.eye(2),np.diag(w*np.arange(N)))+om/2*(np.kron(sp,D)+np.kron(sp.T,D.conj().T))
        E,V=eigh(H)
        for bb1 in (False,True):
            seq=sequence(np.pi/2,bb1)
            state=code.copy();time_total=0.
            rwa=code.reshape(2,N,2).copy()
            for angle,phase in seq:
                phase+=np.pi/2
                duration=angle/(om*gref)
                # U_phi = spin-Z conjugation of full constant-amplitude U_0.
                z=np.exp(1j*phase/2*np.array([1,-1]))
                diag=np.repeat(z,N)
                state=diag[:,None]*(V@(np.exp(-1j*E*duration)[:,None]*(V.conj().T@(diag.conj()[:,None]*state))))
                for j in range(N):
                    axis=np.cos(phase)*sx-np.sin(phase)*sy
                    # Full Hamiltonian uses upper-right exp(+i phi).
                    rwa[:,j,:]=expm(-1j*angle*g[j]/gref/2*axis)@rwa[:,j,:]
                time_total+=duration
            # The sign convention above makes phase+pi/2 a -Y rotation.
            target_now=np.kron(expm(+1j*np.pi/4*sy),np.eye(N))@code
            interaction=np.tile(np.exp(1j*w*np.arange(N)*time_total),2)[:,None]*state
            entries={}
            for name,actual in [('carrier_RWA',rwa.reshape(2*N,2)),('full_one_mode',interaction)]:
                overlap=np.trace(target_now.conj().T@actual)
                phase=np.angle(overlap)
                error=svdvals(np.exp(-1j*phase)*actual-target_now)[0]
                entries[name]={'code_error_up_to_one_global_phase':float(error),'code_entanglement_fidelity':float(abs(overlap/2)**2)}
                if name=='full_one_mode':
                    def corrected(beta):
                        return np.tile(np.exp(1j*beta*np.arange(N)),2)[:,None]*actual
                    fit=minimize_scalar(lambda beta:-abs(np.trace(target_now.conj().T@corrected(beta)))**2,
                                        bounds=(-.03,.03),method='bounded',options={'xatol':1e-13})
                    corr=corrected(fit.x)
                    overlap_corr=np.trace(target_now.conj().T@corr)
                    phase_corr=np.angle(overlap_corr)
                    entries['full_one_mode_with_common_rotation']={
                      'beta':float(fit.x),'positive_wait_s_mod_one_period':float((-fit.x)%(2*np.pi)/w),
                      'code_error_up_to_one_global_phase':float(svdvals(np.exp(-1j*phase_corr)*corr-target_now)[0]),
                      'code_entanglement_fidelity':float(abs(overlap_corr/2)**2)}
            reports.append({'rate_Hz':rate,'pulse':'BB1' if bb1 else 'bare','segments':len(seq),
              'duration_s':time_total,'phase_area_sequence':[[float(a),float(p+np.pi/2)] for a,p in seq],
              'extra_phase_noise_distance_bound_T_over_2Tspin':time_total/(2*2.84821251e-3),**entries})
    out={'status':'MODEL_PREVIEW_NOT_GATE_QUALIFICATION','N':N,'eta':eta,'mode_Hz':w/(2*np.pi),
      'native_repo':'b083acdaa181549ca591d76d86c283da013ed651','reference_g42':gref,
      'g0':g[0],'g119':g[-1],'packet_top10_population':float(np.sum(abs(packets[0][-10:])**2)),
      'packet_mean_n':float(np.sum(np.arange(N)*abs(packets[0])**2)),
      'reports':reports,'wall_seconds':time.perf_counter()-start,
      'access_unpaid':['spectator modes','full three-level parking and return','measured pulse phase/noise and Zeeman leakage','molecular coherence/IR delivery','joint science transfer and complete cost']}
    (HERE/'PARKING_PREVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
