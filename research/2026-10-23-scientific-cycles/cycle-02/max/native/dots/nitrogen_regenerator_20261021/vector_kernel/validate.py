"""Bounded Cantera comparison; preserves full per-case discrepancies and failures."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import sys, time, json, hashlib, resource
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent.parent / 'nitrogen_quench_recovery_20261021'
sys.path[:0] = [str(SOURCE / 'deps'), str(SOURCE)]
import numpy as np
import cantera as ct
from paper_model import gas_model
from kernel import Kernel

def native(g, T, Y):
    n = len(T)
    r = {key: np.empty((6,n)) for key in ('mass_production', 'h_species', 'cp_species', 'Y')}
    r.update({key: np.empty(n) for key in ('rho', 'cp', 'enthalpy', 'viscosity', 'conductivity')})
    r.update({key: np.empty((7,n)) for key in ('forward_rates_of_progress', 'reverse_rates_of_progress', 'net_rates_of_progress', 'log_Kc')})
    for i in range(n):
        g.TPY = T[i], ct.one_atm, Y[:,i]
        r['mass_production'][:,i] = g.net_production_rates*g.molecular_weights
        r['h_species'][:,i] = g.partial_molar_enthalpies/g.molecular_weights
        r['cp_species'][:,i] = g.partial_molar_cp/g.molecular_weights
        r['Y'][:,i] = g.Y
        for key, attr in [('rho','density'), ('cp','cp_mass'), ('enthalpy','enthalpy_mass'), ('viscosity','viscosity'), ('conductivity','thermal_conductivity'), ('forward_rates_of_progress','forward_rates_of_progress'), ('reverse_rates_of_progress','reverse_rates_of_progress'), ('net_rates_of_progress','net_rates_of_progress')]:
            r[key][...,i] = getattr(g,attr)
        r['log_Kc'][:,i] = np.log(g.equilibrium_constants)
    return r

def make_batch(g, seed=20261021):
    rng=np.random.default_rng(seed)
    temps=[]; fractions=[]; labels=[]; failures=[]; eq_indices=[]
    def add(t,y,label):
        temps.append(t); fractions.append(y); labels.append(label)
    anchors=[200.,200.001,202.5,250.,300.,999.999999,1000.,1000.000001,1800.,2200.,3100.,3500.]
    for t in anchors:
        for i in range(6): add(t,np.eye(6)[i],f'pure_{i}')
        add(t,np.ones(6)/6,'equal_mass')
        g.TPX=t,ct.one_atm,{'N2':.79,'O2':.21}; add(t,g.Y.copy(),'air')
        for exp in [12,40,120,280]:
            y=np.full(6,10.**(-exp)); y[0]=.77; y[1]=.23
            add(t,y,f'trace_1e-{exp}')
    for i in range(900):
        t=rng.uniform(200.,3500.)
        y=rng.dirichlet(np.full(6,.25)) if i%2 else 10.**rng.uniform(-280,0,6)
        y/=sum(y); add(t,y,'dirichlet' if i%2 else 'log_trace')
    for t in [200.,300.,800.,1000.,1800.,2200.,3100.,3500.]:
        try:
            g.TPX=t,ct.one_atm,{'N2':.79,'O2':.21}; g.equilibrate('TP',solver='gibbs',max_steps=1000)
            y=g.Y.copy(); eq_indices.append(len(temps));add(t,y,'equilibrium_air')
            for eps in [1e-12,1e-8,1e-4]:
                yy=y.copy();yy[4]*=(1.+eps);yy/=sum(yy);add(t,yy,f'near_equilibrium_NO_{eps}')
        except Exception as e:failures.append({'T':t,'operation':'Cantera equilibrate TP/gibbs','error':repr(e)})
    for t in [300.,1000.,3100.]:
        for y in [np.array([.77,.23,-1e-9,0,0,0]),np.array([2.,3.,1.,0,0,0]),np.array([.9,-.01,.1,0,0,0])]:
            add(t,y,'clipped_or_unnormalized')
    return np.asarray(temps),np.asarray(fractions).T,np.asarray(labels),eq_indices,failures

def main():
    t0=time.perf_counter(); k=Kernel();g=gas_model();T,Y,labels,eq,failures=make_batch(g)
    a=k.evaluate(T,Y,return_rates=True);b=native(g,T,Y)
    gross=b['forward_rates_of_progress']+b['reverse_rates_of_progress']
    gross_mass=(np.abs(k.nu)@gross)*k.W[:,None]
    metrics={}
    for key in ('rho','cp','cp_species','viscosity','conductivity','Y'):
        delta=np.abs(a[key]-b[key]);den=np.maximum(np.abs(b[key]),1e-300)
        metrics[key]={'max_absolute_error':float(delta.max()),'max_relative_error':float((delta/den).max())}
    for key in ('h_species','enthalpy'):
        delta=np.abs(a[key]-b[key]);metrics[key]={'max_absolute_error_J_kg':float(delta.max()),'max_error_over_max_1_abs_reference':float((delta/np.maximum(1,abs(b[key]))).max())}
    for key in ('forward_rates_of_progress','reverse_rates_of_progress'):
        metrics[key]={'max_relative_error':float((abs(a[key]-b[key])/np.maximum(b[key],1e-300)).max())}
    dq=abs(a['net_rates_of_progress']-b['net_rates_of_progress'])
    dm=abs(a['mass_production']-b['mass_production'])
    metrics['net_rates']={'max_absolute_error_kmol_m3_s':float(dq.max()),'max_error_over_gross_reaction_flux':float((dq/np.maximum(gross,1e-300)).max()),'normalization':'|delta q_net|/(q_forward_native+q_reverse_native), not |q_net| near cancellation'}
    metrics['mass_production']={'max_absolute_error_kg_m3_s':float(dm.max()),'max_error_over_species_gross_mass_flux':float((dm/np.maximum(gross_mass,1e-300)).max()),'normalization':'|delta wdot_i|/[W_i sum_r |nu_ir|(q_forward_native+q_reverse_native)]'}
    metrics['log_Kc']={'max_absolute_error':float(abs(a['log_Kc']-b['log_Kc']).max())}
    element=k.element_atoms@(a['mass_production']/k.W[:,None]); elem_gross=k.element_atoms@(gross_mass/k.W[:,None])
    conservation={'reaction_element_stoichiometry_exact_zero':bool(np.all(k.element_atoms@k.nu==0)),
                  'reaction_molecular_weight_roundoff_max_kg_kmol':float(abs(k.W@k.nu).max()),
                  'max_species_mass_sum_absolute_kg_m3_s':float(abs(a['mass_production'].sum(axis=0)).max()),
                  'max_species_mass_sum_over_gross_mass_flux':float((abs(a['mass_production'].sum(axis=0))/np.maximum(gross_mass.sum(axis=0),1e-300)).max()),
                  'max_element_balance_over_gross_element_flux':float((abs(element)/np.maximum(elem_gross,1e-300)).max())}
    balance=[]
    for i in eq:
        balance.append({'T_K':float(T[i]),'native_max_net_over_gross':float((abs(b['net_rates_of_progress'][:,i])/np.maximum(gross[:,i],1e-300)).max()),'kernel_max_net_over_gross':float((abs(a['net_rates_of_progress'][:,i])/np.maximum(gross[:,i],1e-300)).max()),'comparison_max_error_over_gross':float((dq[:,i]/np.maximum(gross[:,i],1e-300)).max())})
    # Compare mixing rules using native pure properties, removing interpolation.
    rng=np.random.default_rng(5713);mixerrs=[];pureerrs=[]
    tt=np.r_[np.linspace(200,210,81),rng.uniform(200,3500,401)]
    muv,kv=k.pure_transport(tt)
    for j,t in enumerate(tt):
        yy=rng.dirichlet(np.ones(6));g.TPY=t,ct.one_atm,yy
        mm,kk=g.viscosity,g.thermal_conductivity; X=g.X; mu=g.species_viscosities
        lam=np.empty(6)
        for s in range(6):g.TPX=t,ct.one_atm,np.eye(6)[s];lam[s]=g.thermal_conductivity
        phi=(1+np.sqrt(mu[:,None]/mu[None,:])*(k.W[None,:]/k.W[:,None])**.25)**2/np.sqrt(8*(1+k.W[:,None]/k.W[None,:]))
        mine_mu=np.sum(X*mu/(phi@X));mine_k=.5*(np.sum(X*lam)+1/np.sum(X/lam))
        mixerrs.append([abs(mine_mu/mm-1),abs(mine_k/kk-1)])
        pureerrs.append([np.max(abs(muv[:,j]/mu-1)),np.max(abs(kv[:,j]/lam-1))])
    invalid=[]
    for name,t,y,p,strict in [('nan_T',np.nan,np.ones(6),101325.,False),('inf_T',np.inf,np.ones(6),101325.,False),('nan_Y',300.,np.array([np.nan,1,0,0,0,0]),101325.,False),('inf_Y',300.,np.array([np.inf,1,0,0,0,0]),101325.,False),('nan_P',300.,np.ones(6),np.nan,False),('low_T',199.9,np.ones(6),101325.,False),('high_T',3500.1,np.ones(6),101325.,False),('wrong_P',300.,np.ones(6),101326.,False),('all_zero_Y',300.,np.zeros(6),101325.,False),('all_negative_Y',300.,-np.ones(6),101325.,False),('strict_negative',300.,np.array([1,0,0,0,0,-1e-15]),101325.,True),('strict_nonunit',300.,np.ones(6),101325.,True)]:
        try:k.evaluate(t,y,p,strict=strict);invalid.append({'case':name,'rejected':False});failures.append({'case':name,'error':'Invalid input was accepted'})
        except (ValueError,FloatingPointError) as e:invalid.append({'case':name,'rejected':True,'error':str(e)})
    passes={
        'thermochemistry':metrics['cp']['max_relative_error']<1e-12 and metrics['h_species']['max_absolute_error_J_kg']<1e-6,
        'kinetics_gross_flux_scaled':metrics['mass_production']['max_error_over_species_gross_mass_flux']<5e-11,
        'transport_sampled_relative':metrics['viscosity']['max_relative_error']<1e-6 and metrics['conductivity']['max_relative_error']<1e-6,
        'conservation':conservation['max_element_balance_over_gross_element_flux']<1e-14,
        'invalid_rejections':all(x['rejected'] for x in invalid),
        'exact_mixing_rule_sampled':bool(np.max(mixerrs)<1e-12),
    }
    np.savez_compressed(ROOT/'validation_cases.npz',T=T,Y=Y,labels=labels,
                        kernel_mass_production=a['mass_production'],native_mass_production=b['mass_production'],
                        kernel_q=a['net_rates_of_progress'],native_q=b['net_rates_of_progress'],gross_q=gross,
                        native_h_species=b['h_species'],kernel_h_species=a['h_species'],
                        native_viscosity=b['viscosity'],kernel_viscosity=a['viscosity'],
                        native_conductivity=b['conductivity'],kernel_conductivity=a['conductivity'])
    summary={'batch_states':len(T),'seed':20261021,'T_range_K':[float(T.min()),float(T.max())],'P_Pa':101325.,'composition_families':dict(zip(*[x.tolist() for x in np.unique(labels,return_counts=True)])),
             'metrics':metrics,'conservation':conservation,'detailed_balance_at_native_equilibrium':balance,
             'mixing_without_interpolation_max_relative_error':dict(zip(['viscosity','conductivity'],np.max(mixerrs,axis=0).tolist())),
             'pure_transport_offgrid_max_relative_error':dict(zip(['viscosity','conductivity'],np.max(pureerrs,axis=0).tolist())),
             'offgrid_transport_temperatures':len(tt),'invalid_inputs':invalid,'passes':passes,
             'failures':failures,'all_declared_gates_pass':all(passes.values()) and not failures,
             'wall_s':time.perf_counter()-t0,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'scope':'Sampled numerical agreement only; no BVP run, global error bound, physical validation or universal performance certificate. Native near-equilibrium cancellation is reported through gross-flux-scaled errors.'}
    (ROOT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if not summary['all_declared_gates_pass']:raise SystemExit(1)

if __name__=='__main__':main()
