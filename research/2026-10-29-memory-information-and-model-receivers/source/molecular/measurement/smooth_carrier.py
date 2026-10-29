"""Full one-mode, amplitude-shaped BB1 preview on the source-generated cat.

Established composite/smooth pulse machinery, applied to the native return gap.
Numerical model only. rtol refinement is retained, no physical gate claimed.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm,svdvals
from parking_preview import model,sequence

HERE=Path(__file__).resolve().parent


def propagate(N,rate,bb1,rtol=2e-9):
    w,eta,g,D,packets,code=model(N)
    om=2*np.pi*rate
    gref=g[42]
    sy=np.array([[0,-1j],[1j,0]])
    target=np.kron(expm(1j*np.pi/4*sy),np.eye(N))@code
    state=code.reshape(2,N,2).copy()
    start=0.
    evaluations=0
    for angle,phase in sequence(np.pi/2,bb1):
        phase+=np.pi/2
        duration=2*angle/(om*gref)
        def rhs(t,flat):
            psi=flat.reshape(2,N,2)
            amp=om*np.sin(np.pi*t/duration)**2
            ep=np.exp(1j*w*np.arange(N)*(start+t))
            d0=ep[:,None]*(D@(ep.conj()[:,None]*psi[1]))
            d1=ep[:,None]*(D.conj().T@(ep.conj()[:,None]*psi[0]))
            return np.array([-1j*amp/2*np.exp(1j*phase)*d0,
                             -1j*amp/2*np.exp(-1j*phase)*d1]).reshape(-1)
        sol=solve_ivp(rhs,(0.,duration),state.reshape(-1),method='DOP853',
                      rtol=rtol,atol=rtol/20,max_step=2*np.pi/w/8)
        assert sol.success
        state=sol.y[:,-1].reshape(2,N,2)
        evaluations+=sol.nfev
        start+=duration
    actual=state.reshape(2*N,2)
    overlap=np.trace(target.conj().T@actual)
    err=svdvals(actual*np.exp(-1j*np.angle(overlap))-target)[0]
    normdef=np.linalg.norm(actual.conj().T@actual-np.eye(2),2)
    return {'N':N,'peak_rate_Hz':rate,'pulse':'smooth_BB1' if bb1 else 'smooth_bare',
      'duration_s':start,'code_error_up_to_one_global_phase':float(err),
      'code_entanglement_fidelity':float(abs(overlap/2)**2),'norm_defect':float(normdef),
      'rtol':rtol,'rhs_evaluations':evaluations,
      'extra_phase_noise_distance_T_over_2Tspin':start/(2*2.84821251e-3)}


def main():
    start=time.perf_counter()
    reports=[propagate(100,85e3,False),propagate(100,85e3,True)]
    # One changed tolerance, same scientific case; not an experimental repeat.
    reports.append(propagate(120,85e3,True,rtol=2e-10))
    out={'status':'MODEL_PREVIEW_NO_GATE_OR_MEASUREMENT_ACQUISITION','reports':reports,
      'wall_seconds':time.perf_counter()-start}
    (HERE/'SMOOTH_CARRIER.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
