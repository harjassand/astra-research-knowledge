"""Exact resonant lower-sideband counterexample for a three-mode converter.

All results are synthetic model calculations. Lab Hamiltonian is explicitly
periodic and number conserving; its rotating-frame covariance is constant.
No actual lower-sideband coupling or device spectrum has been measured.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import solve_continuous_lyapunov
from scipy.optimize import brentq

HBAR=1.054571817e-34; KB=1.380649e-23


def solve(gplus,gminus,kappa=.005,x=0.,absorbed_cold=0.):
    # Frequencies in omega_c units: hot-lower, cold, hot-upper.
    w=np.array([.8,1.,1.2])
    wphys=w*2*np.pi*20e12
    temps=np.array([300.,330.])
    n=1/np.expm1(HBAR*wphys[:,None]/(KB*temps[None,:]))
    rates=kappa*np.array([[0,1],[1,x],[0,1]])
    ktot=rates.sum(axis=1)
    h=np.array([[0,gminus,0],[gminus,0,gplus],[0,gplus,0.]])
    drift=-np.diag(ktot/2)-1j*h
    diffusion=np.diag((rates*n).sum(axis=1))
    N=solve_continuous_lyapunov(drift,-diffusion)
    pop=N.diagonal().real
    heat=(w[:,None]*rates*(n-pop[:,None])).sum(axis=0)
    jl=2*gminus*N[1,0].imag
    jh=2*gplus*N[1,2].imag
    power=.2*(jh-jl)
    nc=n[1,0];nb=(n[1,0]+x*n[1,1])/(1+x)
    G2=gplus*gplus+gminus*gminus
    nbright=(gplus*gplus*n[2,1]+gminus*gminus*n[0,1])/G2
    C=4*G2/(kappa*ktot[1])
    I=ktot[1]*kappa/(ktot[1]+kappa)*C/(1+C)*(nb-nbright)
    pcenter=nb-I/ktot[1]
    qclosed=kappa*(nc-pcenter)
    return dict(gplus=gplus,gminus=gminus,lower_to_upper_coupling_ratio=gminus/gplus,
                cross_bath_fraction_x=x,occupations=n.tolist(),populations=pop.tolist(),
                cold_heat=float(heat[0]),hot_heat=float(heat[1]),
                net_cold_heat=float(heat[0]-absorbed_cold),drive_work=float(power),
                center_to_lower_current=float(jl),center_to_upper_current=float(jh),
                covariance_residual=float(np.max(abs(drift@N+N@drift.conj().T+diffusion))),
                bright_mode_formula_error=float(abs(heat[0]-qclosed)),
                energy_balance_error=float(abs(sum(heat)+power)),
                minimum_covariance_eigenvalue=float(np.linalg.eigvalsh(N).min()),
                maximum_drift_real_eigenvalue=float(np.linalg.eigvals(drift).real.max()),
                entropy_production_normalized=float(-heat[0]/300-heat[1]/330))


def main():
    k=.005;gp=k/2
    results={'status':'EXACT_THREE_MODE_MODEL_ONLY_NO_MEASUREMENT',
             'equal_contact_examples':[solve(gp,gp*r) for r in [0.,.2,.4,.4106408212047883,.5,1.]]}
    n=np.array(results['equal_contact_examples'][0]['occupations'])
    threshold=np.sqrt((n[1,0]-n[2,1])/(n[0,1]-n[1,0]))
    results['closed_form_threshold_coupling_ratio']=float(threshold)
    # Frozen private input, so root can evolve its model independently.
    decl=json.loads(Path(__file__).with_name('root_synthetic_input.json').read_text())['synthetic']
    q0=k/2*decl['delta0']
    rows=[]
    for pt in decl['remote_hot_converter']['cases']:
        if not pt['operating']: continue
        x,z=pt['x'],pt['z'];gp=k*np.sqrt(x*z)/2
        coldabs=pt['cold_loss_per_z']*z*q0
        fn=lambda r:solve(gp,r*gp,k,x,coldabs)['net_cold_heat']
        crit=brentq(fn,0,2,xtol=1e-13)
        nbar=(n[1,0]+x*n[1,1])/(1+x)
        Cplus=4*gp*gp/(k*k*(1+x))
        Dcoef=k/(2+x)
        leak=k*x/(1+x)*(n[1,1]-n[1,0])
        L=leak+coldabs
        y=(Dcoef*Cplus*(nbar-n[2,1])-L*(1+Cplus))/(Cplus*(Dcoef*(n[0,1]-nbar)+L))
        rows.append(dict(loss_fraction_of_max=pt['loss_fraction_of_max'],
                         rwa_net_Q_over_Q0=pt['net_Q_over_Q0'],
                         lower_to_upper_g_threshold=float(crit),
                         threshold_formula=float(np.sqrt(y)),
                         Q_over_Q0_at_half_lower_coupling=float(fn(.5)/q0),
                         Q_over_Q0_at_0_1_lower_coupling=float(fn(.1)/q0),
                         covariance_example=solve(gp,gp*.5,k,x,coldabs)))
    results['root_remote_operating_points']=rows
    p=Path(__file__).with_name('sideband_results.json')
    p.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(dict(threshold=threshold,equal_contact_examples=results['equal_contact_examples'],
         root_remote_operating_points=[{k:v for k,v in r.items() if k!='covariance_example'} for r in rows]),indent=2))


if __name__=='__main__':main()
