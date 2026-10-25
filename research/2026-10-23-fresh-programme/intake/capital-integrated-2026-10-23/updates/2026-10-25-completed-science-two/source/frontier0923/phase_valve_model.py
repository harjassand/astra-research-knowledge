#!/usr/bin/env python3
"""Hypothetical oxygen-to-mechanical-transmission valve; no device/organ fit.

Stress relaxation times are model parameters, not oxygen-conversion times.
All device dimensions are explicit illustrative engineering inputs.
"""
from pathlib import Path
import csv
import json
import math
import numpy as np

OUT=Path(__file__).resolve().parent
K0, BETA, U0 = 1e-3, 2.0, 60e-6  # N/m, dimensionless, m
KV=K0*BETA
TAU_OXY, TAU_HYPO=5.0,600.0      # hypothetical Maxwell stress times, s
MU, WPORT, LPORT=1.5e-3,10e-6,2e-3
HMIN=2e-6
NPHASE=8
PHASES=2*np.pi*np.arange(NPHASE)/NPHASE
PUNIT, QUNIT=100.0,1e-12        # Pa, m^3/s (one nL/s)
RUNIT=PUNIT/QUNIT
POWERUNIT=PUNIT*QUNIT
KUP, CMIN, VC=0.05,0.20,20.0    # dimensionless oxygen model, s*flow units
CFLOW=WPORT/(12*MU*LPORT)


def transfer(omega,tau,beta=BETA):
    return 1j*omega*tau/(beta+1j*omega*tau*(1+beta))


def aperture_conductance(y):
    # Each actuator uncovers two opposed ports. This is the assumed
    # pressure-balanced spool geometry, not a hard mechanical stop.
    h1=HMIN+np.maximum(0,y)
    h2=HMIN+np.maximum(0,-y)
    return CFLOW*np.sum(h1**3+h2**3,axis=-1)*RUNIT


def material_tau(sensor,threshold):
    return TAU_OXY+(TAU_HYPO-TAU_OXY)/(1+(sensor/threshold)**6)


def update_y(y,t,dt,tau,omega):
    # Exact solution over dt for constant tau and sinusoidal U.
    ht=transfer(omega,tau)[:,None]
    z0=np.real(ht*U0*np.exp(1j*(omega*t+PHASES)))
    z1=np.real(ht*U0*np.exp(1j*(omega*(t+dt)+PHASES)))
    rate=BETA/((1+BETA)*tau)
    return z1+(y-z0)*np.exp(-rate[:,None]*dt)


def oxygen_step(c,q,m,dt):
    # Implicit Euler; positivity-preserving solution of the uptake equation.
    a=VC/dt+q
    b=a*KUP-VC/dt*c-q+m
    d=KUP*(VC/dt*c+q)
    return (-b+np.sqrt(b*b+4*a*d))/(2*a)


def steady_oxygen(q,m):
    b=m-q*(1-KUP)
    return (-b+np.sqrt(b*b+4*q*q*KUP))/(2*q)


def geometry():
    rng=np.random.default_rng(9518831)
    z1,z2=rng.normal(size=(2,24))
    r=np.exp(.85*z1)
    m=np.exp(.2*z2);m=m/m.mean()
    return r,m


def benchmark(r,m,qmax,pmax,wmax,kind):
    amax=U0/(1+BETA)
    # Strong uniform-open comparator: every phase port held at maximum
    # available opening, with no continuing mechanical dissipation assumed.
    ggate_max=float(aperture_conductance(np.full((1,NPHASE),amax))[0])
    reff=r+1/ggate_max
    if kind=='uniform_open':
        gg=1/reff
        p=min(pmax,qmax/gg.sum(),math.sqrt(wmax/gg.sum()))
        q=p*gg
        power=p*q.sum()
    elif kind=='ordinary_individual_valves_maxmin':
        # Supplied true R,M; common pressure, individually metered flow.
        b=float(np.max(reff*m))
        scale=min(qmax/m.sum(),pmax/b,math.sqrt(wmax/(b*m.sum())))
        q=scale*m;p=scale*b;power=p*q.sum()
    elif kind=='independent_local_pumps_maxmin':
        scale=min(qmax/m.sum(),float(np.min(pmax/(reff*m))),
                  math.sqrt(wmax/float(np.sum(reff*m*m))))
        q=scale*m;p=float(np.max(reff*q));power=float(np.sum(reff*q*q))
    elif kind=='ideal_local_pumps_bare_tissue_maxmin':
        # Strong architecture bound: independent pumps do not retain this
        # candidate valve's port resistance. Their fabrication is not granted.
        scale=min(qmax/m.sum(),float(np.min(pmax/(r*m))),
                  math.sqrt(wmax/float(np.sum(r*m*m))))
        q=scale*m;p=float(np.max(r*q));power=float(np.sum(r*q*q))
    elif kind=='ordinary_individual_valves_max_adequate_count':
        # Exact finite candidate-pressure search for this steady objective.
        # At fixed P, baseline leakage is compulsory and each extra adequate
        # branch costs M_i-Qfloor_i. Equal values => sort these increments.
        gfloor=float(aperture_conductance(np.zeros((1,NPHASE)))[0])
        qtarget=m*(1+1e-9)
        best=None
        for ptry in sorted(set(np.minimum(reff*qtarget,pmax).tolist()+[pmax])):
            qtry=ptry/(r+1/gfloor)
            # Compare products with a relative roundoff tolerance. Division
            # at the exact candidate pressure can undershoot by one ulp.
            eligible=np.flatnonzero((ptry>=reff*qtarget*(1-1e-12))&(qtry<qtarget))
            increments=qtarget[eligible]-qtry[eligible]
            order=eligible[np.argsort(increments)]
            budget=min(qmax,wmax/ptry)
            if qtry.sum()>budget+1e-9:
                continue
            for k in order:
                extra=qtarget[k]-qtry[k]
                if qtry.sum()+extra <= budget+1e-9:
                    qtry[k]=qtarget[k]
            count=int(np.sum(qtry>=m))
            rank=(count,-ptry*float(qtry.sum()))
            if best is None or rank>best[0]:
                best=(rank,ptry,qtry.copy())
        if best is None:
            raise RuntimeError('No feasible ordinary-valve comparator')
        _,p,q=best;power=p*q.sum()
    elif kind=='independent_local_pumps_max_adequate_count':
        # In this fixture Qcap >= sum(M); only power limits the selected set.
        assert qmax>=m.sum()
        q=np.zeros(len(r));qt=m*(1+1e-9)
        cost=reff*qt**2
        eligible=np.flatnonzero(reff*qt<=pmax)
        for k in eligible[np.argsort(cost[eligible])]:
            if float(np.sum(reff*q*q))+cost[k] <= wmax+1e-9:
                q[k]=qt[k]
        p=float(np.max(reff*q));power=float(np.sum(reff*q*q))
    else:
        raise ValueError(kind)
    c=np.zeros(len(q))
    active=q>0
    c[active]=steady_oxygen(q[active],m[active])
    return dict(kind=kind,adequate_fraction=float(np.mean(c>=CMIN)),
                c_min=float(c.min()),c_median=float(np.median(c)),
                q_total=float(q.sum()),p_max=float(p),hydraulic_power=float(power),
                actuator_net_power=0.0,actuator_gross_positive_power=0.0)


def run(r,m,threshold=.3,sensor_tau=5.0,omega=.02,dt=.2,T=1800.0,
        equal_power=False,trace=False):
    qmax=1.25*m.sum()
    amax=U0/(1+BETA)
    ggate_max=float(aperture_conductance(np.full((1,NPHASE),amax))[0])
    pbase=qmax/np.sum(1/(r+1/ggate_max))
    pmax=12*pbase
    wcap=pbase*qmax if equal_power else math.inf
    c=np.full(len(r),.01);sensor=c.copy();y=np.zeros((len(r),NPHASE))
    # A low-oxygen initial sensor state is explicitly supplied by this fixture,
    # not physically acquired. Mechanical reference starts with zero stored
    # elastic energy; no Maxwell reset is applied during the operation.
    sums=dict(dose=np.zeros(len(r)),adequate_time=np.zeros(len(r)),
              q=0.,p=0.,wh=0.,wa=0.,wgross=0.)
    tailmin=np.ones(len(r));tailc=np.zeros(len(r));tailadequate=np.zeros(len(r));tailtime=0.0
    history=[]
    steps=round(T/dt)
    for j in range(steps):
        t=j*dt
        tau=material_tau(sensor,threshold)
        yn=update_y(y,t,dt,tau,omega)
        ym=(y+yn)/2
        vdrive=-U0*omega*np.sin(omega*(t+dt/2)+PHASES)
        pdrive=KV*ym*vdrive
        dissip=KV*BETA*np.sum(ym*ym/tau[:,None])/POWERUNIT
        gross=float(np.sum(np.maximum(0,pdrive))/POWERUNIT)
        gg=1/(r+1/aperture_conductance(ym))
        wc=max(0,wcap-dissip)
        p=min(pmax,qmax/gg.sum(),math.sqrt(wc/gg.sum()))
        q=p*gg
        cn=oxygen_step(c,q,m,dt)
        if sensor_tau>0:
            sensor=cn+(sensor-cn)*np.exp(-dt/sensor_tau)
        else:
            sensor=cn.copy()
        y=yn;c=cn
        sums['dose']+=np.maximum(0,CMIN-c)*dt
        sums['adequate_time']+=(c>=CMIN)*dt
        sums['q']+=float(q.sum())*dt;sums['p']+=p*dt
        sums['wh']+=p*float(q.sum())*dt
        sums['wa']+=dissip*dt;sums['wgross']+=gross*dt
        if t>=T-300:
            tailmin=np.minimum(tailmin,c);tailc+=c*dt
            tailadequate+=(c>=CMIN)*dt;tailtime+=dt
        if trace and (j%max(1,round(2/dt))==0):
            history.append([t,float(c.min()),float(np.median(c)),float(c.max()),
                            float(np.mean(c>=CMIN)),p,float(q.sum()),dissip,
                            float(np.max(np.abs(y)))])
    result=dict(threshold=threshold,sensor_conversion_time=sensor_tau,
                drive_omega=omega,drive_period=2*np.pi/omega,dt=dt,T=T,
                equal_power=equal_power,q_cap=float(qmax),p_cap=float(pmax),
                power_cap=None if math.isinf(wcap) else float(wcap),
                last_300s_always_adequate_fraction=float(np.mean(tailmin>=CMIN)),
                last_300s_mean_oxygen_adequate_fraction=float(np.mean(tailc/tailtime>=CMIN)),
                last_300s_time_adequate_fraction=float(np.mean(tailadequate)/tailtime),
                whole_run_adequate_time_fraction=float(np.mean(sums['adequate_time'])/T),
                mean_hypoxic_dose=float(np.mean(sums['dose'])),
                terminal_c_min=float(c.min()),terminal_c_median=float(np.median(c)),
                mean_q=float(sums['q']/T),mean_p=float(sums['p']/T),
                mean_hydraulic_power=float(sums['wh']/T),
                mean_actuator_net_power=float(sums['wa']/T),
                mean_actuator_gross_positive_power=float(sums['wgross']/T),
                actuator_energy_j=float(sums['wa']*POWERUNIT),
                hydraulic_energy_j=float(sums['wh']*POWERUNIT),
                reference_uniform_open_pressure=float(pbase))
    return result,history


def audit():
    # Harmonic response and energy equality against time-domain integration.
    errors=[]
    for tau in [5.,50.,600.]:
        for omega in [.01,.02,.1]:
            ht=transfer(omega,tau)
            period=2*np.pi/omega
            t=np.linspace(0,period,200001)
            y=np.real(ht*U0*np.exp(1j*omega*t))
            udot=-omega*U0*np.sin(omega*t)
            pd=KV*y*udot
            loss=KV*BETA*y*y/tau
            pm=float(np.trapezoid(pd,t)/period)
            pl=float(np.trapezoid(loss,t)/period)
            exact=omega/2*np.imag(KV*ht)*U0**2
            errors.append(max(abs(pm/exact-1),abs(pl/exact-1)))
            ynew=update_y(y[:1,None],0,period,np.array([tau]),omega)[0,0]
            assert abs(ynew-y[0])<1e-12
    assert max(errors)<1e-10
    # Fixed load SLS creep is monotone: tau changes alone cannot reverse it.
    v=0.;minimum_increment=math.inf
    for k in range(10000):
        tc=30. if k<2000 else 3000.
        vn=1+(v-1)*np.exp(-.1/tc)
        minimum_increment=min(minimum_increment,vn-v);v=vn
    assert minimum_increment>=0
    return dict(max_harmonic_energy_relative_error=max(errors),
                fixed_load_tau_switch_minimum_creep_increment=minimum_increment)


def main():
    r,m=geometry()
    checks=audit()
    freq=[]
    for period in [10,30,60,120,300,600,1800]:
        om=2*np.pi/period
        aa=[abs(transfer(om,t))*U0 for t in [TAU_OXY,TAU_HYPO]]
        th=np.linspace(0,2*np.pi,4096,endpoint=False)
        gg=[float(np.mean(aperture_conductance((a*np.cos(th))[:,None])))*NPHASE for a in aa]
        pp=[om/2*np.imag(KV*transfer(om,t))*U0**2*NPHASE for t in [TAU_OXY,TAU_HYPO]]
        freq.append(dict(period_s=period,oxy_stroke_um=aa[0]*1e6,
                         hypoxic_stroke_um=aa[1]*1e6,
                         steady_conductance_ratio=gg[1]/gg[0],
                         oxy_actuation_net_w=pp[0],hypoxic_actuation_net_w=pp[1]))
    results=[]
    for eq in [False,True]:
        for threshold in [.01,.10,.30]:
            for sensor_tau in [0.,5.,30.,120.]:
                for omega in [.02,.10]:
                    res,hist=run(r,m,threshold,sensor_tau,omega,equal_power=eq,
                                 trace=(not eq and threshold==.3 and sensor_tau==5 and omega==.02))
                    results.append(res)
                    if hist:
                        with (OUT/'phase_valve_trace.csv').open('w',newline='') as f:
                            w=csv.writer(f);w.writerow(['t_s','oxygen_min','oxygen_median','oxygen_max',
                                                       'adequate_fraction','p_dimensionless','q_dimensionless',
                                                       'actuator_net_power_dimensionless','max_spool_stroke_m'])
                            w.writerows(hist)
    # Time-resolution check on the selected candidate, independent of threshold ranking.
    fine,_=run(r,m,.3,5.,.02,dt=.1)
    coarse=next(x for x in results if not x['equal_power'] and x['threshold']==.3
                and x['sensor_conversion_time']==5 and x['drive_omega']==.02)
    checks['dt_refinement_terminal_median_absolute_difference']=abs(fine['terminal_c_median']-coarse['terminal_c_median'])
    checks['dt_refinement_mean_dose_relative_difference']=abs(fine['mean_hypoxic_dose']/coarse['mean_hypoxic_dose']-1)
    checks['dt_refinement_always_adequate_fraction_difference']=abs(fine['last_300s_always_adequate_fraction']-coarse['last_300s_always_adequate_fraction'])
    qmax=1.25*m.sum();pbase=coarse['reference_uniform_open_pressure'];pmax=12*pbase
    benchmarks=[]
    for eq in [False,True]:
        wcap=pbase*qmax if eq else math.inf
        for kind in ['uniform_open','ordinary_individual_valves_maxmin',
                     'independent_local_pumps_maxmin',
                     'ordinary_individual_valves_max_adequate_count',
                     'independent_local_pumps_max_adequate_count',
                     'ideal_local_pumps_bare_tissue_maxmin']:
            b=benchmark(r,m,qmax,pmax,wcap,kind);b['equal_power']=eq;benchmarks.append(b)
    doc=dict(status='hypothetical material/device; synthetic tissue; no acquired recovery capability',
             checks=checks,physical_parameters=dict(K0_N_per_m=K0,Kv_N_per_m=KV,
                 input_stroke_m=U0,gel_length_m=1e-3,gel_area_m2=1e-8,
                 equivalent_modulus_pa=100.0,max_input_strain=U0/1e-3,
                 phase_copies=NPHASE,minimum_gap_m=HMIN,port_width_m=WPORT,
                 port_length_m=LPORT,viscosity_pas=MU,pressure_unit_pa=PUNIT,
                 flow_unit_m3_per_s=QUNIT,relaxation_times_s=[TAU_OXY,TAU_HYPO]),
             frequency_response=freq,benchmarks=benchmarks,network_cases=results,
             geometry=dict(resistance=r.tolist(),demand_scale=m.tolist()),
             limitations=['oxygen-conversion time and threshold supplied, not measured',
                'initial sensor oxygen equals low tissue oxygen as a supplied initial state',
                'ideal pressure-balanced spool geometry and mechanical clock supplied',
                'spool friction, hydraulic force mismatch and clock losses excluded',
                'lumped oxygen states are not biological recovery or native organ data',
                'published deoxy gel is not a fitted one-mode Maxwell material'])
    (OUT/'phase_valve_results.json').write_text(json.dumps(doc,indent=2)+'\n')
    with (OUT/'phase_valve_sweep.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    print(json.dumps(dict(checks=checks,frequency_response=freq,benchmarks=benchmarks,
                         selected_candidate=coarse),indent=2))


if __name__=='__main__':
    main()
