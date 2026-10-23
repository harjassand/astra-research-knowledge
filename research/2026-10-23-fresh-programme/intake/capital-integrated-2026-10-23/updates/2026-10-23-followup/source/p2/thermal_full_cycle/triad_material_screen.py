"""Conditional pump-normalized three-mode material screen, NOT a device.

The exact two-mode Hcrit theorem is not applied to the cascade. This file
directly optimizes its covariance under a separately stated homogeneous-
normalization scenario, with all infrared absorption rates tied to alpha.
Unknown upper-band losses are assigned favorable reference values; the
prescribed overlap graph is not claimed to solve a Maxwell boundary problem.
"""
from pathlib import Path
import json
import numpy as np
from scipy.constants import c,hbar,k,epsilon_0,pi
from scipy.linalg import solve_continuous_lyapunov
from scipy.optimize import differential_evolution,minimize

OUT=Path(__file__).resolve().parent
FC=c/10.6e-6;FP=c/110e-6
OMEGA=2*pi*np.array([FC,FC+FP,FC+2*FP])
WP=2*pi*FP; NIR=3.28;NPUMP=3.61;D=NIR**2
CHI=100e-12;ALPHA=.006*100;ALPHA_P=2*100
X=c*ALPHA/NIR
V=(10.6e-6/NIR)**3
EP_IM=NPUMP*c*ALPHA_P/WP
NC=1/np.expm1(hbar*OMEGA/(k*300))
NH=1/np.expm1(hbar*OMEGA/(k*315))


def evaluate(logvars,triad=True,overlap=2/pi):
    # g_target/X=y, cold external contact A/X=a;
    # upper total hot linewidths/X=1+e1,1+e2. Unit floor is assigned material
    # absorption alpha_h=alpha_u=alpha_c (UNKNOWN in actual target bands).
    y,a,e1,e2=np.exp(logvars)
    dim=3 if triad else 2
    linewidths=np.array([1+a,1+e1,1+e2])[:dim]
    h=np.zeros((dim,dim),complex)
    h[0,1]=h[1,0]=y
    if triad:h[1,2]=h[2,1]=y*np.sqrt(OMEGA[2]/OMEGA[0])
    diffusion=linewidths*NH[:dim]
    diffusion[0]=NH[0]+a*NC[0]
    drift=-np.diag(linewidths/2)-1j*h
    cov=solve_continuous_lyapunov(drift,-np.diag(diffusion))
    cold=hbar*OMEGA[0]*X*a*(NC[0]-cov[0,0].real)
    hot=hbar*X*np.sum(OMEGA[:dim]*(NH[:dim]-cov.diagonal().real)
        *np.array([1.,1+e1,1+e2])[:dim])
    current01=-2*np.imag(y*cov[1,0])*X
    current12=-2*np.imag(h[1,2]*cov[2,1])*X if triad else 0.
    work=hbar*WP*(current01+current12)
    field2=4*D*D*(X*y)**2/(overlap**2*CHI**2*OMEGA[0]*OMEGA[1])
    absorbed=.5*epsilon_0*WP*EP_IM*V*field2
    return dict(y=float(y),A_over_x=float(a),B1_over_x=float(1+e1),B2_over_x=float(1+e2),
        E_peak_V_per_m=float(np.sqrt(field2)),Qc_W=float(cold),Qh_W=float(hot),
        W_conversion_W=float(work),P_pump_abs_W=float(absorbed),
        Qc_over_Pabs=float(cold/absorbed),
        wall_COP_before_other_losses=float(cold/(work+absorbed)),
        energy_closure_W=float(abs(cold+hot+work)))


def optimize(triad,overlap):
    # Declared finite search, followed by local refinement. Not a global
    # theorem over Maxwell designs or an unbounded contact space.
    bounds=[(-6,8),(-8,10),(-12,10),(-12,10)]
    def cost(z):return -evaluate(z,triad,overlap)['Qc_over_Pabs']*1e10
    de=differential_evolution(cost,bounds,seed=23102026,popsize=16,maxiter=300,
                             tol=1e-10,polish=False,workers=1)
    local=minimize(cost,de.x,method='Nelder-Mead',
        options={'xatol':1e-9,'fatol':1e-11,'maxiter':3000})
    chosen=local.x if local.fun<de.fun else de.x
    # Keep the finite search claim honest: do not silently use a refinement
    # outside the advertised domain.
    if any(z<lo or z>hi for z,(lo,hi) in zip(chosen,bounds)):chosen=de.x
    result=evaluate(chosen,triad,overlap)
    result.update(triad=triad,assumed_overlap=overlap,search_log_bounds=bounds,
        differential_evolution_success=bool(de.success),
        objective_evaluations=int(de.nfev+local.nfev),
        local_refinement_success=bool(local.success))
    return result


def main():
    rows=[optimize(False,1.),optimize(False,2/pi),optimize(True,2/pi)]
    assert max(r['energy_closure_W'] for r in rows)<1e-22
    result=dict(status='CONDITIONAL_MULTIMODE_MATERIAL_SCREEN_NOT_MEASURED_PERFORMANCE',
        actual_upper_band_loss='UNKNOWN',actual_Maxwell_overlap_graph='UNKNOWN',
        rationale='The two-mode analytic bound is not automatically a bound on an upper cascade; compute the cascade directly.',
        assumptions=['Same reference chi, infrared indices and cold/pump absorption as the mixed-source scenario.',
            'Upper and next-upper infrared intensity absorption both ASSUMED equal to alpha_c=0.006 cm^-1.',
            'Prescribed cold-upper-next-upper graph; no lower sideband, domain loss or pump nonthermal noise.',
            'Hot bath at 315 K, cold contact at 300 K, all absorption heat deposited hot.',
            'Uniform favorable mode normalization, per-pair pumped volume (10.6um/3.28)^3.',
            'A and upper external linewidths tunable independently within finite stated search; material linewidth floor retained.',
            'Actual vector fields, cavity frequencies and tensor response must be solved jointly; this is not such a solution.'],
        frequencies_THz=(OMEGA/(2*pi*1e12)).tolist(),pump_THz=FP/1e12,
        intrinsic_infrared_energy_linewidth_per_s=X,volume_m3=V,
        results=rows)
    (OUT/'triad_material_screen_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
