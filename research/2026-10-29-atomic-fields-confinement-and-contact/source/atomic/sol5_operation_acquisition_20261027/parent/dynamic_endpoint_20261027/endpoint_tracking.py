"""Source-template endpoint tracking; supplied dynamics, no physical claim."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='2'
from pathlib import Path
import hashlib,json,time
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[2]/'sol4_frontier_reset_20261027'/'depth_readout_interface'/'outputs'

def templates():
    data=[np.load(SOURCE/f'rigid256_state{s:02d}.npz') for s in (0,15,16)]
    raw=np.array([x['p'] for x in data],dtype=float); pairs=[(0,1),(0,2),(1,2)]
    b=np.array([.5*((np.sqrt(raw[i])-np.sqrt(raw[j]))**2).sum(-1) for i,j in pairs])
    pos=int(b.min(0).argmax()); full=raw[:,pos]
    score=(np.sqrt(full).max(0)-np.sqrt(full).min(0))**2/np.maximum(full.mean(0),1e-300)
    q=full[:,score>=.5]; edges=np.linspace(-6,6,33)
    x=np.digitize(np.log(np.maximum(q[1],1e-300)/np.maximum(q[0],1e-300)),edges)
    y=np.digitize(np.log(np.maximum(q[2],1e-300)/np.maximum(q[0],1e-300)),edges)
    _,code=np.unique(x*(len(edges)+1)+y,return_inverse=True)
    p=np.array([np.bincount(code,weights=r) for r in q]); p=p[:,p.sum(0)>0]
    b2=np.array([.5*((np.sqrt(p[i])-np.sqrt(p[j]))**2).sum() for i,j in pairs])
    meta={'states':['native','layer15','layer16'],'probe_index':pos,
          'probe_xy_angstrom':data[0]['positions'][pos].tolist(),
          'full_detection_probability':full.sum(1).tolist(),
          'retained_probability':p.sum(1).tolist(),'full_pair_B':b[:,pos].tolist(),
          'retained_pair_B':b2.tolist(),'retained_bins':p.shape[1],'score_threshold':.5,
          'source_sha256':{str(s):hashlib.sha256((SOURCE/f'rigid256_state{s:02d}.npz').read_bytes()).hexdigest() for s in (0,15,16)}}
    return p,float(b2.min()),meta

def kernel(kappa):
    return kappa*np.array([[-1.,.5,.5],[1.,-1.,0.],[1.,0.,-1.]])

def simulate(p,kappa,bmin,seed,n=2000,threshold=.995,latency_e=0.):
    rng=np.random.default_rng(seed); q=kernel(kappa); lam=p.sum(1); a=q-np.diag(lam)
    eigen,u=np.linalg.eig(a); inv=np.linalg.inv(u)
    assert abs(eigen.imag).max()<1e-12
    eigen=eigen.real; u=u.real; inv=inv.real
    check=max(float(abs((u*np.exp(eigen*d))@inv-expm(a*d)).max()) for d in (0.,1.,10.,100.,1000.,10000.))
    assert check<1e-10
    delay=expm(q*latency_e)
    means=np.zeros(n); last_click=np.zeros(n); state=rng.integers(0,3,n)
    posterior=np.full((n,3),1/3); static=np.zeros((n,3))
    clicks=np.zeros(n,dtype=int); moves=np.zeros(n,dtype=int)
    reported=np.full(n,-1,dtype=int); static_report=np.full(n,-1,dtype=int)
    true_end=np.full(n,-1,dtype=int); certainty=np.zeros(n)
    active=np.ones(n,dtype=bool); cdf=np.cumsum(p/p.sum(1)[:,None],axis=1); cdf[:,-1]=1.
    max_mean=100/bmin; loops=0
    while active.any():
        idx=np.flatnonzero(active); s=state[idx]
        dt=rng.exponential(1/(kappa+lam[s])); event_time=means[idx]+dt
        expired=event_time>max_mean
        if expired.any():
            z=idx[expired]; means[z]=max_mean; active[z]=False
        idx=idx[~expired]; event_time=event_time[~expired]
        if not len(idx): continue
        s=state[idx]; means[idx]=event_time
        observed=rng.random(len(idx))<lam[s]/(kappa+lam[s])
        z=idx[~observed]
        if len(z):
            old=state[z].copy(); state[z]=0; native=old==0
            state[z[native]]=rng.integers(1,3,native.sum()); moves[z]+=1
        idx=idx[observed]
        if not len(idx): continue
        elapsed=means[idx]-last_click[idx]
        transformed=posterior[idx]@u
        predicted=(transformed*np.exp(elapsed[:,None]*(eigen-eigen.max())))@inv
        assert predicted.min()>-1e-10
        predicted=np.maximum(predicted,0)
        mark=np.empty(len(idx),dtype=int); random=rng.random(len(idx))
        for s in range(3):
            hit=state[idx]==s; mark[hit]=np.searchsorted(cdf[s],random[hit])
        predicted*=p[:,mark].T; predicted/=predicted.sum(1)[:,None]
        posterior[idx]=predicted
        static[idx]+=-elapsed[:,None]*lam+np.log(np.maximum(p[:,mark].T,1e-300))
        last_click[idx]=means[idx]; clicks[idx]+=1
        final=predicted@delay; stop=final.max(1)>=threshold; z=idx[stop]
        if len(z):
            reported[z]=final[stop].argmax(1); certainty[z]=final[stop].max(1)
            static_report[z]=static[z].argmax(1)
            if latency_e:
                dc=np.cumsum(delay[state[z]],axis=1); dc[:,-1]=1.
                true_end[z]=(rng.random(len(z))[:,None]>dc).sum(1)
            else: true_end[z]=state[z]
            means[z]+=latency_e; active[z]=False
        loops+=1; assert loops<100000
    done=reported>=0
    return {'kappa':kappa,'kappa_over_B':kappa/bmin,'trajectories':n,'threshold':threshold,
            'latency_incident_mean':latency_e,'max_incident_mean':max_mean,
            'certified':int(done.sum()),'censored':int((~done).sum()),
            'errors':int((reported[done]!=true_end[done]).sum()),
            'static_errors_at_same_stops':int((static_report[done]!=true_end[done]).sum()),
            'mean_incident_mean':float(means.mean()),'mean_clicks':float(clicks.mean()),
            'mean_moves':float(moves.mean()),'certified_after_move':int((done&(moves>0)).sum()),
            'min_posterior':float(certainty[done].min()) if done.any() else None,
            'endpoint_labels':np.bincount(true_end[done],minlength=3).tolist(),
            'expm_check':check,'iterations':loops}

def main():
    start=time.monotonic(); p,bmin,meta=templates(); rows=[]
    for i,ratio in enumerate((.001,.01,.1,1.)):
        r=simulate(p,ratio*bmin,bmin,20261028+i); rows.append(r); print(json.dumps(r),flush=True)
    bounds=[]
    for ratio in (.001,.01,.1,1.):
        for delay_us in (10.,100.):
            e=20e-12/1.602176634e-19*delay_us*1e-6
            transition=expm(kernel(ratio*bmin)*e)
            bounds.append({'kappa_over_B':ratio,'blanker_delay_us':delay_us,
                           'incident_mean_at_20pA':e,'largest_transition_entry':float(transition.max()),
                           'target15_best_confidence':float(transition[:,1].max())})
    out={'scope':__doc__,'template':meta,'B_min':bmin,'runs':rows,'latency_bounds':bounds,
         'elapsed_seconds':time.monotonic()-start,
         'boundary':'Supplied3-state kernel, rigid templates, known current; no leakage/species loss/multiple defects/thermal uncertainty. Ordinary filter gets identical access. No calibrated rate or advantage.'}
    (ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n'); print('elapsed',out['elapsed_seconds'])

if __name__=='__main__': main()
