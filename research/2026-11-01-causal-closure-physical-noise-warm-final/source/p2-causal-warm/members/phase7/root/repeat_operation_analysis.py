"""Retained-state schedules, exact coherent-history probes and scientific plot.

The steady histories are diagnostics of the physical pair instrument. They
are NOT logical error rates for the full noisy Bacon-Shor consumer. The
mean-energy envelope is unconditioned, not a conditional bound after rare reports.
"""
from pathlib import Path
import json
import os
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','producer-workspace/astra_phase7_matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from bracketed_parity_meter import Model, compute, envelope


def enrich(row):
    model=Model(**row['model'])
    r,a=compute(row['pre'],row['post'],row['lam'],model,500,True)
    K=a['K'];d=np.array(r['final_displacement_real'])+1j*np.array(r['final_displacement_imag'])
    histories=[]
    for label,sign in [('constant parity',1),('alternating parity',-1)]:
        v=np.linalg.solve(np.eye(2)-sign*K,d)
        beta=(a['Epre']@(sign*v))[0]
        shifted=abs(beta+r['lam'])**2
        p=(1-np.exp(-r['map_overlap_C_real']*shifted))/2
        histories.append(dict(history=label,boundary_mean_photons=float(np.vdot(v,v).real),
                              mapping_entry_amplitude_real=float(beta.real),
                              mapping_entry_amplitude_imag=float(beta.imag),
                              shifted_mapping_energy=float(shifted),
                              steady_same_parity_pZ_after_known_phase=float(p)))
    row.update(steady_coherent_history_probes=histories,
               boundary_energy_warning='Ensemble mean occupation or specified coherent histories, not every postselected branch.',
               logical_rate_warning='These pZ values are pair-coherence diagnostics, not recovered logical error.')
    return row,a


def main():
    here=Path(__file__).parent
    src=json.loads((here/'bracketed_control_comparison.json').read_text())
    selected,a=enrich(src['report_target_candidates'][1])
    family=[enrich(r)[0] for r in src['chi2_longer_lower_force_candidates']]
    fast=enrich(src['report_target_candidates'][0])[0]
    out=dict(repeated_report_candidate=selected,
             same_q_001_chi2_family=[fast]+family,
             claim='Finite receiver plus explicit consumer contract; no established total device advantage.')
    (here/'repeated_operation_results.json').write_text(json.dumps(out,indent=2)+'\n')

    # A consistent four-panel record for the q=1e-4 repeated-report candidate.
    m=Model(**selected['model']);pre,post=selected['pre'],selected['post'];T=m.mapping_time
    t=np.linspace(0,pre+T+post,2500)
    g=np.zeros_like(t);chi=np.zeros_like(t);u=np.zeros_like(t)
    p=t<=pre;z=(t>pre)&(t<pre+T);q=t>=pre+T
    g[p]=m.g*envelope(t[p],pre,m.ramp_g)
    g[q]=m.g*envelope(t[q]-pre-T,post,m.ramp_g)
    chi[z]=m.chi*envelope(t[z]-pre,T,m.ramp_chi)
    u[z]=selected['lam']*chi[z]*np.exp(-m.ka*(t[z]-pre)/2)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(2,2,figsize=(12.5,8.2),layout='constrained')
    ax[0,0].plot(t,g,label='readout coupling g(t)',lw=2)
    ax[0,0].plot(t,chi,label='dispersion χ(t)',lw=2)
    ax[0,0].plot(t,u,label='conditional force u(t)',lw=2)
    ax[0,0].set(xlabel='Time × g_max',ylabel='Rate / g_max',title='A  Finite, disjoint controls')
    ax[0,0].legend(fontsize=9,loc='upper right')
    ax[0,0].axvline(pre,color='grey',lw=.8,ls=':');ax[0,0].axvline(pre+T,color='grey',lw=.8,ls=':')
    tt=a['t'];hs=a['parity_signal'];f=a['receiver']
    # Both are imaginary in this phase convention; a fixed LO phase is enough.
    ax[0,1].plot(tt,hs.imag/np.max(abs(hs)),label='parity signal, normalized peak',lw=2)
    ax[0,1].plot(tt,f.imag/np.max(abs(f)),label='receiver weight, normalized peak',lw=2)
    ax[0,1].axhline(0,color='grey',lw=.8)
    ax[0,1].set(xlabel='Time × g_max',ylabel='Normalized amplitude',title='B  A signed observation rejects old modes')
    ax[0,1].legend(fontsize=9,loc='upper left')
    K=a['K'];d=np.array(selected['final_displacement_real'])+1j*np.array(selected['final_displacement_imag'])
    for label,alternating in [('constant parity',False),('alternating parity',True)]:
        v=np.array([10.+0j,0j]);Es=[float(np.vdot(v,v).real)]
        for k in range(1,13):
            s=(-1)**k if alternating else 1
            v=K@v+d*s;Es.append(float(np.vdot(v,v).real))
        ax[1,0].semilogy(np.arange(13),Es,'o-',ms=4,label=label)
    ax[1,0].axhline(selected['nominal_boundary_energy_bound_from_bounded_parity_history'],ls='--',color='grey',label='asymptotic mean-occupation bound')
    ax[1,0].set(xlabel='Completed meter uses',ylabel='Boundary mean photons',title='C  Reuse settles above vacuum')
    ax[1,0].legend(fontsize=9)
    rows=[fast]+family
    xx=[r['total_time'] for r in rows]
    cold=[r['thermal_cases'][0]['pZ_after_known_phase'] for r in rows]
    const=[r['steady_coherent_history_probes'][0]['steady_same_parity_pZ_after_known_phase'] for r in rows]
    alt=[r['steady_coherent_history_probes'][1]['steady_same_parity_pZ_after_known_phase'] for r in rows]
    for yy,label in [(cold,'first cold use'),(const,'constant-parity steady history'),(alt,'alternating-parity steady history')]:
        ax[1,1].plot(xx,np.array(yy)*1e4,'o-',label=label,ms=4)
    ax[1,1].set(xlabel='Operation duration × g_max',ylabel='Same-sector p_Z × 10⁴',title='D  Repeated pair probes at q = 0.001')
    ax[1,1].legend(fontsize=9)
    fig.suptitle('Finite observation with retained quantum apparatus memory',fontsize=16)
    fig.savefig(here/'bracketed_receiver_and_reuse.png',dpi=180)
    fig.savefig(here/'bracketed_receiver_and_reuse.svg')
    print('Saved repeated_operation_results.json and figure.',flush=True)


if __name__=='__main__':
    main()
