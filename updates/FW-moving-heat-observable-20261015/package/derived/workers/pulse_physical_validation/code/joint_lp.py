"""Exploratory joint-domain minimax feasibility with unknown pulse amplitude.

Same positive-RC class as the supplied packet, including both compact endpoints.
EIS-only observation budget is 0.1 mOhm. The voltage pulse budget is varied.
rho=1/I is a fitted nuisance parameter: B*x is compared with rho*dV.
For a fixed voltage error e, |B*x-rho*dV| <= rho*e is linear.
Grid feasibility is only a construction; grid infeasibility is not a continuum
certificate. Never label these LP results physical validation.
"""
from pathlib import Path
import sys, time, json
import numpy as np
from scipy.optimize import linprog
from audit_data import load, pulse_info

BASE=Path(__file__).resolve().parents[1]
SRC=BASE.parents[1]/'sources/astra_pulse_observable/code'
sys.path.insert(0,str(SRC))
from compact_model import features, target

def step_matrix(s,t,on,off):
    """Voltage per amp for a rectangular pulse away from switching instants."""
    t=np.asarray(t); out=np.zeros((len(t),len(s)))
    before=(t>on)&(t<off); after=t>off
    if np.any(before): out[before]=np.array([target(s,u) for u in t[before]-on])
    if np.any(after):
        # Numerically stable difference at slow endpoint. For interior tau:
        # (1-e^-T/tau)e^-(t-off)/tau / w, endpoint R_inf -> 0, cap -> a*T/cinf.
        a=2*np.pi*.01; r=100.; q=1-s
        x=np.divide(s,q,out=np.zeros_like(s),where=q!=0)
        tau=x/a
        w=np.zeros_like(x); inside=(s>0)&(s<1)
        w[inside]=(1+x[inside])/(1+x[inside]**2)-x[inside]/(1+r*r*x[inside]**2)
        block=np.zeros((after.sum(),len(s)))
        dur=off-on
        block[:,inside]=(-np.expm1(-dur/tau[inside])/w[inside])[None,:]*np.exp(-(t[after]-off)[:,None]/tau[inside][None,:])
        block[:,-1]=a*dur/(1-r**-2)
        out[after]=block
    return out

def select(t,info):
    # 0.1s pulse samples retained; relaxed log-spaced sampling thereafter.
    ix=list(range(info['on_index'],info['off_index']-1))
    after=np.flatnonzero(t>info['assumed_off_s']+.3)
    if len(after):
        targets=np.geomspace(.3,t[-1]-info['assumed_off_s'],85)+info['assumed_off_s']
        ix.extend(np.unique(np.searchsorted(t,targets).clip(0,len(t)-1)).tolist())
    return np.unique(ix)

def solve(n=800,which='pos',fmax=1000.,zero_initial=True):
    z,p,o=load(); f=z['f'][0]; use=f<=fmax; f=f[use]
    y=np.r_[z['Z_real'][0,use],z['Z_imag'][0,use]]*1000
    x=np.geomspace(1e-9,1e9,n); s=np.r_[0.,x/(1+x),1.]
    F=features(s,f); A=np.vstack([F.real,F.imag]);
    A=np.column_stack([A,np.r_[np.zeros(len(f)),f/f.max()]])
    epi=.1; As=np.r_[A,-A]; bs=np.r_[y+epi,-y+epi]
    blocks=[]; volts=[]; labels=[]; infos={sign:pulse_info(p,sign) for sign in ['pos','neg']}
    pp=infos['pos']; gap=pp['t'][-1]
    for sign in (['pos','neg'] if which=='both' else [which]):
        info=infos[sign]; ix=select(info['t'],info); t=info['t'][ix]
        B=step_matrix(s,t,info['assumed_on_s'],info['assumed_off_s'])
        v=info['direction']*(info['v'][ix]-info['baseline_V'])*1000
        if sign=='neg':
            # Prior positive pulse still contributes; subtract its value at the
            # negative baseline so data and prediction use the same baseline.
            older=step_matrix(s,t+gap,pp['assumed_on_s'],pp['assumed_off_s'])
            old0=step_matrix(s,np.array([gap]),pp['assumed_on_s'],pp['assumed_off_s'])[0]
            B-=older-old0
        B=np.column_stack([B,np.zeros(len(t))])
        blocks.append(B); volts.append(v); labels.extend([(sign,int(k)) for k in ix])
    B=np.vstack(blocks); v=np.concatenate(volts)
    # rho units A^-1, unknown positive common pulse amplitude.
    ncoef=A.shape[1]
    bounds=[(0,None)]*(ncoef-1)+[(None,None),(1e-4,100)]
    def feasible(e):
        eis=np.column_stack([As,np.zeros(len(As))])
        C=np.r_[eis,np.column_stack([B,-(v+e)]),np.column_stack([-B,v-e])]
        b=np.r_[bs,np.zeros(2*len(v))]
        return linprog(np.zeros(ncoef+1),A_ub=C,b_ub=b,bounds=bounds,method='highs-ds',
            options={'primal_feasibility_tolerance':1e-8,'dual_feasibility_tolerance':1e-8})
    lo=0.; hi=20.; last=feasible(hi)
    if not last.success: return {'status':'infeasible even at 20 mV', 'solver':last.message}
    for _ in range(24):
        mid=(lo+hi)/2; rr=feasible(mid)
        if rr.success: hi=mid; last=rr
        else: lo=mid
    coeff=last.x[:-1]; rho=last.x[-1]; pred=B@coeff/rho
    out={'status':'EXPLORATORY_FINITE_GRID','which':which,'n_nodes':len(s),
         'fmax_Hz':fmax,'EIS_component_budget_mOhm':epi,
         'pulse_min_uniform_error_bracket_mV':[lo,hi],
         'inverse_amplitude_fitted_per_A':rho,'amplitude_inferred_A':1/rho,
         'frequency_max_error_mOhm':float(abs(A@coeff-y).max()),
         'pulse_max_error_mV':float(abs(pred-v).max()),
         'Q10_mOhm':float(np.r_[target(s,10),0]@coeff),
         'Q1000_mOhm':float(np.r_[target(s,1000),0]@coeff),
         'physical_validation':False,
         'contract':'zero initial relaxation; commanded 10s ideal rectangular charge then discharge with unknown common magnitude; inferred voltage switching times; included known first-pulse memory; forced OCV already part of the supplied capacitive+RC total-response class; baseline fixed to observed median before each pulse'}
    name=f'{which}_n{n}_f{int(fmax)}'
    np.savez_compressed(BASE/f'results/joint_lp_{name}_witness.npz',s=s,coef=coeff,rho=rho,
        F=A,y=y,B=B,v=v,pred_mV=pred,labels=np.array(labels,dtype=object))
    return out

def main():
    t0=time.perf_counter(); rows=[]
    for n in [500,1200]:
        for which in ['pos','neg','both']:
            r=solve(n,which); rows.append(r); print(json.dumps(r),flush=True)
    (BASE/'results/joint_lp.json').write_text(json.dumps({'runs':rows,
        'elapsed_s':time.perf_counter()-t0,'continuum_infeasibility_proven':False,
        'matched_information':'Both-domain LP comparator uses all stated EIS observations and selected pulse samples, fits common unknown amplitude, has no smoothing penalty and no fixed relaxation cutoff (compact endpoints included).'},indent=2))

if __name__=='__main__': main()
