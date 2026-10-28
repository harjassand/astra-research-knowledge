#!/usr/bin/env python3
"""Prespecified source-volume GC launches, with passing and trapped classes.

This integrates the source-chart Hamiltonian first-order guiding-center model,
not full Lorentz motion and not a plasma.  Loss means first exit from Q<1.
"""
from pathlib import Path
import numpy as np,json,time
from lopez_native import embedding,h_analytic,field_labels,gc_label_rhs,Q
ROOT=Path(__file__).resolve().parent


def launches():
    positions=[(.15,.02,'axis')]
    for r in (.4,.7):
        for a in np.arange(4)*np.pi/2:
            positions.append((.15+r*np.cos(a)/30,.02+r*np.sin(a)/10,f'r{r:g}_a{a:g}'))
    rows=[];pgrid=np.arange(2048)*2*np.pi/2048
    for lam,beta,name in positions:
        for phi in np.arange(4)*np.pi/2:
            b0=1/h_analytic(lam,beta,phi)
            for kap in (0,.03,.06,.1):
                for sign in (-1,1):
                    rows.append({'labels':[lam,beta,float(phi)],'vparallel':float(sign*np.sqrt(1-kap*b0)),'mu':kap/2,
                                 'class':'uniform_passing','kappa':kap,'position':name,'parallel_sign':sign})
        strength=1/h_analytic(lam,beta,pgrid);bmin=float(strength.min());bmax=float(strength.max());phi=float(pgrid[np.argmin(strength)])
        for depth in (.2,.5,.8):
            bm=bmin+depth*(bmax-bmin);mu=.5/bm
            for sign in (-1,1):
                rows.append({'labels':[lam,beta,phi],'vparallel':float(sign*np.sqrt(1-bmin/bm)),'mu':mu,
                             'class':'initially_trapped','mirror_depth_fraction':depth,'position':name,'parallel_sign':sign,
                             'initial_line_Bmin':bmin,'initial_line_Bmax':bmax})
    return rows


def rhs(y,mu,eps):
    q,v=gc_label_rhs(y[:,:3],y[:,3],mu,eps)
    return np.column_stack((q,v))


def integrate(rows,epsilon,dt=.005,tmax=100):
    n=len(rows);y=np.array([r['labels']+[r['vparallel']] for r in rows]);mu=np.array([r['mu'] for r in rows])
    alive=np.ones(n,bool);loss=np.full(n,np.nan);bounces=np.zeros(n,int);energy=np.zeros(n);eta=np.zeros(n)
    exitlabels=np.full((n,3),np.nan);t=0.;step=0;start=time.monotonic()
    while alive.any() and t<tmax-1e-12:
        ix=np.flatnonzero(alive);z=y[ix];m=mu[ix];d=min(dt,tmax-t)
        k1=rhs(z,m,epsilon);k2=rhs(z+d*k1/2,m,epsilon);k3=rhs(z+d*k2/2,m,epsilon);k4=rhs(z+d*k3,m,epsilon)
        nxt=z+d*(k1+2*k2+2*k3+k4)/6
        bounces[ix]+=(z[:,3]*nxt[:,3]<0)
        en=.5*nxt[:,3]**2+m/h_analytic(nxt[:,0],nxt[:,1],nxt[:,2]);energy[ix]=np.maximum(energy[ix],abs(en-.5)/.5)
        qq=Q(nxt[:,0],nxt[:,1]);gone=qq>=1
        if gone.any():
            old=Q(z[gone,0],z[gone,1]);frac=(1-old)/(qq[gone]-old)
            loss[ix[gone]]=t+d*frac;exitlabels[ix[gone]]=z[gone,:3]+frac[:,None]*(nxt[gone,:3]-z[gone,:3]);alive[ix[gone]]=False
        y[ix]=nxt;t+=d;step+=1
        if step%200==0:
            ids=np.flatnonzero(alive)
            if len(ids):
                q=y[ids,:3];B,dB=field_labels(q[:,0],q[:,1],q[:,2],True);mag=np.linalg.norm(B,axis=1);unit=B/mag[:,None]
                grad=np.einsum('nij,ni->nj',dB,unit)
                eta[ids]=np.maximum(eta[ids],epsilon*np.linalg.norm(grad,axis=1)/mag**2)
    results=[]
    for i,row in enumerate(rows):
        results.append(dict(row,epsilon=epsilon,lost=bool(not alive[i]),loss_time=float(loss[i]) if not alive[i] else None,
                            bounce_count=int(bounces[i]),max_relative_energy_error=float(energy[i]),max_magnetization_parameter=float(eta[i]),
                            exit_labels=exitlabels[i].tolist() if not alive[i] else None,final_labels=y[i,:3].tolist()))
    summary=[]
    for kind in ('uniform_passing','initially_trapped'):
        rr=[r for r in results if r['class']==kind];lt=[r['loss_time'] for r in rr if r['lost']]
        summary.append({'class':kind,'count':len(rr),'lost_count':len(lt),'maximum_loss_time':max(lt,default=None),
                        'minimum_loss_time':min(lt,default=None),'median_loss_time':float(np.median(lt)) if lt else None,
                        'bouncing_count':sum(r['bounce_count']>0 for r in rr),'max_relative_energy_error':max(r['max_relative_energy_error'] for r in rr),
                        'max_magnetization_parameter':max(r['max_magnetization_parameter'] for r in rr)})
    return {'epsilon':epsilon,'dt':dt,'tmax':tmax,'integrated_to':t,'steps':step,'runtime_seconds':time.monotonic()-start,'summary':summary,'orbits':results}


def main():
    rows=launches();out=[]
    for eps in (.004,.002):
        r=integrate(rows,eps,dt=.005,tmax=.4/eps);out.append(r);print(json.dumps({k:v for k,v in r.items() if k!='orbits'}),flush=True)
    # Time-step convergence uses the same declared launches at epsilon .004.
    refined=integrate(rows,.004,dt=.0025,tmax=100);out.append(refined)
    print(json.dumps({k:v for k,v in refined.items() if k!='orbits'}),flush=True)
    a=np.array([r['loss_time'] if r['lost'] else np.nan for r in out[0]['orbits']]);b=np.array([r['loss_time'] if r['lost'] else np.nan for r in refined['orbits']]);both=np.isfinite(a)&np.isfinite(b)
    result={'status':'FINITE_FIRST_ORDER_GC_DIAGNOSTIC','launch_count':len(rows),'runs':out,
            'convergence':{'matching_loss_flags':all(x['lost']==y['lost'] for x,y in zip(out[0]['orbits'],refined['orbits'])),
                           'max_absolute_loss_time_change':float(np.max(abs(a[both]-b[both]))) if both.any() else None,
                           'max_relative_loss_time_change':float(np.max(abs(a[both]-b[both])/b[both])) if both.any() else None},
            'scope':'Exactly declared launches and first-order guiding-center model; deterministic coverage is not a probability estimate or all-initial-condition physical theorem. No electric fields, collisions, plasma currents or coil errors.'}
    (ROOT/'guiding_center_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result['convergence']),flush=True)


if __name__=='__main__':main()
