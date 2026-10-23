"""Audit omitted upper-mode work for the finite-band scalar control.

This is a mathematical consistency check of the already declared synthetic
ladder, not an extension of a material transparency band or a physical RWA
certificate at arbitrarily high frequencies. Pair creation must be nulled.
"""
from pathlib import Path
import json
import time
import numpy as np
from scipy.linalg import eigh
from patterned_converter import (edge_overlaps, pair_overlaps, occupation,
    primitive, M_COLD, R_PUMP, FSR_THz, TC, TH)

OUT=Path(__file__).resolve().parent


def passive_solution(amplitude,nmax,edges,profile):
    """Uniform population damping=1, no vacuum subtraction, eigensystem solve.

    In the Hamiltonian eigenbasis the covariance is D_ab/[1+i(lambda_a-
    lambda_b)]. This independently checks the quadrature Lyapunov solver.
    """
    assert np.max(np.abs(pair_overlaps('pattern',(edges,profile))))<1e-12
    r=R_PUMP;m=M_COLD
    js=np.arange(1,nmax+1)
    temperatures=np.full(nmax,TH);temperatures[m-1]=TC
    nb=occupation(js*FSR_THz,temperatures)
    overlaps=edge_overlaps(nmax,'pattern',(edges,profile))
    gs=amplitude/2*overlaps/(np.pi/4)*np.sqrt(js[:-r]*(js[:-r]+r)/(m*(m+r)))
    gs[np.abs(overlaps)<1e-13]=0.
    h=np.diag(gs,k=r)+np.diag(gs,k=-r)
    lam,U=eigh(h)
    D=U.T@(nb[:,None]*U)
    Ctilde=D/(1+1j*(lam[:,None]-lam[None,:]))
    C=U@Ctilde@U.T
    heat=js/m*(nb-C.diagonal().real)
    currents=-2*gs*np.imag(C[np.arange(r,nmax),np.arange(nmax-r)])
    q0=(occupation(m*FSR_THz,TC)-occupation((m+r)*FSR_THz,TH))/2
    work=r/m*currents.sum()/q0
    cold=heat[m-1]/q0
    net=cold-.05*amplitude**2-.02
    absorption=.5*amplitude**2
    return dict(amplitude=float(amplitude),nmax=int(nmax),
        gross_cold_heat_over_Q0=float(cold),net_cold_heat_over_Q0=float(net),
        work_over_Q0=float(work),absorption_over_Q0=float(absorption),
        steady_COP_before_source_losses=float(net/(work+absorption)),
        closure_over_Q0=float(abs(heat.sum()/q0+work)),
        minimum_numerical_population=float(C.diagonal().real.min()),
        tail_population_energy_above_half_cutoff=float(np.dot(js[nmax//2:],C.diagonal().real[nmax//2:])))


def moment_bound(amplitude,edges,profile,start_tail=1000):
    """Rigorous sufficient weighted-moment bound in the passive scalar model.

    F=p cos(r theta), C_r=int F cos(r theta), J_j=(C_r-C_(2j+r))/2.
    A bounded-variation integration by parts yields |C_k|<=TV(F)/k.
    The implemented total variation is an upper bound, including every jump
    and a conservative within-cell derivative integral.
    """
    r=R_PUMP;m=M_COLD
    cr=float(np.dot(profile,np.diff(edges)/2+np.diff(primitive(2*r,edges))/4))
    tv=float(np.sum(np.abs(np.diff(profile)*np.cos(r*edges[1:-1])))
             +r*np.dot(np.abs(profile),np.diff(edges)))
    K=2*amplitude/(np.pi*np.sqrt(m*(m+r)))
    # Every prefix site j<start_tail needs its outgoing and incoming edge.
    nmax=start_tail+r
    js=np.arange(1,nmax+1)
    overlap=edge_overlaps(nmax,'pattern',(edges,profile))
    g=K*np.sqrt(js[:-r]*(js[:-r]+r))*overlap
    g[np.abs(overlap)<1e-13]=0.
    bounds={}
    for power in [1,2]:
        weights=js.astype(float)**power
        coeff=np.zeros(nmax)
        edge_term=(weights[r:]-weights[:-r])*abs(g)
        coeff[:-r]+=edge_term;coeff[r:]+=edge_term
        prefix=float(np.max((coeff/weights)[:start_tail-1]))
        Jbar=abs(cr)/2+tv/(2*(2*start_tail-r))
        tail1=2*r*K*Jbar*np.sqrt(1+r/start_tail)
        tail=tail1 if power==1 else (2+r/start_tail)*tail1
        bounds[str(power)]=dict(prefix_maximum=prefix,tail_upper_bound=float(tail),
            uniform_beta_upper_bound=max(prefix,float(tail)),
            strictly_below_unit_damping=bool(max(prefix,float(tail))<1))
    return dict(Cr=cr,asymptotic_overlap=cr/2,total_variation_upper_bound=tv,
        tail_start_index=start_tail,moment_bounds=bounds)


def main():
    started=time.perf_counter()
    data=json.loads((OUT/'finite_band_pattern_results.json').read_text())
    design=data['designs'][0]
    edges=np.array(design['profile_edges_radians']);profile=np.array(design['profile_values'])
    cases=[]
    for name,amp,reference in [
        ('maximum_COP',design['COP_optimization']['amplitude'],design['COP_optimization']),
        ('maximum_heat',design['net_heat_optimization']['optimized_amplitude'],design['net_heat_optimization'])]:
        rows=[passive_solution(amp,n,edges,profile) for n in [88,176,352]]
        assert abs(rows[0]['work_over_Q0']-reference['work_over_Q0'])<1e-8
        assert abs(rows[0]['net_cold_heat_over_Q0']-reference['net_heat_over_Q0'])<1e-8
        bound=moment_bound(amp,edges,profile)
        assert bound['moment_bounds']['2']['strictly_below_unit_damping']
        cases.append(dict(operating_point=name,cutoffs=rows,analytic_moment_check=bound,
            work_change_88_to_352=rows[-1]['work_over_Q0']-rows[0]['work_over_Q0'],
            COP_change_88_to_352=rows[-1]['steady_COP_before_source_losses']-rows[0]['steady_COP_before_source_losses']))
    result=dict(status='SYNTHETIC_UPPER_TAIL_WORK_AUDIT_NOT_MATERIAL_VALIDATION',
        purpose='Resolve a concrete cutoff risk in the finite-band lower-blocked pattern, whose high-mode overlaps do not tend to zero.',
        scope='Same 192-cell profile, fixed selected drive points; no new optimization or empirical material inputs.',
        derivation='For C positive, 2|C_jk|<=N_j+N_k. Weighted moment E_p=sum j^p N_j therefore obeys dE_p/dt <= -(1-beta_p)E_p + sum j^p n_j. The prefix and bounded-variation tail bounds are uniform in cutoff. beta_2<1 bounds the second moment, excluding a hidden divergent mean-energy steady tail in this ideal passive ladder.',
        caution='The finite prefix of the analytic moment condition is evaluated in floating point, with a large margin; it is not an interval-arithmetic certificate or a sharp truncation error bar. Numerical cutoff changes are reported separately. Tiny negative populations/tail energies are roundoff retained transparently. High-frequency dispersion and RWA validity still require a physical mode model.',
        cases=cases,receipts=dict(local_wall_seconds=time.perf_counter()-started,
            provider_model_id='UNKNOWN',tokens='UNKNOWN',billing='UNKNOWN'))
    (OUT/'upper_tail_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
