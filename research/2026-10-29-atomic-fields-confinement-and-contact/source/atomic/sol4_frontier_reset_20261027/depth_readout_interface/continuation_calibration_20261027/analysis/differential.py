"""Charged paired calibration with arbitrary shared native means.

Before mean: kb*b[k]. After mean: ka*(b[k]+delta_h[k](w)).
Each b[k] is unknown, w in [0,1] is inferred, and delta is the two-endpoint
training contrast family. Native/background labels and nuisance values are
not estimated by an oracle. Counts are split offline into independent Poisson
halves. Cross-fit split-likelihood confidence sets use ordinary universal
inference (Wasserman/Ramdas/Balakrishnan, PNAS 2020).
"""
from pathlib import Path
import argparse,json,time,math
import numpy as np
from scipy.optimize import brentq
from scipy.stats import beta
from paired_screen import load
ROOT=Path(__file__).resolve().parents[1]

def loglik(nb,na,mb,ma):
    return float(np.sum(nb*np.log(np.maximum(mb,1e-300))-mb+na*np.log(np.maximum(ma,1e-300))-ma))

def profile(nb,na,kb,ka,d0,d1):
    u=kb+ka;total=nb+na
    def evaluate(w):
        delta=d0+w*d1
        disc=(u*delta+nb-na)**2+4*nb*na
        b=(total-u*delta+np.sqrt(np.maximum(disc,0)))/(2*u)
        b=np.maximum(b,np.maximum(-delta,0))
        f=loglik(nb,na,kb*b,ka*(b+delta))
        gd=np.full_like(delta,-ka)
        positive=b+delta>1e-14
        gd[positive]=na[positive]/(b[positive]+delta[positive])-ka
        boundary=(~positive)&(delta<0)&(na==0)
        gd[boundary]=nb[boundary]/delta[boundary]+kb
        zero=(total==0)&(np.abs(delta)<1e-14)
        gd[zero]=0
        return f,float(gd@d1),b
    f0,g0,b0=evaluate(0.);f1,g1,b1=evaluate(1.)
    if np.max(np.abs(d1))<1e-18 or g0<=0:
        return {'score':f0,'upper':f0+1e-7,'w':0.,'b':b0,'delta':d0}
    if g1>=0:
        return {'score':f1,'upper':f1+1e-7,'w':1.,'b':b1,'delta':d0+d1}
    w=brentq(lambda x:evaluate(x)[1],0,1,xtol=1e-9)
    f,g,b=evaluate(w)
    # Supporting tangents to a concave profile provide a numerical upper
    # bound for the denominator maximum. Near kinks use both sides. Values
    # remain floating-point, not outward-rounded interval certificates.
    lines=[]
    for v in sorted(set([max(0.,w-1e-6),w,min(1.,w+1e-6)])):
        ff,gg,_=evaluate(v);lines.append((gg,ff-gg*v))
    candidates=[0.,1.]
    for i,(gi,ci) in enumerate(lines):
        for gj,cj in lines[i+1:]:
            if abs(gi-gj)>1e-14:
                x=(cj-ci)/(gi-gj)
                if 0<=x<=1:candidates.append(x)
    upper=max(min(gg*x+c for gg,c in lines) for x in candidates)+1e-7
    return {'score':f,'upper':max(upper,f+1e-7),'w':float(w),'b':b,'delta':d0+w*d1}

def grouped(p,codes,n):
    return np.asarray([np.bincount(codes,weights=x.ravel(),minlength=n) for x in p])

def interval(k,n):
    return [float(0 if k==0 else beta.ppf(.025,k,n-k+1)),float(1 if k==n else beta.ppf(.975,k+1,n-k))]

def run_case(name,true_label,pb,pa,models,classes,a,dose,ratio,ntrials,rng,alpha):
    before=dose*ratio/(1+ratio);after=dose/(1+ratio);kb=a*before/2;ka=a*after/2
    d0=models[0]-models[0,0];d1=(models[1]-models[1,0])-d0
    outcomes={'correct_singleton':0,'wrong_singleton':0,'empty_rejection':0,'ambiguous':0,'true_excluded':0,'forced_profile_MLE_errors':0}
    label_index=classes.index(true_label) if true_label in classes else None
    maxgap=0.;fitw=[]
    for rep in range(ntrials):
        nb0=rng.poisson(kb*pb);nb1=rng.poisson(kb*pb);na0=rng.poisson(ka*pa);na1=rng.poisson(ka*pa)
        fits0=[profile(nb0,na0,kb,ka,d0[i],d1[i]) for i in range(len(classes))]
        fits1=[profile(nb1,na1,kb,ka,d0[i],d1[i]) for i in range(len(classes))]
        j0=int(np.argmax([f['score'] for f in fits0]));j1=int(np.argmax([f['score'] for f in fits1]))
        def predictive(trainfits,best,trainb,traina,testb,testa):
            fit=trainfits[best]
            # Any positive predictive Poisson distribution gives a valid
            # numerator. Mix the fitted contrast prediction with a saturated
            # independent-stage prediction so unmodeled changes can reject.
            fam=loglik(testb,testa,kb*fit['b']+.5,ka*(fit['b']+fit['delta'])+.5)
            free=loglik(testb,testa,trainb+.5,traina+.5)
            return float(np.logaddexp(fam,free)-math.log(2))
        q0=predictive(fits1,j1,nb1,na1,nb0,na0);q1=predictive(fits0,j0,nb0,na0,nb1,na1)
        loge=np.logaddexp(q0-np.array([f['upper'] for f in fits0]),q1-np.array([f['upper'] for f in fits1]))-math.log(2)
        C=np.flatnonzero(loge<math.log(1/alpha))
        if len(C)==0:outcomes['empty_rejection']+=1
        elif len(C)>1:outcomes['ambiguous']+=1
        elif label_index is not None and C[0]==label_index:outcomes['correct_singleton']+=1
        else:outcomes['wrong_singleton']+=1
        if label_index is not None and label_index not in C:outcomes['true_excluded']+=1
        full=[profile(nb0+nb1,na0+na1,2*kb,2*ka,d0[i],d1[i]) for i in range(len(classes))]
        best=int(np.argmax([f['score'] for f in full]));fitw.append(full[best]['w'])
        if label_index is not None and best!=label_index:outcomes['forced_profile_MLE_errors']+=1
        maxgap=max(maxgap,max(f['upper']-f['score'] for f in fits0+fits1+full))
    frequencies={k:v/ntrials for k,v in outcomes.items()}
    if label_index is None:
        outcomes['forced_profile_MLE_errors']=None
        frequencies['forced_profile_MLE_errors']=None
    return {'truth':name,'true_label':true_label,'total_nominal_dose_e_per_angstrom2':dose,
            'before_dose':before,'after_dose':after,'native_to_after_ratio':ratio,'trials':ntrials,
            'counts':outcomes,'frequencies':frequencies,
            'forced_profile_MLE_error_counter_applicable':label_index is not None,
            'unsupported_MLE_point_reports':ntrials if label_index is None else 0,
            'correct_singleton_clopper_pearson_95':interval(outcomes['correct_singleton'],ntrials),
            'true_exclusion_clopper_pearson_95':interval(outcomes['true_excluded'],ntrials),
            'fitted_w_mean':float(np.mean(fitw)),'maximum_profile_upper_gap':maxgap,
            'incident_electrons':float(dose*45*a),'alpha':alpha}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bins',type=int,default=32);parser.add_argument('--trials',type=int,default=100)
    parser.add_argument('--doses',default='10000,30000,100000,300000');parser.add_argument('--ratios',default='1');parser.add_argument('--tag',default='pilot')
    parser.add_argument('--seed',type=int,default=719004)
    args=parser.parse_args();start=time.monotonic()
    data=np.load(ROOT/f'outputs/count_partition_{args.bins}.npz');codes=data['codes'];models=data['training_patterns'].reshape(2,5,-1)
    classes=data['class_labels'].tolist();a=float(data['scan_cell_area']);n=models.shape[-1]
    hs,hp,_=load('heldout065_seed8021',own=True);held=grouped(hp,codes,n)
    cases=[]
    for h in [0,15,16]:
        i=classes.index(h);cases.append(('covered_mix_w05',h,.5*(models[0,0]+models[1,0]),.5*(models[0,i]+models[1,i])))
        cases.append(('heldout_sigma0065_seed8021',h,held[hs.index(0)],held[hs.index(h)]))
    cases.append(('post_calibration_nuisance_drift_native',0,models[0,0],models[1,0]))
    two=list((ROOT/'outputs').glob('two_cr1516_sigma065_state*.npz'))
    if two:
        pp=np.load(two[0])['p'];pa=grouped(pp[None],codes,n)[0]
        cases.append(('unmodeled_two_cr15_16_sigma0065',-1,held[hs.index(0)],pa))
    rng=np.random.default_rng(args.seed);rows=[]
    for dose in [float(x) for x in args.doses.split(',')]:
        for ratio in [float(x) for x in args.ratios.split(',')]:
            for name,h,pb,pa in cases:
                out=run_case(name,h,pb,pa,models,classes,a,dose,ratio,args.trials,rng,.005)
                rows.append(out);print(json.dumps({k:v for k,v in out.items() if k in ['truth','true_label','total_nominal_dose_e_per_angstrom2','native_to_after_ratio','counts']}),flush=True)
    result={'scope':__doc__,'bins':args.bins,'class_set':classes,'rows':rows,'seed':args.seed,
            'elapsed_seconds':time.monotonic()-start,'source':'Actual multislice probabilities; exact independent Poisson counts aggregated by a training-only detector partition.',
            'coverage':'Exact procedure requires delta_truth=delta_h(w), shared static background, independent Poisson observations, known dose, and conservative null likelihood suprema. Computed profiles use floating-point supporting-tangent bounds, not interval certificates; numerical coverage is conditional on those bounds. Physical CrSBr coverage is not acquired.',
            'frozen_result_files_modified':False}
    (ROOT/f'outputs/differential_{args.tag}.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
