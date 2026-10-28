#!/usr/bin/env python3
"""Declared phase/pitch coverage in the source's irrational paraboloidal member.

The boundary is our psi=psi_axis+.2 diagnostic tube, not an acquired device
wall or a published largest torus. Domain restrictions are independently
monitored. The ensemble is deterministic, not a probability sample.
"""
from pathlib import Path
import json,time
import numpy as np
import sengupta_paraboloid as s
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent
SHIFT=.2


def radial_label(z,theta,shift):
    def q(r):return np.array([s.U0+r*np.cos(theta),r*np.sin(theta),z])
    hi=.01
    while s.surface_label(q(hi))<s.PSI0+shift and s.regular(q(hi)):hi*=1.25
    assert s.regular(q(hi))
    rr=brentq(lambda r:s.surface_label(q(r))-s.PSI0-shift,0,hi,xtol=1e-13)
    return q(rr)


def geometry():
    zs=np.linspace(0,2*np.pi,4097)
    axis=np.column_stack((np.full(len(zs),s.U0),np.zeros(len(zs)),zs));axisdata=s.data(axis)
    length=np.trapezoid(np.linalg.norm(axisdata['J'][:,:,2],axis=1),zs)
    Bmean=np.trapezoid(axisdata['strength']*np.linalg.norm(axisdata['J'][:,:,2],axis=1),zs)/length
    boundary=np.array([radial_label(z,t,SHIFT) for z in np.arange(64)*2*np.pi/64 for t in np.arange(64)*2*np.pi/64])
    bd=s.data(boundary);axisat=boundary.copy();axisat[:,0]=s.U0;axisat[:,1]=0
    distances=np.linalg.norm(s.embedding(boundary)-s.embedding(axisat),axis=1)
    amin=float(distances.min());eps=.005*Bmean*amin
    return {'axis_length':float(length),'arclength_mean_axis_B':float(Bmean),'sampled_minimum_local_boundary_distance':amin,
            'epsilon':float(eps),'nominal_rho_over_sampled_radius':.005,'boundary_sample_count':len(boundary),
            'sampled_minimum_regular_margin_u_minus_abs_v':float(np.min(boundary[:,0]-abs(boundary[:,1]))),
            'sampled_maximum_scaled_profile_coordinate':float(np.max(abs(np.column_stack((s.KAPPA*(boundary[:,0]-s.U0),s.KAPPA*boundary[:,1]))))),
            'sampled_minimum_D':float(bd['D'].min()),'sampled_B_range':[float(bd['strength'].min()),float(bd['strength'].max())],
            'boundary_certification':'Dense finite geometry diagnostic; not a directed enclosure or a proof of the complete tube.'}


def launches():
    rows=[]
    # Four distinct mirror phases; the initial 0,pi/2,pi,3pi/2 diagnostic
    # accidentally sampled the same high-field axis phase. It is preserved
    # separately in sengupta_ensemble_initial.json, not silently discarded.
    for z in np.arange(4)*np.pi/8:
        positions=[('axis',np.array([s.U0,0,z]))]
        for r in (.4,.7):
            for t in np.arange(4)*np.pi/2:positions.append((f'r{r}_theta{t}',radial_label(z,t,SHIFT*r*r)))
        for name,q in positions:
            B=float(s.data(q)['strength'])
            for pitch in (0,.05,.2,.5,.8,.95):
                for sign in (-1,1):
                    rows.append({'position':name,'labels':list(q),'perpendicular_speed_squared_fraction':pitch,
                        'parallel_sign':sign,'mu':pitch/(2*B),'vparallel':sign*np.sqrt(1-pitch)})
    return rows


def rhs(y,mu,eps):
    dq,dv=s.gc_rhs(y[:,:3],y[:,3],mu,eps)
    return np.column_stack((dq,dv))


def run(dt=.01,transits=50,subset=None,geom=None):
    geom=geometry() if geom is None else geom
    rows=launches();rows=rows if subset is None else [rows[i] for i in subset]
    eps=geom['epsilon'];tmax=transits*geom['axis_length'];n=len(rows)
    y=np.array([r['labels']+[r['vparallel']] for r in rows]);mu=np.array([r['mu'] for r in rows])
    live=np.ones(n,bool);lost=np.zeros(n,bool);invalid=np.zeros(n,bool);exit_time=np.full(n,np.nan)
    bounces=np.zeros(n,int);energy=np.zeros(n);minshift=np.full(n,np.inf);maxshift=np.zeros(n);maxeta=np.zeros(n)
    t=0.;step=0;start=time.monotonic();last=start
    while live.any() and t<tmax-1e-12:
        ids=np.flatnonzero(live);old=y[ids].copy();m=mu[ids];d=min(dt,tmax-t)
        k1=rhs(old,m,eps);k2=rhs(old+.5*d*k1,m,eps);k3=rhs(old+.5*d*k2,m,eps);k4=rhs(old+d*k3,m,eps)
        new=old+d*(k1+2*k2+2*k3+k4)/6
        shift=s.surface_label(new[:,:3])-s.PSI0;oldshift=s.surface_label(old[:,:3])-s.PSI0
        bad=~s.regular(new[:,:3]);gone=shift>=SHIFT
        if gone.any():
            lossids=ids[gone];lost[lossids]=True
            exit_time[lossids]=t+d*(SHIFT-oldshift[gone])/(shift[gone]-oldshift[gone])
        invalid[ids[bad]]=True;live[ids[gone|bad]]=False
        vals=s.data(new[:,:3],True)
        energy[ids]=np.maximum(energy[ids],abs(new[:,3]**2+2*m*vals['strength']-1))
        bounces[ids]+=(new[:,3]*old[:,3]<0)
        minshift[ids]=np.minimum(minshift[ids],shift);maxshift[ids]=np.maximum(maxshift[ids],shift)
        eta=eps*np.linalg.norm(vals['grad_strength'],axis=1)/vals['strength']**2
        maxeta[ids]=np.maximum(maxeta[ids],eta)
        y[ids]=new;t+=d;step+=1
        if time.monotonic()-last>20:
            print(json.dumps({'family':'Sengupta paraboloid','dt':dt,'axis_transits':t/geom['axis_length'],'live':int(live.sum()),'steps':step}),flush=True);last=time.monotonic()
    out=[]
    for i,row in enumerate(rows):
        out.append(dict(row,lost=bool(lost[i]),invalid=bool(invalid[i]),exit_time=float(exit_time[i]) if lost[i] else None,
            parallel_sign_changes=int(bounces[i]),minimum_normalized_label_shift=float(minshift[i]/SHIFT),maximum_normalized_label_shift=float(maxshift[i]/SHIFT),
            max_relative_energy_error=float(energy[i]),max_local_magnetization_parameter=float(maxeta[i]),final_labels=list(y[i,:3])))
    summary={'dt':dt,'axis_transits':transits,'integrated_time':t,'launch_count':n,'tube_exit_count':int(lost.sum()),'regularity_failure_count':int(invalid.sum()),
        'bounce_count_orbits':int(np.sum(bounces>0)),'max_relative_energy_error':float(energy.max()),'max_local_magnetization_parameter':float(maxeta.max()),
        'minimum_exit_time':float(np.nanmin(exit_time)) if lost.any() else None,'maximum_exit_time':float(np.nanmax(exit_time)) if lost.any() else None,
        'runtime_seconds':time.monotonic()-start,'steps':step}
    print(json.dumps(summary),flush=True)
    return {'summary':summary,'orbits':out}


def main():
    geom=geometry();rows=launches();mainrun=run(geom=geom)
    result={'status':'FINITE_FIRST_ORDER_GUIDING_CENTER_DIAGNOSTIC','geometry':geom,'boundary_label':s.PSI0+SHIFT,'runs':[mainrun],
        'scope':'Reference irrational paraboloidal member only. Boundary is a declared diagnostic psi tube, geometry sampled rather than rigorously certified. Finite deterministic ensemble, first-order GC only; no full Lorentz, collisions, coil errors or plasma response.'}
    (ROOT/'sengupta_ensemble_results.json').write_text(json.dumps(result,indent=2))
    # Predetermined 80-launch high-pitch subset, every declared phase and
    # both directions, at the axis and all four outer (r=.7) positions.
    ids=[i for i,r in enumerate(rows) if (r['position']=='axis' or r['position'].startswith('r0.7_')) and r['perpendicular_speed_squared_fraction']>=.8]
    result['runs'].append(run(dt=.005,subset=ids,geom=geom))
    (ROOT/'sengupta_ensemble_results.json').write_text(json.dumps(result,indent=2))


if __name__=='__main__':main()
