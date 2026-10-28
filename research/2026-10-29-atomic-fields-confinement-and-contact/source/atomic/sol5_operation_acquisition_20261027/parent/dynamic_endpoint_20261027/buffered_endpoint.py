"""Charge delayed shutoff and use all late counts for endpoint heralding."""
from endpoint_tracking import templates,kernel,ROOT
import json,time
import numpy as np

def run(p,kappa,bmin,delay,n=2000,seed=3391,threshold=.995):
    rng=np.random.default_rng(seed); lam=p.sum(1); a=kernel(kappa)-np.diag(lam)
    ev,u=np.linalg.eig(a); inv=np.linalg.inv(u); ev=ev.real; u=u.real; inv=inv.real
    def predict(rows,dt):
        z=((rows@u)*np.exp(dt[:,None]*(ev-ev.max())))@inv
        assert z.min()>-1e-10
        z=np.maximum(z,0); return z/z.sum(1)[:,None]
    clock=np.zeros(n); last=np.zeros(n); state=rng.integers(0,3,n)
    post=np.full((n,3),1/3); active=np.ones(n,bool); off=np.full(n,np.inf)
    initial_report=np.full(n,-1,int); final_report=np.full(n,-1,int); truth=np.full(n,-1,int)
    confidence=np.zeros(n); clicks=np.zeros(n,int); moves=np.zeros(n,int)
    cdf=np.cumsum(p/lam[:,None],axis=1); cdf[:,-1]=1.
    deadline=100/bmin; iterations=0
    while active.any():
        ix=np.flatnonzero(active); s=state[ix]
        event=clock[ix]+rng.exponential(1/(kappa+lam[s]))
        forced=np.isinf(off[ix])&(event>deadline); off[ix[forced]]=deadline+delay
        ended=event>off[ix]; z=ix[ended]
        if len(z):
            end=predict(post[z],off[z]-last[z]); confidence[z]=end.max(1)
            certified=confidence[z]>=threshold
            final_report[z[certified]]=end[certified].argmax(1)
            truth[z]=state[z]; clock[z]=off[z]; active[z]=False
        ix=ix[~ended]; event=event[~ended]
        if not len(ix): continue
        s=state[ix]; clock[ix]=event
        observed=rng.random(len(ix))<lam[s]/(kappa+lam[s]); z=ix[~observed]
        if len(z):
            old=state[z].copy(); state[z]=0; native=old==0
            state[z[native]]=rng.integers(1,3,native.sum()); moves[z]+=1
        ix=ix[observed]
        if not len(ix): continue
        pred=predict(post[ix],clock[ix]-last[ix]); mark=np.empty(len(ix),int)
        uniform=rng.random(len(ix))
        for s in range(3):
            hit=state[ix]==s; mark[hit]=np.searchsorted(cdf[s],uniform[hit])
        pred*=p[:,mark].T; pred/=pred.sum(1)[:,None]
        post[ix]=pred; last[ix]=clock[ix]; clicks[ix]+=1
        trigger=np.isinf(off[ix])&(pred.max(1)>=threshold)
        z=ix[trigger]; off[z]=clock[z]+delay; initial_report[z]=pred[trigger].argmax(1)
        iterations+=1; assert iterations<100000
    certified=final_report>=0; triggered=initial_report>=0
    return {'kappa_over_B':kappa/bmin,'delay_incident_mean':delay,'trajectories':n,
            'triggered_before_deadline':int(triggered.sum()),'certified_final':int(certified.sum()),
            'uncertified_final':int((~certified).sum()),
            'wrong_final_reports':int((final_report[certified]!=truth[certified]).sum()),
            'pre_delay_report_wrong_at_end':int((initial_report[triggered]!=truth[triggered]).sum()),
            'certified_end_label_differs_from_trigger':int((certified&triggered&(final_report!=initial_report)).sum()),
            'final_labels':np.bincount(final_report[certified],minlength=3).tolist(),
            'mean_incident_mean':float(clock.mean()),'mean_moves':float(moves.mean()),
            'mean_clicks':float(clicks.mean()),'minimum_final_posterior':float(confidence[certified].min()) if certified.any() else None}

def main():
    start=time.monotonic(); p,bmin,meta=templates(); rows=[]
    delay=20e-12/1.602176634e-19*100e-6
    for i,ratio in enumerate((.01,.1,1.)):
        r=run(p,ratio*bmin,bmin,delay,seed=20261029+i); rows.append(r); print(json.dumps(r),flush=True)
    out={'scope':__doc__,'runs':rows,'template_B_min':bmin,'elapsed_seconds':time.monotonic()-start,
         'boundary':'Supplied3-state kernel and rigid templates. Late data including no-click survival available through timestamped beamoff. Conditional heralding, not precommitted target preparation or physical validation.'}
    (ROOT/'BUFFERED_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n'); print(out['elapsed_seconds'])

if __name__=='__main__': main()
