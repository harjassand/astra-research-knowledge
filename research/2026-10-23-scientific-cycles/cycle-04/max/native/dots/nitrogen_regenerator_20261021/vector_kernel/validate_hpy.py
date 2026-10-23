"""Compare branch-aware HP inversion with Cantera and preserve splice ambiguity."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import json, time
import numpy as np
from validate import ROOT, Kernel, gas_model, native, make_batch, ct

def main():
    t0=time.perf_counter();k=Kernel();g=gas_model();T,Y,labels,eq,failures=make_batch(g)
    ref=native(g,T,Y);h=ref['enthalpy'];r=k.evaluate_hpy(h,Y,return_rates=True)
    nativeT=[];nativeH=[]
    for i in range(len(T)):
        # Same specified initial guess for every independent native inversion.
        g.TPY=300.,ct.one_atm,Y[:,i]
        g.HPY=h[i],ct.one_atm,Y[:,i]
        nativeT.append(g.T);nativeH.append(g.enthalpy_mass)
    nativeT=np.array(nativeT);nativeH=np.array(nativeH)
    ambiguous=r['diagnostics']['NASA_splice_ambiguous']
    normal=~ambiguous
    metrics={'max_abs_T_difference_unique_branch_K':float(abs(r['T'][normal]-nativeT[normal]).max()),
             'max_abs_T_difference_all_K':float(abs(r['T']-nativeT).max()),
             'max_abs_T_reconstruction_unique_branch_K':float(abs(r['T'][normal]-T[normal]).max()),
             'max_abs_T_reconstruction_all_K':float(abs(r['T']-T).max()),
             'max_abs_native_T_reconstruction_unique_branch_K':float(abs(nativeT[normal]-T[normal]).max()),
             'max_abs_h_residual_kernel_J_kg':float(abs(r['enthalpy']-h).max()),
             'max_abs_h_residual_native_J_kg':float(abs(nativeH-h).max()),
             'max_kernel_HP_iterations':int(r['diagnostics']['HP_iterations'].max()),
             'ambiguous_states':int(ambiguous.sum())}
    # A deliberately impossible h in the positive NO2 splice gap must fail.
    yy=np.eye(6)[5];hl=k.evaluate(1000.,yy)['enthalpy'][0];hr=k.evaluate(np.nextafter(1000.,np.inf),yy)['enthalpy'][0];hm=(hl+hr)/2
    gap={'NO2_jump_J_kg':float(hr-hl),'target_J_kg':float(hm)}
    try:k.temperature_from_enthalpy(hm,yy);gap['strictly_rejected']=False;failures.append({'case':'NO2 splice gap','error':'silently accepted'})
    except ValueError as e:gap['strictly_rejected']=True;gap['error']=str(e)
    clamped=k.temperature_from_enthalpy(hm,yy,trial_clamp=True)
    gap.update(clamped_T_K=float(clamped['T'][0]),clamp_flag=bool(clamped['diagnostics']['enthalpy_clamped'][0]),original_residual_J_kg=float(clamped['diagnostics']['enthalpy_residual_original_J_kg'][0]))
    other=[]
    for name,hh,yy,opts in [('outside_low',-1e9,np.eye(6)[0],{}),('outside_high',1e9,np.eye(6)[0],{}),('nan',np.nan,np.eye(6)[0],{}),('inf',np.inf,np.eye(6)[0],{}),('strict_trial_clamp_conflict',0.,np.eye(6)[0],{'strict':True,'trial_clamp':True}),('infinite_rtol',1e9,np.eye(6)[0],{'strict':True,'rtol':np.inf}),('nan_atol',1e9,np.eye(6)[0],{'strict':True,'atol':np.nan}),('negative_atol',0.,np.eye(6)[0],{'atol':-1.}),('invalid_iteration_limit',0.,np.eye(6)[0],{'max_iter':0}),('loose_tolerance_domain_bypass',1e9,np.eye(6)[0],{'strict':True,'rtol':1e6})]:
        try:k.temperature_from_enthalpy(hh,yy,**opts);other.append({'name':name,'rejected':False});failures.append({'case':name,'error':'accepted invalid h'})
        except ValueError as e:other.append({'name':name,'rejected':True,'error':str(e)})
    saved={'T_reference':T,'h_native':h,'Y':Y,'native_T_from_h':nativeT,'kernel_T_from_h':r['T'],'NASA_ambiguous':ambiguous,'kernel_h_residual':r['enthalpy']-h,'native_h_residual':nativeH-h}
    np.savez_compressed(ROOT/'hpy_validation_cases.npz',**saved)
    passed=(metrics['max_abs_T_reconstruction_unique_branch_K']<1e-7 and metrics['max_abs_h_residual_kernel_J_kg']<2e-5 and gap['strictly_rejected'] and gap['clamp_flag'] and not failures)
    result={'states':len(T),'metrics':metrics,'positive_splice_gap':gap,'invalid':other,'failures':failures,'all_declared_gates_pass':passed,'initial_gate_failure':{'file':'hpy_validation_initial_overstrict_gate.json','test':'Native-vs-kernel temperature difference < 1e-5 K','observed_K':1.795783850866428e-5,'resolution':'Preserved failure. Reference native HP solve itself misses TP-derived target by 0.0266769 J/kg. Final correctness gate is reconstruction of known TP input on unique branch (<1e-7 K) plus kernel enthalpy residual (<2e-5 J/kg), not a relaxed comparison-to-native threshold.'},'wall_s':time.perf_counter()-t0,'scope':'Source NASA low/high branches have small h discontinuities. Multiple roots are explicitly flagged; near-gap impossible h fails by default, with opt-in diagnostic trial clamping only. No guarantee of matching a stateful native HP branch choice.'}
    (ROOT/'hpy_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    if not result['all_declared_gates_pass']:raise SystemExit(1)
if __name__=='__main__':main()
