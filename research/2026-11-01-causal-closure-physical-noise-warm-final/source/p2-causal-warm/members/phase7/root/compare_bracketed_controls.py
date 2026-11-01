"""Conventional optimization adopts the same finite observation construction.

These are feasible fixed-envelope schedules, not global device optima.
Changing chi changes the storage-loss dose and drive action, so the fastest
schedule must not inherit the low-loss schedule's favorable number.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr
from bracketed_parity_meter import Model, compute, optimize_duration, envelope


def add_energy(row):
    m=Model(**row['model'])
    _,a=compute(row['pre'],row['post'],row['lam'],m,300,True)
    p=float(np.linalg.norm(a['Epre'],2))
    q=float(np.linalg.norm(a['Epost'],2))
    lam=row['lam']
    U=quad(lambda t:lam*m.chi*float(envelope(t,m.mapping_time,m.ramp_chi))*np.exp(-m.ka*t/2),0,m.mapping_time,epsabs=1e-11)[0]
    action=quad(lambda t:(lam*m.chi*float(envelope(t,m.mapping_time,m.ramp_chi))*np.exp(-m.ka*t/2))**2,0,m.mapping_time,epsabs=1e-11)[0]
    Erob=(q*U/(1-p*q))**2
    Enom=row['nominal_boundary_energy_bound_from_bounded_parity_history']
    row.update(read_pre_operator_norm=p,read_post_operator_norm=q,
               integrated_absolute_mapping_force=U,mapping_drive_action=action,
               robust_boundary_energy_bound=Erob,
               nominal_map_entry_energy_bound=p*p*Enom,
               robust_map_entry_energy_bound=p*p*Erob,
               robust_peak_total_energy_bound=(p*np.sqrt(Erob)+U)**2)
    # Thermal main-line report only in the EXACT zero-intrinsic-loss model.
    zero=Model(**{**row['model'],'ka':0.})
    rz=compute(row['pre'],row['post'],lam,zero,300)
    N=rz['N_selected']
    thermal=[]
    for nb in [0.,.001,.01,.1,1.]:
        qn=float(ndtr(-2*np.sqrt(m.eta*N)/np.sqrt(1+2*m.eta*nb)))
        gn=float(.5*np.exp(-2*(2*nb+1)*N))
        en=qn+gn*gn/qn
        thermal.append(dict(fresh_line_nbar=nb,q=qn,e=en))
    row['zero_intrinsic_loss_fresh_thermal_report_cases']=thermal
    # Readout-only admission: no invented probabilistic model for storage,
    # data, idle, controls or persistent apparatus faults is included here.
    e=row['selected_pointer_CP_bad_weight']
    row['readout_only_two_or_more_tags_upper_bound_120_uses']=min(1.,120*119/2*e*e)
    row['parallel_5x5_no_fresh_fault_cycle_sensing_time']=4*row['total_time']
    row['parallel_5x5_one_fresh_fault_cycle_sensing_time']=6*row['total_time']
    return row


def main():
    fastest=[]
    for chi in [1.,1.25,1.5,1.75,2.]:
        r=add_energy(optimize_duration(Model(chi=chi),start=(1.5,1.5),order=140))
        fastest.append(r)
        print('CHI',chi,'T',r['total_time'],'pZ',r['thermal_cases'][0]['pZ_after_known_phase'],
              'Ebound',r['robust_boundary_energy_bound'],flush=True)
    at_chi2=[]
    m=Model()
    for tau in [2.,2.5,3.,4.]:
        unit=compute(tau,tau,1.,m,300)
        lam=np.sqrt(m.target_N/unit['N_selected'])
        r=add_energy(compute(tau,tau,float(lam),m,500))
        at_chi2.append(r)
    # Stronger readout accuracy using the same single map, fixed force cap.
    report_targets=[]
    for target in [1e-3,1e-4,2e-5]:
        r=add_energy(optimize_duration(Model(q=target),start=(2.5,2.5),order=140))
        report_targets.append(r)
        print('REPORT',target,'T',r['total_time'],'N',r['N_selected'],flush=True)
    out=dict(fixed_control_family_fast_candidates=fastest,
             chi2_longer_lower_force_candidates=at_chi2,
             report_target_candidates=report_targets,
             disclaimer='No global optimization, hardware comparison or total logical error rate.')
    Path(__file__).with_name('bracketed_control_comparison.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':
    main()
