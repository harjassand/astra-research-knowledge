"""Conditional source-compatible LTI attack on the actual paired voltage path."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy.optimize import linprog
import positive_relaxation as r

HERE=Path(__file__).resolve().parent
PATH=HERE.parents[1]/'coupled_bound'/'actual_voltage_path.csv'
# HERE=work/electrical16/material/relaxation; electrical16 is parents[1].
sys.path.insert(0,str(HERE.parent))
import source_envelope as fe


def summarize(fit,taus,costA,costB):
    if not fit['success']:return r.clean(fit)
    x=fit['_x'];C=x[1:]*1e-6*taus/r.V
    g=x[0]*1e-6/r.V
    w=2*np.pi*1e4
    return dict(**r.clean(fit),
      loss_bank_A_J_m2=float(costA@x),loss_bank_B_J_m2=float(costB@x),
      mean_loss_per_bank_full_cycle_J_m2=float((costA+costB)@x/2),
      sum_extra_C_F_per_source_device=float(C.sum()),
      sum_extra_C_F_per_single_film_m2=float(C.sum()/r.AREA),
      sum_extra_C_F_per_tenfilm_bank_m2=float(C.sum()/r.AREA*r.N),
      extra_equilibrium_step_charge_C_per_singlefilm_m2=float(C.sum()*r.V/r.AREA),
      DC_conductance_S_per_singlefilm_m2=float(g/r.AREA),
      extra_C_real_at10kHz_F_per_singlefilm_m2=float(np.sum(C/(1+(w*taus)**2))/r.AREA),
      extra_real_admittance_at10kHz_S_per_singlefilm_m2=float(np.sum(C*w*w*taus/(1+(w*taus)**2))/r.AREA))


def actual(n=1201,uncertainty_scale=1.,dc=None):
    x=np.genfromtxt(PATH,delimiter=',',names=True);t=x['time_s']
    taus=np.geomspace(1e-6,10,n)
    ca,ra=r.generic_coefficients(t,x['VA_V'],taus)
    cb,rb=r.generic_coefficients(t,x['VB_V'],taus)
    fit=r.solve(taus,uncertainty_scale=uncertainty_scale,force_dc=dc,
                objective_cost=(ca+cb)/2)
    out=summarize(fit,taus,ca,cb)
    out['voltage_path_period_s']=float(t[-1]-t[0])
    out['both_Debye_reset_max_V']=max(ra,rb)
    return out,fit,taus,ca,cb


def analytic_loss_bound(path,uncertainty_scale=1.):
    """All-positive-tau Debye/DC lower bound, independent of spectral gridding.

    If t*omega_1>=1, each Fourier harmonic obeys
      omega_k^2 tau^2/(1+omega_k^2 tau^2) >= exp(-t*/tau).
    Proof: with z=t*/tau,a=omega_k*t*>=1,
      d/dz log[e^z/(1+z^2/a^2)] = 1-2z/(a^2+z^2)>=0.
    Parseval then gives E >= (I_step(t*)/V_step)*int(V-mean V)^2dt.
    The DC branch satisfies the same bound since int V^2>=int AC V^2.
    """
    t=path['time_s'];P=float(t[-1]-t[0]);dt=np.diff(t)
    variance=[]
    for field in ['VA_V','VB_V']:
        v=path[field]
        integral=float(np.sum(dt*(v[:-1]+v[1:])/2))
        square=float(np.sum(dt*(v[:-1]**2+v[:-1]*v[1:]+v[1:]**2)/3))
        variance.append(square-integral**2/P)
    trace=np.genfromtxt(HERE.parent/'source_10ms_current.csv',delimiter=',',names=True)
    keep=(trace['time_s']>=max(.001,P/(2*np.pi)))
    allowed=np.flatnonzero(keep)
    selected=allowed[np.argmax(trace['source_current_A'][allowed])]
    low=float(trace['source_current_A'][selected]-r.UNCERTAINTY_UA*1e-6*uncertainty_scale)
    bound=low/r.V*np.mean(variance)*r.N/r.AREA
    return dict(lower_loss_J_per_bank_fullcycle_m2=float(bound),
                source_time_s=float(trace['time_s'][selected]),
                source_current_lower_A=low,period_s=P,
                omega1_times_source_time=float(2*np.pi*trace['time_s'][selected]/P),
                AC_voltage_variance_integrals_V2_s=variance,
                scope='Analytical lower bound over ALL positive tau, any positive spectral measure, and nonnegative DC shunt; exact for supplied piecewise-linear voltage interpolation; conditional constitutive/initial-state assumptions unchanged')


def main():
    base,fit,taus,ca,cb=actual()
    variants=[actual(n=n)[0] for n in [401,801,1601]]
    variants += [actual(uncertainty_scale=s)[0] for s in [.5,2.,4.]]
    nodc=actual(dc=0.)[0]
    Ccost=np.r_[0.,1e-6*taus/r.V/r.AREA]
    mincap=r.solve(taus,objective_cost=Ccost)
    # This is a different optimization, reducing Ceq while allowing DC loss.
    mc=summarize(mincap,taus,ca,cb)
    mc['minimum_extra_C_F_per_singlefilm_m2']=mc.pop('minimum_loss_J_per_bank_m2')
    mc.pop('dc_loss_J_per_bank_m2');mc.pop('absorption_loss_J_per_bank_m2')
    for c in mc['active_components']:
        c['capacitance_objective_contribution_F_per_singlefilm_m2']=c.pop('loss_J_per_bank_m2')
    mc['objective_is_extra_C_F_per_singlefilm_m2_not_loss']=True
    dq=(fe.qref(r.V)-fe.qref(0.))/fe.N
    Wrect=fe.DATA['source_fullfield_reversible_338_348_work_J_m2']
    result=dict(scope='CONDITIONAL_SAME_SPECTRUM_LTI_CLASS_ACTUAL_VOLTAGE_PATH',
      waveform_path=str(PATH),waveform_sha256=hashlib.sha256(PATH.read_bytes()).hexdigest(),
      source_trace_sha256=hashlib.sha256((HERE.parent/'source_10ms_current.csv').read_bytes()).hexdigest(),
      material_assumption='Same positive T-independent LTI Debye+DC step response at both banks; zero initial polarization in the source pulse; class not established by source',
      same_spectrum_for_both_banks=True,objective='(loss_A+loss_B)/2 perbank fullcycle = loss_pair_halfcycle when symmetric',
      actual_cycle_minimum=base,zero_DC_minimum=nodc,
      analytical_all_tau_loss_bound=analytic_loss_bound(np.genfromtxt(PATH,delimiter=',',names=True)),
      convergence_and_pixel_sensitivity=variants,
      minimum_extra_equilibrium_capacitance_fit=mc,
      source_reference=dict(qref_10kHz_branch_voltage_step_C_per_singlefilm_m2=dq,
          secant_qref_step_over_voltage_F_per_singlefilm_m2=dq/r.V,
          qref_is_equilibrium_capacitance=False,
          differential_qref_C_at0_F_per_singlefilm_m2=float(fe.cref(0.)/fe.N),
          differential_qref_C_atVmax_F_per_singlefilm_m2=float(fe.cref(r.V)/fe.N),
          fullsource_338_348_monotone_rectangle_work_J_perbank_m2=Wrect),
      favorable_candidate_comparison=dict(root_ideal_work_perpair_halfcycle_J_m2=.162702,
          root_unallocated_TE_advantage_budget_perpair_halfcycle_J_m2=.025607,
          boundloss_over_candidate_ideal_work=base['mean_loss_per_bank_full_cycle_J_m2']/.162702,
          boundloss_over_fullsource_reversible_rectangle=base['mean_loss_per_bank_full_cycle_J_m2']/Wrect),
      interpretation=[
        'An initially uncharged positive LTI absorption model reproducing the conditioning current cannot be silently loss-free on the supplied actual bounded-circuit voltage path, even when all DC leakage is removed.',
        'The 10kHz source qref is a dynamical branch average, not a measured equilibrium charge curve. Slow absorption can be nearly invisible at10kHz; large inferred Ceq therefore does not by itself contradict that source curve.',
        'Adding these branches to a potential that claims qref is the equilibrium Q(V) changes its equilibrium charge and stored energy. It requires a refitted background and additional entropy/internal-state model; no double-count-free physical total model has been established.',
        'The fitted first pulse is not evidence that the same initially-zero, T-independent LTI response recurs after conditioning. This conditional exclusion does not exclude actual nonlinear or trained FE operation.',
        'These losses are evaluated on an externally fixed voltage path. If branches are physical, their currents, field charge, resistor heat and circuit timing must be included in a new coupled trajectory; they cannot be subtracted from an unchanged engine and called actual performance.',
        'The full-source caloric rectangle bound is useful only for the declared FE reversible envelope and one bounded monotone field excursion in338..348K; no universal all-material heat-engine bound is claimed.'])
    (HERE/'actual_cycle_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(base=base,mincap=mc,comparison=result['favorable_candidate_comparison']),indent=2))


if __name__=='__main__':main()
