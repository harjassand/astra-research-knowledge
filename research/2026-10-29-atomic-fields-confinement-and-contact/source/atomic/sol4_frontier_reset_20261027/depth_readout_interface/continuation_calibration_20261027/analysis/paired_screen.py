"""Paired Poisson calibration eliminates arbitrary shared native intensities.

Given each feature's before+after total, the after count is binomial with
probability r/(z+r), z=D_before/D_after, r=candidate defect/native ratio.
The null r=1 is exact for any shared native pattern. Non-null ratios are a
physical transfer assumption. Thermal parameters are not supplied to inference.
"""
from pathlib import Path
import json,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent

def load(tag,own=False):
    where=ROOT if own else BASE
    files=sorted((where/'outputs').glob(f'{tag}_state*.npz'))
    ss=[int(f.stem[-2:]) for f in files];dd=[np.load(f) for f in files]
    return ss,np.asarray([d['p'] for d in dd],dtype=np.float64),dd[0]

def main():
    t=time.monotonic();ss,model,d=load('rigid256');a=float(d['scan_cell_area'])
    m=model.reshape(len(model),-1)
    logr=np.log(np.maximum(m,1e-300))-np.log(np.maximum(m[ss.index(0)],1e-300))
    st,truth,dt=load('phonon4_sigma01');p=truth.reshape(len(truth),-1);native=p[st.index(0)]
    rows=[]
    for z in [.1,.25,.5,1,2,4,10,1000]:
        den=np.logaddexp(np.log(z),logr)
        la=logr-den;lb=np.log(z)-den
        score=a*(p@la.T+z*native@lb.T)
        for k,true in enumerate(st):
            best=int(np.argmax(score[k]));correct=ss.index(true);order=np.argsort(score[k])[::-1]
            rows.append({'native_to_after_dose_ratio':z,'true_state':true,
                         'best_conditional_state':ss[best],
                         'expected_score_best_minus_correct_per_after_dose':float(score[k,best]-score[k,correct]),
                         'expected_score_first_minus_second_per_after_dose':float(score[k,order[0]]-score[k,order[1]]),
                         'correct_asymptotic_forced_label':bool(ss[best]==true)})
    predictions=native[None,:]*np.exp(logr)
    kl=a*(np.sum(p*np.log(np.maximum(p,1e-300))-p,axis=1)[:,None]-p@np.log(np.maximum(predictions,1e-300)).T+predictions.sum(1)[None,:])
    ideal=[]
    for k,true in enumerate(st):
        best=int(np.argmin(kl[k]));ideal.append({'true_state':true,'best_perfect_native_calibrated_state':ss[best],
             'KL_best_per_after_dose':float(kl[k,best]),'KL_correct_state_per_after_dose':float(kl[k,ss.index(true)]),
             'predicted_detection_probability_max':float(predictions[best].reshape(45,-1).sum(1).max())})
    out={'scope':__doc__,'training':'rigid17 defect/native ratios only','truth':'four-snapshot sigma=.1A templates; not acquired physics',
         'thermal_label_supplied_to_estimator':False,'shared_nuisance_assumption':True,
         'conditional_rows':rows,'infinite_native_reference_diagnostic':ideal,'elapsed_seconds':time.monotonic()-t}
    (ROOT/'outputs/paired_screen.json').write_text(json.dumps(out,indent=2))
    print('balanced:',json.dumps([r for r in rows if r['native_to_after_dose_ratio']==1]),flush=True)
    print('perfect native:',json.dumps(ideal),flush=True)
if __name__=='__main__':main()
