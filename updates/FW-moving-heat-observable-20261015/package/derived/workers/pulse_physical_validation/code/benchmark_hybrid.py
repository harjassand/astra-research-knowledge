"""Execute pinned original hybrid-drt; all pulse results remain conditional.

Amplitude is inferred from positive-pulse training data by the separate joint
LP, never described as a measured current. Negative pulse data are held out
for the charge-trained models. The broad baseline allows the upstream
cross-domain offset and a linear voltage baseline; strict baseline does not.
"""
from pathlib import Path
import json, time, traceback, warnings, platform
import numpy as np
import scipy
from hybdrt.models import DRT
from audit_data import load, pulse_info
from joint_lp import select

BASE=Path(__file__).resolve().parents[1]
COMMIT='e01dba1bf5f02fa6b63c82169c0652a5a695344d'

def predict(model,t,steps,sizes):
    t=np.asarray(t)
    # Upstream subtracts the mean current of samples before the first supplied
    # step. A window beginning after that step otherwise has an empty mean.
    # Include a zero-current prehistory sample, then discard its prediction.
    prepend=t[0]>=min(steps)
    eval_t=np.r_[0.,t] if prepend else t
    old_steps=model.nonconsec_step_times
    if old_steps is not None: model.nonconsec_step_times=np.asarray(steps)
    result=model.predict_response(times=eval_t, step_times=np.asarray(steps),
        step_sizes=np.asarray(sizes), op_mode='galv', offset_steps=False,
        smooth_inf_response=False, include_vz_offset=True, v_baseline=0.)
    model.nonconsec_step_times=old_steps
    return result[1:] if prepend else result

def run(kind):
    z,p,_=load(); f=z['f'][0]; zz=z['Z'][0]
    use=f<=1000; f=f[use]; zz=zz[use]
    pi=pulse_info(p,'pos'); ni=pulse_info(p,'neg'); gap=pi['t'][-1]
    ix=np.unique(np.r_[np.arange(pi['on_index']),select(pi['t'],pi)])
    tt=pi['t'][ix]; vv=pi['v'][ix]-pi['baseline_V']
    lp=json.loads((BASE/'results/joint_lp.json').read_text())['runs']
    train_amp=[r['amplitude_inferred_A'] for r in lp if r['which']=='pos'][-1]
    # Basis covers 12 decades, with explicit capacitor and inductance.
    model=DRT(fixed_basis_tau=np.logspace(-6,6,121), fit_capacitance=True,
              fit_inductance=True, tau_basis_type='gaussian', warn=True)
    t0=time.perf_counter()
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        if kind=='eis_only':
            model.fit_eis(f,zz,nonneg=True,max_iter=75,xtol=.005)
        else:
            current=np.where((tt>pi['assumed_on_s'])&(tt<pi['assumed_off_s']),train_amp,0.)
            broad=kind=='hybrid_charge_flexible'
            model.fit_hybrid(tt,current,vv,f,zz,
                step_times=np.array([pi['assumed_on_s'],pi['assumed_off_s']]),
                step_sizes=np.array([train_amp,-train_amp]),
                nonneg=True, offset_steps=False, smooth_inf_response=False,
                offset_baseline=broad, v_baseline_deg=1 if broad else 0,
                vz_offset=broad, max_iter=200,xtol=.005,
                eis_error_structure=None,chrono_error_structure='uniform')
        fit_seconds=time.perf_counter()-t0
        yp=predict(model,pi['t'],[pi['assumed_on_s'],pi['assumed_off_s']],
                   [train_amp,-train_amp])
        # Model the known prior positive pulse, then the negative pulse.
        steps=[pi['assumed_on_s'],pi['assumed_off_s'],
               gap+ni['assumed_on_s'],gap+ni['assumed_off_s']]
        sizes=[train_amp,-train_amp,-train_amp,train_amp]
        # Include neighboring times for a well-defined sample increment.
        pred_at_baseline=predict(model,np.array([gap-.01,gap,gap+.01]),steps,sizes)[1]
        yn=predict(model,ni['t']+gap,steps,sizes)-pred_at_baseline
        yp_meas=pi['v']-pi['baseline_V']; yn_meas=ni['v']-ni['baseline_V']
        fitted_baseline_pos=model.predict_v_baseline(pi['t'])
        fitted_baseline_neg=model.predict_v_baseline(ni['t']+gap)-model.predict_v_baseline(np.array([gap]))[0]
        yp_fit=yp+fitted_baseline_pos
        yn_drift=yn+fitted_baseline_neg
        zi=model.predict_z(f)
        qp=model.qphb_history[-1] if model.qphb_history else {}
        assert np.all(np.isfinite(yp)) and np.all(np.isfinite(yn))
        fitparams={k: np.asarray(v).tolist() for k,v in model.fit_parameters.items()
                   if k in ['R_inf','inductance','C_inv','v_baseline','vz_offset','vz_offset_eps']}
        # Use data selection identical to the joint LP for maximum errors.
        pix=select(pi['t'],pi); nix=select(ni['t'],ni)
        out={'status':'EXECUTED_ORIGINAL_UPSTREAM','kind':kind,'commit':COMMIT,
            'fit_seconds':fit_seconds,'iteration_count':len(model.qphb_history),
            'warnings':[str(w.message) for w in ws],
            'frequency_max_component_residual_mOhm':float(max(abs((zi-zz).real).max(),abs((zi-zz).imag).max())*1000),
            'frequency_RMSE_complex_mOhm':float(np.sqrt(np.mean(abs(zi-zz)**2))*1000),
            'charge_selected_max_residual_mV':float(abs(yp[pix]-yp_meas[pix]).max()*1000),
            'charge_fit_with_fitted_baseline_selected_max_residual_mV':float(abs(yp_fit[pix]-yp_meas[pix]).max()*1000),
            'discharge_heldout_selected_max_residual_mV':float(abs(yn[nix]-yn_meas[nix]).max()*1000),
            'discharge_heldout_with_extrapolated_baseline_selected_max_residual_mV':float(abs(yn_drift[nix]-yn_meas[nix]).max()*1000),
            'charge_endpoint_residual_mV':float((yp[pi['end_index']]-yp_meas[pi['end_index']])*1000),
            'discharge_endpoint_residual_mV':float((yn[ni['end_index']]-yn_meas[ni['end_index']])*1000),
            'amplitude_inferred_from_training_A':train_amp,
            'amplitude_measured':False,'current_waveform_measured':False,
            'physical_validation':False,'fitted_nuisance_parameters':fitparams,
            'negative_pulse_used_in_training':False,
            'heldout_voltage_used_for_alignment_and_baseline':True,
            'contract':'Positive pulse + EIS training (except eis_only), negative pulse held out; common fitted current amplitude; ideal commanded 10s waveform inferred from voltage; no acquired current; same stationary response; included known first-pulse memory. Baseline-referenced predictions exclude extrapolating a fitted linear unforced baseline into the heldout state.'}
        np.savez_compressed(BASE/f'results/hybrid_{kind}_predictions.npz',
            pos_time=pi['t'],pos_measured_V=yp_meas,pos_predicted_V=yp,
            pos_fitted_baseline_V=fitted_baseline_pos,pos_total_fit_V=yp_fit,
            neg_time=ni['t'],neg_measured_V=yn_meas,neg_predicted_V=yn,
            neg_extrapolated_baseline_V=fitted_baseline_neg,neg_with_drift_predicted_V=yn_drift,
            f=f,z_measured=zz,z_predicted=zi,training_amplitude_A=train_amp)
        return out

def main():
    rows=[]
    for kind in ['eis_only','hybrid_charge_strict','hybrid_charge_flexible']:
        try: row=run(kind)
        except Exception as exc:
            row={'kind':kind,'status':'FAILED','error':str(exc),'traceback':traceback.format_exc()}
        rows.append(row); print(json.dumps(row,default=str),flush=True)
        (BASE/'results/hybrid_baseline.json').write_text(json.dumps({'runs':rows,
            'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
            'physical_validation':False,'upstream_source_modified':False},indent=2,default=str))

if __name__=='__main__':main()
