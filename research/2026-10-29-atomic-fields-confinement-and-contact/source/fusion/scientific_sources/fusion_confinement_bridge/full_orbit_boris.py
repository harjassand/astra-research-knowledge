#!/usr/bin/env python3
"""Full Lorentz tests in the unperturbed explicit López field.

Dimensionless dx/dt=v, dv/dt=v cross B/epsilon; |v|=1 initially.
Boris drift/rotate/drift is energy-preserving for this magnetic-only problem.
Each orbit terminates at its FIRST source-domain exit Q=1.  Root continuation
follows the prescribed root and does not select a new min-Q root after exit.
"""
from pathlib import Path
import numpy as np,json,time
from lopez_native import embedding,field_labels,field_known_root,root_continue,label_data,h_analytic
ROOT=Path(__file__).resolve().parent


def rotate(v,b,dt,eps):
    t=b*(dt/(2*eps));s=2*t/(1+np.sum(t*t,axis=1))[:,None]
    return v+np.cross(v+np.cross(v,t),s)


def build_launches(eps,gyro_count=4):
    rows=[];xx=[];vv=[];zz=[]
    for phase in np.arange(4)*np.pi/2:
        R=embedding(.15,.02,phase);B=field_labels(.15,.02,phase);mag=np.linalg.norm(B);b=B/mag
        n=np.array([2*np.sqrt(.15)*np.cos(phase),2*np.sqrt(.15)*np.sin(phase),.15-1])/1.15
        e2=np.cross(b,n)
        for kap in (0,.06,.1):
            for sign in (-1,1):
                for gamma in ([0] if kap==0 else np.arange(gyro_count)*2*np.pi/gyro_count):
                    perp=np.sqrt(kap*mag)*(np.cos(gamma)*n+np.sin(gamma)*e2)
                    v=sign*np.sqrt(1-kap*mag)*b+perp
                    x=R+eps/mag*np.cross(b,perp)
                    z,res=root_continue(x,np.sqrt(.15)*np.exp(1j*phase))
                    lam,beta,q=label_data(x,z)
                    assert q<1 and res<1e-12
                    rows.append({'phase':float(phase),'kappa':kap,'parallel_sign':sign,'gyro_phase':float(gamma),
                                 'gc_initial_labels':[.15,.02,float(phase)],'initial_particle_Q':float(q)})
                    xx.append(x);vv.append(v);zz.append(z)
    return rows,np.array(xx),np.array(vv),np.array(zz)


def run(eps,phase_step=.16,gyro_count=4,tmax=100):
    rows,x,v,z=build_launches(eps,gyro_count);n=len(rows)
    # Directed action geometry enclosure supplies B<=1/.14881660 in Q<=1.
    b_bound=1/.1488166013419809;dt=phase_step*eps/b_bound
    live=np.ones(n,bool);loss=np.full(n,np.nan);exitbeta=np.full(n,np.nan);maxenergy=np.zeros(n);maxmu=np.zeros(n)
    rooterror=0.;fallback=0;step=0;t=0.;start=time.monotonic();lastprogress=start
    while live.any() and t<tmax-1e-12:
        ids=np.flatnonzero(live);oldx=x[ids];oldv=v[ids];oldz=z[ids];d=min(dt,tmax-t)
        half=oldx+oldv*d/2
        zh,res=root_continue(half,oldz,iterations=3)
        if np.max(res)>1e-11:
            zh,res=root_continue(half,zh,iterations=6);fallback+=1
        rooterror=max(rooterror,float(np.max(res)))
        B=field_known_root(half,zh)
        nv=rotate(oldv,B,d,eps);nx=half+nv*d/2
        nz,res=root_continue(nx,zh,iterations=3)
        if np.max(res)>1e-11:
            nz,res=root_continue(nx,nz,iterations=6);fallback+=1
        rooterror=max(rooterror,float(np.max(res)))
        lam,beta,q=label_data(nx,nz);_,_,oldq=label_data(oldx,oldz)
        gone=q>=1
        if gone.any():
            frac=(1-oldq[gone])/(q[gone]-oldq[gone]);loss[ids[gone]]=t+d*frac
            _,oldbeta,_=label_data(oldx[gone],oldz[gone]);exitbeta[ids[gone]]=oldbeta+frac*(beta[gone]-oldbeta)
            live[ids[gone]]=False
        x[ids]=nx;v[ids]=nv;z[ids]=nz
        maxenergy[ids]=np.maximum(maxenergy[ids],abs(np.sum(nv*nv,axis=1)-1))
        if step%100==0:
            Bnow=field_known_root(nx,nz);mag=np.linalg.norm(Bnow,axis=1);unit=Bnow/mag[:,None]
            vpar=np.sum(nv*unit,axis=1);mu=(np.sum(nv*nv,axis=1)-vpar*vpar)/(2*mag)
            target=np.array([rows[i]['kappa']/2 for i in ids]);maxmu[ids]=np.maximum(maxmu[ids],abs(mu-target))
        t+=d;step+=1
        if time.monotonic()-lastprogress>20:
            print(json.dumps({'epsilon':eps,'phase_step':phase_step,'time':t,'alive':int(live.sum()),'steps':step}),flush=True);lastprogress=time.monotonic()
    gc=json.loads((ROOT/'guiding_center_results.json').read_text())
    source=next(r for r in gc['runs'] if r['epsilon']==eps and r['dt']==.005)
    out=[]
    for i,row in enumerate(rows):
        match=next(g for g in source['orbits'] if g['position']=='axis' and g['class']=='uniform_passing'
                   and abs(g['labels'][2]-row['phase'])<1e-10 and g['kappa']==row['kappa'] and g['parallel_sign']==row['parallel_sign'])
        out.append(dict(row,epsilon=eps,lost=bool(not live[i]),loss_time=float(loss[i]) if not live[i] else None,
                        gc_loss_time=match['loss_time'],relative_exit_time_difference_from_GC=float((loss[i]-match['loss_time'])/match['loss_time']) if not live[i] else None,
                        exit_beta=float(exitbeta[i]) if not live[i] else None,max_relative_energy_error=float(maxenergy[i]),max_absolute_mu_deviation=float(maxmu[i])))
    lt=[r['loss_time'] for r in out if r['lost']]
    summary={'epsilon':eps,'phase_step':phase_step,'dt':dt,'launch_count':n,'lost_count':len(lt),'integrated_to':t,'steps':step,
             'maximum_loss_time':max(lt,default=None),'minimum_loss_time':min(lt,default=None),'median_loss_time':float(np.median(lt)) if lt else None,
             'max_relative_loss_time_difference_from_GC':max((abs(r['relative_exit_time_difference_from_GC']) for r in out if r['lost']),default=None),
             'max_relative_energy_error':float(max(maxenergy)),'max_root_error_estimate':rooterror,'root_refinement_fallbacks':fallback,
             'runtime_seconds':time.monotonic()-start}
    print(json.dumps(summary),flush=True)
    return {'summary':summary,'orbits':out}


def uniform_field_check():
    eps=.004;dt=.0001;b=np.array([[0.,0.,2.]])
    x=np.zeros((1,3));v=np.array([[1.,0.,.2]])/np.sqrt(1.04)
    center=x+eps/2*np.cross(v,np.array([[0.,0.,1.]]));transverse=center[0,:2].copy();err=0
    for k in range(10000):
        half=x+v*dt/2;v=rotate(v,b,dt,eps);x=half+v*dt/2
        cen=x+eps/2*np.cross(v,np.array([[0.,0.,1.]]));err=max(err,float(np.linalg.norm(cen[0,:2]-transverse)))
    return {'uniform_field_center_error':err,'uniform_field_speed_squared_error':float(abs(np.sum(v*v)-1)),'steps':10000}


def main():
    checks=uniform_field_check();runs=[]
    # The full passing ensemble has four toroidal phases, three pitch values,
    # both directions, and four gyro phases whenever perpendicular speed !=0.
    for eps,step,gyros in [(.004,.16,4),(.002,.16,4),(.004,.08,2)]:
        runs.append(run(eps,step,gyros,tmax=.2/eps))
        (ROOT/'full_orbit_results.json').write_text(json.dumps({'status':'FINITE_FULL_LORENTZ_DIAGNOSTIC','uniform_field_check':checks,'runs':runs,
            'scope':'Specified deterministic positive-charge, magnetic-only full Lorentz launches. Loss is first exit of source-certified Q<1, not escape from an unspecified global field. No collisions, plasma response or coil error is included.'},indent=2))


if __name__=='__main__':main()
