"""Ordinary joint native-reference/depth calibration with latent nuisance.

The nuisance parameter w is inferred from counts, never supplied. The small
model is an intensity mixture between rigid and sigma=.1 A templates. This is
not asserted to describe intermediate temperatures or experimental CrSBr.
Held-out sigma=.065 A/independent-seed multislice truths test that coverage.
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from paired_screen import load
ROOT=Path(__file__).resolve().parents[1]

def bmatrix(q,a):
    q=q.reshape(len(q),-1);s=np.sqrt(q)
    return .5*a*np.maximum(q.sum(1)[:,None]+q.sum(1)[None,:]-2*s@s.T,0)

def main():
    started=time.monotonic();classes=[0,10,11,15,16]
    sr,rig,d=load('rigid256');st,th,_=load('phonon4_sigma01')
    r=np.asarray([rig[sr.index(h)].ravel() for h in classes]);t=np.asarray([th[st.index(h)].ravel() for h in classes]);delta=t-r
    a=float(d['scan_cell_area']);nu=r.shape[-1]
    # Finite endpoint family: exact worst-class bounds, shared nuisance unknown.
    endpoint=np.concatenate([r,t]);cl=classes+classes;B=bmatrix(endpoint,a)
    B0=bmatrix(np.stack([r[0]]*5+[t[0]]*5),a)
    same=np.equal.outer(cl,cl);rows=[]
    for frac in [0,.01,.05,.1,.25,.5,.75]:
        bb=(1-frac)*B+frac*B0;bb[same]=np.inf
        def risk(dose):return np.exp(-dose*bb).sum(1).max()
        hi=1.
        while risk(hi)>.005:hi*=2
        dose=brentq(lambda dd:risk(dd)-.005,1e-100,hi)
        rows.append({'fraction_of_total_dose_on_native_reference':frac,'total_sufficient_dose':float(dose),
                     'native_reference_dose':float(dose*frac),'after_dose':float(dose*(1-frac))})
    truthsets=[('covered_sigma01',False,'phonon4_sigma01'),('heldout_sigma0065_seed8021',True,'heldout065_seed8021')]
    truth_results=[]
    for label,own,tag in truthsets:
        ss,p,dd=load(tag,own=own);p=p.reshape(len(p),-1);native=p[ss.index(0)]
        for z in [0,.1,1,10]:
            for ii,h in enumerate(ss):
                after=p[ii];out=[]
                for jj,mh in enumerate(classes):
                    def derivative(w):
                        pa=r[jj]+w*delta[jj];pb=r[0]+w*delta[0]
                        return a*(np.sum(after*delta[jj]/pa)-delta[jj].sum()+z*(np.sum(native*delta[0]/pb)-delta[0].sum()))
                    if derivative(0)<=0:w=0.
                    elif derivative(1)>=0:w=1.
                    else:w=brentq(derivative,0,1)
                    pa=r[jj]+w*delta[jj];pb=r[0]+w*delta[0]
                    def kl(x,y):return a*np.sum(x*np.log(np.maximum(x,1e-300)/np.maximum(y,1e-300))-x+y)
                    out.append({'candidate_state':mh,'fitted_w':float(w),'joint_KL_per_after_dose':float(kl(after,pa)+z*kl(native,pb))})
                best=min(out,key=lambda x:x['joint_KL_per_after_dose']);correct=next(x for x in out if x['candidate_state']==h)
                truth_results.append({'truth':label,'true_state':h,'native_to_after_dose_ratio':z,
                                      'best_state':best['candidate_state'],'fitted_w':best['fitted_w'],
                                      'KL_best_per_after_dose':best['joint_KL_per_after_dose'],
                                      'KL_correct_per_after_dose':correct['joint_KL_per_after_dose'],
                                      'candidate_fits':out,'correct_asymptotic_label':best['candidate_state']==h})
    result={'scope':__doc__,'class_set':classes,'endpoint_family_unknown_nuisance_risk':rows,
            'continuous_joint_expected_count_results':truth_results,'elapsed_seconds':time.monotonic()-started,
            'nuisance_label_supplied':False,'calibration_reference_state':'Known native assumed; preparation and read survival not acquired.'}
    (ROOT/'outputs/joint_screen.json').write_text(json.dumps(result,indent=2))
    print('endpoint risk:',json.dumps(rows),flush=True)
    print('held-out:',json.dumps([{k:v for k,v in x.items() if k!='candidate_fits'} for x in truth_results if 'heldout' in x['truth']]),flush=True)
if __name__=='__main__':main()
